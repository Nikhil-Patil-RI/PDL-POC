"""
Prospects Query Builder for unified prospects search.

This query builder handles field mapping between CombinedICP and both
company and person queries.

Field Mapping:
- Common fields (location_*, industry, size) → company query uses as-is
- Common fields (location_*, industry, size) → person query maps to job_company_*
- Person-only fields (person_location_*, job_title_*, skills) → person query as-is
- Company-only fields (sic_code, naics_code, founded_*, etc.) → company query only
"""

from src.schema.combined_icp import CombinedICP


class ProspectsQueryBuilder:
    """Build PDL SQL queries from CombinedICP schema."""

    def __init__(self, icp: CombinedICP):
        self.icp = icp
        self.conditions: list[str] = []

    def build_company_query(self) -> str:
        """
        Build company search query from CombinedICP.

        Uses common fields + company-only fields.
        """
        self.conditions = []

        # SIC/NAICS codes (company-only)
        self._add_in_condition("sic_code", self.icp.sic_code)
        self._add_in_condition("naics_code", self.icp.naics_code)

        # Common location fields (use as-is for company)
        self._add_in_condition("location_country", self.icp.location_country)
        self._add_not_in_condition("location_country", self.icp.location_country_not_in)
        self._add_in_condition("location_region", self.icp.location_region)
        self._add_in_condition("location_locality", self.icp.location_locality)
        self._add_like_conditions("location_name", self.icp.location_name)
        self._add_not_like_conditions("location_name", self.icp.location_name_not_in)

        # Common company attributes (use as-is for company)
        self._add_in_condition("industry", self.icp.industry)
        self._add_not_in_condition("industry", self.icp.industry_not_in)
        self._add_in_condition("size", self.icp.size)
        self._add_in_condition("inferred_revenue", self.icp.inferred_revenue)
        self._add_in_condition("type", self.icp.type)
        self._add_in_condition("name", self.icp.name)
        self._add_in_condition("tags", self.icp.tags)

        # Company-only fields
        self._add_exact_condition("founded", self.icp.founded)
        self._add_range_conditions(
            "founded", self.icp.founded_min, self.icp.founded_max
        )
        self._add_exact_condition("employee_count", self.icp.employee_count)
        self._add_range_conditions(
            "employee_count", self.icp.employee_count_min, self.icp.employee_count_max
        )
        self._add_range_conditions(
            "total_funding_raised",
            self.icp.total_funding_raised_min,
            self.icp.total_funding_raised_max,
        )

        if not self.conditions:
            return "SELECT * FROM company"

        where_clause = " AND ".join(self.conditions)
        return f"SELECT * FROM company WHERE {where_clause}"

    def build_person_query(self) -> str:
        """
        Build person search query from CombinedICP.

        Maps common fields to job_company_* prefix.
        """
        self.conditions = ["work_email IS NOT NULL"]

        # Map common location fields to job_company_location_*
        self._add_in_condition(
            "job_company_location_country", self.icp.location_country
        )
        self._add_not_in_condition(
            "job_company_location_country", self.icp.location_country_not_in
        )
        self._add_in_condition("job_company_location_region", self.icp.location_region)
        self._add_in_condition(
            "job_company_location_locality", self.icp.location_locality
        )
        self._add_like_conditions("job_company_location_name", self.icp.location_name)
        self._add_not_like_conditions(
            "job_company_location_name", self.icp.location_name_not_in
        )

        # Map common company attributes to job_company_*
        self._add_in_condition("job_company_industry", self.icp.industry)
        self._add_not_in_condition("job_company_industry", self.icp.industry_not_in)
        self._add_in_condition("job_company_size", self.icp.size)
        self._add_in_condition(
            "job_company_inferred_revenue", self.icp.inferred_revenue
        )
        self._add_in_condition("job_company_type", self.icp.type)

        # Person-specific location fields (person's own location)
        self._add_in_condition("location_country", self.icp.person_location_country)
        self._add_in_condition("location_region", self.icp.person_location_region)
        self._add_in_condition("location_locality", self.icp.person_location_locality)
        self._add_like_conditions("location_name", self.icp.person_location_name)
        self._add_not_like_conditions(
            "location_name", self.icp.person_location_name_not_in
        )

        # Job title fields (person-only)
        self._add_in_condition("job_title", self.icp.job_title)
        self._add_in_condition("job_title_role", self.icp.job_title_role)
        self._add_in_condition("job_title_sub_role", self.icp.job_title_sub_role)
        self._add_in_condition("job_title_levels", self.icp.job_title_levels)
        self._add_in_condition("job_title_class", self.icp.job_title_class)

        # Skills (person-only)
        self._add_in_condition("skills", self.icp.skills)

        where_clause = " AND ".join(self.conditions)
        return f"SELECT * FROM person WHERE {where_clause}"

    def build_person_query_with_company_ids(self, company_ids: list[str]) -> str:
        """
        Build person query with job_company_id filter for SIC-based flow.

        Args:
            company_ids: List of PDL company IDs from company search.
        """
        self.conditions = ["work_email IS NOT NULL"]

        # Add job_company_id filter (preserve case - PDL IDs are case-sensitive)
        if company_ids:
            formatted_ids = ", ".join(f"'{cid}'" for cid in company_ids)
            self.conditions.append(f"job_company_id IN ({formatted_ids})")

        # Add person-specific filters (don't map common fields - using company IDs instead)
        # Person location
        self._add_in_condition("location_country", self.icp.person_location_country)
        self._add_in_condition("location_region", self.icp.person_location_region)
        self._add_in_condition("location_locality", self.icp.person_location_locality)
        self._add_like_conditions("location_name", self.icp.person_location_name)
        self._add_not_like_conditions(
            "location_name", self.icp.person_location_name_not_in
        )

        # Job title fields
        self._add_in_condition("job_title", self.icp.job_title)
        self._add_in_condition("job_title_role", self.icp.job_title_role)
        self._add_in_condition("job_title_sub_role", self.icp.job_title_sub_role)
        self._add_in_condition("job_title_levels", self.icp.job_title_levels)
        self._add_in_condition("job_title_class", self.icp.job_title_class)

        # Skills
        self._add_in_condition("skills", self.icp.skills)

        where_clause = " AND ".join(self.conditions)
        return f"SELECT * FROM person WHERE {where_clause}"

    # ==========================================================================
    # Helper Methods
    # ==========================================================================

    def _add_in_condition(self, field: str, values: list[str] | None) -> None:
        """Add 'field IN (values)' condition."""
        if values:
            formatted_values = ", ".join(f"'{v}'" for v in values)
            self.conditions.append(f"{field} IN ({formatted_values})")

    def _add_not_in_condition(self, field: str, values: list[str] | None) -> None:
        """Add 'field NOT IN (values)' condition."""
        if values:
            formatted_values = ", ".join(f"'{v}'" for v in values)
            self.conditions.append(f"{field} NOT IN ({formatted_values})")

    def _add_like_conditions(self, field: str, values: list[str] | None) -> None:
        """Add 'field LIKE '%value%'' conditions with OR."""
        if values:
            like_clauses = [f"{field} LIKE '%{v}%'" for v in values]
            if len(like_clauses) == 1:
                self.conditions.append(like_clauses[0])
            else:
                self.conditions.append(f"({' OR '.join(like_clauses)})")

    def _add_not_like_conditions(self, field: str, values: list[str] | None) -> None:
        """Add 'field NOT LIKE '%value%'' conditions with AND."""
        if values:
            for v in values:
                self.conditions.append(f"{field} NOT LIKE '%{v}%'")

    def _add_exact_condition(self, field: str, value: int | float | None) -> None:
        """Add 'field = value' condition."""
        if value is not None:
            self.conditions.append(f"{field} = {value}")

    def _add_range_conditions(
        self, field: str, min_val: int | float | None, max_val: int | float | None
    ) -> None:
        """Add range conditions (>= min, <= max)."""
        if min_val is not None:
            self.conditions.append(f"{field} >= {min_val}")
        if max_val is not None:
            self.conditions.append(f"{field} <= {max_val}")
