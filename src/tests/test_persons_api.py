"""
Tests for Persons API endpoints.
"""

import json
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.schema.icp import ICP


client = TestClient(app)


class TestSearchPersonsAPI:
    """Test cases for search_persons endpoint."""

    @patch("src.api.persons.get_pdl_client")
    def test_search_persons_success(self, mock_get_client):
        """Test successful search persons request."""
        # Mock PDL client response
        mock_client = MagicMock()
        mock_client.person_search.return_value = {
            "status": 200,
            "total": 2,
            "data": [
                {
                    "id": "pdl-123",
                    "first_name": "John",
                    "last_name": "Doe",
                    "full_name": "John Doe",
                    "work_email": "john@example.com",
                    "job_title": "CTO",
                    "job_company_name": "Tech Corp",
                    "location_country": "united states",
                },
                {
                    "id": "pdl-456",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "full_name": "Jane Smith",
                    "work_email": "jane@example.com",
                    "job_title": "VP Engineering",
                    "job_company_name": "Startup Inc",
                    "location_country": "united states",
                },
            ],
            "scroll_token": "next_page_token",
        }
        mock_get_client.return_value = mock_client

        request_data = {
            "number_of_persons": 10,
            "icp": {
                "job_company_industry": ["computer software"],
                "location_country": ["united states"],
            },
        }

        response = client.post("/api/v1/search_persons", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["persons_found"] == 2
        assert len(data["persons"]) == 2
        assert data["persons"][0]["id"] == "pdl-123"
        assert data["scroll_token"] == "next_page_token"

    @patch("src.api.persons.get_pdl_client")
    def test_search_persons_pdl_error(self, mock_get_client):
        """Test search persons when PDL returns error."""
        mock_client = MagicMock()
        mock_client.person_search.return_value = {
            "status": 400,
            "error": {"message": "Invalid query"},
        }
        mock_get_client.return_value = mock_client

        request_data = {
            "number_of_persons": 10,
            "icp": {"job_company_industry": ["computer software"]},
        }

        response = client.post("/api/v1/search_persons", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["status_code"] == 400

    def test_search_persons_validation_error(self):
        """Test search persons with invalid request."""
        request_data = {
            # Missing required fields (icp)
        }

        response = client.post("/api/v1/search_persons", json=request_data)
        assert response.status_code == 422


class TestEnrichPersonsAPI:
    """Test cases for enrich_persons endpoint."""

    @patch("src.api.persons.get_pdl_client")
    @patch("src.api.persons._export_persons_to_json")
    def test_enrich_persons_success(self, mock_export, mock_get_client):
        """Test successful enrich persons request."""
        mock_client = MagicMock()
        mock_client.person_search.return_value = {
            "status": 200,
            "total": 1,
            "data": [
                {
                    "id": "pdl-789",
                    "first_name": "Bob",
                    "last_name": "Wilson",
                    "full_name": "Bob Wilson",
                    "work_email": "bob@example.com",
                    "job_title": "Director",
                    "job_company_name": "Enterprise Co",
                },
            ],
        }
        # Mock bulk enrichment response (returns list of enriched persons)
        mock_client.person_bulk_enrichment.return_value = [
            {
                "status": 200,
                "data": {
                    "id": "pdl-789",
                    "first_name": "Bob",
                    "last_name": "Wilson",
                    "full_name": "Bob Wilson",
                    "work_email": "bob@example.com",
                    "job_title": "Director",
                    "job_company_name": "Enterprise Co",
                },
            },
        ]
        mock_get_client.return_value = mock_client
        mock_export.return_value = "/exports/persons_20260120_120000.json"

        request_data = {
            "number_of_persons": 10,
            "icp": {"job_company_industry": ["computer software"]},
        }

        response = client.post("/api/v1/enrich_persons", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["persons_enriched"] == 1
        assert data["export_file"] is not None
        # Verify bulk enrichment was called with the PDL IDs from search
        mock_client.person_bulk_enrichment.assert_called_once_with(
            pdl_ids=["pdl-789"]
        )

    def test_enrich_persons_validation_error(self):
        """Test enrich persons with invalid request."""
        request_data = {
            "number_of_persons": 0,  # Invalid: must be >= 1
            "icp": {},
        }

        response = client.post("/api/v1/enrich_persons", json=request_data)
        assert response.status_code == 422

