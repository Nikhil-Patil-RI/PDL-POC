"""
Persons API endpoints for PDL-POC.

Provides endpoints for:
- search_persons: Search persons using PDL Person Search API
- enrich_persons: Enrich persons using PDL Person Enrichment API
"""

import json
import os
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from src.schema.persons import (
    EnrichPersonsRequest,
    EnrichPersonsResponse,
    SearchPersonsRequest,
    SearchPersonsResponse,
)
from src.utils.pdl_client import get_pdl_client
from src.utils.query_builder import build_pdl_query

router = APIRouter()


@router.post("/search_persons", response_model=SearchPersonsResponse)
async def search_persons(request: SearchPersonsRequest) -> SearchPersonsResponse:
    """
    Search persons using PDL Person Search API.

    This endpoint searches for persons matching the ICP criteria
    without consuming enrichment credits.
    """
    try:
        # Build SQL query from ICP
        sql_query = build_pdl_query(request.icp)

        # Get PDL client
        client = get_pdl_client()

        # Execute search
        response = client.person_search(
            sql_query=sql_query,
            size=request.number_of_persons,
        )

        # Check for errors
        if response.get("status") != 200:
            return SearchPersonsResponse(
                success=False,
                status_code=response.get("status", 500),
                message=response.get("error", {}).get("message", "PDL search failed"),
                persons_found=0,
                persons_requested=request.number_of_persons,
                persons=[],
                icp=request.icp.model_dump(),
            )

        # Return PDL data directly
        persons = response.get("data", [])

        return SearchPersonsResponse(
            success=True,
            status_code=200,
            message="Persons retrieved successfully",
            persons_found=response.get("total", len(persons)),
            persons_requested=request.number_of_persons,
            persons=persons,
            icp=request.icp.model_dump(),
            scroll_token=response.get("scroll_token"),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/enrich_persons", response_model=EnrichPersonsResponse)
async def enrich_persons(request: EnrichPersonsRequest) -> EnrichPersonsResponse:
    """
    Enrich persons using PDL Person Enrichment API.

    This endpoint first searches for persons, then enriches them
    and exports results to a JSON file.
    """
    try:
        client = get_pdl_client()
        enriched_persons: list[dict[str, Any]] = []

        # If person_ids provided, enrich directly
        if request.person_ids:
            for pdl_id in request.person_ids[:request.number_of_persons]:
                try:
                    result = client.person_enrichment(pdl_id=pdl_id)
                    if result.get("status") == 200:
                        enriched_persons.append(result.get("data", {}))
                except Exception:
                    continue
        else:
            # Search first, then enrich using bulk enrichment
            sql_query = build_pdl_query(request.icp)
            search_response = client.person_search(
                sql_query=sql_query,
                size=request.number_of_persons,
            )

            if search_response.get("status") != 200:
                return EnrichPersonsResponse(
                    success=False,
                    status_code=search_response.get("status", 500),
                    message="PDL search failed",
                    persons_enriched=0,
                    persons_requested=request.number_of_persons,
                    persons=None,
                )

            # Extract PDL IDs from search results
            search_data = search_response.get("data", [])
            pdl_ids = [person.get("id") for person in search_data if person.get("id")]

            if pdl_ids:
                # Call bulk enrichment API with PDL IDs
                # Response format: [{"status": 200, "likelihood": 10, "data": {...}}, ...]
                bulk_response = client.person_bulk_enrichment(pdl_ids=pdl_ids)

                # Extract enriched data from bulk response (list of results)
                for item in bulk_response:
                    if item.get("status") == 200 and item.get("data"):
                        enriched_persons.append(item.get("data"))

        # Export to JSON file
        export_file = _export_persons_to_json(enriched_persons)

        return EnrichPersonsResponse(
            success=True,
            status_code=200,
            message="Persons enriched successfully",
            persons_enriched=len(enriched_persons),
            persons_requested=request.number_of_persons,
            persons=enriched_persons,
            export_file=export_file,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


def _export_persons_to_json(
    persons: list[dict[str, Any]],
) -> str:
    """
    Export persons to a JSON file with timestamp.

    Args:
        persons: List of person data to export.

    Returns:
        Path to the exported JSON file.
    """
    # Create exports directory if it doesn't exist
    exports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "exports")
    os.makedirs(exports_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"persons_{timestamp}.json"
    filepath = os.path.join(exports_dir, filename)

    # Export data
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "total_persons": len(persons),
        "persons": persons,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    return filepath

