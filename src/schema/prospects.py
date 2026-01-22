"""
Prospects Schema for unified prospects API.

This schema defines the request and response models for the unified
prospects router that supports both SIC-based and direct search modes.

Uses CombinedICP for unified company/person criteria with automatic mode detection.

Reference: docs/PROSPECTS_FLOW_DESIGN.md
"""

from pydantic import BaseModel, ConfigDict, Field

from src.schema.combined_icp import CombinedICP


class ProspectSearchRequest(BaseModel):
    """
    Unified request schema for prospect search.

    Uses CombinedICP which automatically detects mode:
    - If sic_code or naics_code present → SIC-based flow (company search first)
    - Otherwise → Direct flow (person search only)

    Common fields (location_country, industry, size) are mapped to:
    - Company query: as-is (location_country, industry, size)
    - Person query: with job_company_ prefix (job_company_location_country, etc.)
    """

    size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of results per page (max 100)",
    )
    scroll_token: str | None = Field(
        default=None,
        description="Pagination token for fetching next page of results",
    )
    icp: CombinedICP = Field(
        default_factory=CombinedICP,
        description="Combined ICP with company and person criteria",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "size": 10,
                "icp": {
                    # Company-only (triggers SIC-based flow)
                    "sic_code": ["7371", "7372"],
                    # Common fields (company HQ location)
                    "location_country": ["united states"],
                    "size": ["51-200", "201-500"],
                    "industry": ["computer software"],
                    # Person-only
                    "job_title_role": ["engineering"],
                    "job_title_levels": ["director", "vp"],
                    "skills": ["python", "aws"],
                },
            }
        }
    )


class ProspectPreviewResponse(BaseModel):
    """Response schema for prospect preview endpoint."""

    success: bool = Field(..., description="Whether the request was successful")
    mode: str = Field(..., description="Search mode used (sic_based or direct)")
    companies_found: int = Field(
        default=0,
        description="Number of companies found (for sic_based mode)",
    )
    persons_found: int = Field(..., description="Number of persons found")
    preview_data: list[dict] = Field(
        default_factory=list,
        description="Preview data (person records)",
    )
    scroll_token: str | None = Field(
        default=None,
        description="Pagination token for fetching next page",
    )
    message: str | None = Field(
        default=None,
        description="Optional message or error details",
    )


class ProspectGenerateResponse(BaseModel):
    """Response schema for prospect generate endpoint."""

    success: bool = Field(..., description="Whether the request was successful")
    mode: str = Field(..., description="Search mode used (sic_based or direct)")
    companies_found: int = Field(
        default=0,
        description="Number of companies found (for sic_based mode)",
    )
    persons_generated: int = Field(..., description="Number of persons generated")
    export_path: str | None = Field(
        default=None,
        description="Path to the exported JSON file",
    )
    scroll_token: str | None = Field(
        default=None,
        description="Pagination token for fetching next page",
    )
    message: str | None = Field(
        default=None,
        description="Optional message or error details",
    )
