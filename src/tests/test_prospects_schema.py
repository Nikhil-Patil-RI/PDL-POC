"""
Tests for Prospects Schema - Refactored to use CombinedICP.

Following TDD: Write tests first, then implement the schema.

The new design uses CombinedICP which:
- Contains all fields from both company and person schemas
- Automatically detects mode based on sic_code/naics_code presence
- Maps common fields to both company and person queries
"""

import pytest
from pydantic import ValidationError

from src.schema.prospects import (
    ProspectSearchRequest,
    ProspectPreviewResponse,
    ProspectGenerateResponse,
)
from src.schema.combined_icp import CombinedICP


class TestProspectSearchRequest:
    """Test cases for ProspectSearchRequest schema with CombinedICP."""

    def test_request_with_sic_code_triggers_sic_based_mode(self):
        """Test that sic_code in ICP triggers SIC-based mode."""
        request = ProspectSearchRequest(
            icp=CombinedICP(
                sic_code=["7371", "7372"],
                job_title_role=["engineering"],
            ),
        )
        assert request.icp.is_sic_based is True
        assert request.icp.sic_code == ["7371", "7372"]

    def test_request_with_naics_code_triggers_sic_based_mode(self):
        """Test that naics_code in ICP triggers SIC-based mode."""
        request = ProspectSearchRequest(
            icp=CombinedICP(
                naics_code=["541511"],
                job_title_role=["engineering"],
            ),
        )
        assert request.icp.is_sic_based is True

    def test_request_without_codes_is_direct_mode(self):
        """Test that absence of sic/naics codes means direct mode."""
        request = ProspectSearchRequest(
            icp=CombinedICP(
                job_title_role=["engineering"],
                location_country=["united states"],
            ),
        )
        assert request.icp.is_sic_based is False

    def test_request_with_combined_fields(self):
        """Test request with both company and person fields."""
        request = ProspectSearchRequest(
            icp=CombinedICP(
                # Company-only (triggers SIC-based)
                sic_code=["7371"],
                # Common fields
                location_country=["united states"],
                size=["51-200", "201-500"],
                industry=["computer software"],
                # Person-only
                job_title_role=["engineering"],
                job_title_levels=["director", "vp"],
                skills=["python", "aws"],
            ),
        )
        assert request.icp.is_sic_based is True
        assert request.icp.location_country == ["united states"]
        assert request.icp.job_title_role == ["engineering"]

    def test_size_default_value(self):
        """Test that size defaults to 10."""
        request = ProspectSearchRequest(icp=CombinedICP())
        assert request.size == 10

    def test_size_validation_min(self):
        """Test that size must be at least 1."""
        with pytest.raises(ValidationError):
            ProspectSearchRequest(size=0, icp=CombinedICP())

    def test_size_validation_max(self):
        """Test that size must be at most 100."""
        with pytest.raises(ValidationError):
            ProspectSearchRequest(size=101, icp=CombinedICP())

    def test_scroll_token_optional(self):
        """Test that scroll_token is optional."""
        request = ProspectSearchRequest(icp=CombinedICP())
        assert request.scroll_token is None

    def test_scroll_token_can_be_set(self):
        """Test that scroll_token can be set."""
        request = ProspectSearchRequest(
            icp=CombinedICP(),
            scroll_token="abc123",
        )
        assert request.scroll_token == "abc123"

    def test_empty_icp_is_valid(self):
        """Test that empty ICP is valid (direct mode)."""
        request = ProspectSearchRequest(icp=CombinedICP())
        assert request.icp.is_sic_based is False


class TestProspectPreviewResponse:
    """Test cases for ProspectPreviewResponse schema."""

    def test_preview_response_structure(self):
        """Test the structure of preview response."""
        response = ProspectPreviewResponse(
            success=True,
            mode="sic_based",
            companies_found=10,
            persons_found=50,
            preview_data=[{"full_name": "Test User"}],
        )
        assert response.success is True
        assert response.mode == "sic_based"
        assert response.companies_found == 10
        assert response.persons_found == 50


class TestProspectGenerateResponse:
    """Test cases for ProspectGenerateResponse schema."""

    def test_generate_response_structure(self):
        """Test the structure of generate response."""
        response = ProspectGenerateResponse(
            success=True,
            mode="direct",
            persons_generated=25,
            export_path="/exports/prospects_20240122.json",
        )
        assert response.success is True
        assert response.mode == "direct"
        assert response.persons_generated == 25
        assert response.export_path is not None
