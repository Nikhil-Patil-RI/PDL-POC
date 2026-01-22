"""
Tests for CombinedICP Schema.

Following TDD: Write tests first, then implement the schema.

CombinedICP unifies company and person criteria into a single schema.
Field mapping:
- Common fields (company HQ location) map to both company and person queries
- Company-only fields: sic_code, naics_code, founded_*, employee_count_*, etc.
- Person-only fields: person_location_*, job_title_*, skills
"""

import pytest
from pydantic import ValidationError

from src.schema.combined_icp import CombinedICP


class TestCombinedICPFieldMapping:
    """Test field presence and mapping in CombinedICP."""

    def test_common_location_fields_present(self):
        """Test that common location fields are present (company HQ)."""
        icp = CombinedICP(
            location_country=["united states"],
            location_region=["california"],
            location_locality=["san francisco"],
            location_name=["san francisco, california, united states"],
        )
        assert icp.location_country == ["united states"]
        assert icp.location_region == ["california"]

    def test_company_only_fields_present(self):
        """Test company-only fields: sic_code, naics_code, founded, etc."""
        icp = CombinedICP(
            sic_code=["7371", "7372"],
            naics_code=["541511"],
            founded_min=2000,
            founded_max=2020,
            employee_count_min=50,
            employee_count_max=500,
        )
        assert icp.sic_code == ["7371", "7372"]
        assert icp.naics_code == ["541511"]
        assert icp.founded_min == 2000

    def test_person_only_fields_present(self):
        """Test person-only fields: person_location_*, job_title_*, skills."""
        icp = CombinedICP(
            person_location_country=["united states"],
            person_location_region=["california"],
            job_title=["software engineer"],
            job_title_role=["engineering"],
            job_title_levels=["senior", "director"],
            skills=["python", "aws"],
        )
        assert icp.person_location_country == ["united states"]
        assert icp.job_title_role == ["engineering"]
        assert icp.skills == ["python", "aws"]

    def test_combined_fields(self):
        """Test combining company and person fields."""
        icp = CombinedICP(
            # Company fields
            sic_code=["7371"],
            location_country=["united states"],
            size=["51-200", "201-500"],
            industry=["computer software"],
            # Person fields
            job_title_role=["engineering"],
            job_title_levels=["director", "vp"],
        )
        assert icp.sic_code == ["7371"]
        assert icp.size == ["51-200", "201-500"]
        assert icp.job_title_levels == ["director", "vp"]


class TestCombinedICPValidation:
    """Test validation in CombinedICP."""

    def test_size_validation(self):
        """Test size field validation."""
        with pytest.raises(ValidationError):
            CombinedICP(size=["invalid-size"])

    def test_industry_validation(self):
        """Test industry field validation."""
        with pytest.raises(ValidationError):
            CombinedICP(industry=["invalid-industry"])

    def test_job_title_role_validation(self):
        """Test job_title_role field validation."""
        with pytest.raises(ValidationError):
            CombinedICP(job_title_role=["invalid-role"])

    def test_job_title_levels_validation(self):
        """Test job_title_levels field validation."""
        with pytest.raises(ValidationError):
            CombinedICP(job_title_levels=["invalid-level"])


class TestCombinedICPModeDetection:
    """Test mode detection based on field presence."""

    def test_is_sic_based_with_sic_code(self):
        """Test that sic_code triggers SIC-based mode."""
        icp = CombinedICP(sic_code=["7371"])
        assert icp.is_sic_based is True

    def test_is_sic_based_with_naics_code(self):
        """Test that naics_code triggers SIC-based mode."""
        icp = CombinedICP(naics_code=["541511"])
        assert icp.is_sic_based is True

    def test_is_direct_without_codes(self):
        """Test that absence of sic/naics codes means direct mode."""
        icp = CombinedICP(job_title_role=["engineering"])
        assert icp.is_sic_based is False

    def test_empty_icp_is_direct(self):
        """Test that empty ICP is direct mode."""
        icp = CombinedICP()
        assert icp.is_sic_based is False
