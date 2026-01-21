"""Company Search and Enrichment API endpoints."""

import json
import os
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from src.schema.company import CompanySearchSchema
from src.utils.company_query_builder import build_company_query
from src.utils.pdl_client import get_pdl_client

router = APIRouter(prefix="/api/v1", tags=["companies"])


class CompanySearchRequest(BaseModel):
    """Request schema for company search."""

    criteria: CompanySearchSchema = Field(
        ..., description="Company search criteria based on PDL Company Schema"
    )
    size: int = Field(
        default=25, ge=1, le=100, description="Number of results per page (max 100)"
    )
    scroll_token: str | None = Field(
        default=None, description="Token for pagination"
    )


class CompanyEnrichmentRequest(BaseModel):
    """Request schema for company enrichment.

    Provide either:
    - company_ids: List of PDL company IDs to enrich directly
    - criteria: Search criteria to find companies, then enrich the results
    """

    company_ids: list[str] | None = Field(
        default=None, description="List of PDL company IDs to enrich directly"
    )
    criteria: CompanySearchSchema | None = Field(
        default=None, description="Search criteria to find companies first, then enrich"
    )
    number_of_companies: int = Field(
        default=10, ge=1, le=100, description="Number of companies to enrich (max 100)"
    )


@router.post("/search_companies")
async def search_companies(request: CompanySearchRequest):
    """
    Search for companies using PDL Company Search API.

    Args:
        request: CompanySearchRequest containing criteria, size, and scroll_token.

    Returns:
        dict with companies matching the criteria.
    """
    try:
        # Build SQL query
        sql_query = build_company_query(request.criteria)

        # Get PDL client
        client = get_pdl_client()

        # Execute search
        response = client.company_search(
            sql_query=sql_query,
            size=request.size,
            scroll_token=request.scroll_token,
        )

        return {
            "status": "success",
            "query": sql_query,
            "total": response.get("total", 0),
            "count": len(response.get("data", [])),
            "scroll_token": response.get("scroll_token"),
            "data": response.get("data", []),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Company search failed: {str(e)}")


@router.post("/enrich_companies")
async def enrich_companies(request: CompanyEnrichmentRequest):
    """
    Enrich companies using PDL Company Enrichment API.

    Provide either:
    - company_ids: List of PDL company IDs to enrich directly
    - criteria: Search criteria to find companies first, then enrich the results

    Args:
        request: Company enrichment request with company_ids or criteria.

    Returns:
        dict with enriched company data.
    """
    try:
        # Get PDL client
        client = get_pdl_client()
        enriched_companies: list[dict] = []

        # Validate request - need either company_ids or criteria
        if not request.company_ids and not request.criteria:
            raise ValueError("Either company_ids or criteria must be provided")

        # If company_ids provided, enrich directly
        if request.company_ids:
            pdl_ids = request.company_ids[:request.number_of_companies]
            if pdl_ids:
                bulk_response = client.company_bulk_enrichment(pdl_ids=pdl_ids)
                # Response is a flat list where each item IS the company data with status embedded
                for item in bulk_response:
                    if item.get("status") == 200:
                        enriched_companies.append(item)
        else:
            # Search first, then enrich using bulk enrichment
            sql_query = build_company_query(request.criteria)
            search_response = client.company_search(
                sql_query=sql_query,
                size=request.number_of_companies,
            )

            if search_response.get("status") != 200:
                raise HTTPException(
                    status_code=search_response.get("status", 500),
                    detail=f"Company search failed: {search_response.get('error', {}).get('message', 'Unknown error')}",
                )

            # Extract PDL IDs from search results
            search_data = search_response.get("data", [])
            pdl_ids = [company.get("id") for company in search_data if company.get("id")]

            if pdl_ids:
                # Call bulk enrichment API with PDL IDs
                bulk_response = client.company_bulk_enrichment(pdl_ids=pdl_ids)

                # Response is a flat list where each item IS the company data with status embedded
                for item in bulk_response:
                    if item.get("status") == 200:
                        enriched_companies.append(item)

        # Export to JSON file
        export_file = _export_companies_to_json(enriched_companies)

        return {
            "status": "success",
            "count": len(enriched_companies),
            "data": enriched_companies,
            "export_file": export_file,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Company enrichment failed: {str(e)}")


def _export_companies_to_json(
    companies: list[dict[str, Any]],
) -> str:
    """
    Export companies to a JSON file with timestamp.

    Args:
        companies: List of company data to export.

    Returns:
        Path to the exported JSON file.
    """
    # Create exports directory if it doesn't exist
    exports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "exports")
    os.makedirs(exports_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"companies_{timestamp}.json"
    filepath = os.path.join(exports_dir, filename)

    # Export data
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "total_companies": len(companies),
        "companies": companies,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    return filepath
