"""
Tests for Prospects API Router - Refactored to use CombinedICP.

Following TDD: Write tests first, then implement the router.

The new API uses CombinedICP which automatically detects mode:
- If sic_code or naics_code present → SIC-based flow
- Otherwise → Direct flow
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


class TestProspectsPreviewAPI:
    """Test cases for POST /api/v1/prospects/preview endpoint."""

    @patch("src.api.prospects.get_pdl_client")
    def test_preview_sic_based_success(self, mock_get_client):
        """Test SIC-based mode (with sic_code) preview returns companies and persons."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock company search response
        mock_client.company_search.return_value = {
            "status": 200,
            "total": 2,
            "data": [
                {"id": "company1", "name": "Company One"},
                {"id": "company2", "name": "Company Two"},
            ],
        }

        # Mock person search response
        mock_client.person_search.return_value = {
            "status": 200,
            "total": 5,
            "data": [
                {"id": "person1", "full_name": "John Doe"},
                {"id": "person2", "full_name": "Jane Smith"},
            ],
        }

        response = client.post(
            "/api/v1/prospects/preview",
            json={
                "size": 10,
                "icp": {
                    "sic_code": ["7371"],
                    "job_title_role": ["engineering"],
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["mode"] == "sic_based"
        assert data["companies_found"] == 2
        assert data["persons_found"] == 2

    @patch("src.api.prospects.get_pdl_client")
    def test_preview_direct_mode_success(self, mock_get_client):
        """Test direct mode (without sic/naics codes) searches persons WITHOUT enrichment."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock person search response
        mock_client.person_search.return_value = {
            "status": 200,
            "total": 2,
            "data": [
                {"id": "person1", "full_name": "John Doe"},
                {"id": "person2", "full_name": "Jane Smith"},
            ],
        }

        response = client.post(
            "/api/v1/prospects/preview",
            json={
                "size": 10,
                "icp": {
                    "job_title_role": ["engineering"],
                    "location_country": ["united states"],
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["mode"] == "direct"
        assert data["companies_found"] == 0
        assert data["persons_found"] == 2
        # Preview should NOT call enrichment
        mock_client.person_enrichment.assert_not_called()

    def test_preview_empty_icp_is_valid(self):
        """Test that empty ICP is valid (direct mode)."""
        # This should fail at PDL call level, not validation level
        with patch("src.api.prospects.get_pdl_client") as mock_get_client:
            mock_client = MagicMock()
            mock_get_client.return_value = mock_client
            mock_client.person_search.return_value = {
                "status": 200,
                "total": 0,
                "data": [],
            }

            response = client.post(
                "/api/v1/prospects/preview",
                json={
                    "size": 10,
                    "icp": {},
                },
            )
            # Should not fail validation - empty ICP is valid
            assert response.status_code == 200


class TestProspectsGenerateAPI:
    """Test cases for POST /api/v1/prospects/generate endpoint."""

    @patch("src.api.prospects.get_pdl_client")
    def test_generate_sic_based_with_enrichment(self, mock_get_client):
        """Test SIC-based generate includes enrichment and exports to file."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock company search response
        mock_client.company_search.return_value = {
            "status": 200,
            "total": 1,
            "data": [{"id": "company1", "name": "Company One"}],
        }

        # Mock person search response
        mock_client.person_search.return_value = {
            "status": 200,
            "total": 2,
            "data": [
                {"id": "person1", "full_name": "John Doe"},
                {"id": "person2", "full_name": "Jane Smith"},
            ],
        }

        # Mock person enrichment response
        mock_client.person_enrichment.return_value = {
            "status": 200,
            "data": {
                "id": "person1",
                "full_name": "John Doe",
                "work_email": "john@company.com",
            },
        }

        response = client.post(
            "/api/v1/prospects/generate",
            json={
                "size": 10,
                "icp": {
                    "sic_code": ["7371"],
                    "job_title_role": ["engineering"],
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["mode"] == "sic_based"
        assert data["export_path"] is not None
        assert "prospects_" in data["export_path"]
        # Generate SHOULD call enrichment for SIC-based mode too
        assert mock_client.person_enrichment.call_count == 2

    @patch("src.api.prospects.get_pdl_client")
    def test_generate_direct_mode_with_enrichment(self, mock_get_client):
        """Test direct mode generate includes enrichment and exports to file."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock person search response
        mock_client.person_search.return_value = {
            "status": 200,
            "total": 2,
            "data": [
                {"id": "person1", "full_name": "John Doe"},
                {"id": "person2", "full_name": "Jane Smith"},
            ],
        }

        # Mock person enrichment response
        mock_client.person_enrichment.return_value = {
            "status": 200,
            "data": {
                "id": "person1",
                "full_name": "John Doe",
                "work_email": "john@company.com",
            },
        }

        response = client.post(
            "/api/v1/prospects/generate",
            json={
                "size": 10,
                "icp": {
                    "job_title_role": ["engineering"],
                    "location_country": ["united states"],
                },
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["mode"] == "direct"
        assert data["export_path"] is not None
        assert "prospects_" in data["export_path"]
        # Generate SHOULD call enrichment for direct mode
        assert mock_client.person_enrichment.call_count == 2
