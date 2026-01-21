"""
Request/Response schemas for Persons API.

Returns PDL (People Data Labs) person data directly without transformation.
Reference: docs/PERSON_RESPONSE.md
"""

from typing import Any

from pydantic import BaseModel, Field

from src.schema.icp import ICP


# === Search Persons Schemas ===

class SearchPersonsRequest(BaseModel):
    """Request schema for search_persons endpoint."""

    number_of_persons: int = Field(
        default=10, ge=1, le=100, description="Number of persons to search (1-100)"
    )
    icp: ICP = Field(..., description="Ideal Customer Profile criteria for search")
    scroll_token: str | None = Field(None, description="Token for fetching next page")


class SearchPersonsResponse(BaseModel):
    """Response schema for search_persons endpoint."""

    success: bool = Field(..., description="Whether the request was successful")
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Response message")
    persons_found: int = Field(..., description="Total number of persons found")
    persons_requested: int = Field(..., description="Number of persons requested")
    persons: list[dict[str, Any]] = Field(
        default_factory=list, description="List of PDL person records"
    )
    icp: dict[str, Any] | None = Field(None, description="ICP criteria used for search")
    scroll_token: str | None = Field(None, description="Token for next page")


# === Enrich Persons Schemas ===

class EnrichPersonsRequest(BaseModel):
    """Request schema for enrich_persons endpoint."""

    number_of_persons: int = Field(
        ..., ge=1, le=1000, description="Number of persons to enrich (1-1000)"
    )
    icp: ICP = Field(..., description="Ideal Customer Profile criteria for search")
    person_ids: list[str] | None = Field(
        None, description="Optional list of PDL IDs to enrich directly"
    )


class EnrichPersonsResponse(BaseModel):
    """Response schema for enrich_persons endpoint."""

    success: bool = Field(..., description="Whether the request was successful")
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Response message")
    persons_enriched: int = Field(..., description="Number of persons enriched")
    persons_requested: int = Field(..., description="Number of persons requested")
    persons: list[dict[str, Any]] | None = Field(
        None, description="List of PDL person records"
    )
    export_file: str | None = Field(None, description="Path to exported JSON file")

