

# Company Schema

<HTMLBlock>
  {`
  <head>
  <style>

  h4 {
    text-transform: uppercase;
  }
  </style>
  </head>
  `}
</HTMLBlock>

# Overview

This page details the company-related fields that we provide through the [Company Enrichment](https://docs.peopledatalabs.com/docs/company-enrichment-api) and [Company Search](https://docs.peopledatalabs.com/docs/company-search-api) APIs.

* [Base Company Fields](#base-company-fields): Common fields available to all customers by default
* [Company Insights Fields](#company-insights-fields): Premium fields presenting summaries of the employee headcount and trends, built by aggregating data from our Person dataset
* [Premium Company Fields](#premium-company-fields): Premium company fields such as related companies, subsidiaries, acquisitions and more

> 📘 Field Availability
>
> Please note: Not all fields are available in all bundles.

* For more information about data formatting, see [Data Types](https://docs.peopledatalabs.com/docs/data-types).
* For a full example record, see [Example Company Record](https://docs.peopledatalabs.com/docs/example-company-record).
* For a simplified overview of our company fields, check out the [Company Data Overview](https://docs.peopledatalabs.com/docs/company-data-overview).
* For more details about our company fields, including fill rates and which fields are included in the base vs premium [field bundles](https://docs.peopledatalabs.com/docs/data-field-bundles), check out our [Company Stats](https://docs.peopledatalabs.com/docs/company-stats) pages.
* For a full data ingestion JSON schema, check out [this page](https://docs.peopledatalabs.com/docs/receiving-and-updating-data#data-ingestion-schemas).
* If you'd like access to premium fields or have questions about which fields are included in your specific field bundle(s), please [speak to one of our data consultants](https://peopledatalabs.com/talk-to-sales).

***

# Base Company Fields

These fields are available to all customers by default.

## Identifiers

### `id`

<table>
  <tr>
    <th>Description</th>
    <td>The identifier for the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The ID is a unique, hashed value that represents a specific company record.

#### Example

```json
  "id": "tnHcNHbCv8MKeLh92946LAkX6PKg"
```

### `name`

<table>
  <tr>
    <th>Description</th>
    <td>The company's main common name.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The company name will be lowercase with any leading/trailing whitespace removed. It is **not** guaranteed to be unique.

For the correct capitalization of the company name, see [`display_name`](#display_name).

The name value returned here does not undergo much cleaning or standardization. However, we clean and tokenize company names behind the scenes so they can be found using the [Company Search API](https://docs.peopledatalabs.com/docs/company-search-api). To see how company name cleaning works, check out the [Company Cleaner API](https://docs.peopledatalabs.com/docs/cleaner-apis#companyclean).

#### Example

```json
  "name": "people data labs"
```

### `display_name`

<table>
  <tr>
    <th>Description</th>
    <td>The company name, capitalized using the company’s self-reported name.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The `display_name` field preserves the capitalization of the company name (unlike [`name`](#name) which is always lowercase). `display_name` is set using the company’s self-reported name, so it should be accurate even for companies with non-standard capitalization (such as VMware, FedEx, or Dell EMC).

Use this field to display properly capitalized company names in a UI or other customer-facing project or product.

#### Example

```json
  "display_name": "VMware"
```

## Company Information

### `affiliated_profiles`

<table>
  <tr>
    <th>Description</th>
    <td><a href="#id">Company IDs</a> that are affiliated with the queried company (parents and subsidiaries.)</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

A list of [Company IDs](#id) that we have flagged as having an association to this company (either a parent or a subsidiary.) See [Parents and Subsidiaries](#parents-and-subsidiaries) for fields based on specific company associations.

#### Example

```json
  "affiliated_profiles": [
    "a1cpOkL4SHp0wSAKjbCeuwtAlno0",
    "3WBa1kollMtBbib5DoiCwwhyD9ks"
  ]
```

### `alternative_domains`

<table>
  <tr>
    <th>Description</th>
    <td>A list of alternate domains associated with this company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

If a company rebrands or otherwise changes its primary domain, old company websites will be kept in this list.

See [`website`](#website) for how we handle domains.

#### Example

```json
  "alternative_domains": [
    "peopledatalabs.com",
    "talentiq.co",
    "peopledatalabs.co"
  ]
```

### `alternative_names`

<table>
  <tr>
    <th>Description</th>
    <td>A list of names associated with this company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

A list of [names](#name) associated with the company filtered to ensure data quality.

#### Example

```json
  "alternative_names": [
    "people data labs",
    "people data labs inc",
    "talentiq"
  ]
```

### `employee_count`

<table>
  <tr>
    <th>Description</th>
    <td>The current number of employees working at the company based on our number of profiles.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (>= 0)</code></td>
  </tr>
</table>

#### Field Details

`employee_count` is an integer greater than or equal to zero. We calculate it by finding the number of profiles whose `experience.company.id ` matches the company with a non-null `job_start_date` and no end date.

For the company's self-reported size range, use the [`size`](#size) field instead. For more information about the different types of employee count data we provide, see [Employee Count Fields](https://docs.peopledatalabs.com/docs/employee-count-fields).

This number may be higher or lower than a company's real employee count depending on how many false positives and false negatives we have in our data as well as missing or duplicate individuals.

#### Example

```json
  "employee_count": 78
```

### `employee_count_by_country`

<table>
  <tr>
    <th>Description</th>
    <td>The number of current employees broken out by country.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

Each country will be one of our [Canonical Countries](https://docs.peopledatalabs.com/docs/location-countries). For more information about how each count is calculated, see [Employee Count Breakdowns](https://docs.peopledatalabs.com/docs/company-schema#employee-count-breakdowns).

Beginning in v25.0, this field will also contain an `other_uncategorized` subfield. Profiles that we have associated with the company but do not have enough information to assign a location to will be included in this field. For more information, see [Employee Count Fields](https://docs.peopledatalabs.com/docs/employee-count-fields).

#### Example

```json
  "employee_count_by_country": {
    "united states": 67,
    "canada": 2,
    "india": 1,
    "bangladesh": 1,
    "other_uncategorized": 2
  }
```

### `founded`

<table>
  <tr>
    <th>Description</th>
    <td>The founding year of the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (> 0)</code></td>
  </tr>
</table>

#### Field Details

The founding year will be an integer greater than zero. If no year is found, it will be `null`.

If different sources list different founding years, we will choose the year that appears in the most sources. If multiple years appear in the same number of sources, we will use the latest year.

#### Example

```json
  "founded": 2015
```

### `headline`

<table>
  <tr>
    <th>Description</th>
    <td>The company’s headline summary.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

`headline` is a short description of the company, limited to 300 characters.

#### Example

```json
  "headline": "Your Single Source of Truth"
```

### `size`

<table>
  <tr>
    <th>Description</th>
    <td>A range representing the number of people working at the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

The value of this field will be one of our canonical [Company Sizes](https://docs.peopledatalabs.com/docs/company-sizes). We derive it from the company's self-reported size on their social media profile.

For the true number of employees, use the [`employee_count`](#employee_count) field.

#### Example

```json
  "size": "11-50"
```

### `summary`

<table>
  <tr>
    <th>Description</th>
    <td>A description of the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The company summary is a lowercase string and can contain escape characters such as `\n`. The string is limited to a maximum of 1000 characters.

#### Example

```
  "summary": "people data labs builds people data. \n\nuse our dataset
              of 1.5 billion unique person profiles to build products,
              enrich person profiles, power predictive modeling/ai,
              analysis, and more. we work with technical teams as their
              engineering focused people data partner. \n\nwe work with
              thousands of data science teams as their engineering focused
              people data partner. these include enterprises like adidas,
              ebay, and acxiom, as well as startups like madison logic,
              zoho, and workable. we are a deeply technical company, and
              are backed by two leading engineering venture capital firms
              - founders fund and 8vc.",
```

### `tags`

<table>
  <tr>
    <th>Description</th>
    <td>Tags associated with the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

Each tag is a lowercase string.

There may be tags that seem to overlap (for example: `"data"`, `"analytics"` and `"data and analytics"`). This is intentional so that it is easier to search for companies matching a tag.

#### Example

```json
  "tags": [
    "data",
    "people data",
    "data science",
    "artificial intelligence",
    "data and analytics",
    "machine learning",
    "analytics",
    "database",
    "software",
    "developer apis"
   ]
```

### `website`

<table>
  <tr>
    <th>Description</th>
    <td>The primary company website.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

This field contains the address of the primary company website associated with the record.

We standardize websites by removing `https://www.` and any additional subdomains and paths (with certain exceptions). Popular hosting platforms (like Facebook, Blogspot, Wix, etc.) will retain their subdomains and paths. For example, `samspizza.blogspot.com` or `etsy.com/sams-pizza`.

Websites using link shortening services (like Bit.ly, TinyURL, ShortURL, etc.) will appear in full.

We have a list of invalid URL items (domains, subdomains and TLDs) that we check against. We also check if an iteration of the company name appears in the website address as a simple validation.

Ideally, this is the website address that people commonly use when accessing a company's site (such as `facebook.com`) and not an alias (such as `fb.com`).

As with [Social Presence](#social-presence), we do **not** verify that the website is valid.

#### Example

```json
  "website": "peopledatalabs.com"
```

## Funding Data

### `funding_stages`

<table>
  <tr>
    <th>Description</th>
    <td>All disclosed funding stages for the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Enum (String)]</code></td>
  </tr>
</table>

#### Field Details

An unordered list of all funding stages for funding events announced by the company.

This is generated from the separate events in  [`funding_details.funding_type`](#funding_details).

All values in the list must be [Canonical Funding Rounds](https://docs.peopledatalabs.com/docs/funding-rounds). If there are multiple events tied to the same round (ex: Series A), that label will only appear once in the list.

#### Example

```json
  "funding_stages": [
    "series_b",
    "series_a",
    "seed"
  ]
```

### `last_funding_date`

<table>
  <tr>
    <th>Description</th>
    <td>The date of the company’s most recent funding event.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#dates"><code>String (Date)</code></a></td>
  </tr>
</table>

#### Field Details

The date of the company’s most recent funding event. This represents the publicly disclosed date of the closing of the financing, and will be independent of any prior dates associated with that same funding round.

#### Example

```json
  "last_funding_date": "2021-11-16"
```

### `latest_funding_stage`

<table>
  <tr>
    <th>Description</th>
    <td>The stage of the company’s most recent funding event.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

Must be one of the [Canonical Funding Rounds](https://docs.peopledatalabs.com/docs/funding-rounds).

#### Example

```json
  "latest_funding_stage": "series_b"
```

### `number_funding_rounds`

<table>
  <tr>
    <th>Description</th>
    <td>The number of funding rounds announced by the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (> 0)</code></td>
  </tr>
</table>

#### Field Details

The number of separate funding events for the company. This is the total number of events in  [`funding_details`](#funding_details).

If multiple events are tied to the same funding round, they will each be counted toward the total (ex: 3 Series A events will add 3 to the total count).

#### Example

```json
  "number_funding_rounds": 7
```

### `total_funding_raised`

<table>
  <tr>
    <th>Description</th>
    <td>The cumulative amount raised by the company in USD.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Float  (> 0)</code></td>
  </tr>
</table>

#### Field Details

The cumulative amount raised by the company during all publicly disclosed funding rounds.

The value for this field is represented in USD. It is the sum of all known values from individual funding rounds (each of which is represented in $ USD using “then-current” currency exchange rates).

#### Example

```json
  "total_funding_raised": 55250000.0
```

## Industry Types

### `industry`

<table>
  <tr>
    <th>Description</th>
    <td>The self-reported industry of the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

Industry is self-reported and will be one of our [Canonical Industries](https://docs.peopledatalabs.com/docs/industries). If no industry is found, the field will be `null`.

#### Example

```json
  "industry": "animation"
```

<br />

### `industry_v2`

<table>
  <tr>
    <th>Description</th>

    <td>
      Industry v2 is the self-reported industry from an expanded list of <a href="https://docs.peopledatalabs.com/docs/industries-v2">Canonical v2 Industries</a>. If no industry is found, the field will be <code>null</code>
    </td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/industries-v2"><code>Enum (String)</code></a></td>
  </tr>
</table>

#### Field Details

Industry is self-reported and will be one of our [Canonical V2 Industries](https://docs.peopledatalabs.com/docs/industries-v2). If no industry is found, the field will be `null`.

#### Example

```json
  "industry": "textile manufacturing"
```

### `naics`

<table>
  <tr>
    <th>Description</th>
    <td>An array of objects containing the industry classifications for a company according to the North American Industry Classification System (NAICS). A company can (and frequently does) have multiple NAICS codes.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

Each NAICS code associated with the company will be included in the list. For each NAICS code, we provide the actual six-digit code as well as the official description for each level of the NAICS code.

PDL uses [NAICS 2017 industry categorization](https://www.bls.gov/cew/classifications/industry/home.htm).

PDL offers self-reported NAICS industry categorizations within the company data, where this data serves as an alternative to Industry and SIC for users to categorize or segment companies. Because the data PDL publishes represents self-reported data where the industry values were selected by employees of those companies prior to the 2022 revision, we have not bulk converted to, or inferred, NAICS 2022 categories for our existing NAICS values.

A NAICS code doesn’t have to use all six digits. Any unspecified field(s) in our data will have a `null` value.

| Field               | Data Type | Description                                                                                                                                                           |
| ------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `naics_code`        | `String`  | The NAICS code associated with a company’s industry classification. [See canonical values](https://docs.peopledatalabs.com/docs/naics-codes).                         |
| `sector`            | `String`  | The industry classification according to the first two digits in the NAICS code. [See canonical values](https://docs.peopledatalabs.com/docs/naics-sectors).          |
| `sub_sector`        | `String`  | The industry classification according to the first three digits in the NAICS code. [See canonical values](https://docs.peopledatalabs.com/docs/naics-subsectors).     |
| `industry_group`    | `String`  | The industry classification according to the first four digits in the NAICS code. [See canonical values](https://docs.peopledatalabs.com/docs/naics-industry-groups). |
| `naics_industry`    | `String`  | The industry classification according to the first five digits in the NAICS code. [See canonical values](https://docs.peopledatalabs.com/docs/naics-industries).      |
| `national_industry` | `String`  | The industry classification according to all six digits in the NAICS code. [See canonical values.](https://docs.peopledatalabs.com/docs/naics-national-industries)    |

#### Example

```json
  "naics": [
    {
      "naics_code": "423920",
      "sector": "wholesale trade",
      "sub_sector": "merchant wholesalers, durable goods",
      "industry_group": "miscellaneous durable goods merchant wholesalers",
      "naics_industry": "toy and hobby goods and supplies merchant wholesalers",
      "national_industry": "toy and hobby goods and supplies merchant wholesalers"
    },
    ...
  ]
```

### `sic`

<table>
  <tr>
    <th>Description</th>
    <td>An array of objects containing the industry classifications for a company according to the Standard Industrial Classification (SIC) system. A company can (and frequently does) have multiple SIC codes.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

Each SIC code associated with the company will be included in the list. For each SIC code, we provide the actual four-digit code as well as the official description for each level of the SIC code.

A SIC code doesn’t have to use all four digits. Any unspecified field(s) in our data will have a `null` value.

| Field             | Data Type | Description                                                                      |
| ----------------- | --------- | -------------------------------------------------------------------------------- |
| `sic_code`        | `String`  | The SIC code associated with a company’s industry classification.                |
| `major_group`     | `String`  | The industry classification according to the first two digits in the SIC code.   |
| `industry_group`  | `String`  | The industry classification according to the first three digits in the SIC code. |
| `industry_sector` | `String`  | The industry classification according to all four digits in the SIC code.        |

#### Example

```json
  "sic": [
    {
      "sic_code": "7372",
      "major_group": "business services",
      "industry_group": "computer programming, data processing, and other computer related services",
      "industry_sector": "prepackaged software"
    },
    ...
   ]
```

## Primary Location

### `location`

<table>
  <tr>
    <th>Description</th>
    <td>An object containing increasingly granular information about the location of the company’s current headquarters.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

A company's location is the location of its Headquarters (HQ). We determine a company’s current Headquarters/primary office based on the location that we see most often in our sources.

For more information on our standard location fields, see [Data Formatting: Locations](https://docs.peopledatalabs.com/docs/data-formatting#locations).

#### Example

```json
  "location": {
    "name": "san francisco, california, united states",
    "locality": "san francisco",
    "region": "california",
    "metro": "san francisco, california",
    "country": "united states",
    "continent": "north america",
    "street_address": "455 market street",
    "address_line_2": "suite 1670",
    "postal_code": "94105",
    "geo": "37.77,-122.41"
  }
```

## Stock Information

### `mic_exchange`

<table>
  <tr>
    <th>Description</th>
    <td>The MIC code for the stock exchange that the company's <a href="#ticker">ticker</a> is listed on.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

`mic_exchange` represents the Market Identified Code (MIC) standard exchange code corresponding to the stock exchange of the company.

The value of `mic_exchange` will always be one of our [Canonical MIC Codes](https://docs.peopledatalabs.com/docs/mic-codes) or `null` if there is no [ticker](#ticker).

#### Example

```json
  "mic_exchange": "xnams"
```

### `ticker`

<table>
  <tr>
    <th>Description</th>
    <td>The company ticker (only for public companies.)</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String (Uppercase)</code></td>
  </tr>
</table>

#### Field Details

`ticker` is the uppercase string of the company’s stock symbol.

If a company is not public (as listed in its [`type`](#type)), its ticker will be `null`.

#### Example

```json
  "ticker": "MOO"
```

### `type`

<table>
  <tr>
    <th>Description</th>
    <td>The company type.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

`type` will be one of the Canonical [Company Types](https://docs.peopledatalabs.com/docs/company-types). If a company has a known [`ticker`](#ticker), then its `type` is public. If a company does not have a ticker and its ultimate parent company does, then its type is public\_subsidiary.

#### Example

```json
  "type": "private"
```

## Social Presence

We currently include company social profiles for LinkedIn, Yellow Pages, Xing, Twitter, Facebook and Crunchbase. Any profiles that we find for the company from these sources will be added to the [`profiles`](#profiles) list.

Each social profile URL has one or more standard formats that we parse and turn into a standard PDL format for that social URL. We invalidate profiles that have non-valid company stubs (for example, `linkedin.com/in`), and we also have a blacklist of usernames that we know are invalid.

We do **not** validate if a URL is valid (that is, whether you can access it) because doing this at scale is considered a Direct Denial of Service (DDoS) attack and/or a form of crawling. This is highly discouraged! We try to mitigate invalid URLs as much as possible by using Entity Resolution (Merging) to link URLs together and then tagging the primary URL at the top level for key networks.

### `linkedin_id`

<table>
  <tr>
    <th>Description</th>
    <td>The main LinkedIn profile ID for the company based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "linkedin_id": "18170482"
```

### `linkedin_slug`

<table>
  <tr>
    <th>Description</th>
    <td>The company’s LinkedIn URL slug.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

To support our [upcoming change to PDL Company IDs](https://docs.peopledatalabs.com/changelog/january-2024-release-notes-v25#company-id), we are adding the new `linkedin_slug` field. This field is generated in the same way as our [current company `id` field](https://docs.peopledatalabs.com/docs/company-schema#id).

For new company records that do not have associated LinkedIn pages, this field will be null.

#### Example

```json
  "linkedin_slug": "peopledatalabs"
```

### `linkedin_url`

<table>
  <tr>
    <th>Description</th>
    <td>The main LinkedIn profile URL for the company based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "linkedin_url": "linkedin.com/company/peopledatalabs"
```

### `facebook_url`

<table>
  <tr>
    <th>Description</th>
    <td>The main Facebook profile URL for the company based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "facebook_url": "facebook.com/peopledatalabs"
```

### `twitter_url`

<table>
  <tr>
    <th>Description</th>
    <td>The main Twitter profile URL for the company based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "twitter_url": "twitter.com/peopledatalabs"
```

### `profiles`

<table>
  <tr>
    <th>Description</th>
    <td>A list of all known social profile URLs for the company from <a href="#social-presence">our known sources</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Example

```json
  "profiles": [
    "linkedin.com/company/peopledatalabs",
    "linkedin.com/company/18170482",
    "facebook.com/peopledatalabs",
    "twitter.com/peopledatalabs",
    "crunchbase.com/organization/talentiq"
  ]
```

## PDL Record Information & Metadata

### `dataset_version`

<table>
  <tr>
    <th>Description</th>
    <td>The major or minor release number.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

Note: This number corresponds to the [data release number](https://docs.peopledatalabs.com/changelog), not the API release number.

#### Example

```json
  "dataset_version": "19.2"
```

***

# Company Insights Fields

Premium fields presenting summaries of the employee headcount and trends, built by aggregating data from from our [Person Dataset](https://docs.peopledatalabs.com/docs/fields).

## Average Employee Tenure

Average employee tenure is the average number of years employees work for the company. It is represented by a floating number greater than zero and rounded to the nearest thousandth. It could skew lower if there have been a lot of recent hires.

The average is calculated using `experience.start_date` and `experience.end_date` for each employee found in our Person records.

If no start date is given or if a date only contains a year but no month, then the experience is not counted toward the average.

### `average_employee_tenure`

<table>
  <tr>
    <th>Description</th>
    <td>The average years of experience at the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Float (> 0)</code></td>
  </tr>
</table>

#### Field Details

This insight shows the average number of years that employees at the company have worked based on `experience.start_date` and `experience.end_date`.

#### Example

```json
  "average_employee_tenure": 2.75
```

### `average_tenure_by_level`

<table>
  <tr>
    <th>Description</th>
    <td>The average years of experience at the company by job level.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This insight shows the average number of years that employees at the company have worked broken out by their level at the company. The average for each level is calculated using the same logic as [`average_employee_tenure`](#average_employee_tenure).

The level names come from `experience.title.levels`, meaning they will always be one of the [Canonical Job Levels](https://docs.peopledatalabs.com/docs/job-title-levels).

#### Example

```json
  "average_tenure_by_level": {
    "entry": 0.3,
    "unpaid": 2.0,
    "senior": 6.0,
    "director": 3.0,
    "vp": 2.4,
    "training": 0.2,
    "manager": 4.0,
    "owner": 3.2,
    "partner": 2.4,
    "cxo": 8.1
  }
```

### `average_tenure_by_role`

<table>
  <tr>
    <th>Description</th>
    <td>The average years of experience at the company by job role.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This insight shows the average number of years that employees at the company have worked broken out by their role at the company. The average for each role is calculated using the same logic as [`average_employee_tenure`](#average_employee_tenure).

The role names come from `experience.title.role`, meaning they will always be one of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).

#### Example

```json
  "average_tenure_by_role": {
    "real_estate": 4.5,
    "design": 2.0,
    "trades": 3.2,
    "marketing": 0.1,
    "education": 6.5,
    "legal": 8.0,
    "customer_service": 4.0,
    "finance": 5.0,
    "public_relations": 8.1,
    "engineering": 2.1,
    "human_resources": 0.5,
    "media": 0.4,
    "sales": 0.6,
    "operations": 0.1,
    "health": 2.0
  }
```

## Employee Count Breakdowns

The count for each category will always be an integer value greater than or equal to zero.

This number may be higher or lower than a company's real employee count depending on how many false positives and false negatives we have in our data, missing and duplicate individuals, and missing information on start dates and job roles.

If no start date is given, then the experience is not counted.

For the overall employee count, see [`employee_count`](#employee_count). For the company's self-reported size, see [`size`](#size).

Note that discrepancies between the [`employee_count`](#employee_count), the most recent [`employee_count_by_month`](#employee_count_by_month), and aggregated[`employee_count_by_month_by_role`](#employee_count_by_month_by_role) and [`employee_count_by_month_by_level`](#employee_count_by_month_by_level) counts are expected. For more information about the logic used to calculate these values, see [this page](https://docs.peopledatalabs.com/docs/employee-count-fields).

### `employee_count_by_month`

<table>
  <tr>
    <th>Description</th>
    <td>The number of employees at the end of each month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The total number of profiles associated with this company at the end of each month in the format `YYYY-MM`. The date range begins at the start date of the first associated employee or January 1, 2010, whichever is most recent. The final month in the range will be the last full month before the last monthly [Data Build](https://docs.peopledatalabs.com/docs/data-build). Most often this is the month before request was submitted. For example, if you make a request mid-March, the response will contain all data up to that February.

#### Example

```json
  "employee_count_by_month": {
    "2021-07": 84,
    "2021-08": 86,
    "2021-09": 84
  }
```

### `employee_count_by_month_by_level`

<table>
  <tr>
    <th>Description</th>
    <td>The number of employees at the end of each month, broken down by job level.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The total number of profiles associated with this company at the end of each month in the format `YYYY-MM` broken down by `experience.title.levels`. The level names will always be one of the [Canonical Job Levels](https://docs.peopledatalabs.com/docs/job-title-levels).

The date range begins at the start date of the first associated employee or January 1, 2010, whichever is most recent. The final month in the range will be the last full month before the last monthly [Data Build](https://docs.peopledatalabs.com/docs/data-build). Most often this is the month before request was submitted. For example, if you make a request mid-March, the response will contain all data up to that February.

If a person changes levels within a company during the same month, they will be counted in the same month towards both levels. An individual may have more than a single level for the same experience object, in which case they will contribute towards multiple levels.

#### Example

```json
  "employee_count_by_month_by_level": {
    "2015-03": {
      "partner": 0,
      "vp": 0,
      "owner": 1,
      "entry": 0,
      "director": 0,
      "unpaid": 0,
      "senior": 0,
      "cxo": 1,
      "manager": 0,
      "training": 0
    },
    ...
    "2021-06": {
      "partner": 0,
      "vp": 3,
      "owner": 1,
      "entry": 10,
      "director": 2,
      "unpaid": 2,
      "senior": 5,
      "cxo": 1,
      "manager": 3,
      "training": 0
    }
  }
```

### `employee_count_by_month_by_role`

<table>
  <tr>
    <th>Description</th>
    <td>The number of employees at the end of each month, broken down by job role.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The total number of profiles associated with this company at the end of each month in the format `YYYY-MM` broken down by `experience.title.role`. The role names will always be one of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).

The date range begins at the start date of the first associated employee or January 1, 2010, whichever is most recent. The final month in the range will be the last full month before the last monthly [Data Build](https://docs.peopledatalabs.com/docs/data-build). Most often this is the month before request was submitted. For example, if you make a request mid-March, the response will contain all data up to that February.

If a person changes roles with a company during the same month, they will only be counted for a single role.

Beginning in v25.0, each month will also contain an `other_uncategorized` subfield. Profiles that we have associated with the company but do not have enough information to assign a role to will be included in this field. For more information, see [Employee Count Fields](https://docs.peopledatalabs.com/docs/employee-count-fields).

#### Example

```json
  "employee_count_by_month_by_role": {
    "2015-03": {
      "engineering": 0,
      "education": 0,
      "media": 0,
      "design": 0,
      "trades": 0,
      "health": 0,
      "real_estate": 0,
      "customer_service": 0,
      "legal": 0,
      "human_resources": 0,
      "finance": 0,
      "public_relations": 0,
      "marketing": 0,
      "sales": 0,
      "operations": 0,
      "other_uncategorized": 1
    },
    ...
    "2021-06": {
      "engineering": 1,
      "education": 0,
      "media": 0,
      "design": 0,
      "trades": 0,
      "health": 0,
      "real_estate": 0,
      "customer_service": 0,
      "legal": 0,
      "human_resources": 0,
      "finance": 0,
      "public_relations": 0,
      "marketing": 0,
      "sales": 0,
      "operations": 0,
      "other_uncategorized": 8
    }
  }
```

### `employee_count_by_class`

<table>
  <tr>
    <th>Description</th>
    <td>The number of current employees broken down by <a href="https://docs.peopledatalabs.com/docs/job-title-class">Job Title Class</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The total number of profiles associated with this company at the end of the most recent month, broken down by `experience.title.class`. The role names will always be one of the [Canonical Job Title Class](https://docs.peopledatalabs.com/docs/job-title-class) labels. This field will also contain an `other_uncategorized` subfield that contains profiles we have associated with the company but do not have enough information to assign a role to.

#### Example

```json
 "employee_count_by_class": {
    "other_uncategorized": 16,
    "general_and_administrative": 12,
    "research_and_development": 29,
    "sales_and_marketing": 22,
    "services": 14,
  }

```

### `employee_count_by_role`

<table>
  <tr>
    <th>Description</th>
    <td>The number of employees (<code>INT</code>) by Job Role on the final day of the most recent month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The total number of profiles associated with this company at the end of the most recent month, broken down by `experience.title.role`. The role names will always be one of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles). This field will also contain an `other_uncategorized` subfield that contains profiles we have associated with the company but do not have enough information to assign a role to.

This field is equivalent to the final month in the [`employee_count_by_month_by_role`](https://docs.peopledatalabs.com/docs/company-schema#employee_count_by_month_by_role) field.

#### Example

```json
  "employee_count_by_role": {
    "real_estate": 0,
    "design": 2,
    "trades": 0,
    "marketing": 4,
    "education": 4,
    "legal": 0,
    "customer_service": 10,
    "finance": 6,
    "public_relations": 1,
    "engineering": 24,
    "human_resources": 3,
    "media": 1,
    "sales": 12,
    "operations": 10,
    "health": 0,
    "other_uncategorized": 10
  }
```

### `employee_count_by_sub_role`

<table>
  <tr>
    <th>Description</th>
    <td>The number of current employees broken down by <a href="https://docs.peopledatalabs.com/docs/job-title-subroles">Job Title Sub Role</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The total number of profiles associated with this company at the end of the most recent month, broken down by `experience.title.sub_role`. The role names will always be one of the [Canonical Job Title Subroles](https://docs.peopledatalabs.com/docs/job-title-subroles). This field will also contain an `other_uncategorized` subfield that contains profiles we have associated with the company but do not have enough information to assign a role to.

#### Example

```json
{
  "employee_count_by_sub_role": {
    "other_uncategorized": 19,
    "health_and_safety": 0,
    "graphic_design": 1,
    "veterinarian": 0,
    "data_science": 2,
    "restaurants": 0,
    "marketing_services": 2,
    "planning_and_analysis": 1,
...
    "mechanical": 0
  }
}

```

## Employee Growth and Churn Rates

All calculation time frames are based on the month that you make the request. If you make the request in April, the three-month rate will use data from January onward.

If no start date is given, then the experience is not counted.

Additionally, if a date only contains a year but no month, it is assumed to be to be January for start dates and December (or the current month if December is in the future) for end dates.

### `employee_churn_rate`

<table>
  <tr>
    <th>Description</th>
    <td>The rate of change in employee headcount from N months prior.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This is a representation of net employee turnover. The churn rate is rounded to four decimal points and is always greater than or equal to 0. If the company had 0 employees or did not exist at the start time for a specific window, then the churn rate is `null`.

Churn rate is calculated as `max(employee_count_n_months_ago - employee_count_current, 0)/employee_count_n_months_ago`. For example, if a company has 200 employees at the beginning of the month, and at the end of the month 100 leave and 100 remain then its churn rate = 100 / 200 = 0.5.

| Field      | Data Type      |
| ---------- | -------------- |
| `3_month`  | `Float (>= 0)` |
| `6_month`  | `Float (>= 0)` |
| `12_month` | `Float (>= 0)` |
| `24_month` | `Float (>= 0)` |

#### Example

```json
  "employee_churn_rate": {
    "3_month": 0.015,
    "6_month": 0.02,
    "12_month": 0.035,
    "24_month": 0.155
  }
```

### `employee_growth_rate`

<table>
  <tr>
    <th>Description</th>
    <td>The percentage increase in total headcount from N months prior.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The growth rate is rounded to four decimal points and can be negative if the current number of employees is less than in the past. If the company had zero employees or did not exist at the start time for a specific window, then the growth rate is `null`.

Growth rate is calculated as `(current_employee_count / previous_employee_count) - 1`. For example, if a company has 100 employees at the beginning of the month, and at the end of the month has grown to 200 employees then its growth rate = (200 / 100) - 1 = 1.0.

| Field      | Data Type |
| ---------- | --------- |
| `3_month`  | `Float`   |
| `6_month`  | `Float`   |
| `12_month` | `Float`   |
| `24_month` | `Float`   |

#### Example

```json
  "employee_growth_rate": {
    "3_month": 0.0595,
    "6_month": 0.0723,
    "12_month": 0.8542,
    "24_month": 1.4722
  }
```

### `employee_growth_rate_12_month_by_class`

<table>
  <tr>
    <th>Description</th>
    <td>The twelve month rate of change by <a href="https://docs.peopledatalabs.com/docs/job-title-class">Job Title Class</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The 12 month growth rate of the total number of profiles associated with this company at the end of the most recent month in the format `YYYY-MM` broken down by `experience.title.class`. The role names will always be one of the [Canonical Job Title Class](https://docs.peopledatalabs.com/docs/job-title-class) labels. This field will also contain an `other_uncategorized` subfield that contains profiles we have associated with the company but do not have enough information to assign a role to.

The growth rate is rounded to four decimal points and can be negative if the current number of employees is less than in the past. If the company had zero employees or did not exist at the start time for a specific window, then the growth rate is `null`.

Growth rate is calculated as `(current_employee_count / previous_employee_count) - 1`. For example, if a company has 100 employees at the beginning of the month 12 months ago, and at the end of the most recent month has grown to 200 employees then its growth rate = (200 / 100) - 1 = 1.0.

The 12 month growth rate will be computed using the last full month before the last monthly Data Build. Most often this is the month before request was submitted. For example, if you make a request mid-March, the response will contain the 12 month growth rate from February."

#### Example

```json
 "employee_growth_rate_12_month_by_class": {
    "other_uncategorized": 0.2,
    "general_and_administrative": -0.167,
    "research_and_development": 0.1,
    "sales_and_marketing": -0.333,
    "services": 0.0,
  }

```

### `employee_growth_rate_12_month_by_role`

<table>
  <tr>
    <th>Description</th>
    <td>The twelve month rate of change (<code>FLOAT</code>) by Job Role on the final day of the most recent month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The 12 month growth rate of the total number of profiles associated with this company at the end of the most recent month in the format `YYYY-MM` broken down by `experience.title.role`. The role names will always be one of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles). This field will also contain an `other_uncategorized` subfield that contains profiles we have associated with the company but do not have enough information to assign a role to.

The growth rate is rounded to four decimal points and can be negative if the current number of employees is less than in the past. If the company had zero employees or did not exist at the start time for a specific window, then the growth rate is `null`.

Growth rate is calculated as `(current_employee_count / previous_employee_count) - 1`. For example, if a company has 100 employees at the beginning of the month 12 months ago, and at the end of the most recent month has grown to 200 employees then its growth rate = (200 / 100) - 1 = 1.0.

The 12 month growth rate will be computed using the last full month before the last monthly Data Build. Most often this is the month before request was submitted. For example, if you make a request mid-March, the response will contain the 12 month growth rate from February.

#### Example

```json
 "employee_count_12_month_growth_by_role": {
    "real_estate": null,
    "design": -0.2500,
    "trades": null,
    "marketing": -0.5000,
    "education": 0.0000,
    "legal": null,
    "customer_service": -0.4545,
    "finance": -0.2500,
    "public_relations": null,
    "engineering": -0.1220,
    "human_resources": -0.1667,
    "media": 0.0000,
    "sales": -0.1852,
    "operations": 0.000,
    "health": null,
    "other_uncategorized": 0.1471
  }
```

### `employee_growth_rate_12_month_by_sub_role`

<table>
  <tr>
    <th>Description</th>
    <td>The twelve month rate of change by <a href="https://docs.peopledatalabs.com/docs/job-title-subroles">Job Title Sub Role</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The 12 month growth rate of the total number of profiles associated with this company at the end of the most recent month in the format `YYYY-MM` broken down by `experience.title.sub_role`. The role names will always be one of the [Canonical Job Title Subroles](https://docs.peopledatalabs.com/docs/job-title-subroles). This field will also contain an `other_uncategorized` subfield that contains profiles we have associated with the company but do not have enough information to assign a role to.

The growth rate is rounded to four decimal points and can be negative if the current number of employees is less than in the past. If the company had zero employees or did not exist at the start time for a specific window, then the growth rate is `null`.

Growth rate is calculated as `(current_employee_count / previous_employee_count) - 1`. For example, if a company has 100 employees at the beginning of the month 12 months ago, and at the end of the most recent month has grown to 200 employees then its growth rate = (200 / 100) - 1 = 1.0.

The 12 month growth rate will be computed using the last full month before the last monthly Data Build. Most often this is the month before request was submitted. For example, if you make a request mid-March, the response will contain the 12 month growth rate from February.

#### Example

```json
 "employee_growth_rate_12_month_by_sub_role": {
    "other_uncategorized": -0.2667,
    "advisory": 0.0,
    "analyst": null,
    "creative": null,
    "education": 0.2,
    "engineering": -0.069,
    "finance": 0.0,
    "health": null,
    "hospitality": null,
    "product_design": -0.675,
    "recruiting": 0.0,
    "manufacturing": null,
    "marketing": 0.0,
    "solutions_engineer": -0.2667,
	...
    "retail": null
  }

```

## Gross Additions and Departures

This insight shows the total number of employees that joined or left the company each month.

The count for each month will always be an integer greater than or equal to zero. The month range begins at the start date of the first associated employee or January 1, 2010, whichever is most recent. The final month in the range will be the last full month before the last monthly [Data Build](https://docs.peopledatalabs.com/docs/data-build). Most often this is the month before request was submitted. For example, if you make a request mid-March, the response will contain all data up to that February.

This number may be higher or lower than a company's real employee count depending on how many false positives and false negatives we have in our data, missing and duplicate individuals, and missing information on start/end dates.

If a start or end date is not given or only contains a year but no month, it is not counted. This differs from [`employee_count_by_month`](#employee_count_by_month) that assumes January if there is no month.

### `gross_additions_by_month`

<table>
  <tr>
    <th>Description</th>
    <td>The total number of profiles that joined the company each month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The total number of profiles that joined the company each month in the format `YYYY-MM` based on `experience.start_date`.

#### Example

```json
  "gross_additions_by_month": {
    "2015-03": 1,
    "2015-04": 1,
    ...
    "2021-05": 2,
    "2021-06": 2
  }
```

### `gross_departures_by_month`

<table>
  <tr>
    <th>Description</th>
    <td>The total number of profiles that left the company each month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

The total number of profiles that left the company each month in the format `YYYY-MM` based on `experience.end_date`.

#### Example

```json
  "gross_departures_by_month": {
    "2015-03": 1,
    "2015-04": 1,
    ...
    "2021-05": 2,
    "2021-06": 2
  }
```

## Inferred Revenue

### `inferred_revenue`

<table>
  <tr>
    <th>Description</th>
    <td>Company's estimated annual revenue range in US dollars.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

A company's inferred revenue is an estimated range of its annual revenue in US dollars and can be used as a filter in [Company Search queries](https://docs.peopledatalabs.com/docs/company-search-api).

The revenue estimate is calculated using a predictive model that factors in details generated for our [Company Insights Fields](#company-insights-fields) (for example, [employee\_count\_by\_month\_by\_role](#employee_count_by_month_by_role)) as well as for other inputs that have been shown to be highly correlative.

The range will be one of our [Canonical Inferred Revenue Ranges](https://docs.peopledatalabs.com/docs/inferred-revenue-ranges).

#### Example

```json
  "inferred_revenue": "$10M-$25M"
```

## Recent Executive Changes

These insights provide details on executives that have joined or left the company in the past three months at the time you make the request.

There is no limit on the number of executives that can be in either list. To determine if someone is an executive, we check if their `experience.title.levels` in the company matches `CXO`, `owner` or `VP`. If no level is specified, then the experience is not counted.

If a start or end date is not given for an executive, then the experience is not counted. If the date only contains a year, the month is assumed to be January.

### `recent_exec_departures`

<table>
  <tr>
    <th>Description</th>
    <td>The profiles of all of CXOs, owners and VPs that have left the company in the last three months.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

For each executive that has left the company in the past three months, we provide the following information:

| Field                            | Data Type                | Description                                                                                                                                                            |
| -------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `departed_date`                  | `String (Date: YYYY-MM)` | The month the executive left the company.                                                                                                                              |
| `pdl_id`                         | `String`                 | The ID of the executive in our [Person Dataset](https://docs.peopledatalabs.com/docs/fields).                                                                          |
| `job_title`                      | `String`                 | The executive's previous job title at the company.                                                                                                                     |
| `job_title_role`                 | `Enum (String)`          | The executive's previous job role at the company. This will be one of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).                 |
| `job_title_sub_role`             | `Enum (String)`          | The executive's previous job subrole at the company. This will be one of the [Canonical Job Subroles](https://docs.peopledatalabs.com/docs/job-title-subroles).        |
| `job_title_class`                | `Enum (String)`          | The expense line item category this executive would fall into. This will be one of the [Canonical Job Classes](https://docs.peopledatalabs.com/docs/job-title-class) . |
| `job_title_levels`               | `Array [Enum (String)]`  | The executive's previous job levels at the company. This will be in the [Canonical Job Levels](https://docs.peopledatalabs.com/docs/job-title-levels).                 |
| `new_company_id`                 | `String`                 | The [ID](#id) of the new company the executive joined.                                                                                                                 |
| `new_company_job_title`          | `String`                 | The executive's current job title at the new company.                                                                                                                  |
| `new_company_job_title_role`     | `Enum (String)`          | The executive's current job role at the new company. This will be one of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).              |
| `new_company_job_title_sub_role` | `Enum (String)`          | The executive's current job subrole at the new company. This will be one of the [Canonical Job Classes](https://docs.peopledatalabs.com/docs/job-title-class)  .       |
| `new_company_job_title_class`    | `Enum (String)`          | The executive's current job class at the new company. This will be one of the [Canonical Job Subroles](https://docs.peopledatalabs.com/docs/job-title-subroles) .      |
| `new_company_job_title_levels`   | `Array [Enum (String)]`  | The executive's current job levels at the new company. This will be in the [Canonical Job Levels](https://docs.peopledatalabs.com/docs/job-title-levels).              |

#### Example

```json
  "recent_exec_departures": [
    {
      "departed_date": "2024-06",
      "pdl_id": "sosPKkiBABHsppzWEYyqgg_0000",
      "job_title": "vice president of revenue operations",
      "job_title_role": "analyst",
      "job_title_sub_role": "revenue_operations",
      "job_title_class": "general_and_administrative",
      "job_title_levels": ["vp"],
      "new_company_id": "ZFOfaDnanwu1hrtXsyfFEw521uw0",
      "new_company_job_title": "senior vice president, revenue operations",
      "new_company_job_title_role": "analyst",
      "new_company_job_title_sub_role": "revenue_operations",
      "new_company_job_title_class": "general_and_administrative",
      "new_company_job_title_levels": ["senior", "vp"]
    },
    ...
  ]
```

### `recent_exec_hires`

<table>
  <tr>
    <th>Description</th>
    <td>The profiles of all of CXOs, owners and VPs that have joined the company in the last three months.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

For each executive that has joined the company in the past three months, we provide the following information:

| Field                                 | Data Type                | Description                                                                                                                                                             |
| ------------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `joined_date`                         | `String (Date: YYYY-MM)` | The month the executive joined the company.                                                                                                                             |
| `pdl_id`                              | `String`                 | The ID of the executive in our [Person Dataset](https://docs.peopledatalabs.com/docs/fields).                                                                           |
| `job_title`                           | `String`                 | The executive's current job title at the company.                                                                                                                       |
| `job_title_role`                      | `Enum (String)`          | The executive's current job role at the company. This will be one of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).                   |
| `job_title_sub_role`                  | `Enum (String)`          | The executive's current job subrole at the company. This will be one of the [Canonical Job Subroles](https://docs.peopledatalabs.com/docs/job-title-subroles).          |
| `job_title_class`                     | `Enum (String)`          | The expense line item category this executive would fall into. This will be one of the [Canonical Job Classes](https://docs.peopledatalabs.com/docs/job-title-class)  . |
| `job_title_levels`                    | `Array [Enum (String)]`  | The executive's current job level at the company. This will be in the [Canonical Job Levels](https://docs.peopledatalabs.com/docs/job-title-levels).                    |
| `previous_company_id`                 | `String`                 | The [ID](#id) of the company the executive left.                                                                                                                        |
| `previous_company_job_title`          | `String`                 | The executive's previous job title at the old company.                                                                                                                  |
| `previous_company_job_title_role`     | `Enum (String)`          | The executive's previous job role at the old company. This will be one of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).              |
| `previous_company_job_title_sub_role` | `Enum (String)`          | The executive's previous job subrole at the old company. This will be one of the [Canonical Job Subroles](https://docs.peopledatalabs.com/docs/job-title-subroles).     |
| `previous_company_job_title_class`    | `Enum (String)`          | The executive's previous job class at the old company. This will be one of the [Canonical Job Classes](https://docs.peopledatalabs.com/docs/job-title-class) .          |
| `previous_company_job_title_levels`   | `Array [Enum (String)]`  | The executive's previous job levels at the old company. This will be in the [Canonical Job Levels](https://docs.peopledatalabs.com/docs/job-title-levels).              |

#### Example

```json
"recent_exec_hires": [
  {
    "joined_date": "2024-06",
    "pdl_id": "un-fsOccjHy1yElqJObW6g_0000",
    "job_title": "chief of staff to the chief executive officer and founder",
    "job_title_role": "operations",
    "job_title_sub_role": "aides",
    "job_title_class": "general_and_administrative",
    "job_title_levels": ["owner"],
    "previous_company_id": "RjhjJnYUCiAfXFyxCHLDQQ5opPrK",
    "previous_company_job_title": "business operations manager, reality labs",
    "previous_company_job_title_role": "professional_service",
    "previous_company_job_title_sub_role": "investment_banking",
    "previous_company_job_title_class": null,
    "previous_company_job_title_levels": ["manager"]
  },
    ...
  ]
```

## Top Next and Previous Employers

The top ten next and previous companies employees are broken down by job role.

Companies are listed using their [PDL Company ID](#id).

The first list of companies will be under the `"all"` key. This represents the top 10 companies for any role.

The roles are based on the employee’s role at the company queried. Each role listed in the break down will come from the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).

If no start date is given or no role exists, then the experience is not counted.

If there are fewer than ten next/previous employers for a role, it will return as many as there are.

### `top_next_employers`

<table>
  <tr>
    <th>Description</th>
    <td>The top ten companies employees moved to, and how many employees moved there, across all time periods.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This field uses `experience.title.role` and `experience.start_date` to find the top next employers. Companies are ranked by the number of previous employees currently employed there.

A company is considered to be a ""next employer"" if the employee has a start date after their start date for the company being queried.

This field is functionally identical to the legacy `top_next_employers_by_role field`, but adds a displayable company name to the response structure.

#### Example

```json JSON
"top_next_employers": {
  "finance": [
    {
      "id": "3kgY1DOS3BewEUBVRyl5Lg3tl13v",
      "count": 1,
      "display_name": "Essex Property Trust"
    },
    {
      "id": "OCuR0U1nT6kt66YfnUVKlQaeEYUr",
      "count": 1,
      "display_name": "Green Street"
    }
  ],
  "education": [
    {
      "id": "69IOeBijO7bNzClSGs6bxg4Dt7Ge",
      "count": 1,
      "display_name": "DoorDash"
    }
  ],
  "all": [
    {
      "id": "gbzAHmeUyu5rJyy4eUrPPgtM5jdC",
      "count": 5,
      "display_name": "Five by Five"
    },
    {
      "id": "Dn0GAueIRsYzwepbYEGIAQVi7Qyl",
      "count": 3,
      "display_name": "Anaconda"
    },
    ...
  ]
...
}

```

### `top_next_employers_12_month`

<table>
  <tr>
    <th>Description</th>
    <td>The top ten next employers, counting only employee changes within the last 12 months.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This field modifies the top\_next\_employers field, with a filter to only count for employees with job changes that have occurred within the last 12 months

#### Example

```json
"top_next_employers_12_month": {
  "education": [
    {
      "id": "69IOeBijO7bNzClSGs6bxg4Dt7Ge",
      "count": 1,
      "display_name": "DoorDash"
    }
  ],
  "all": [
    {
      "id": "gbzAHmeUyu5rJyy4eUrPPgtM5jdC",
      "count": 4,
      "display_name": "Five by Five"
    },
    {
      "id": "Dn0GAueIRsYzwepbYEGIAQVi7Qyl",
      "count": 2,
      "display_name": "Anaconda"
    },
    ...
  ]
...
}

```

### `top_next_employers_by_role`

> ⚠️ Deprecated Field
>
> As of April 2025, the `top_next_employer_by_role` field is deprecated and no longer recommended for use. It will be fully replaced in July 2025 (v31.0) by the new [`top_next_employers`](#top_next_employers) field which is now available in beta. We encourage all users to transition to this new field before the final sunset in July.
>
> For more information please see our [April 2025 Release Notes (v30.0)](https://docs.peopledatalabs.com/changelog/april-2025-release-notes-v300).

<table>
  <tr>
    <th>Description</th>
    <td>The top ten companies employees moved to and how many employees moved there.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This insight uses `experience.title.role` and `experience.start_date` to find the top next employers. Companies are ranked by the number of previous employees currently employed there.

A company is considered to be a "next employer" if the employee has a start date after their start date for the company being queried.

#### Example

```json
  "top_next_employers_by_role": {
    "all": {
      "aKCIYBNF9ey6o5CjHCCO4goHYKlf" : 573,
      "RjhjJnYUCiAfXFyxCHLDQQ5opPrK" : 498,
      ...
    },
    "finance": {
      "RZOFiRjw26VpLObnwmYXGgRyn3aW" : 294,
      "BWiTKOBgRTsSttn62R7EBQvww4gF" : 112,
      ...
    },
    ...
  }
```

### `top_previous_employers`

<table>
  <tr>
    <th>Description</th>
    <td>The top ten previous companies employees worked for previously, and how many current employees were previously employed by them, across all time periods.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This field uses `experience.title.role` and `experience.start_date` to find the top previous employers. Companies are ranked by the number of current employees previously employed there.

A company is considered to be a "previous employer" if the employee has a start date before their start date for the company being queried.

This field is functionally identical to the legacy `top_previous_employers_by_role field`, but adds a displayable company name to the response structure."

#### Example

```json
"top_previous_employers": {
  "finance": [
    {
      "id": "7L0SglhytLJVj2JOx3PqVgDa2lnM",
      "count": 1,
      "display_name": "MineralTree, Inc."
    },
    {
      "id": "HKCBzjcdUhVPHCmb246CSAYwkTC1",
      "count": 1,
      "display_name": "Center for Effective Government"
    },
    {
      "id": "Pt8QqdHiI5swPLyB4kwkWAnYh66C",
      "count": 1,
      "display_name": "University of Massachusetts Dartmouth"
    }
  ],
  "education": [
    {
      "id": "CKHJ5P60N4XW4oZXB8BdmgKL8vvO",
      "count": 1,
      "display_name": "US Army"
    },
    {
      "id": "DCD55P9HCbJ6EkJhEdPp0AFqPzf3",
      "count": 1,
      "display_name": "Oracle"
    }
  ],
  "all": [
    {
      "id": "aubMfPvUgxL09C7OTtPqqQFVuAR9",
      "count": 11,
      "display_name": "Pipl"
    },
    {
      "id": "Cw9vt7WFFRbhLDnoCeRbswn15Qhi",
      "count": 6,
      "display_name": "Intel Corporation"
    },
    ...
  ]
...
}

```

### `top_previous_employers_12_month`

<table>
  <tr>
    <th>Description</th>
    <td>The top ten previous employers, counting only employee changes within the last 12 months.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This field modifies the `top_previous_employers` field, with a filter to only count for employees with job changes that have occurred within the last 12 months

#### Example

```json
"top_previous_employers_12_month": {
  "education": [
    {
      "id": "DCD55P9HCbJ6EkJhEdPp0AFqPzf3",
      "count": 1,
      "display_name": "Oracle"
    }
  ],
  "all": [
    {
      "id": "aubMfPvUgxL09C7OTtPqqQFVuAR9",
      "count": 3,
      "display_name": "Pipl"
    },
    {
      "id": "Cw9vt7WFFRbhLDnoCeRbswn15Qhi",
      "count": 2,
      "display_name": "Intel Corporation"
    },
    ...
  ]
...
}

```

### `top_previous_employers_by_role`

> ⚠️ Deprecated Field
>
> As of April 2025, the `top_previous_employer_by_role` field is deprecated and no longer recommended for use. It will be fully replaced in July 2025 (v31.0) by the new [`top_previous_employers`](#top_previous_employers) field which is now available in beta. We encourage all users to transition to this new field before the final sunset in July.
>
> For more information please see our [April 2025 Release Notes (v30.0)](https://docs.peopledatalabs.com/changelog/april-2025-release-notes-v300).

<table>
  <tr>
    <th>Description</th>
    <td>The top ten previous companies employees worked for and how many current employees were previously employed by them.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This insight uses `experience.title.role` and `experience.start_date` to find the top previous employers. Companies are ranked by the number of current employees previously employed there.

A company is considered to be a "previous employer" if the employee has a start date before their start date for the company being queried.

#### Example

```json
  "top_previous_employers_by_role": {
    "all": {
      "aKCIYBNF9ey6o5CjHCCO4goHYKlf" : 573,
      "RjhjJnYUCiAfXFyxCHLDQQ5opPrK" : 498,
      ...
    },
    "finance": {
      "RZOFiRjw26VpLObnwmYXGgRyn3aW" : 294,
      "BWiTKOBgRTsSttn62R7EBQvww4gF" : 112,
      ...
    },
    ...
  }
```

## Top US Metros

### `top_us_employee_metros`

<table>
  <tr>
    <th>Description</th>
    <td>The top ten US metros where employees are based.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

This insight contains the top ten US metros for the company, ordered by the current headcount at each location. For each metro, we also provide the current headcount and the growth rate in that metro over the last twelve months.

Each metro listed is one of our [Canonical Metros](https://docs.peopledatalabs.com/docs/location-metros).

To determine the headcount at each location, we use our Person Data to find the location where each current employee works. If an employee does not have location data or they are not based in the US, they are not included in the count.

| Field                  | Data Type       | Description                                                                                                         |
| ---------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------- |
| `current_headcount`    | `Integer (> 0)` | The number of employees in the metro.                                                                               |
| `12_month_growth_rate` | `Float`         | The [growth rate](#employee_growth_rate) in the metro over the last twelve months, precise to fourth decimal place. |

#### Example

```json
  "top_us_employee_metros": {
    "san francisco, california, united states" : {
      "current_headcount" : 1207,
      "12_month_growth_rate" : .0040
    },
    "austin, texas, united states" : {
      "current_headcount" : 532,
      "12_month_growth_rate" : .0900
    },
    ...
  }
```

***

# Premium Company Fields

These high-value fields are available through our premium offerings.

## Premium Company Information

### `linkedin_follower_count`

<table>
  <tr>
    <th>Description</th>
    <td>The number of followers on a company’s LinkedIn profile.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (>= 0)</code></td>
  </tr>
</table>

#### Field Details

The number of followers on a company’s LinkedIn profile.

#### Example

```Text JSON
   "linkedin_follower_count": 5880
```

## Funding Details

### `funding_details`

<table>
  <tr>
    <th>Description</th>
    <td>List of all funding events associated with the company, with corresponding details.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

Each publicly disclosed funding event will be added to the `funding_details` list as an Object with the following fields:

| Field                   | Data Type                                                                | Description                                                                                                                                  |
| ----------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `funding_round_date`    | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The publicly disclosed date of the closing of the financing event.                                                                           |
| `funding_raised`        | `Float (> 0)`                                                            | The total amount raised during the funding event.                                                                                            |
| `funding_currency`      | `Enum (String)`                                                          | The currency code for the `funding_raised` value. Currently, this will always be `usd`.                                                      |
| `funding_type`          | `Enum (String)`                                                          | The funding stage of the funding event. Must be one of our [Canonical Funding Rounds](https://docs.peopledatalabs.com/docs/funding-rounds).  |
| `investing_companies`   | `Array [String]`                                                         | The [PDL Company IDs](https://docs.peopledatalabs.com/docs/company-schema#id) of the investing companies participating in the funding event. |
| `investing_individuals` | `Array [String (Titlecase)]`                                             | The names of any other investing individuals participating in the funding event.                                                             |

#### Example

```json
  "funding_details": [
    {
      "funding_round_date": "2021-11-16",
      "funding_raised": 45000000.0,
      "funding_currency": "usd",
      "funding_type": "series_b",
      "investing_companies": [
        "UHKkwjzET0f4c2FLBt5BOgB7eZH9",
        "s5O9wCcVnokBzzvX4TQwEwg07z1L"
      ],
      "investing_individuals": [
        "Guillaume \"G\" Cabane"
      ]
    },
    ...
  ]
```

## Parents and Subsidiaries

These insights provide the [company IDs](#id) of the queried company's parent and subsidiary companies.

### `all_subsidiaries`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="#id">IDs</a> of every company owned by the queried company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

The subsidiary company values will be the [ID](#id) of the company. If no subsidiaries are found, the value will be `null`.

#### Example

```json
  "all_subsidiaries" : [
    "HwrPqD6yDTnKmmPQFCgIeQ5hOn8j",
    "xhI4e4JvjGZF4SprW5hhCgmLfVjB",
    "niEc7rpuQ1GXwpuDPeeN2QWYggDC",
    "2BrnzFlEfHtRXJUakLCQYQuO0JnJ",
    "uBF8GihqobELnphsfR9ppwQbM9x7",
    "N7iFUv1vUYWF8t0JXHmL5gvFy4XE",
    "97JIBSIC059vdTevziAFJA7qSRNZ",
    "amtMwZGXmNDYoqBCSQBXQAxXVeWV"
  ]
```

### `direct_subsidiaries`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="#id">IDs</a> of each company that the queried company directly owns.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

The subsidiary company values will be the [ID](#id) of the company. If no subsidiaries are found, the value will be `null`.

#### Example

```json
  "direct_subsidiaries" : [
    "HwrPqD6yDTnKmmPQFCgIeQ5hOn8j",
    "2BrnzFlEfHtRXJUakLCQYQuO0JnJ",
    "uBF8GihqobELnphsfR9ppwQbM9x7",
    "N7iFUv1vUYWF8t0JXHmL5gvFy4XE",
    "97JIBSIC059vdTevziAFJA7qSRNZ",
    "amtMwZGXmNDYoqBCSQBXQAxXVeWV"
  ]
```

### `immediate_parent`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="#id">ID</a> of the company that directly owns the queried company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The parent company value will be the [ID](#id) of the company. If no parents are found, the value will be `null`.

#### Example

```json
  "immediate_parent": "amtMwZGXmNDYoqBCSQBXQAxXVeWV"
```

### `ultimate_parent`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="#id">ID</a> of the ultimate organizational entity that owns the queried company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The parent company value will be the [ID](#id) of the company. If no parents are found, the value will be `null`.

#### Example

```json
  "ultimate_parent": "0XQ1XCKrHIFF3H6tBVRdzAIknJNS"
```

### `ultimate_parent_ticker`

<table>
  <tr>
    <th>Description</th>
    <td>Stock symbol of the company's ultimate parent (only for subsidiaries of public companies)</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The `ultimate_parent_ticker` field will be populated for records where the company is a subsidiary of a public company. These companies will also have a [`type`](https://docs.peopledatalabs.com/docs/company-schema#type) value of `public_subsidiary` following the v28.0 release in October 2024.

#### Example

```json
  "ultimate_parent_ticker": "CRM",
```

### `ultimate_parent_mic_exchange`

<table>
  <tr>
    <th>Description</th>
    <td>MIC exchange code that corresponds to the stock exchange of the company's ultimate parent (only for subsidiaries of public companies)</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The `ultimate_parent_mic_exchange` field will be populated for records where the company is a subsidiary of a public company. These companies will also have a [`type`](https://docs.peopledatalabs.com/docs/company-schema#type) value of `public_subsidiary` following the v28.0 release in October 2024.

#### Example

```json
  "ultimate_parent_mic_exchange": "XNYS"
```

## Affiliated Entities

### `affiliated_entities`

<table>
  <tr>
    <th>Description</th>
    <td>An object containing information on related company profiles.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

| Field                    | Data Type        | Description                                                                                                                                                                                                                           |
| :----------------------- | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `affiliated_id`          | `String`         | PDL Company ID of the affiliated company record.                                                                                                                                                                                      |
| `display_name`           | `String`         | display\_name of the affiliated company record.                                                                                                                                                                                        |
| `relationship`           | `Enum (String)`  | Categorization of the relationship type to the affiliated company record. The value of this field will be one of our canonical [Relationship Types](https://docs.peopledatalabs.com/docs/relationship_types)                          |
| `relationship_catalyst`  | `Enum (String)`  | Categorization of the event that formed the relationship to the affiliated company record. The value of this field will be one of our canonical [Relationship Catalysts](https://docs.peopledatalabs.com/docs/relationship_catalysts) |
| `relationship_status`    | `Enum (String)`  | Whether the relationship is active, pending, or inactive. The value of this field will be one of our canonical [Relationship Statuses](https://docs.peopledatalabs.com/docs/relationship_status).                                     |
| `start_date`             | `String (Date)`  | Date when the affiliated company became related. For mergers or acquisitions, this will be the date that the transaction is closed (when that information is available); otherwise, this will be the date announced.                  |
| `end_date`               | `String (Date)`  | When applicable, the date when the the affiliated company was divested or otherwise no longer affiliated.                                                                                                                             |
| `relationship_citations` | `Array [String]` | List of URL links to news articles, press releases, or company webpages that describe the business relationship.                                                                                                                      |

#### Example

```json
  "affiliated_entities": [
    {
      "affiliated_id": "es7LgyqRNsFDLcWXC3WAvACHVh9g",
      "display_name": "Salesforce",
      "relationship": "ultimate_parent"
    }
  ]
```

<br />

## Office Insights

### `locations`

<table>
  <tr>
    <th>Description</th>
    <td>An object containing increasingly granular information about all locations associated to the company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Field Details

In addition to a company's location of its Headquarters (HQ) we provide a list of known offices. As of v31.1 (August 2025 Release) we are also tagging offices as active or inactive and the date it was first and last observed in our data sources:

| Field        | Data Type | Description                                                                                         |
| :----------- | :-------- | :-------------------------------------------------------------------------------------------------- |
| `first_seen` | `String`  | The date that this location was first observed in association with the company record.              |
| `last_seen`  | `String`  | The date that this location was last observed in association with the company record.               |
| `is_active`  | `Boolean` | Denotes whether this location was active (“true”) or inactive (“false”) as of the last observation. |

For more information on our standard location fields, see [Data Formatting: Locations](https://docs.peopledatalabs.com/docs/data-formatting#locations).

#### Example

```json
"locations": [
  {
    "name": "palo alto, california, united states",
    "locality": "palo alto",
    "region": "california",
    "metro": "san jose, california",
    "country": "united states",
    "continent": "north america",
    "street_address": "1455 3rd street",
    "address_line_2": null,
    "postal_code": "94304",
    "geo": "37.44,-122.14",
    "first_seen": "2022-06-11",
    "last_seen": "2024-03-12",
    "is_primary": false,
    "is_active": true
  },
  {
    "name": "san francisco, california, united states",
    "locality": "san francisco",
    "region": "california",
    "metro": "san francisco, california",
    "country": "united states",
    "continent": "north america",
    "street_address": "1455 3rd street",
    "address_line_2": null,
    "postal_code": "94108",
    "geo": "37.77,-122.41",
    "first_seen": "2022-06-11",
    "last_seen": "2024-03-12",
    "is_primary": false,
    "is_active": true
  },
  {
    "name": "san francisco, california, united states",
    "locality": "san francisco",
    "region": "california",
    "metro": "san francisco, california",
    "country": "united states",
    "continent": "north america",
    "street_address": "1725 3rd street",
    "address_line_2": null,
    "postal_code": "94158",
    "geo": "37.77,-122.41",
    "first_seen": "2022-06-11",
    "last_seen": "2024-03-12",
    "is_primary": true,
    "is_active": true
  },

```

<br />

### `num_active_locations`

<table>
  <tr>
    <th>Description</th>
    <td>Count of all active locations associated to the company record.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer > 0</code></td>
  </tr>
</table>

#### Example

```json
"num_active_locations": 20
```

<br />

### `num_total_locations`

<table>
  <tr>
    <th>Description</th>
    <td>Count of all locations associated with the company record.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer > 0</code></td>
  </tr>
</table>

#### Example

```json
"num_total_locations": 30
```

## Job Posting Insights

These fields provide an aggregate summary of the open and filled job postings at a company.

### `active_job_postings`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that existed over the course of the most recent month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer</code></td>
  </tr>
</table>

#### Example

```json
"active_job_postings": 4
```

### `deactivated_job_postings`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct job postings that were removed/no longer captured over the course of the most recent month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer</code></td>
  </tr>
</table>

#### Example

```json
"deactivated_job_postings": 3
```

### `active_job_postings_by_role`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that existed over the course of the most recent month, categorized by Job Title Role.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"active_job_postings_by_role": {
    "support": 1,
    "product": 1,
    "engineering": 2
}
```

### `deactivated_job_postings_by_role`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that were removed/no longer captured over the course of the most recent month, categorized by Job Title Role.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"deactivated_job_postings_by_role": {
    "other_uncategorized": 1,
    "product": 1,
    "engineering": 1
}
```

### `active_job_postings_by_class`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that existed over the course of the most recent month, categorized by Job Title Class.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"active_job_postings_by_class": {
    "general_and_administrative": 1,
    "research_and_development": 2,
    "services": 1
}
```

### `deactivated_job_postings_by_class`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that existed over the course of the most recent month, categorized by Job Title Class.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"deactivated_job_postings_by_class": {
    "other_uncategorized": 1,
    "general_and_administrative": 1,
    "research_and_development": 2
}
```

### `active_job_postings_by_sub_role`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that existed over the course of the most recent month, categorized by Job Title Subrole.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"active_job_postings_by_sub_role": {
  "other_uncategorized": 1,
  "product_management" : 1,
  "data_engineering" : 2   
}
```

### `deactivated_job_postings_by_sub_role`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that were removed/no longer captured over the course of the most recent month, categorized by Job Title Subrole.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"deactivated_job_postings_by_sub_role": {
  "other_uncategorized": 1,
  "product_management" : 1,
  "data_engineering" : 1   
}
```

### `active_job_postings_by_country`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that existed over the course of the most recent month, categorized by the Country of the job posting.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"active_job_postings_by_country": {
    "other_uncategorized": 1,
    "remote_location": 8,
    "brazil": 36,
    "united states": 331,
    "canada": 84,
    "netherlands": 2
}
```

### `active_job_postings_by_metro`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that existed over the course of the most recent month, categorized by the Metro of the job posting.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"active_job_postings_by_metro": {
    "other_uncategorized": 142,
    "remote_location": 8,
    "denver, colorado, united states": 1,
    "san francisco, california, united states": 127,
    "seattle, washington, united states": 35,
    "atlanta, georgia, united states": 1,        
    "new york, new york, united states": 100,
    "salt lake city, utah, united states": 54,
    "austin, texas, united states": 1,
    "san diego, california, united states": 1
}
```

### `active_job_postings_by_month`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that existed over the course of each month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"active_job_postings_by_month": {
    "2024-10": 2,
    "2024-11": 3,
    "2024-12": 4,
    "2025-01": 7,
    "2025-02": 4
}
```

### `deactivated_job_postings_by_month`

<table>
  <tr>
    <th>Description</th>
    <td>Count of distinct, active job postings that were removed/no longer captured over the course of each month.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Object</code></td>
  </tr>
</table>

#### Example

```json
"deactivated_job_postings_by_month": {
    "2024-12": 1,
    "2025-01": 0,
    "2025-02": 4
}
```