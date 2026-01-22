"""
Prospects API endpoints for PDL-POC.

Provides unified endpoints for prospect search with automatic mode detection:
- SIC-based (if sic_code/naics_code present): Company Search → Extract IDs → Person Search
- Direct (otherwise): Person Search → Person Enrichment

Uses CombinedICP schema and ProspectsQueryBuilder for unified query building.

Reference: docs/PROSPECTS_FLOW_DESIGN.md
"""

import json
import os
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from src.schema.prospects import (
    ProspectSearchRequest,
    ProspectPreviewResponse,
    ProspectGenerateResponse,
)
from src.utils.pdl_client import get_pdl_client
from src.utils.prospects_query_builder import ProspectsQueryBuilder

router = APIRouter(prefix="/api/v1/prospects", tags=["prospects"])


@router.post("/preview", response_model=ProspectPreviewResponse)
async def preview_prospects(request: ProspectSearchRequest) -> ProspectPreviewResponse:
    """
    Preview prospects without saving to file.

    Mode is automatically detected from ICP:
    - If sic_code or naics_code present → SIC-based flow
    - Otherwise → Direct flow

    Flow A (SIC-based):
        1. Company Search with SIC codes
        2. Extract company PDL IDs
        3. Person Search with job_company_id filter

    Flow B (Direct):
        1. Person Search
        2. Person Enrichment
    """
    try:
        client = get_pdl_client()

        if request.icp.is_sic_based:
            return await _preview_sic_based(client, request)
        else:
            return await _preview_direct(client, request)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)}")


@router.post("/generate", response_model=ProspectGenerateResponse)
async def generate_prospects(
    request: ProspectSearchRequest,
) -> ProspectGenerateResponse:
    """
    Generate prospects with enrichment and save to file.

    Both flows include enrichment:
    - SIC-based: Company Search → Person Search → Enrichment → Save
    - Direct: Person Search → Enrichment → Save
    """
    try:
        client = get_pdl_client()

        if request.icp.is_sic_based:
            # SIC-based: includes enrichment
            result = await _generate_sic_based(client, request)
        else:
            # Direct: includes enrichment
            result = await _generate_direct(client, request)

        # Export to file
        export_path = _export_prospects_to_json(result.preview_data)

        return ProspectGenerateResponse(
            success=result.success,
            mode=result.mode,
            companies_found=result.companies_found,
            persons_generated=result.persons_found,
            export_path=export_path,
            scroll_token=result.scroll_token,
            message=result.message,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generate failed: {str(e)}")


async def _preview_sic_based(
    client: Any, request: ProspectSearchRequest
) -> ProspectPreviewResponse:
    """Handle SIC-based flow: Company Search → Person Search."""
    query_builder = ProspectsQueryBuilder(request.icp)

    # Step 1: Build company query using ProspectsQueryBuilder
    company_query = query_builder.build_company_query()

    # Step 2: Search companies
    company_response = client.company_search(
        sql_query=company_query,
        size=request.size,
        scroll_token=request.scroll_token,
    )

    if company_response.get("status") != 200:
        return ProspectPreviewResponse(
            success=False,
            mode="sic_based",
            companies_found=0,
            persons_found=0,
            message=f"Company search failed: {company_response.get('error', {}).get('message', 'Unknown error')}",
        )

    companies = company_response.get("data", [])
    company_ids = [c.get("id") for c in companies if c.get("id")]

    if not company_ids:
        return ProspectPreviewResponse(
            success=True,
            mode="sic_based",
            companies_found=0,
            persons_found=0,
            message="No companies found matching criteria",
        )

    # Step 3: Search persons with job_company_id filter
    person_query = query_builder.build_person_query_with_company_ids(company_ids)

    person_response = client.person_search(
        sql_query=person_query,
        size=request.size,
    )

    if person_response.get("status") != 200:
        return ProspectPreviewResponse(
            success=False,
            mode="sic_based",
            companies_found=len(companies),
            persons_found=0,
            message=f"Person search failed: {person_response.get('error', {}).get('message', 'Unknown error')}",
        )

    persons = person_response.get("data", [])

    return ProspectPreviewResponse(
        success=True,
        mode="sic_based",
        companies_found=len(companies),
        persons_found=len(persons),
        preview_data=persons,
        scroll_token=person_response.get("scroll_token"),
    )


async def _generate_sic_based(
    client: Any, request: ProspectSearchRequest
) -> ProspectPreviewResponse:
    """Handle SIC-based flow for Generate: Company Search → Person Search → Enrichment."""
    query_builder = ProspectsQueryBuilder(request.icp)

    # Step 1: Build company query using ProspectsQueryBuilder
    company_query = query_builder.build_company_query()

    # Step 2: Search companies
    company_response = client.company_search(
        sql_query=company_query,
        size=request.size,
        scroll_token=request.scroll_token,
    )

    if company_response.get("status") != 200:
        return ProspectPreviewResponse(
            success=False,
            mode="sic_based",
            companies_found=0,
            persons_found=0,
            message=f"Company search failed: {company_response.get('error', {}).get('message', 'Unknown error')}",
        )

    companies = company_response.get("data", [])
    company_ids = [c.get("id") for c in companies if c.get("id")]

    if not company_ids:
        return ProspectPreviewResponse(
            success=True,
            mode="sic_based",
            companies_found=0,
            persons_found=0,
            message="No companies found matching criteria",
        )

    # Step 3: Search persons with job_company_id filter
    person_query = query_builder.build_person_query_with_company_ids(company_ids)

    person_response = client.person_search(
        sql_query=person_query,
        size=request.size,
    )

    if person_response.get("status") != 200:
        return ProspectPreviewResponse(
            success=False,
            mode="sic_based",
            companies_found=len(companies),
            persons_found=0,
            message=f"Person search failed: {person_response.get('error', {}).get('message', 'Unknown error')}",
        )

    persons = person_response.get("data", [])

    if not persons:
        return ProspectPreviewResponse(
            success=True,
            mode="sic_based",
            companies_found=len(companies),
            persons_found=0,
            message="No persons found matching criteria",
        )

    # Step 4: Person Enrichment - enrich each person using their PDL ID
    enriched_persons: list[dict] = []
    for person in persons:
        pdl_id = person.get("id")
        if pdl_id:
            try:
                enrich_response = client.person_enrichment(pdl_id=pdl_id)
                if enrich_response.get("status") == 200:
                    enriched_persons.append(enrich_response.get("data", person))
                else:
                    # Use search data if enrichment fails
                    enriched_persons.append(person)
            except Exception:
                enriched_persons.append(person)
        else:
            enriched_persons.append(person)

    return ProspectPreviewResponse(
        success=True,
        mode="sic_based",
        companies_found=len(companies),
        persons_found=len(enriched_persons),
        preview_data=enriched_persons,
        scroll_token=person_response.get("scroll_token"),
    )


async def _preview_direct(
    client: Any, request: ProspectSearchRequest
) -> ProspectPreviewResponse:
    """Handle Direct flow for Preview: Person Search only (NO enrichment)."""
    query_builder = ProspectsQueryBuilder(request.icp)

    # Person Search - maps common fields to job_company_* prefix
    person_query = query_builder.build_person_query()

    person_response = client.person_search(
        sql_query=person_query,
        size=request.size,
        scroll_token=request.scroll_token,
    )

    if person_response.get("status") != 200:
        return ProspectPreviewResponse(
            success=False,
            mode="direct",
            companies_found=0,
            persons_found=0,
            message=f"Person search failed: {person_response.get('error', {}).get('message', 'Unknown error')}",
        )

    persons = person_response.get("data", [])

    if not persons:
        return ProspectPreviewResponse(
            success=True,
            mode="direct",
            companies_found=0,
            persons_found=0,
            message="No persons found matching criteria",
        )

    # Preview: Return search results directly (NO enrichment)
    return ProspectPreviewResponse(
        success=True,
        mode="direct",
        companies_found=0,
        persons_found=len(persons),
        preview_data=persons,
        scroll_token=person_response.get("scroll_token"),
    )


async def _generate_direct(
    client: Any, request: ProspectSearchRequest
) -> ProspectPreviewResponse:
    """Handle Direct flow for Generate: Person Search → Person Enrichment."""
    query_builder = ProspectsQueryBuilder(request.icp)

    # Step 1: Person Search - maps common fields to job_company_* prefix
    person_query = query_builder.build_person_query()

    person_response = client.person_search(
        sql_query=person_query,
        size=request.size,
        scroll_token=request.scroll_token,
    )

    if person_response.get("status") != 200:
        return ProspectPreviewResponse(
            success=False,
            mode="direct",
            companies_found=0,
            persons_found=0,
            message=f"Person search failed: {person_response.get('error', {}).get('message', 'Unknown error')}",
        )

    persons = person_response.get("data", [])

    if not persons:
        return ProspectPreviewResponse(
            success=True,
            mode="direct",
            companies_found=0,
            persons_found=0,
            message="No persons found matching criteria",
        )

    # Step 2: Person Enrichment - enrich each person using their PDL ID
    enriched_persons: list[dict] = []
    for person in persons:
        pdl_id = person.get("id")
        if pdl_id:
            try:
                enrich_response = client.person_enrichment(pdl_id=pdl_id)
                if enrich_response.get("status") == 200:
                    enriched_persons.append(enrich_response.get("data", person))
                else:
                    # Use search data if enrichment fails
                    enriched_persons.append(person)
            except Exception:
                enriched_persons.append(person)
        else:
            enriched_persons.append(person)

    return ProspectPreviewResponse(
        success=True,
        mode="direct",
        companies_found=0,
        persons_found=len(enriched_persons),
        preview_data=enriched_persons,
        scroll_token=person_response.get("scroll_token"),
    )


def _export_prospects_to_json(prospects: list[dict]) -> str:
    """
    Export prospects to a JSON file with timestamp.

    Args:
        prospects: List of prospect data to export.

    Returns:
        Path to the exported JSON file.
    """
    # Create exports directory if it doesn't exist
    exports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "exports")
    os.makedirs(exports_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prospects_{timestamp}.json"
    filepath = os.path.join(exports_dir, filename)

    # Export data
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "total_prospects": len(prospects),
        "prospects": prospects,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    return filepath
