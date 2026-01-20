"""
Prospects API endpoints for PDL-POC.

Provides endpoints for:
- preview_prospects: Search prospects using PDL Person Search API
- generate_prospects: Enrich prospects using PDL Person Enrichment API
"""

import json
import os
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from src.schema.prospects import (
    GenerateProspectsRequest,
    GenerateProspectsResponse,
    PreviewProspectsRequest,
    PreviewProspectsResponse,
)
from src.utils.pdl_client import get_pdl_client
from src.utils.query_builder import build_pdl_query

router = APIRouter()


@router.post("/preview_prospects", response_model=PreviewProspectsResponse)
async def preview_prospects(request: PreviewProspectsRequest) -> PreviewProspectsResponse:
    """
    Preview prospects using PDL Person Search API.
    
    This endpoint searches for prospects matching the ICP criteria
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
            size=request.number_of_prospects,
        )
        
        # Check for errors
        if response.get("status") != 200:
            return PreviewProspectsResponse(
                success=False,
                status_code=response.get("status", 500),
                message=response.get("error", {}).get("message", "PDL search failed"),
                prospects_found=0,
                prospects_requested=request.number_of_prospects,
                prospects=[],
                icp=request.icp.model_dump(),
            )
        
        # Return PDL data directly
        prospects = response.get("data", [])
        
        return PreviewProspectsResponse(
            success=True,
            status_code=200,
            message="Prospects retrieved successfully",
            prospects_found=response.get("total", len(prospects)),
            prospects_requested=request.number_of_prospects,
            prospects=prospects,
            icp=request.icp.model_dump(),
            scroll_token=response.get("scroll_token"),
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/generate_prospects", response_model=GenerateProspectsResponse)
async def generate_prospects(request: GenerateProspectsRequest) -> GenerateProspectsResponse:
    """
    Generate and enrich prospects using PDL Person Enrichment API.
    
    This endpoint first searches for prospects, then enriches them
    and exports results to a JSON file.
    """
    try:
        client = get_pdl_client()
        enriched_prospects: list[dict[str, Any]] = []
        
        # If prospect_ids provided, enrich directly
        if request.prospect_ids:
            for pdl_id in request.prospect_ids[:request.number_of_prospects]:
                try:
                    result = client.person_enrichment(pdl_id=pdl_id)
                    if result.get("status") == 200:
                        enriched_prospects.append(result.get("data", {}))
                except Exception:
                    continue
        else:
            # Search first, then enrich using bulk enrichment
            sql_query = build_pdl_query(request.icp)
            search_response = client.person_search(
                sql_query=sql_query,
                size=request.number_of_prospects,
            )

            if search_response.get("status") != 200:
                return GenerateProspectsResponse(
                    success=False,
                    status_code=search_response.get("status", 500),
                    message="PDL search failed",
                    prospects_generated=0,
                    prospects_requested=request.number_of_prospects,
                    prospects_enriched=0,
                    prospects=None,
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
                        enriched_prospects.append(item.get("data"))
        
        # Export to JSON file
        export_file = _export_prospects_to_json(enriched_prospects)
        
        return GenerateProspectsResponse(
            success=True,
            status_code=200,
            message="Prospects generated successfully",
            prospects_generated=len(enriched_prospects),
            prospects_requested=request.number_of_prospects,
            prospects_enriched=len(enriched_prospects),
            prospects=enriched_prospects,
            export_file=export_file,
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


def _export_prospects_to_json(
    prospects: list[dict[str, Any]],
) -> str:
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
