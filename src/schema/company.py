"""Company Search Schema based on PDL Company Schema."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.schema.icp import VALID_INDUSTRIES

# Canonical PDL Company Sizes
# Source: https://docs.peopledatalabs.com/docs/company-sizes
VALID_COMPANY_SIZES: set[str] = {
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1001-5000",
    "5001-10000",
    "10001+",
}

# Canonical PDL Company Types
# Source: https://docs.peopledatalabs.com/docs/company-types
VALID_COMPANY_TYPES: set[str] = {
    "educational",
    "government",
    "nonprofit",
    "private",
    "public",
    "public_subsidiary",
}

# Canonical PDL Inferred Revenue Ranges (lowercase)
# Source: https://docs.peopledatalabs.com/docs/inferred-revenue-ranges
VALID_INFERRED_REVENUE: set[str] = {
    "$0-$1m",
    "$1m-$10m",
    "$10m-$50m",
    "$50m-$100m",
    "$100m-$250m",
    "$250m-$500m",
    "$500m-$1b",
    "$1b-$10b",
    "$10b+",
}


class CompanySearchSchema(BaseModel):
    """Schema for company search criteria based on PDL Company Schema."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                # Company identifiers
                "name": ["google", "microsoft"],
                # Company attributes
                "size": ["1001-5000", "5001-10000"],
                "type": ["public"],
                "industry": ["computer software", "internet"],
                "industry_not_in": ["staffing and recruiting"],
                "inferred_revenue": ["$100m-$250m", "$250m-$500m"],
                "founded": 1998,
                "founded_min": 1990,
                "founded_max": 2010,
                # Location fields
                "location_name": ["san francisco, california, united states"],
                "location_name_not_in": ["new york, new york, united states"],
                "location_country": ["united states"],
                "location_country_not_in": ["china", "russia"],
                "location_region": ["california"],
                "location_locality": ["san francisco"],
                "location_continent": ["north america"],
                # Tags
                "tags": ["saas", "b2b"],
                # Employee count
                "employee_count": 5000,
                "employee_count_min": 1000,
                "employee_count_max": 10000,
                # Funding fields
                "total_funding_raised_min": 1000000,
                "total_funding_raised_max": 100000000,
                # Industry codes
                "naics_code": ["541511"],
                "sic_code": ["7371"],
            }
        }
    )

    # Company identifiers
    name: list[str] | None = Field(
        default=None, description="Company names (lowercase)"
    )

    # Company attributes
    size: list[str] | None = Field(
        default=None,
        description="Company size ranges (e.g., '51-200', '201-500')",
    )
    type: list[str] | None = Field(
        default=None,
        description="Company types (e.g., 'private', 'public')",
    )
    industry: list[str] | None = Field(
        default=None,
        description="Company industry (include filter)",
    )
    industry_not_in: list[str] | None = Field(
        default=None,
        description="Exclude companies in these industries",
    )
    inferred_revenue: list[str] | None = Field(
        default=None,
        description="Inferred revenue range (e.g., '$10m-$50m')",
    )
    founded: int | None = Field(
        default=None, description="Year the company was founded"
    )
    founded_min: int | None = Field(default=None, description="Minimum founding year")
    founded_max: int | None = Field(default=None, description="Maximum founding year")

    # Location fields
    location_name: list[str] | None = Field(
        default=None,
        description="Full location string (e.g., 'san francisco, california, united states')",
    )
    location_name_not_in: list[str] | None = Field(
        default=None, description="Exclude companies in these locations"
    )
    location_country: list[str] | None = Field(
        default=None, description="Company HQ country"
    )
    location_country_not_in: list[str] | None = Field(
        default=None, description="Exclude companies in these countries"
    )
    location_region: list[str] | None = Field(
        default=None, description="Company HQ region/state"
    )
    location_locality: list[str] | None = Field(
        default=None, description="Company HQ city"
    )
    location_continent: list[str] | None = Field(
        default=None, description="Company HQ continent"
    )
    location_postal_code: list[str] | None = Field(
        default=None, description="Company HQ postal code"
    )

    # Tags/Keywords
    tags: list[str] | None = Field(
        default=None, description="Industry tags associated with the company"
    )

    # Employee count range
    employee_count: int | None = Field(default=None, description="Exact employee count")
    employee_count_min: int | None = Field(
        default=None, description="Minimum employee count"
    )
    employee_count_max: int | None = Field(
        default=None, description="Maximum employee count"
    )

    # Funding fields
    total_funding_raised_min: float | None = Field(
        default=None, description="Minimum total funding raised (in USD)"
    )
    total_funding_raised_max: float | None = Field(
        default=None, description="Maximum total funding raised (in USD)"
    )

    # Industry classification codes
    naics_code: list[str] | None = Field(
        default=None, description="NAICS industry codes"
    )
    sic_code: list[str] | None = Field(default=None, description="SIC industry codes")

    @field_validator("size", mode="before")
    @classmethod
    def validate_size(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        invalid = [s for s in v if s not in VALID_COMPANY_SIZES]
        if invalid:
            raise ValueError(
                f"Invalid company size(s): {invalid}. "
                f"Valid values: {sorted(VALID_COMPANY_SIZES)}"
            )
        return v

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [t.lower() for t in v]
        invalid = [t for t in normalized if t not in VALID_COMPANY_TYPES]
        if invalid:
            raise ValueError(
                f"Invalid company type(s): {invalid}. "
                f"Valid values: {sorted(VALID_COMPANY_TYPES)}"
            )
        return normalized

    @field_validator("inferred_revenue", mode="before")
    @classmethod
    def validate_inferred_revenue(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return None
        normalized = [r.lower() for r in v]
        invalid = [r for r in normalized if r not in VALID_INFERRED_REVENUE]
        if invalid:
            raise ValueError(
                f"Invalid inferred revenue(s): {invalid}. "
                f"Valid values: {sorted(VALID_INFERRED_REVENUE)}"
            )
        return normalized

    @field_validator("industry", "industry_not_in", mode="before")
    @classmethod
    def validate_industry(cls, v: list[str] | None) -> list[str] | None:
        """Validate industry values are from the canonical PDL list."""
        if v is None:
            return None
        normalized = [i.lower() for i in v]
        invalid_values = [val for val in normalized if val not in VALID_INDUSTRIES]
        if invalid_values:
            raise ValueError(
                f"Invalid industry value(s): {invalid_values}. "
                f"See valid values at: https://pdl-prod-schema.s3.us-west-2.amazonaws.com/28.0/enums/industry.txt"
            )
        return normalized

    @field_validator(
        "location_name",
        "location_name_not_in",
        "location_country",
        "location_country_not_in",
        mode="before",
    )
    @classmethod
    def validate_location_fields(cls, v: list[str] | None) -> list[str] | None:
        """Normalize location values to lowercase."""
        if v is None:
            return None
        return [loc.lower() for loc in v]
