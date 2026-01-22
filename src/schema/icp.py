"""
ICP (Ideal Customer Profile) Schema for PDL-POC.

This schema contains fields supported by People Data Labs
for person search and enrichment.

Reference: docs/PERSON_SCHEMA.md
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator

# PDL canonical company size values
VALID_COMPANY_SIZES = [
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1001-5000",
    "5001-10000",
    "10001+",
]

# PDL canonical inferred revenue values
VALID_INFERRED_REVENUE = [
    "$0-$1M",
    "$1M-$10M",
    "$10M-$25M",
    "$25M-$50M",
    "$50M-$100M",
    "$100M-$250M",
    "$250M-$500M",
    "$500M-$1B",
    "$1B-$10B",
    "$10B+",
]

# PDL canonical industry values
VALID_INDUSTRIES = [
    "accounting",
    "airlines/aviation",
    "alternative dispute resolution",
    "alternative medicine",
    "animation",
    "apparel & fashion",
    "architecture & planning",
    "arts and crafts",
    "automotive",
    "aviation & aerospace",
    "banking",
    "biotechnology",
    "broadcast media",
    "building materials",
    "business supplies and equipment",
    "capital markets",
    "chemicals",
    "civic & social organization",
    "civil engineering",
    "commercial real estate",
    "computer & network security",
    "computer games",
    "computer hardware",
    "computer networking",
    "computer software",
    "construction",
    "consumer electronics",
    "consumer goods",
    "consumer services",
    "cosmetics",
    "dairy",
    "defense & space",
    "design",
    "e-learning",
    "education management",
    "electrical/electronic manufacturing",
    "entertainment",
    "environmental services",
    "events services",
    "executive office",
    "facilities services",
    "farming",
    "financial services",
    "fine art",
    "fishery",
    "food & beverages",
    "food production",
    "fund-raising",
    "furniture",
    "gambling & casinos",
    "glass, ceramics & concrete",
    "government administration",
    "government relations",
    "graphic design",
    "health, wellness and fitness",
    "higher education",
    "hospital & health care",
    "hospitality",
    "human resources",
    "import and export",
    "individual & family services",
    "industrial automation",
    "information services",
    "information technology and services",
    "insurance",
    "international affairs",
    "international trade and development",
    "internet",
    "investment banking",
    "investment management",
    "judiciary",
    "law enforcement",
    "law practice",
    "legal services",
    "legislative office",
    "leisure, travel & tourism",
    "libraries",
    "logistics and supply chain",
    "luxury goods & jewelry",
    "machinery",
    "management consulting",
    "maritime",
    "market research",
    "marketing and advertising",
    "mechanical or industrial engineering",
    "media production",
    "medical devices",
    "medical practice",
    "mental health care",
    "military",
    "mining & metals",
    "motion pictures and film",
    "museums and institutions",
    "music",
    "nanotechnology",
    "newspapers",
    "non-profit organization management",
    "oil & energy",
    "online media",
    "outsourcing/offshoring",
    "package/freight delivery",
    "packaging and containers",
    "paper & forest products",
    "performing arts",
    "pharmaceuticals",
    "philanthropy",
    "photography",
    "plastics",
    "political organization",
    "primary/secondary education",
    "printing",
    "professional training & coaching",
    "program development",
    "public policy",
    "public relations and communications",
    "public safety",
    "publishing",
    "railroad manufacture",
    "ranching",
    "real estate",
    "recreational facilities and services",
    "religious institutions",
    "renewables & environment",
    "research",
    "restaurants",
    "retail",
    "security and investigations",
    "semiconductors",
    "shipbuilding",
    "sporting goods",
    "sports",
    "staffing and recruiting",
    "supermarkets",
    "telecommunications",
    "textiles",
    "think tanks",
    "tobacco",
    "translation and localization",
    "transportation/trucking/railroad",
    "utilities",
    "venture capital & private equity",
    "veterinary",
    "warehousing",
    "wholesale",
    "wine and spirits",
    "wireless",
    "writing and editing",
]

# PDL canonical job title class values
VALID_JOB_TITLE_CLASSES = [
    "general_and_administrative",
    "research_and_development",
    "sales_and_marketing",
    "services",
    "unemployed",
]

# PDL canonical job title levels values
VALID_JOB_TITLE_LEVELS = [
    "cxo",
    "director",
    "entry",
    "manager",
    "owner",
    "partner",
    "senior",
    "training",
    "unpaid",
    "vp",
]

# PDL canonical job title role values
VALID_JOB_TITLE_ROLES = [
    "advisory",
    "analyst",
    "creative",
    "education",
    "engineering",
    "finance",
    "fulfillment",
    "health",
    "hospitality",
    "human_resources",
    "legal",
    "manufacturing",
    "marketing",
    "operations",
    "partnerships",
    "product",
    "professional_service",
    "public_service",
    "research",
    "sales",
    "sales_engineering",
    "support",
    "trade",
    "unemployed",
]

# PDL canonical job title sub-role values
VALID_JOB_TITLE_SUB_ROLES = [
    "academic",
    "account_executive",
    "account_management",
    "accounting",
    "accounting_services",
    "administrative",
    "advisor",
    "agriculture",
    "aides",
    "architecture",
    "artist",
    "board_member",
    "bookkeeping",
    "brand",
    "building_and_grounds",
    "business_analyst",
    "business_development",
    "chemical",
    "compliance",
    "construction",
    "consulting",
    "content",
    "corporate_development",
    "curation",
    "customer_success",
    "customer_support",
    "data_analyst",
    "data_engineering",
    "data_science",
    "dental",
    "devops",
    "doctor",
    "electric",
    "electrical",
    "emergency_services",
    "entertainment",
    "executive",
    "fashion",
    "financial",
    "fitness",
    "fraud",
    "graphic_design",
    "growth",
    "hair_stylist",
    "hardware",
    "health_and_safety",
    "human_resources",
    "implementation",
    "industrial",
    "information_technology",
    "insurance",
    "investment_banking",
    "investor",
    "investor_relations",
    "journalism",
    "judicial",
    "legal",
    "legal_services",
    "logistics",
    "machinist",
    "marketing_design",
    "marketing_services",
    "mechanic",
    "mechanical",
    "military",
    "network",
    "nursing",
    "partnerships",
    "pharmacy",
    "planning_and_analysis",
    "plumbing",
    "political",
    "primary_and_secondary",
    "procurement",
    "product_design",
    "product_management",
    "professor",
    "project_management",
    "protective_service",
    "qa_engineering",
    "quality_assurance",
    "realtor",
    "recruiting",
    "restaurants",
    "retail",
    "revenue_operations",
    "risk",
    "sales_development",
    "scientific",
    "security",
    "social_service",
    "software",
    "solutions_engineer",
    "strategy",
    "student",
    "talent_analytics",
    "therapy",
    "tour_and_travel",
    "training",
    "translation",
    "transport",
    "unemployed",
    "veterinarian",
    "warehouse",
    "web",
    "wellness",
]


class ICP(BaseModel):
    """
    Ideal Customer Profile schema for People Data Labs API.

    All fields map directly to PDL person schema fields for SQL-based search.
    Reference: docs/PERSON_SCHEMA.md
    """

    # === Person Location Fields (location_*) ===
    location_name: list[str] | None = Field(
        None, description="Person's location name (uses LIKE for partial matching)"
    )
    location_name_not_in: list[str] | None = Field(
        None, description="Exclude persons in these locations (uses NOT LIKE)"
    )
    location_country: list[str] | None = Field(None, description="Person's country")
    location_region: list[str] | None = Field(None, description="Person's state/region")
    location_locality: list[str] | None = Field(None, description="Person's city")

    # === Current Job Title Fields (job_title*) ===
    job_title: list[str] | None = Field(None, description="Person's job title")
    job_title_role: list[str] | None = Field(
        None,
        description="Job title role. Valid values: engineering, sales, marketing, finance, etc.",
    )

    @field_validator("job_title_role")
    @classmethod
    def validate_job_title_role(cls, v: list[str] | None) -> list[str] | None:
        """Validate job title role values are from the canonical PDL list."""
        if v is None:
            return v
        invalid_values = [val for val in v if val.lower() not in VALID_JOB_TITLE_ROLES]
        if invalid_values:
            raise ValueError(
                f"Invalid job_title_role value(s): {invalid_values}. "
                f"See valid values at: https://pdl-prod-schema.s3.us-west-2.amazonaws.com/30.0/enums/job_title_role.txt"
            )
        return [val.lower() for val in v]

    job_title_sub_role: list[str] | None = Field(
        None,
        description="Job title sub-role. Valid values: software, devops, data_science, web, etc.",
    )

    @field_validator("job_title_sub_role")
    @classmethod
    def validate_job_title_sub_role(cls, v: list[str] | None) -> list[str] | None:
        """Validate job title sub-role values are from the canonical PDL list."""
        if v is None:
            return v
        invalid_values = [
            val for val in v if val.lower() not in VALID_JOB_TITLE_SUB_ROLES
        ]
        if invalid_values:
            raise ValueError(
                f"Invalid job_title_sub_role value(s): {invalid_values}. "
                f"See valid values at: https://pdl-prod-schema.s3.us-west-2.amazonaws.com/30.0/enums/job_title_sub_role.txt"
            )
        return [val.lower() for val in v]

    job_title_levels: list[str] | None = Field(
        None,
        description="Seniority level. Valid values: cxo, vp, director, manager, senior, entry, owner, partner, training, unpaid",
    )

    @field_validator("job_title_levels")
    @classmethod
    def validate_job_title_levels(cls, v: list[str] | None) -> list[str] | None:
        """Validate job title levels values are from the canonical PDL list."""
        if v is None:
            return v
        invalid_values = [val for val in v if val.lower() not in VALID_JOB_TITLE_LEVELS]
        if invalid_values:
            raise ValueError(
                f"Invalid job_title_levels value(s): {invalid_values}. "
                f"See valid values at: https://pdl-prod-schema.s3.us-west-2.amazonaws.com/28.0/enums/job_title_levels.txt"
            )
        return [val.lower() for val in v]

    job_title_class: list[str] | None = Field(
        None,
        description="Expense category. Valid values: general_and_administrative, research_and_development, sales_and_marketing, services, unemployed",
    )

    @field_validator("job_title_class")
    @classmethod
    def validate_job_title_class(cls, v: list[str] | None) -> list[str] | None:
        """Validate job title class values are from the canonical PDL list."""
        if v is None:
            return v
        invalid_values = [
            val for val in v if val.lower() not in VALID_JOB_TITLE_CLASSES
        ]
        if invalid_values:
            raise ValueError(
                f"Invalid job_title_class value(s): {invalid_values}. "
                f"See valid values at: https://pdl-prod-schema.s3.us-west-2.amazonaws.com/30.0/enums/job_title_class.txt"
            )
        return [val.lower() for val in v]

    # === Current Company Fields (job_company_*) ===
    job_company_industry: list[str] | None = Field(
        None,
        description="Company industry. Examples: computer software, financial services, hospital & health care",
    )

    @field_validator("job_company_industry")
    @classmethod
    def validate_industry(cls, v: list[str] | None) -> list[str] | None:
        """Validate industry values are from the canonical PDL list."""
        if v is None:
            return v
        # Normalize to lowercase for comparison
        invalid_values = [val for val in v if val.lower() not in VALID_INDUSTRIES]
        if invalid_values:
            raise ValueError(
                f"Invalid industry value(s): {invalid_values}. "
                f"See valid values at: https://pdl-prod-schema.s3.us-west-2.amazonaws.com/28.0/enums/industry.txt"
            )
        return [val.lower() for val in v]  # Normalize to lowercase

    job_company_size: list[str] | None = Field(
        None,
        description="Company size. Valid values: 1-10, 11-50, 51-200, 201-500, 501-1000, 1001-5000, 5001-10000, 10001+",
    )

    @field_validator("job_company_size")
    @classmethod
    def validate_company_size(cls, v: list[str] | None) -> list[str] | None:
        """Validate company size values are from the canonical PDL list."""
        if v is None:
            return v
        invalid_sizes = [size for size in v if size not in VALID_COMPANY_SIZES]
        if invalid_sizes:
            raise ValueError(
                f"Invalid company size(s): {invalid_sizes}. "
                f"Valid values are: {VALID_COMPANY_SIZES}"
            )
        return v

    job_company_type: list[str] | None = Field(
        None, description="Company type: public, private, nonprofit, etc."
    )
    job_company_inferred_revenue: list[str] | None = Field(
        None,
        description="Revenue range. Valid values: $0-$1M, $1M-$10M, $10M-$25M, $25M-$50M, $50M-$100M, $100M-$250M, $250M-$500M, $500M-$1B, $1B-$10B, $10B+",
    )

    @field_validator("job_company_inferred_revenue")
    @classmethod
    def validate_inferred_revenue(cls, v: list[str] | None) -> list[str] | None:
        """Validate inferred revenue values are from the canonical PDL list."""
        if v is None:
            return v
        invalid_values = [val for val in v if val not in VALID_INFERRED_REVENUE]
        if invalid_values:
            raise ValueError(
                f"Invalid inferred revenue value(s): {invalid_values}. "
                f"Valid values are: {VALID_INFERRED_REVENUE}"
            )
        return v

    # === Company Location Fields (job_company_location_*) ===
    job_company_location_name: list[str] | None = Field(
        None, description="Company HQ location name (uses LIKE for partial matching)"
    )
    job_company_location_name_not_in: list[str] | None = Field(
        None, description="Exclude companies in these locations (uses NOT LIKE)"
    )
    job_company_location_country: list[str] | None = Field(
        None, description="Company HQ country"
    )
    job_company_location_region: list[str] | None = Field(
        None, description="Company HQ region/state"
    )
    job_company_location_locality: list[str] | None = Field(
        None, description="Company HQ city"
    )

    job_company_location_postal_code: list[str] | None = Field(
        None, description="Company HQ postal code"
    )

    # === Person Skills ===
    skills: list[str] | None = Field(None, description="Person's skills")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                # Person Location
                "location_name": ["san francisco, california"],
                "location_name_not_in": ["new york"],
                "location_country": ["united states"],
                "location_region": ["california"],
                "location_locality": ["san francisco"],
                # Job Title
                "job_title": ["software engineer"],
                "job_title_role": ["engineering"],
                "job_title_sub_role": ["software"],
                "job_title_levels": ["senior", "manager"],
                "job_title_class": ["research_and_development"],
                # Company
                "job_company_industry": ["computer software"],
                "job_company_size": ["51-200", "201-500"],
                "job_company_type": ["private"],
                "job_company_inferred_revenue": ["$10M-$25M", "$25M-$50M"],
                # Company Location
                "job_company_location_name": [
                    "san francisco, california, united states"
                ],
                "job_company_location_name_not_in": ["new york"],
                "job_company_location_country": ["united states"],
                "job_company_location_region": ["california"],
                "job_company_location_locality": ["san francisco"],
                "job_company_location_postal_code": ["94101"],
                # Skills
                "skills": ["python", "machine learning"],
            }
        }
    )
