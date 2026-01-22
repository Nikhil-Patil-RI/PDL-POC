# Prospects Flow Design - PDL POC

## Overview

This document outlines the design for a unified **Prospects Router** that replaces Apollo with PDL for prospect generation. The design supports two user flows based on whether SIC codes are provided.

---

## API Endpoints

### 1. Preview Prospects
```
POST /api/v1/prospects/preview
```

### 2. Generate Prospects
```
POST /api/v1/prospects/generate
```

---

## Flow Logic

### Flow A: SIC-Based (Company-First)
**Condition:** User provides SIC codes

```
1. Company Search API (with sic_code filter + company criteria)
2. Extract company PDL IDs from results
3. Person Search API (with job_company_id IN (...) + person filters)
4. Return preview data (no save)
```

### Flow B: Direct Person Search
**Condition:** User does NOT provide SIC codes

```
1. Person Search API (with person filters including job_company_* fields)
2. Person Enrichment API (with person pdl_id from search results)
3. Return enriched data (no save)
```

---

## Current State vs Target State

### Current State (sdr-backend with Apollo)
```
Org Search → Get Org IDs → People Search (with org_ids) → Enrich → DB Write
```

### Target State (PDL POC)
```
Flow A (SIC-based): Company Search → Get PDL IDs → Person Search (with job_company_id) → Return
Flow B (Direct):    Person Search → Person Enrichment → Return
```

---

## Key PDL Insights

### 1. `job_company_id` Field
The Person Schema includes `job_company_id` which is the company's PDL ID. This allows filtering persons by their employer's PDL ID:

```sql
SELECT * FROM person WHERE job_company_id IN ('id1', 'id2', 'id3') AND ...
```

### 2. Search APIs Return Full Data
PDL Search APIs return **complete records** - no need for additional enrichment calls when using search:
- Company Search → Returns full company data (name, industry, location, funding, etc.)
- Person Search → Returns full person data (name, email, job_company_* fields, etc.)

### 3. When Enrichment Is Needed
- **NOT needed**: When using search APIs (data is already complete)
- **Needed**: When you have external IDs (e.g., company websites, LinkedIn URLs)

---

## User Flows

### Flow A: SIC-Based (Company-First) Flow

**Use Case:** User wants to find prospects at companies in specific SIC/NAICS industries.

```
User Input:
  - SIC codes: ["7371", "7372"]
  - Company criteria: location=India, size=51-200
  - Person criteria: job_title_role=engineering, job_title_levels=director

Step 1: Company Search API
  SQL: SELECT * FROM company WHERE sic_code IN ('7371', '7372') AND location.country='india' AND size IN ('51-200')
  Result: Companies with PDL IDs [id1, id2, id3, ...]

Step 2: Person Search API
  SQL: SELECT * FROM person WHERE job_company_id IN ('id1', 'id2', 'id3') AND job_title_role='engineering' AND job_title_levels='director'
  Result: Persons matching criteria at those companies

Output: Combined company + person data
```

### Flow B: Direct Person Search Flow

**Use Case:** User wants to find prospects by person criteria only (no SIC requirement).

```
User Input:
  - Person criteria: job_title_role=sales, location_country=united states, job_company_industry=computer software

Step 1: Person Search API
  SQL: SELECT * FROM person WHERE job_title_role='sales' AND location_country='united states' AND job_company_industry='computer software'
  Result: Persons matching criteria (with pdl_id)

Step 2: Person Enrichment API
  Input: pdl_id from search results
  Result: Enriched person data

Output: Enriched person data (includes job_company_* fields)
```

---

## API Design

### Unified Prospects Router: `/api/v1/prospects`

#### 1. Preview Prospects (No Credits for Enrichment)
```
POST /api/v1/prospects/preview
```

**Purpose:** Show preview data without consuming enrichment credits.

**Request:**
```json
{
  "mode": "sic_based" | "direct",
  "size": 10,
  "sic_codes": ["7371"],           // Required if mode="sic_based"
  "naics_codes": ["541511"],       // Optional
  "company_criteria": {            // For SIC-based mode
    "location_country": ["india"],
    "size": ["51-200", "201-500"]
  },
  "person_criteria": {             // For both modes
    "job_title_role": ["engineering", "sales"],
    "job_title_levels": ["director", "vp"],
    "location_country": ["india"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "mode": "sic_based",
  "companies_found": 25,
  "persons_found": 50,
  "preview_data": [
    {
      "person": { "full_name": "...", "job_title": "...", "work_email": "..." },
      "company": { "name": "...", "industry": "...", "size": "..." }
    }
  ],
  "scroll_token": "..."
}
```

#### 2. Generate Prospects (Full Flow + Export)
```
POST /api/v1/prospects/generate
```

**Purpose:** Generate prospects and export to JSON/database.

Same request format as preview, with additional options:
```json
{
  "mode": "sic_based",
  "size": 100,
  "export_format": "json",
  "sic_codes": ["7371"],
  "company_criteria": {...},
  "person_criteria": {...}
}
```


---

## Implementation Details

### Query Building Strategy

#### SIC-Based Mode Query Building

```python
# Step 1: Build Company Search Query
def build_company_query(sic_codes, naics_codes, company_criteria):
    conditions = []

    # Add SIC/NAICS codes
    if sic_codes:
        conditions.append(f"sic_code IN ({format_values(sic_codes)})")
    if naics_codes:
        conditions.append(f"naics_code IN ({format_values(naics_codes)})")

    # Add company criteria (location, size, industry, etc.)
    # ... existing company_query_builder logic

    return f"SELECT * FROM company WHERE {' AND '.join(conditions)}"

# Step 2: Build Person Search Query with Company IDs
def build_person_query(company_ids, person_criteria):
    conditions = []

    # Add company filter using job_company_id
    conditions.append(f"job_company_id IN ({format_values(company_ids)})")

    # Add person criteria (job_title, location, etc.)
    # ... existing query_builder logic

    return f"SELECT * FROM person WHERE {' AND '.join(conditions)}"
```

#### Direct Mode Query Building + Enrichment

```python
# Step 1: Direct person search
def build_person_query(person_criteria):
    conditions = []

    # Add person criteria
    # ... existing query_builder logic (ICP fields)

    return f"SELECT * FROM person WHERE {' AND '.join(conditions)}"

# Step 2: Enrich persons using PDL IDs from search results
async def enrich_persons(person_ids: list[str]):
    """
    Call Person Enrichment API for each person pdl_id from search results.
    """
    enriched_persons = []
    for pdl_id in person_ids:
        enriched = await person_enrichment_api(pdl_id=pdl_id)
        enriched_persons.append(enriched)
    return enriched_persons
```

---

## Optimization Strategies

### 1. Avoid Redundant API Calls

| Scenario | Action | Reason |
|----------|--------|--------|
| Using search criteria | Use search results directly | Search returns full data |
| Have external IDs | Use bulk enrichment | Need to fetch data by ID |

### 2. Pagination with scroll_token

```python
async def paginated_search(criteria, target_count):
    all_results = []
    scroll_token = None

    while len(all_results) < target_count:
        response = await search_api(
            criteria=criteria,
            size=min(100, target_count - len(all_results)),
            scroll_token=scroll_token
        )

        all_results.extend(response.data)
        scroll_token = response.scroll_token

        if not scroll_token:  # No more results
            break

    return all_results
```

### 3. Batch Processing for Large Requests

For requests > 100 prospects:
- Return first batch immediately
- Process remaining in background
- Provide progress tracking

---

## Comparison: Apollo vs PDL

| Aspect | Apollo (Current) | PDL (New) |
|--------|------------------|-----------|
| Company Search | `organization_search` | `company/search` |
| Person Search | `people_search` (with org_ids) | `person/search` (with job_company_id) |
| Link Field | Apollo org_id | job_company_id (PDL ID) |
| Enrichment | Required for emails/phones | Search returns full data |
| Industry Filter | industry param | sic_code, naics_code, industry |
| Credits | Per search + per enrichment | Per search only |

---

## Implementation Phases

### Phase 1: Schema & Router Setup
- [ ] Create `ProspectSearchRequest` schema
- [ ] Create `ProspectSearchResponse` schema
- [ ] Create `src/api/prospects.py` router
- [ ] Add `job_company_id` support to query builder

### Phase 2: Preview Flow
- [ ] Implement `preview_prospects` endpoint
- [ ] Implement SIC-based flow (company → person search → return preview)
- [ ] Implement direct flow (person search → person enrichment → return enriched data)
- [ ] No save/export in preview mode

### Phase 3: Generate Flow
- [ ] Implement `generate_prospects` endpoint
- [ ] Same flows as preview but with save/export to JSON
- [ ] Add pagination with scroll_token

### Phase 4: Optimization
- [ ] Add batch processing for large requests
- [ ] Add progress tracking
- [ ] Add caching for company IDs

---

## File Structure

```
src/
├── api/
│   ├── prospects.py          # New unified router
│   ├── persons.py            # Keep for direct person API access
│   └── companies.py          # Keep for direct company API access
├── schema/
│   ├── prospects.py          # ProspectSearchRequest, ProspectSearchResponse
│   ├── icp.py               # Existing ICP schema
│   └── company.py           # Existing CompanySearchSchema
├── services/
│   └── prospect_service.py   # Business logic for prospect generation
└── utils/
    ├── query_builder.py      # Existing person query builder
    └── company_query_builder.py  # Existing company query builder
```

---

## Sample Request/Response

### Preview Request (SIC-Based Mode)
```bash
curl -X POST "http://localhost:8000/api/v1/prospects/preview" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "sic_based",
    "size": 10,
    "sic_codes": ["7371", "7372"],
    "company_criteria": {
      "location_country": ["india"],
      "size": ["51-200", "201-500"]
    },
    "person_criteria": {
      "job_title_role": ["engineering"],
      "job_title_levels": ["director", "vp"]
    }
  }'
```

### Preview Request (Direct Mode)
```bash
curl -X POST "http://localhost:8000/api/v1/prospects/preview" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "direct",
    "size": 10,
    "person_criteria": {
      "job_title_role": ["sales"],
      "location_country": ["united states"],
      "job_company_industry": ["computer software"]
    }
  }'
```

---

## Schema Design

### ProspectSearchRequest (Unified Schema)

```python
from typing import Literal
from pydantic import BaseModel, Field, model_validator

class ProspectSearchRequest(BaseModel):
    mode: Literal["sic_based", "direct"] = Field(
        ..., description="Search mode: sic_based requires SIC codes, direct uses person criteria only"
    )
    size: int = Field(default=10, ge=1, le=100, description="Number of results per page")
    scroll_token: str | None = Field(default=None, description="Pagination token")

    # SIC-based mode fields
    sic_codes: list[str] | None = Field(default=None, description="SIC codes (required for sic_based mode)")
    naics_codes: list[str] | None = Field(default=None, description="NAICS codes (optional)")
    company_criteria: CompanySearchSchema | None = Field(default=None, description="Company filters")

    # Person criteria (used in both modes)
    person_criteria: ICP = Field(..., description="Person search criteria")

    @model_validator(mode="after")
    def validate_mode_requirements(self) -> "ProspectSearchRequest":
        if self.mode == "sic_based" and not self.sic_codes:
            raise ValueError("sic_codes required when mode is 'sic_based'")
        return self


class ProspectPreviewResponse(BaseModel):
    success: bool
    mode: str
    companies_found: int = 0
    persons_found: int
    preview_data: list[dict]
    scroll_token: str | None = None
    message: str | None = None


class ProspectGenerateResponse(BaseModel):
    success: bool
    mode: str
    companies_found: int = 0
    persons_generated: int
    export_path: str | None = None
    scroll_token: str | None = None
    message: str | None = None
```

---

## Next Steps

1. Review and approve this design document
2. Begin Phase 1 implementation
3. Write tests for each phase
4. Iterate based on testing results
