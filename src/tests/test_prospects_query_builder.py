"""
Tests for Prospects Query Builder.

Following TDD: Write tests first, then implement the query builder.

The prospects query builder handles field mapping between CombinedICP
and both company and person queries.
"""

import pytest

from src.schema.combined_icp import CombinedICP
from src.utils.prospects_query_builder import ProspectsQueryBuilder


class TestProspectsQueryBuilderCompanyQuery:
    """Test company query building from CombinedICP."""

    def test_build_company_query_with_sic_code(self):
        """Test building company query with SIC code."""
        icp = CombinedICP(sic_code=["7371", "7372"])
        builder = ProspectsQueryBuilder(icp)
        query = builder.build_company_query()

        assert "sic_code IN ('7371', '7372')" in query
        assert "SELECT * FROM company WHERE" in query

    def test_build_company_query_with_location(self):
        """Test that common location fields map to company query."""
        icp = CombinedICP(
            sic_code=["7371"],
            location_country=["united states"],
            location_region=["california"],
        )
        builder = ProspectsQueryBuilder(icp)
        query = builder.build_company_query()

        assert "location_country IN ('united states')" in query
        assert "location_region IN ('california')" in query

    def test_build_company_query_with_size_and_industry(self):
        """Test company attributes in query."""
        icp = CombinedICP(
            sic_code=["7371"],
            size=["51-200", "201-500"],
            industry=["computer software"],
        )
        builder = ProspectsQueryBuilder(icp)
        query = builder.build_company_query()

        assert "size IN ('51-200', '201-500')" in query
        assert "industry IN ('computer software')" in query


class TestProspectsQueryBuilderPersonQuery:
    """Test person query building from CombinedICP."""

    def test_build_person_query_basic(self):
        """Test building person query with job title filters."""
        icp = CombinedICP(
            job_title_role=["engineering"],
            job_title_levels=["director", "vp"],
        )
        builder = ProspectsQueryBuilder(icp)
        query = builder.build_person_query()

        assert "job_title_role IN ('engineering')" in query
        assert "job_title_levels IN ('director', 'vp')" in query
        assert "work_email IS NOT NULL" in query

    def test_build_person_query_maps_common_fields(self):
        """Test that common location fields map to job_company_* in person query."""
        icp = CombinedICP(
            location_country=["united states"],
            location_region=["california"],
            industry=["computer software"],
            size=["51-200"],
        )
        builder = ProspectsQueryBuilder(icp)
        query = builder.build_person_query()

        # Common fields should be mapped to job_company_* prefix
        assert "job_company_location_country IN ('united states')" in query
        assert "job_company_location_region IN ('california')" in query
        assert "job_company_industry IN ('computer software')" in query
        assert "job_company_size IN ('51-200')" in query

    def test_build_person_query_with_person_location(self):
        """Test person-specific location fields (person's own location)."""
        icp = CombinedICP(
            person_location_country=["united states"],
            person_location_region=["new york"],
        )
        builder = ProspectsQueryBuilder(icp)
        query = builder.build_person_query()

        # Person location fields should NOT have job_company_ prefix
        assert "location_country IN ('united states')" in query
        assert "location_region IN ('new york')" in query

    def test_build_person_query_with_skills(self):
        """Test skills filter in person query."""
        icp = CombinedICP(skills=["python", "aws"])
        builder = ProspectsQueryBuilder(icp)
        query = builder.build_person_query()

        assert "skills IN ('python', 'aws')" in query


class TestProspectsQueryBuilderWithCompanyIds:
    """Test person query with company IDs for SIC-based flow."""

    def test_build_person_query_with_company_ids(self):
        """Test adding job_company_id filter for SIC-based flow."""
        icp = CombinedICP(job_title_role=["engineering"])
        builder = ProspectsQueryBuilder(icp)
        company_ids = ["company1", "company2"]
        query = builder.build_person_query_with_company_ids(company_ids)

        assert "job_company_id IN ('company1', 'company2')" in query
        assert "job_title_role IN ('engineering')" in query

    def test_preserves_case_for_company_ids(self):
        """Test that company IDs preserve case (PDL IDs are case-sensitive)."""
        icp = CombinedICP()
        builder = ProspectsQueryBuilder(icp)
        company_ids = ["RRaBQHrRdGzKrWpBkSdyeAxluorX"]
        query = builder.build_person_query_with_company_ids(company_ids)

        assert "job_company_id IN ('RRaBQHrRdGzKrWpBkSdyeAxluorX')" in query
