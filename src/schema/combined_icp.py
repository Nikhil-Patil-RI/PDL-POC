"""
Combined ICP Schema for unified prospects search.

This schema unifies company and person criteria into a single schema.

Field Mapping:
- Common fields (company HQ location): Maps to company query AND person query (with job_company_ prefix)
- Company-only fields: sic_code, naics_code, founded_*, employee_count_*, type, tags
- Person-only fields: person_location_*, job_title_*, skills

Mode Detection:
- If sic_code or naics_code present → SIC-based flow (company search first)
- Otherwise → Direct flow (person search only)
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator, computed_field

from src.schema.icp import (
    VALID_COMPANY_SIZES,
    VALID_INDUSTRIES,
    VALID_JOB_TITLE_CLASSES,
    VALID_JOB_TITLE_LEVELS,
    VALID_JOB_TITLE_ROLES,
    VALID_JOB_TITLE_SUB_ROLES,
)
from src.schema.company import VALID_COMPANY_TYPES, VALID_INFERRED_REVENUE


class CombinedICP(BaseModel):
    """
    Combined ICP schema for unified prospects search.

    Supports both SIC-based (company-first) and direct (person-only) flows.
    """

    # ==========================================================================
    # COMMON FIELDS - Company HQ Location (maps to both company and person queries)
    # In company query: location_*
    # In person query: job_company_location_*
    # ==========================================================================
    location_country: list[str] | None = Field(None, description="Company HQ country")
    location_country_not_in: list[str] | None = Field(
        None, description="Exclude companies in these countries"
    )
    location_region: list[str] | None = Field(
        None, description="Company HQ region/state"
    )
    location_locality: list[str] | None = Field(None, description="Company HQ city")
    location_name: list[str] | None = Field(
        None, description="Company HQ location name (uses LIKE for partial matching)"
    )
    location_name_not_in: list[str] | None = Field(
        None, description="Exclude companies in these locations"
    )

    # ==========================================================================
    # COMMON FIELDS - Company Attributes (maps to both company and person queries)
    # In company query: industry, size
    # In person query: job_company_industry, job_company_size
    # ==========================================================================
    industry: list[str] | None = Field(None, description="Company industry")
    industry_not_in: list[str] | None = Field(
        None, description="Exclude companies in these industries"
    )
    size: list[str] | None = Field(None, description="Company size range")
    inferred_revenue: list[str] | None = Field(
        None, description="Company inferred revenue range"
    )
    type: list[str] | None = Field(
        None, description="Company type (private, public, etc.)"
    )

    # ==========================================================================
    # COMPANY-ONLY FIELDS - Used only in company query (triggers SIC-based flow)
    # ==========================================================================
    sic_code: list[str] | None = Field(
        None, description="SIC industry codes (triggers SIC-based flow)"
    )
    naics_code: list[str] | None = Field(
        None, description="NAICS industry codes (triggers SIC-based flow)"
    )
    founded: int | None = Field(None, description="Year the company was founded")
    founded_min: int | None = Field(None, description="Minimum founding year")
    founded_max: int | None = Field(None, description="Maximum founding year")
    employee_count: int | None = Field(None, description="Exact employee count")
    employee_count_min: int | None = Field(None, description="Minimum employee count")
    employee_count_max: int | None = Field(None, description="Maximum employee count")
    total_funding_raised_min: float | None = Field(
        None, description="Minimum total funding raised"
    )
    total_funding_raised_max: float | None = Field(
        None, description="Maximum total funding raised"
    )
    tags: list[str] | None = Field(None, description="Industry tags")
    name: list[str] | None = Field(None, description="Company names")

    # ==========================================================================
    # PERSON-ONLY FIELDS - Used only in person query
    # ==========================================================================
    # Person's own location (different from company HQ)
    person_location_country: list[str] | None = Field(
        None, description="Person's country"
    )
    person_location_region: list[str] | None = Field(
        None, description="Person's state/region"
    )
    person_location_locality: list[str] | None = Field(
        None, description="Person's city"
    )
    person_location_name: list[str] | None = Field(
        None, description="Person's location name"
    )
    person_location_name_not_in: list[str] | None = Field(
        None, description="Exclude persons in these locations"
    )

    # Job title fields
    job_title: list[str] | None = Field(None, description="Person's job title")
    job_title_role: list[str] | None = Field(
        None, description="Job title role (engineering, sales, etc.)"
    )
    job_title_sub_role: list[str] | None = Field(
        None, description="Job title sub-role (software, devops, etc.)"
    )
    job_title_levels: list[str] | None = Field(
        None, description="Seniority level (cxo, vp, director, etc.)"
    )
    job_title_class: list[str] | None = Field(None, description="Expense category")

    # Skills
    skills: list[str] | None = Field(None, description="Person's skills")

    # ==========================================================================
    # COMPUTED PROPERTY - Mode Detection
    # ==========================================================================
    @computed_field
    @property
    def is_sic_based(self) -> bool:
        """Determine if this ICP triggers SIC-based flow."""
        return bool(self.sic_code or self.naics_code)

    # ==========================================================================
    # VALIDATORS
    # ==========================================================================
    @field_validator("size", mode="before")
    @classmethod
    def validate_size(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        invalid = [s for s in v if s not in VALID_COMPANY_SIZES]
        if invalid:
            raise ValueError(f"Invalid company size(s): {invalid}")
        return v

    @field_validator("industry", "industry_not_in", mode="before")
    @classmethod
    def validate_industry(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [i.lower() for i in v]
        invalid = [val for val in normalized if val not in VALID_INDUSTRIES]
        if invalid:
            raise ValueError(f"Invalid industry value(s): {invalid}")
        return normalized

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [t.lower() for t in v]
        invalid = [t for t in normalized if t not in VALID_COMPANY_TYPES]
        if invalid:
            raise ValueError(f"Invalid company type(s): {invalid}")
        return normalized

    @field_validator("inferred_revenue", mode="before")
    @classmethod
    def validate_inferred_revenue(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [r.lower() for r in v]
        invalid = [r for r in normalized if r not in VALID_INFERRED_REVENUE]
        if invalid:
            raise ValueError(f"Invalid inferred revenue(s): {invalid}")
        return normalized

    @field_validator("job_title_role", mode="before")
    @classmethod
    def validate_job_title_role(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [r.lower() for r in v]
        invalid = [val for val in normalized if val not in VALID_JOB_TITLE_ROLES]
        if invalid:
            raise ValueError(f"Invalid job_title_role value(s): {invalid}")
        return normalized

    @field_validator("job_title_sub_role", mode="before")
    @classmethod
    def validate_job_title_sub_role(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [r.lower() for r in v]
        invalid = [val for val in normalized if val not in VALID_JOB_TITLE_SUB_ROLES]
        if invalid:
            raise ValueError(f"Invalid job_title_sub_role value(s): {invalid}")
        return normalized

    @field_validator("job_title_levels", mode="before")
    @classmethod
    def validate_job_title_levels(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [l.lower() for l in v]
        invalid = [val for val in normalized if val not in VALID_JOB_TITLE_LEVELS]
        if invalid:
            raise ValueError(f"Invalid job_title_levels value(s): {invalid}")
        return normalized

    @field_validator("job_title_class", mode="before")
    @classmethod
    def validate_job_title_class(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [c.lower() for c in v]
        invalid = [val for val in normalized if val not in VALID_JOB_TITLE_CLASSES]
        if invalid:
            raise ValueError(f"Invalid job_title_class value(s): {invalid}")
        return normalized

    @field_validator(
        "location_country",
        "location_country_not_in",
        "location_region",
        "location_locality",
        "location_name",
        "location_name_not_in",
        "person_location_country",
        "person_location_region",
        "person_location_locality",
        "person_location_name",
        "person_location_name_not_in",
        mode="before",
    )
    @classmethod
    def normalize_location_fields(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        return [loc.lower() for loc in v]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                # Common - Company HQ location
                "location_country": ["united states"],
                "location_region": ["california"],
                "size": ["51-200", "201-500"],
                "industry": ["computer software"],
                # Company-only (triggers SIC-based flow)
                "sic_code": ["7371"],
                # Person-only
                "job_title_role": ["engineering"],
                "job_title_levels": ["director", "vp"],
                "skills": ["python", "aws"],
            }
        }
    )
