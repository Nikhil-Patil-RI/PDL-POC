"""
Request/Response schemas for Prospects API.

Returns PDL (People Data Labs) person data directly without transformation.
Reference: docs/PERSON_RESPONSE.md
"""

from typing import Any

from pydantic import BaseModel, Field

from src.schema.icp import ICP


# === Preview Prospects Schemas ===

class PreviewProspectsRequest(BaseModel):
    """Request schema for preview_prospects endpoint."""

    number_of_prospects: int = Field(
        default=10, ge=1, le=100, description="Number of prospects to preview (1-100)"
    )
    icp: ICP = Field(..., description="Ideal Customer Profile criteria for search")
    scroll_token: str | None = Field(None, description="Token for fetching next page")


class PreviewProspectsResponse(BaseModel):
    """Response schema for preview_prospects endpoint."""

    success: bool = Field(..., description="Whether the request was successful")
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Response message")
    prospects_found: int = Field(..., description="Total number of prospects found")
    prospects_requested: int = Field(..., description="Number of prospects requested")
    prospects: list[dict[str, Any]] = Field(
        default_factory=list, description="List of PDL person records"
    )
    icp: dict[str, Any] | None = Field(None, description="ICP criteria used for search")
    scroll_token: str | None = Field(None, description="Token for next page")


# === Generate Prospects Schemas ===

class GenerateProspectsRequest(BaseModel):
    """Request schema for generate_prospects endpoint."""

    number_of_prospects: int = Field(
        ..., ge=1, le=1000, description="Number of prospects to generate (1-1000)"
    )
    icp: ICP = Field(..., description="Ideal Customer Profile criteria for search")
    prospect_ids: list[str] | None = Field(
        None, description="Optional list of PDL IDs to enrich directly"
    )


class GenerateProspectsResponse(BaseModel):
    """Response schema for generate_prospects endpoint."""

    success: bool = Field(..., description="Whether the request was successful")
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Response message")
    prospects_generated: int = Field(..., description="Number of prospects generated")
    prospects_requested: int = Field(..., description="Number of prospects requested")
    prospects_enriched: int = Field(..., description="Number of prospects successfully enriched")
    prospects: list[dict[str, Any]] | None = Field(
        None, description="List of PDL person records"
    )
    export_file: str | None = Field(None, description="Path to exported JSON file")
