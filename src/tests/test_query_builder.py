"""
Tests for PDL SQL Query Builder.
"""

import pytest

from src.schema.icp import ICP
from src.utils.query_builder import PDLQueryBuilder, build_pdl_query


class TestPDLQueryBuilder:
    """Test cases for PDLQueryBuilder class."""

    def test_empty_icp_includes_work_email_filter(self):
        """Test that empty ICP includes work_email IS NOT NULL."""
        icp = ICP()
        query = build_pdl_query(icp)
        assert query == "SELECT * FROM person WHERE work_email IS NOT NULL"

    def test_all_queries_include_work_email_filter(self):
        """Test that all queries include work_email IS NOT NULL."""
        icp = ICP(location_country=["united states"])
        query = build_pdl_query(icp)
        assert "work_email IS NOT NULL" in query

    def test_location_country_filter(self):
        """Test location country filter with single value."""
        icp = ICP(location_country=["united states"])
        query = build_pdl_query(icp)
        assert "location_country IN ('united states')" in query

    def test_location_country_multiple_values(self):
        """Test location country filter with multiple values."""
        icp = ICP(location_country=["united states", "canada"])
        query = build_pdl_query(icp)
        assert "location_country IN ('united states', 'canada')" in query

    def test_location_region_filter(self):
        """Test location region filter."""
        icp = ICP(location_region=["california", "texas"])
        query = build_pdl_query(icp)
        assert "location_region IN ('california', 'texas')" in query

    def test_location_locality_filter(self):
        """Test location locality filter."""
        icp = ICP(location_locality=["san francisco", "austin"])
        query = build_pdl_query(icp)
        assert "location_locality IN ('san francisco', 'austin')" in query

    def test_job_title_filter(self):
        """Test job title filter."""
        icp = ICP(job_title=["cto", "vp of engineering"])
        query = build_pdl_query(icp)
        assert "job_title IN ('cto', 'vp of engineering')" in query

    def test_job_title_role_filter(self):
        """Test job title role filter."""
        icp = ICP(job_title_role=["engineering", "sales"])
        query = build_pdl_query(icp)
        assert "job_title_role IN ('engineering', 'sales')" in query

    def test_job_title_sub_role_filter(self):
        """Test job title sub-role filter."""
        icp = ICP(job_title_sub_role=["web", "devops"])
        query = build_pdl_query(icp)
        assert "job_title_sub_role IN ('web', 'devops')" in query

    def test_job_title_levels_filter(self):
        """Test job title levels filter."""
        icp = ICP(job_title_levels=["cxo", "vp", "director"])
        query = build_pdl_query(icp)
        assert "job_title_levels IN ('cxo', 'vp', 'director')" in query

    def test_job_company_industry_filter(self):
        """Test company industry filter."""
        icp = ICP(job_company_industry=["computer software", "hospital & health care"])
        query = build_pdl_query(icp)
        assert "job_company_industry IN ('computer software', 'hospital & health care')" in query

    def test_job_company_size_filter(self):
        """Test company size filter."""
        icp = ICP(job_company_size=["51-200", "201-500"])
        query = build_pdl_query(icp)
        assert "job_company_size IN ('51-200', '201-500')" in query

    def test_job_company_location_name_filter(self):
        """Test company HQ location name filter uses LIKE for partial matching."""
        icp = ICP(job_company_location_name=["san francisco, california, united states"])
        query = build_pdl_query(icp)
        assert "job_company_location_name LIKE '%san francisco, california, united states%'" in query

    def test_job_company_location_country_filter(self):
        """Test company HQ country filter."""
        icp = ICP(job_company_location_country=["united states"])
        query = build_pdl_query(icp)
        assert "job_company_location_country IN ('united states')" in query

    def test_job_company_location_region_filter(self):
        """Test company HQ region filter."""
        icp = ICP(job_company_location_region=["california"])
        query = build_pdl_query(icp)
        assert "job_company_location_region IN ('california')" in query

    def test_job_company_location_locality_filter(self):
        """Test company HQ city filter."""
        icp = ICP(job_company_location_locality=["san francisco"])
        query = build_pdl_query(icp)
        assert "job_company_location_locality IN ('san francisco')" in query

    def test_combined_filters(self):
        """Test multiple filters combined with AND."""
        icp = ICP(
            location_country=["united states"],
            job_title_levels=["cxo", "vp"],
            job_company_industry=["computer software"],
        )
        query = build_pdl_query(icp)

        assert "SELECT * FROM person WHERE" in query
        assert "work_email IS NOT NULL" in query
        assert "location_country IN ('united states')" in query
        assert "job_title_levels IN ('cxo', 'vp')" in query
        assert "job_company_industry IN ('computer software')" in query
        assert " AND " in query

    def test_values_are_lowercased(self):
        """Test that string values are lowercased."""
        icp = ICP(location_country=["United States", "CANADA"])
        query = build_pdl_query(icp)
        assert "('united states', 'canada')" in query

