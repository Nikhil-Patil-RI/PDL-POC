"""
SQL Query Builder for PDL Person Search.

Converts ICP schema to PDL-compatible SQL queries.
All fields map directly to PDL person schema fields.
"""

import logging

from src.schema.icp import ICP

logger = logging.getLogger(__name__)


class PDLQueryBuilder:
    """
    Builds SQL queries for PDL Person Search API from ICP criteria.

    PDL uses SQL-like syntax: SELECT * FROM person WHERE <conditions>
    All queries include: work_email IS NOT NULL
    """

    def __init__(self, icp: ICP):
        """Initialize with ICP criteria."""
        self.icp = icp
        self.conditions: list[str] = []

    def build(self) -> str:
        """Build complete SQL query from ICP."""
        # Always require work_email to be present
        self.conditions = ["work_email IS NOT NULL"]

        self._add_person_location_conditions()
        self._add_job_title_conditions()
        self._add_company_conditions()
        self._add_company_location_conditions()
        self._add_skills_conditions()

        where_clause = " AND ".join(self.conditions)
        return f"SELECT * FROM person WHERE {where_clause}"

    def _add_person_location_conditions(self) -> None:
        """Add person location filter conditions."""
        self._add_in_condition("location_country", self.icp.location_country)
        self._add_in_condition("location_region", self.icp.location_region)
        self._add_in_condition("location_locality", self.icp.location_locality)

    def _add_job_title_conditions(self) -> None:
        """Add job title filter conditions."""
        self._add_in_condition("job_title", self.icp.job_title)
        self._add_in_condition("job_title_role", self.icp.job_title_role)
        self._add_in_condition("job_title_sub_role", self.icp.job_title_sub_role)
        self._add_in_condition("job_title_levels", self.icp.job_title_levels)
        self._add_in_condition("job_title_class", self.icp.job_title_class)

    def _add_company_conditions(self) -> None:
        """Add current company filter conditions."""
        self._add_in_condition("job_company_industry", self.icp.job_company_industry)
        self._add_in_condition("job_company_size", self.icp.job_company_size)
        self._add_in_condition("job_company_type", self.icp.job_company_type)
        self._add_in_condition("job_company_inferred_revenue", self.icp.job_company_inferred_revenue)

    def _add_company_location_conditions(self) -> None:
        """Add company HQ location filter conditions."""
        self._add_in_condition("job_company_location_name", self.icp.job_company_location_name)
        self._add_in_condition("job_company_location_country", self.icp.job_company_location_country)
        self._add_in_condition("job_company_location_region", self.icp.job_company_location_region)
        self._add_in_condition("job_company_location_locality", self.icp.job_company_location_locality)

    def _add_skills_conditions(self) -> None:
        """Add person skills filter conditions."""
        self._add_in_condition("skills", self.icp.skills)

    # Fields that should preserve original case (not be lowercased)
    # Note: job_company_inferred_revenue has a lowercase normalizer in PDL's Elasticsearch,
    # so it should be lowercased (not preserved). Only job_company_size needs case preservation.
    PRESERVE_CASE_FIELDS = {"job_company_size"}

    def _add_in_condition(self, field: str, values: list[str] | None) -> None:
        """Add IN condition for a field."""
        if values:
            preserve_case = field in self.PRESERVE_CASE_FIELDS
            formatted = self._format_list_values(values, preserve_case=preserve_case)
            self.conditions.append(f"{field} IN {formatted}")

    def _add_range_condition(self, field: str, min_val: int | None, max_val: int | None) -> None:
        """Add range condition for a field."""
        if min_val is not None:
            self.conditions.append(f"{field} >= {min_val}")
        if max_val is not None:
            self.conditions.append(f"{field} <= {max_val}")

    @staticmethod
    def _format_list_values(values: list[str], preserve_case: bool = False) -> str:
        """Format list values for SQL IN clause."""
        if preserve_case:
            formatted = ", ".join(f"'{v}'" for v in values)
        else:
            formatted = ", ".join(f"'{v.lower()}'" for v in values)
        return f"({formatted})"


def build_pdl_query(icp: ICP) -> str:
    """Build PDL SQL query from ICP."""
    builder = PDLQueryBuilder(icp)
    query = builder.build()
    print(f"PDL SQL Query: {query}")
    return query

