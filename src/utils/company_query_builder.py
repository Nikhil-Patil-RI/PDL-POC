"""Company Query Builder for PDL Company Search API."""

from src.schema.company import CompanySearchSchema


def build_company_query(criteria: CompanySearchSchema) -> str:
    """
    Build a PDL SQL query from company search criteria.

    Args:
        criteria: CompanySearchSchema with search criteria.

    Returns:
        SQL query string for PDL Company Search API.
    """
    conditions: list[str] = []

    # Company identifiers
    if criteria.name:
        _add_in_condition(conditions, "name", criteria.name)

    # Company attributes
    if criteria.size:
        _add_in_condition(conditions, "size", criteria.size)
    if criteria.type:
        _add_in_condition(conditions, "type", criteria.type)
    if criteria.industry:
        _add_in_condition(conditions, "industry", criteria.industry)
    if criteria.industry_not_in:
        _add_not_in_condition(conditions, "industry", criteria.industry_not_in)
    if criteria.inferred_revenue:
        _add_in_condition(conditions, "inferred_revenue", criteria.inferred_revenue)

    # Founded year filters
    if criteria.founded:
        conditions.append(f"founded = {criteria.founded}")
    if criteria.founded_min:
        conditions.append(f"founded >= {criteria.founded_min}")
    if criteria.founded_max:
        conditions.append(f"founded <= {criteria.founded_max}")

    # Location filters
    if criteria.location_name:
        _add_like_condition(conditions, "location.name", criteria.location_name)
    if criteria.location_name_not_in:
        _add_not_like_condition(conditions, "location.name", criteria.location_name_not_in)
    if criteria.location_country:
        _add_in_condition(conditions, "location.country", criteria.location_country)
    if criteria.location_country_not_in:
        _add_not_in_condition(conditions, "location.country", criteria.location_country_not_in)
    if criteria.location_region:
        _add_in_condition(conditions, "location.region", criteria.location_region)
    if criteria.location_locality:
        _add_in_condition(conditions, "location.locality", criteria.location_locality)
    if criteria.location_metro:
        _add_in_condition(conditions, "location.metro", criteria.location_metro)
    if criteria.location_continent:
        _add_in_condition(conditions, "location.continent", criteria.location_continent)

    # Tags filter
    if criteria.tags:
        _add_in_condition(conditions, "tags", criteria.tags)

    # Employee count filters
    if criteria.employee_count:
        conditions.append(f"employee_count = {criteria.employee_count}")
    if criteria.employee_count_min:
        conditions.append(f"employee_count >= {criteria.employee_count_min}")
    if criteria.employee_count_max:
        conditions.append(f"employee_count <= {criteria.employee_count_max}")

    # Funding filters
    if criteria.total_funding_raised_min:
        conditions.append(f"total_funding_raised >= {criteria.total_funding_raised_min}")
    if criteria.total_funding_raised_max:
        conditions.append(f"total_funding_raised <= {criteria.total_funding_raised_max}")

    # Industry classification codes
    if criteria.naics_code:
        _add_in_condition(conditions, "naics.naics_code", criteria.naics_code)
    if criteria.sic_code:
        _add_in_condition(conditions, "sic.sic_code", criteria.sic_code)

    # Build final query
    if conditions:
        where_clause = " AND ".join(conditions)
        return f"SELECT * FROM company WHERE {where_clause}"
    else:
        return "SELECT * FROM company"


def _add_in_condition(
    conditions: list[str],
    field: str,
    values: list[str],
    uppercase: bool = False,
) -> None:
    """Add an IN condition for a list of values."""
    if uppercase:
        escaped_values = [v.upper().replace("'", "''") for v in values]
    else:
        escaped_values = [v.lower().replace("'", "''") for v in values]

    if len(escaped_values) == 1:
        conditions.append(f"{field} = '{escaped_values[0]}'")
    else:
        formatted = ", ".join(f"'{v}'" for v in escaped_values)
        conditions.append(f"{field} IN ({formatted})")


def _add_not_in_condition(
    conditions: list[str],
    field: str,
    values: list[str],
) -> None:
    """Add a NOT IN condition for a list of values (exclusion filter)."""
    escaped_values = [v.lower().replace("'", "''") for v in values]

    if len(escaped_values) == 1:
        conditions.append(f"{field} != '{escaped_values[0]}'")
    else:
        formatted = ", ".join(f"'{v}'" for v in escaped_values)
        conditions.append(f"{field} NOT IN ({formatted})")


def _add_like_condition(
    conditions: list[str],
    field: str,
    values: list[str],
) -> None:
    """Add LIKE conditions with wildcards for partial matching."""
    escaped_values = [v.lower().replace("'", "''") for v in values]

    if len(escaped_values) == 1:
        conditions.append(f"{field} LIKE '%{escaped_values[0]}%'")
    else:
        like_conditions = [f"{field} LIKE '%{v}%'" for v in escaped_values]
        conditions.append(f"({' OR '.join(like_conditions)})")


def _add_not_like_condition(
    conditions: list[str],
    field: str,
    values: list[str],
) -> None:
    """Add NOT LIKE conditions with wildcards for exclusion."""
    escaped_values = [v.lower().replace("'", "''") for v in values]

    for v in escaped_values:
        conditions.append(f"{field} NOT LIKE '%{v}%'")
