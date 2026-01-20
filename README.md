# PDL-POC (People Data Labs Proof of Concept)

A FastAPI-based proof of concept for integrating with People Data Labs (PDL) API for prospect generation and enrichment.

## Features

- **Preview Prospects**: Search for prospects matching ICP criteria (no enrichment credits)
- **Generate Prospects**: Search and enrich prospects with full data
- **SQL Query Builder**: Dynamically builds PDL SQL queries from ICP schema
- **Bulk Enrichment**: Enriches up to 100 prospects per API call
- **JSON Export**: Exports enriched prospects to timestamped JSON files

## Tech Stack

- **Python 3.12+**
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **PDL Python SDK** - People Data Labs client
- **Pytest** - Testing

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PDL-POC
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your PDL API key
   ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PDL_API_KEY` | Your People Data Labs API key | Yes |

## Usage

### Start the server

```bash
uvicorn src.main:app --reload
```

### API Endpoints

#### Preview Prospects
```bash
POST /api/v1/preview_prospects
```

Request body:
```json
{
  "number_of_prospects": 10,
  "icp": {
    "job_title_role": ["engineering"],
    "job_title_levels": ["director", "vp"],
    "job_company_industry": ["computer software"],
    "job_company_size": ["51-200", "201-500"]
  }
}
```

#### Generate Prospects
```bash
POST /api/v1/generate_prospects
```

Request body:
```json
{
  "number_of_prospects": 10,
  "icp": {
    "job_title_role": ["engineering"],
    "job_company_industry": ["computer software"]
  }
}
```

## ICP Fields

| Field | Description | Example |
|-------|-------------|---------|
| `job_title` | Exact job titles | `["Software Engineer", "CTO"]` |
| `job_title_role` | Job role category | `["engineering", "sales"]` |
| `job_title_sub_role` | Job sub-role | `["software", "devops"]` |
| `job_title_levels` | Seniority level | `["cxo", "vp", "director"]` |
| `job_company_industry` | Company industry | `["computer software"]` |
| `job_company_size` | Company size range | `["51-200", "201-500"]` |
| `location_country` | Person's country | `["united states"]` |

## Running Tests

```bash
pytest src/tests/ -v
```

## Project Structure

```
PDL-POC/
├── src/
│   ├── api/
│   │   └── prospects.py      # API endpoints
│   ├── schema/
│   │   ├── icp.py            # ICP schema with validation
│   │   └── prospects.py      # Request/Response schemas
│   ├── utils/
│   │   ├── pdl_client.py     # PDL API client wrapper
│   │   └── query_builder.py  # SQL query builder
│   ├── tests/
│   │   ├── test_prospects_api.py
│   │   └── test_query_builder.py
│   └── main.py               # FastAPI app
├── exports/                  # Generated prospect exports
├── .env                      # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## License

MIT

