"""
PDL Client Utility for People Data Labs API.

Wraps the peopledatalabs SDK for person search and enrichment operations.
"""

import os
from typing import Any

from dotenv import load_dotenv
from peopledatalabs import PDLPY

load_dotenv()


class PDLClient:
    """
    Client wrapper for People Data Labs API operations.
    
    Provides methods for:
    - Person search using SQL queries
    - Person enrichment
    """

    def __init__(self, api_key: str | None = None, sandbox: bool = False):
        """
        Initialize PDL client.
        
        Args:
            api_key: PDL API key. Defaults to PDL_KEY env variable.
            sandbox: Whether to use sandbox mode for testing.
        """
        self.api_key = api_key or os.getenv("PDL_KEY", "")
        if not self.api_key:
            raise ValueError("PDL API key is required. Set PDL_KEY environment variable.")
        
        self.client = PDLPY(api_key=self.api_key, sandbox=sandbox)

    def person_search(
        self,
        sql_query: str,
        size: int = 25,
        scroll_token: str | None = None,
        titlecase: bool = True,
    ) -> dict[str, Any]:
        """
        Search for persons using SQL query.
        
        Args:
            sql_query: SQL query string for PDL person search.
            size: Number of results per page (max 100).
            scroll_token: Token for pagination.
            titlecase: Whether to titlecase names in response.
            
        Returns:
            dict with status, data, total, scroll_token, etc.
        """
        params = {
            "sql": sql_query,
            "size": min(size, 100),
            "pretty": True,
            "titlecase": titlecase,
        }
        
        if scroll_token:
            params["scroll_token"] = scroll_token
        
        response = self.client.person.search(**params)
        return response.json()

    def person_enrichment(
        self,
        pdl_id: str | None = None,
        linkedin_url: str | None = None,
        email: str | None = None,
        name: str | None = None,
        company: str | None = None,
        min_likelihood: int = 6,
        titlecase: bool = True,
    ) -> dict[str, Any]:
        """
        Enrich a person's data using PDL enrichment API.
        
        Args:
            pdl_id: PDL person ID for direct lookup.
            linkedin_url: LinkedIn profile URL.
            email: Email address.
            name: Full name of the person.
            company: Company name.
            min_likelihood: Minimum match likelihood (1-10).
            titlecase: Whether to titlecase names in response.
            
        Returns:
            dict with status and enriched person data.
        """
        params: dict[str, Any] = {
            "min_likelihood": min_likelihood,
            "pretty": True,
            "titlecase": titlecase,
        }
        
        if pdl_id:
            params["pdl_id"] = pdl_id
        if linkedin_url:
            params["profile"] = linkedin_url
        if email:
            params["email"] = email
        if name:
            params["name"] = name
        if company:
            params["company"] = company
        
        response = self.client.person.enrichment(**params)
        return response.json()

    def person_bulk_enrichment(
        self,
        pdl_ids: list[str],
        titlecase: bool = True,
    ) -> list[dict[str, Any]]:
        """
        Bulk enrich multiple persons by PDL ID.

        Request format per PDL docs:
        {
            "requests": [
                {"params": {"pdl_id": "..."}},
                {"params": {"pdl_id": "..."}}
            ]
        }

        Response format per PDL docs:
        [
            {"status": 200, "likelihood": 10, "data": {...}},
            {"status": 200, "likelihood": 10, "data": {...}}
        ]

        Args:
            pdl_ids: List of PDL person IDs to enrich.
            titlecase: Whether to titlecase names in response.

        Returns:
            List of enrichment results with status and data.
        """
        # Build requests in PDL's expected format: [{"params": {...}}, ...]
        bulk_requests = [{"params": {"pdl_id": pdl_id}} for pdl_id in pdl_ids]

        params = {
            "requests": bulk_requests,
            "pretty": True,
            "titlecase": titlecase,
        }

        response = self.client.person.bulk(**params)
        return response.json()


# Singleton instance
_pdl_client: PDLClient | None = None


def get_pdl_client(sandbox: bool = False) -> PDLClient:
    """Get or create PDL client instance."""
    global _pdl_client
    if _pdl_client is None:
        _pdl_client = PDLClient(sandbox=sandbox)
    return _pdl_client

