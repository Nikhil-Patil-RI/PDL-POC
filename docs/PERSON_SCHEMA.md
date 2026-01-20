

# Person Schema

# Overview

This page details the Person Data that we provide through our Person APIs, such as [Person Enrichment](https://docs.peopledatalabs.com/docs/person-enrichment-api) and [Person Search](https://docs.peopledatalabs.com/docs/person-search-api).

> 📘 Field Availability
>
> **Not all fields are available in all bundles.**
>
> Free plans, by default, do not have access to contact fields like emails, phone numbers, and street addresses and will instead appear as true if the value exists or false if it does not. To unlock the values, please upgrade to a Pro plan. Read more here: [Plan types: Free vs Pro](https://support.peopledatalabs.com/hc/en-us/articles/27546010665115-Plan-types-Free-vs-Pro)

<Image align="center" border={false} src="https://files.readme.io/97461a90a5ce33f98656a8e35e26c2260064c6949efd7e6898411b6f0d17c0f2-freevpro.png" />

* For more information about data formatting, see [Data Types](https://docs.peopledatalabs.com/docs/data-types) and [Data Formatting](https://docs.peopledatalabs.com/docs/data-formatting)
* For a full example record, see [Example Person Record](https://docs.peopledatalabs.com/docs/example-record).
* For a simplified overview of our person fields, check out the [Person Data Overview](https://docs.peopledatalabs.com/docs/person-data-overview).
* For more details about our person fields, including fill rates and which fields are included in the base vs premium [field bundles](https://docs.peopledatalabs.com/docs/person-data-field-bundles), check out our [Person Stats](https://docs.peopledatalabs.com/docs/datasets) pages.
* For a full data ingestion JSON schema, check out [this page](https://docs.peopledatalabs.com/docs/receiving-and-updating-data#data-ingestion-schemas).
* If you'd like access to premium fields or have questions about which fields are included in your specific field bundle(s), please [speak to one of our data consultants](https://peopledatalabs.com/talk-to-sales).

***

## Identifiers

### `first_name`

<table>
  <tr>
    <th>Description</th>
    <td>The person's first name.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The person's first name.

#### Example

```json
  "first_name": "sean"
```

### `full_name`

<table>
  <tr>
    <th>Description</th>
    <td>The person's full name.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The first and the last name fields appended with a space.

#### Example

```json
  "full_name": "sean thorne"
```

### `id`

<table>
  <tr>
    <th>Description</th>
    <td>A unique persistent identifier for the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The ID is a unique, persistent, and hashed value that represents a specific person.

As of [v24](https://docs.peopledatalabs.com/changelog/october-2023-release-notes-v24#person-id-max-length), IDs have a max length of **64 characters**, although in practice we expect IDs to be closer to 32 characters in length.

See `<https://docs.peopledatalabs.com/docs/persistent-ids>` for more information.

#### Example

```json
  "id": "qEnOZ5Oh0poWnQ1luFBfVw_0000"
```

### `last_initial`

<table>
  <tr>
    <th>Description</th>
    <td>The first letter of the person's last name.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String (1 character)</code></td>
  </tr>
</table>

#### Field Details

The first letter of the person's last name.

#### Example

```json
  "last_initial": "t"
```

### `last_name`

<table>
  <tr>
    <th>Description</th>
    <td>The person's last name.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The person's last name.

#### Example

```json
  "last_name": "thorne"
```

### `middle_initial`

<table>
  <tr>
    <th>Description</th>
    <td>The first letter of the person's middle name.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String (1 character)</code></td>
  </tr>
</table>

#### Field Details

The first letter of the person's middle name.

#### Example

```json
  "middle_initial": "f"
```

### `middle_name`

<table>
  <tr>
    <th>Description</th>
    <td>The person's middle name.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The person's middle name.

#### Example

```json
  "middle_name": "fong"
```

### `name_aliases`

<table>
  <tr>
    <th>Description</th>
    <td>Any other names the person goes by.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

Any associated names or aliases besides the primary one used in the [`full_name`](#full_name) field.

<Callout icon="💡" theme="default">
  ### Sort Order

  Name aliases are sorted with the primary alias first. The remaining aliases are sorted by `num_sources`, `last_seen`, `first_seen`, `full_name`, all in reverse order (highest first, most recent, Z→A):

  1. Primary name first
  2. `num_sources` (highest first)
  3. `last_seen` (most recent first)
  4. `first_seen` (most recent first)
  5. `full_name` (Z→A)
</Callout>

#### Example

```json
  "name_aliases": [
    "andrew nichol",
    "r andrew nichol",
    "robert nichol"
  ]
```

## Contact Information

### `emails`

<table>
  <tr>
    <th>Description</th>
    <td>Email addresses associated with the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

<Callout icon="⚠️">
  **Note** This array contains historical email addresses and should **not** directly be used for email outreach.  [Recommended Alternatives](https://docs.peopledatalabs.com/docs/email-data-for-outreach)
</Callout>

Each email associated with the person will be added to this list as its own object.

| Field          | Data Type                                                                | Description                                                                                                             |
| -------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `address`      | `String`                                                                 | The fully parsed email address                                                                                          |
| `first_seen`   | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this entity was first associated with the Person record.                                                  |
| `last_seen`    | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this entity was last associated with the Person record.                                                   |
| `num_sources`  | `Integer (> 0)`                                                          | The number of sources that have contributed to the association of this entity with the Person record.                   |
| `md5_hash`     | `String`                                                                 | A 128-bit hash of an email in md5 format.                                                                               |
| `sha_256_hash` | `String`                                                                 | A 256-bit hash of an email in sha256 format.                                                                            |
| `type`         | `Enum (String)`                                                          | The type of email address. Must be one of our [Canonical Email Types](https://docs.peopledatalabs.com/docs/email-types) |

<Callout icon="💡" theme="default">
  ### Sort Order

  Emails are sorted first by `last_seen`, then by `first_seen`, `email` , all in reverse order (most recent first, Z→A):

  1. `last_seen` (most recent first)
  2. `first_seen` (most recent first)
  3. `email` (Z→A)
</Callout>

#### Example

```json
  "emails": [
    {
      "address": "sean@peopledatalabs.com",
      "type": "current_professional",
      "md5_hash": "89eb6bc60e92f3d6ffbb4e7b4d15cacd",
      "sha_256_hash": "138ea1a7076bb01889af2309de02e8b826c27f022b21ea8cf11aca9285d5a04e",
      "first_seen": "2017-06-02",
      "last_seen": "2019-07-18",
      "num_sources": 17
    },
    {
      "address": "sean@gmail.com",
      "type": "personal",
      "md5_hash": "17725f5327de7695d658f124636cbd23",
      "sha_256_hash": "ae0591a02b4cb0be73fff1ebe061a95b1bfc23350a9a297923edda014c6a88f8",
      "first_seen": "2017-06-02",
      "last_seen": "2019-07-18",
      "num_sources": 17
    }
  ]
```

### `mobile_phone`

<table>
  <tr>
    <th>Description</th>
    <td> The personal mobile phone associated with this individual. Mobile phones can only be associated with 1 person in the PDL data.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#phone-numbers"><code>String (Phone)</code></a></td>
  </tr>
</table>

#### Field Details

The `mobile_phone` field is generated from a highly confident source of mobile phones. We've hand-validated a sample of these and seen over 90% accuracy.

#### Example

```json
  "mobile_phone": "+15558675309"
```

### `personal_emails`

<table>
  <tr>
    <th>Description</th>
    <td>All personal emails associated with the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

The list of all [`emails`](#emails) tagged as `type = personal`.

<Callout icon="💡" theme="default">
  ### Sort Order

  Personal emails are sorted with the recommended personal email first. The remaining emails are sorted in the same order as the `emails` array:`last_seen`, then by `first_seen`, `email`, all in reverse order (most recent first, Z→A):

  1. Recommended personal email first
  2. `last_seen` (most recent first)
  3. `first_seen` (most recent first)
  4. `email` (Z→A)
</Callout>

#### Example

```json
  "personal_emails": [
    "sean@gmail.com"
  ]
```

### `phone_numbers`

<table>
  <tr>
    <th>Description</th>
    <td>All phone numbers associated with the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#phone-numbers"><code>Array \[String (Phone)]</code></a></td>
  </tr>
</table>

#### Field Details

For more detailed metadata on individual phone numbers, see the [`phones`](#phones) field.

<Callout icon="💡" theme="default">
  ### Sort Order

  Phone numbers are sorted with any mobile phone numbers first. The rest of the array is sorted by `num_sources`, `last_seen`, `first_seen`,  all in reverse order and using the E.164 format (highest first, most recent first):

  1. Mobile phone numbers first
  2. `num_sources` (highest first)
  3. `last_seen` (most recent first)
  4. `first_seen` (most recent first)
</Callout>

#### Example

```json
  "phone_numbers": [
    "+15558675309"
  ]
```

### `phones`

<table>
  <tr>
    <th>Description</th>
    <td>The list of phone numbers associated with this record with additional metadata.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

Each phone number object in this list will contain the following information.

| Field         | Data Type                                                                         | Description                                                                                      |
| ------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `first_seen`  | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates)          | The date that this number was first associated with this record.                                 |
| `last_seen`   | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates)          | The date that this number was last associated with this record.                                  |
| `num_sources` | `Integer (> 0)`                                                                   | The number of sources that have contributed to the association of this profile with this record. |
| `number`      | [`String (Phone)`](https://docs.peopledatalabs.com/docs/data-types#phone-numbers) | The phone number.                                                                                |

<Callout icon="💡" theme="default">
  ### Sort Order

  Phones are sorted with any mobile phone numbers first. The rest of the array is sorted by `num_sources`, `last_seen`, `first_seen`,  all in reverse order and using the E.164 format (highest first, most recent first):

  1. Mobile phone numbers first
  2. `num_sources` (highest first)
  3. `last_seen` (most recent first)
  4. `first_seen` (most recent first)
</Callout>

#### Example

```json
  "phones": [
    {
      "number": "+15558675309",
      "first_seen": "2017-06-02",
      "last_seen": "2019-07-18",
      "num_sources": 17
    }
  ]
```

### `recommended_personal_email`

<table>
  <tr>
    <th>Description</th>
    <td>The best available email to reach a person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

This field is generated by analyzing the all of a person's emails in the [`personal_emails`](#personal_emails) list to identify the best available email.

Through testing, we’ve found that using the email identified in `recommended_personal_email` versus selecting a random email address from [`personal_emails`](#personal_emails) resulted in ~37% higher deliverability.

#### Example

```json
  "recommended_personal_email": "sean@gmail.com"
```

### `work_email`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current work email.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The value for this field must use valid email address formatting. It is common and expected that work email domains may differ from the company's website for a number of reasons:

* The company changed their website domain
* The company has opted for a shorter email domain
* The company has been merged into or was acquired by another company

#### Example

```json
  "work_email": "sean@peopledatalabs.com"
```

## Current Company

These fields describe the company the person currently works at. These fields will match the corresponding values in our [Company Schema](https://docs.peopledatalabs.com/docs/company-schema) and will use the same formatting and parsing logic.

### `job_company_12mo_employee_growth_rate`

<table>
  <tr>
    <th>Description</th>
    <td>The person’s current company’s  percentage increase in total headcount over the past 12 months. Mapped from <a href="https://docs.peopledatalabs.com/docs/company-schema#employee_growth_rate"><code>employee\_growth\_rate.12\_month</code></a>.<br /><br />Growth rate is calculated as <code>(current\_employee\_count / previous\_employee\_count) - 1</code>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Float</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_12mo_employee_growth_rate": -0.1379
```

### `job_company_facebook_url`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#facebook_url">Facebook URL</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_facebook_url": "facebook.com/peopledatalabs"
```

### `job_company_founded`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#founded">founding year</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (> 0)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_founded": 2015
```

### `job_company_employee_count`

<table>
  <tr>
    <th>Description</th>
    <td>The total number of PDL profiles associated with the person’s current company. Mapped from <a href="https://docs.peopledatalabs.com/docs/company-schema#employee_count"><code>employee\_count</code></a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer  (>= 0)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_employee_count": 125
```

### `job_company_id`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#id">PDL ID</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_id": "tnHcNHbCv8MKeLh92946LAkX6PKg"
```

### `job_company_industry`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#industry">industry</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_industry": "computer software"
```

### `job_company_inferred_revenue`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/company-schema#inferred_revenue">estimated annual revenue range</a> in USD of the person’s current company.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_inferred_revenue": "$25M-$50M"
```

### `job_company_linkedin_id`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#linkedin_id">LinkedIn ID</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_linkedin_id": "18170482"
```

### `job_company_linkedin_url`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#linkedin_url">LinkedIn URL</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_linkedin_url": "linkedin.com/company/peopledatalabs"
```

### `job_company_location_address_line_2`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-formatting#common-location-fields">street address line 2</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_address_line_2": "suite 1670"
```

### `job_company_location_continent`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-types#locations">continent</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_continent": "north america"
```

### `job_company_location_country`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-types#locations">country</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_country": "united states"
```

### `job_company_location_geo`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-types#locations">city-center geographic coordinates</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_geo": "37.77,-122.41"
```

### `job_company_location_locality`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-types#locations">locality</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_locality": "san francisco"
```

### `job_company_location_metro`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-formatting#locations">metro area</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_metro": "san francisco, california"
```

### `job_company_location_name`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-formatting#locations">location name</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_name": "san francisco, california, united states"
```

### `job_company_location_postal_code`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-formatting#locations">postal code</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_postal_code": "94105"
```

### `job_company_location_region`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-formatting#locations">region</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_region": "california"
```

### `job_company_location_street_address`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's headquarters' <a href="https://docs.peopledatalabs.com/docs/data-formatting#locations">street address</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_location_street_address": "455 market st"
```

### `job_company_name`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#name">name</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_name": "people data labs"
```

### `job_company_size`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-sizes">size range</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_size": "51-200"
```

### `job_company_ticker`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#ticker">ticker</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_ticker": "goog"
```

### `job_company_total_funding_raised`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/company-schema#total_funding_raised">cumulative amount of money raised</a> in USD by the person’s current company during all publicly disclosed funding rounds.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (> 0)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_total_funding_raised": 55250000.0
```

### `job_company_twitter_url`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#twitter_url">Twitter URL</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_twitter_url": "twitter.com/peopledatalabs"
```

### `job_company_type`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#type">type</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_type": "public"
```

### `job_company_website`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current company's <a href="https://docs.peopledatalabs.com/docs/company-schema#website">website</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_company_website": "peopledatalabs.com"
```

## Current Job

These fields describe the person's most recent work experience.

### `inferred_salary`

<table>
  <tr>
    <th>Description</th>
    <td>The inferred salary range (USD) for the person's current job.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

Must be one of our [Canonical Inferred Salary Ranges](https://docs.peopledatalabs.com/docs/inferred-salaries).

#### Example

```json
  "inferred_salary": "70,000-85,000"
```

### `job_last_changed`

<table>
  <tr>
    <th>Description</th>
    <td>The timestamp that reflects when the top-level job information changed.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#dates"><code>String (Date)</code></a></td>
  </tr>
</table>

#### Field Details

An update is the time when the current employment information is modified in the record.

> 🚧 Limitations of Observed Data
>
> This field reflects **observed data**. This means that this timestamp will reflect the date when updates were propagated into our data build from our data sources, and may contain some lag time compared to real-life events. For example, if User A changed their job on October 1, 2023, but did not update that publicly until December 1, 2023, our timestamp for job\_last\_changed will be December.

#### Example

```json
  "job_last_changed": "2023-12-01"
```

### `job_last_verified` <a name="job_last_updated" />

<table>
  <tr>
    <th>Description</th>
    <td>The timestamp that reflects when the top level job information was last validated by a data source.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#dates"><code>String (Date)</code></a></td>
  </tr>
</table>

#### Field Details

An update is the time when the information in a record is validated through a data source. For more information how this timestamp is generated see: [Experience & Location Updates](https://docs.peopledatalabs.com/docs/last_updated-field)

#### Example

```json
  "job_last_verified": "2024-01-05"
```

### `job_onet_broad_occupation`

<table>
  <tr>
    <th>Description</th>
    <td>The O\*NET Broad Occupation associated with the person’s current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_onet_broad_occupation": "Chief Executives"
```

### `job_onet_code`

<table>
  <tr>
    <th>Description</th>
    <td>The 8-digit O\*NET code for the person’s current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The 8-digit O\*NET code for the person’s current job title, [following the 2018 SOC guidelines](https://www.bls.gov/soc/2018/soc_2018_class_and_coding_structure.pdf).

#### Example

```json
  "job_onet_code": "11-1011.00"
```

### `job_onet_major_group`

<table>
  <tr>
    <th>Description</th>
    <td>The O\*NET Major Group associated with the person’s current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_onet_major_group": "Management Occupations"
```

### `job_onet_minor_group`

<table>
  <tr>
    <th>Description</th>
    <td>The O\*NET Minor Group associated with the person’s current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_onet_minor_group": "Top Executives"
```

### `job_onet_specific_occupation`

<table>
  <tr>
    <th>Description</th>
    <td>The O\*NET Specific Occupation associated with the person’s current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "job_onet_specific_occupation": "Chief Executives"
```

### `job_onet_specific_occupation_detail`

<table>
  <tr>
    <th>Description</th>
    <td>A more detailed job title classification than O\*NET Specific Occupation.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

A more detailed job title for records where the specific occupation within O\*NET's standard hierarchy isn't granular enough to accurately describe the job title.

For example, the highest level of granularity in O\*NET for C-suite positions is Chief Executives. With this field, we can specify the type of executive role.

#### Example

```json
  "job_onet_specific_occupation_detail": "Chief Technology Officer"
```

### `job_start_date`

<table>
  <tr>
    <th>Description</th>
    <td>The date the person started their current job.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#dates"><code>String (Date)</code></a></td>
  </tr>
</table>

#### Example

```json
  "job_start_date": "2015-03"
```

### `job_summary`

<table>
  <tr>
    <th>Description</th>
    <td>User-inputted summary of their current job.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The summary is lowercased, but otherwise kept as-is from the raw source.

#### Example

```json
  "job_summary": "worked on the \"search analytics\" team to understand our users better"
```

### `job_title`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The person's current job title.

#### Example

```json
  "job_title": "co-founder and chief executive officer"
```

### `job_title_class`

<table>
  <tr>
    <th>Description</th>
    <td>The expense line item category this employee would fall into.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

Each class in the list will be one of our [Canonical Job Title Classes](https://docs.peopledatalabs.com/docs/job-title-class-post-v271).

#### Example

```json
  "job_title_class": "research_and_development"
```

### `job_title_levels`

<table>
  <tr>
    <th>Description</th>
    <td>The derived level(s) of the person's current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Enum (String)]</code></td>
  </tr>
</table>

#### Field Details

Each level in the list will be one of our [Canonical Job Title Levels](https://docs.peopledatalabs.com/docs/job-title-levels).

<HTMLBlock>
  {`
  <p class="page-header">Job Title Levels Hierarchy from "least important" to "most important":</p>
  <div>
    <button class="btn btn-scale">Unpaid</button>
    <button class="btn btn-scale">Training</button>
    <button class="btn btn-scale">Entry</button>
    <button class="btn btn-scale">Manager</button>
    <button class="btn btn-scale">Senior</button>
    <button class="btn btn-scale">Partner</button>
    <button class="btn btn-scale">Director</button>
    <button class="btn btn-scale">VP</button>
    <button class="btn btn-scale">Owner</button>
    <button class="btn btn-scale">CXO</button>
  </div>
  `}
</HTMLBlock>

Note: The `cxo` level is a catch-all for "Chief \_\_ Officer" roles, so a CEO, CIO, CTO, etc. will all have `job_title_levels: ["cxo"]`.

#### Example

```json
  "job_title_levels": ["cxo", "owner"]
```

### `job_title_role`

<table>
  <tr>
    <th>Description</th>
    <td>The derived role of the person's current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

The value will be one of our [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).

> 🚧 Major Update as of v29.1 (February 29.1)
>
> In v29.1 (February 2024) we made significant improvements to our role and sub\_role categorizations and updated many of the canonical values associated with these fields.
>
> Please see our [February 2025 Release Notes (v29.1)](https://docs.peopledatalabs.com/changelog/february-2025-release-notes-v291)for further information.

#### Example

```json
  "job_title_role": "operations"
```

### `job_title_sub_role`

<table>
  <tr>
    <th>Description</th>
    <td>The derived subrole of the person's current job title.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

The value will be one of our [Canonical Job Sub Roles](https://docs.peopledatalabs.com/docs/job-title-subroles). Each subrole maps to a role. See `<https://docs.peopledatalabs.com/docs/title-subroles-to-roles>` for a complete mapping list.

> 🚧 Major Update as of v29.1 (February 29.1)
>
> In v29.1 (February 2024) we made significant improvements to our role and sub\_role categorizations and updated many of the canonical values associated with these fields.
>
> Please see our [February 2025 Release Notes (v29.1)](https://docs.peopledatalabs.com/changelog/february-2025-release-notes-v291)for further information.

#### Example

```json
  "job_title_sub_role": "logistics"
```

## Demographics

### `birth_date`

<table>
  <tr>
    <th>Description</th>
    <td>The day the person was born.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#dates"><code>String (Date)</code></a></td>
  </tr>
</table>

#### Field Details

If this field exists, [`birth_year`](#birth_year) will agree with it.

#### Example

```json
  "birth_date": "1990-12-02"
```

### `birth_year`

<table>
  <tr>
    <th>Description</th>
    <td>The year the person was born.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer</code></td>
  </tr>
</table>

#### Field Details

The approximated birth year associated with this person profile. If a profile has a [`birth_date`](#birth_date), the `birth_year` field will match it.

#### Example

```json
  "birth_year": 1990
```

### `sex`

<a name="gender" />

> 🚧 `gender` was renamed to `sex` in v26.0
>
> In v26.0 (April 2024) we renamed this field from `gender` to `sex`, in accordance with legislative changes defining aspects of gender as sensitive personal data (which PDL does not process or output).
>
> Please see our [April 2024 Release Announcement (v26.0)](https://docs.peopledatalabs.com/changelog/april-2024-release-announcement-v260#rename-gender-breaking) for further information.

<table>
  <tr>
    <th>Description</th>
    <td>The person's sex.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

The value will always be one of our [Canonical Sex](https://docs.peopledatalabs.com/docs/sex).

#### Example

```json
  "sex": "male"
```

### `languages`

<table>
  <tr>
    <th>Description</th>
    <td>Languages the person knows.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

The languages listed are based on user input, we do not verify them.

| Field         | Data Type       | Description                                                                                                  |
| ------------- | --------------- | ------------------------------------------------------------------------------------------------------------ |
| `name`        | `Enum (String)` | The language. Must be one of our [Canonical Languages](https://docs.peopledatalabs.com/docs/language-names). |
| `proficiency` | `Integer (1-5)` | Self-ranked language proficiency from 1 (limited) to 5 (fluent).                                             |

<Callout icon="💡" theme="default">
  ### Sort Order

  Languages are sorted by `proficiency` first, followed by `name`, all in reverse order (highest proficiency first, Z→A):

  1. `proficiency` (highest first)
  2. `name` (Z→A)
</Callout>

#### Example

```json
  "languages": [
    {
      "name": "english",
      "proficiency": 5
    }
  ]
```

## Education

### `education`

<table>
  <tr>
    <th>Description</th>
    <td>The person's education information.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

The education objects associated with this person profile, which, when output in CSV format, have indexing based on recency and associativity.

Each education object in the list will include the following data:

| Field                        | Data Type                                                                | Description                                                                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `degrees`                    | `Array [Enum (String)]`                                                  | The degrees the person earned at the school. All values will be [Canonical Education Degrees](https://docs.peopledatalabs.com/docs/education-degrees) |
| `end_date`                   | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date the person left the school. If the person is still at the school, will be `null`.                                                            |
| `gpa`                        | `Float`                                                                  | The GPA the person earned at the school.                                                                                                              |
| `majors`                     | `Array [Enum (String)]`                                                  | All majors earned at the school. All values will be [Canonical Education Majors](https://docs.peopledatalabs.com/docs/education-majors).              |
| `minors`                     | `Array [Enum (String)]`                                                  | All minors earned at the school. All values will be [Canonical Education Majors](https://docs.peopledatalabs.com/docs/education-majors).              |
| `raw`                        | `Array [String]`                                                         | Raw education data that was parsed into the `degrees`, `majors`, and `minors` fields.                                                                 |
| [`school`](#educationschool) | `Object`                                                                 | The school the person attended.                                                                                                                       |
| `start_date`                 | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date the person started at the school.                                                                                                            |
| `summary`                    | `String`                                                                 | User-inputted summary of their education.                                                                                                             |

<Callout icon="💡" theme="default">
  ### Sort Order

  Education entries are sorted first by `start_date`, then by `end_date`. If dates are identical, then sorting occurs by `school.name`, followed by `majors`, `minors` and `degrees`, all in reverse order (most recent first, Z→A):

  1. `start_date`(most recent first)
  2. `end_date` (most recent first)
  3. `school.name` (Z→A)
  4. countries`majors` (Z→A)
  5. `minors` (Z→A)
  6. `degrees` (Z→A)
</Callout>

##### `education.school`

To tap into our school matching logic, use our [School Cleaner API](https://docs.peopledatalabs.com/docs/cleaner-apis) to retrieve possible school values.

| Field          | Sub Field   | Data Type        | Description                                                                                                                                                            |
| -------------- | ----------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `domain`       |             | `String`         | The primary website domain associated with the school.                                                                                                                 |
| `facebook_url` |             | `String`         | The school's Facebook URL                                                                                                                                              |
| `id`           |             | `String`         | The **NON-PERSISTENT** ID for the school in our records.                                                                                                               |
| `linkedin_id`  |             | `String`         | The school's LinkedIn ID                                                                                                                                               |
| `linkedin_url` |             | `String`         | The school's LinkedIn URL                                                                                                                                              |
| `location`     |             | `Object`         | The location of the school. See [Common Location Fields](https://docs.peopledatalabs.com/docs/data-formatting#common-location-fields) for detailed field descriptions. |
|                | `continent` | `Enum (String)`  |                                                                                                                                                                        |
|                | `country`   | `Enum (String)`  |                                                                                                                                                                        |
|                | `locality`  | `String`         |                                                                                                                                                                        |
|                | `name`      | `String`         |                                                                                                                                                                        |
|                | `region`    | `String`         |                                                                                                                                                                        |
| `name`         |             | `String`         | The name of the school.                                                                                                                                                |
| `raw`          |             | `Array [String]` | Raw school name.                                                                                                                                                       |
| `twitter_url`  |             | `String`         | The school's Twitter URL                                                                                                                                               |
| `type`         |             | `Enum (String)`  | The school type. Will be one of our [Canonical School Types](https://docs.peopledatalabs.com/docs/education-school-types).                                             |
| `website`      |             | `String`         | The website URL associated with the school, which could include subdomains.                                                                                            |

#### Example

```json
  "education": [
    {
      "school": {
        "name": "university of oregon",
        "type": "post-secondary institution",
        "id": "64LkgfdwWYkCC2TjbldMDQ_0",
        "location": {
          "name": "eugene, oregon, united states",
          "locality": "eugene",
          "region": "oregon",
          "country": "united states",
          "continent": "north america"
        },
        "linkedin_url": "linkedin.com/school/university-of-oregon",
        "linkedin_id": "19207",
        "facebook_url": "facebook.com/universityoforegon",
        "twitter_url": "twitter.com/uoregon",
        "website": "uoregon.edu",
        "domain": "uoregon.edu",
        "raw": [
          "university of oregon"
        ]
      },
      "end_date": "2014",
      "start_date": "2010",
      "gpa": null,
      "degrees": [],
      "majors": [
        "entrepreneurship"
      ],
      "minors": [],
      "raw": [
        "data analytics & entrepreneurship",
        ", entrepreneurship",
        "entrepreneurship"
      ],
      "summary": "when i was at oregon i volunteered at a local homeless shelter 3 days a week"
    },
  ]
```

## Location

For more information on our standard location fields, see [Common Location Fields](https://docs.peopledatalabs.com/docs/data-formatting#common-location-fields).

### `countries`

<table>
  <tr>
    <th>Description</th>
    <td>All <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">countries</a> associated with the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Enum (String)]</code></td>
  </tr>
</table>

<Callout icon="💡" theme="default">
  ### Sort Order

  Countries are sorted using location sort order, with any duplicate countries removed.

  <LocationSortOrder />
</Callout>

#### Example

```json
  "countries": [
    "united states"
  ]
```

### `location_address_line_2`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">street address line 2</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "location_address_line_2": "apartment 12"
```

### `location_continent`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">continent</a> of the person's current address. One of our <a href="https://docs.peopledatalabs.com/docs/location-continents">Canonical Continents</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "location_continent": "north america"
```

### `location_country`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">country</a> of the person's current address. One of our <a href="https://docs.peopledatalabs.com/docs/location-countries">Canonical Countries</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "location_country": "united states"
```

### `location_geo`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">geo code</a> of the city center of the person's current address.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "location_geo": "37.87,-122.27"
```

### `location_last_updated`

<table>
  <tr>
    <th>Description</th>
    <td>The timestamp that a new data source contributed to the record for the person's current address.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#dates"><code>String (Date)</code></a></td>
  </tr>
</table>

#### Field Details

An update is the time when either new information is added to the record or existing information is validated.

#### Example

```json
  "location_last_updated": "2018-11-05"
```

### `location_locality`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">locality</a> of the person's current address.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "location_locality": "berkeley"
```

### `location_metro`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">metro</a> of the person's current address. One of our <a href="https://docs.peopledatalabs.com/docs/location-metros">Canonical Metros</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Example

```json
  "location_metro": "san francisco, california"
```

### `location_name`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">location</a> of the person's current address.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "location_name": "berkeley, california, united states"
```

### `location_names`

<table>
  <tr>
    <th>Description</th>
    <td>All <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">location names</a> associated with the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

<Callout icon="💡" theme="default">
  ### Sort Order

  Location names are sorted by location order with duplicate names removed

  <LocationSortOrder />
</Callout>

#### Example

```json
  "location_names": [
    "berkeley, california, united states",
    "san francisco, california, united states"
  ]
```

### `location_postal_code`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">postal code</a> of the person's current address.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "location_postal_code": "94704"
```

### `location_region`

<table>
  <tr>
    <th>Description</th>
    <td>The <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">region</a> of the person's current address.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "location_region": "california"
```

### `location_street_address`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">street address</a>.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "location_street_address": "455 fake st"
```

### `regions`

<table>
  <tr>
    <th>Description</th>
    <td>All <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">regions</a> associated with the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

<Callout icon="💡" theme="default">
  ### Sort Order

  Regions are sorted by location order, with any duplicate regions removed.

  <LocationSortOrder />
</Callout>

#### Example

```json
  "regions": [
    "california, united states"
  ]
```

### `street_addresses`

<table>
  <tr>
    <th>Description</th>
    <td>All <a href="https://docs.peopledatalabs.com/docs/data-types#common-location-fields">street addresses</a> associated with the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

Each address associated with the person will be added to this list as its own object.

In addition to the [Common Location Fields](https://docs.peopledatalabs.com/docs/data-types#common-location-fields), `street_addresses` will also include:

| Field         | Data Type                                                                | Description                                                                                           |
| ------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `first_seen`  | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this entity was first associated with the Person record.                                |
| `last_seen`   | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this entity was last associated with the Person record.                                 |
| `num_sources` | `Integer (> 0)`                                                          | The number of sources that have contributed to the association of this entity with the Person record. |

<Callout icon="💡" theme="default">
  ### Sort Order

  Street addresses are sorted by location order.

  <LocationSortOrder />
</Callout>

#### Example

```json
  "street_addresses": [
    {
      "name": "berkeley, california, united states",
      "locality": "berkeley",
      "metro": "san francisco, california",
      "region": "california",
      "country": "united states",
      "continent": "north america",
      "street_address": "455 fake st",
      "address_line_2": "apartment 12",
      "postal_code": "94704",
      "geo": "37.87,-122.27",
      "first_seen": "2017-06-02",
      "last_seen": "2019-07-18",
      "num_sources": 17
    }
  ]
```

## Lower Confidence Data

PDL values high confidence data that is very likely to be associated with a person. The data in these fields have lower confidence than the data used in other fields.

### `possible_birth_dates`

<table>
  <tr>
    <th>Description</th>
    <td>Birthdays associated with this person that have a lower level of confidence.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#dates"><code>Array \[String (Date)]</code></a></td>
  </tr>
</table>

#### Field Details

The dates in this field use the same format as the [`birth_date`](#birth_date) field.

<Callout icon="💡" theme="default">
  ### Sort Order

  Possible birth dates are sorted by `num_sources`, `last_seen`, `first_seen`, `birth_date`, all in reverse order (highest first, most recent first):

  1. `num_sources` (highest first)
  2. `last_seen` (most recent first)
  3. `first_seen` (most recent first)
  4. `birth_date` (most recent first)
</Callout>

#### Example

```json
  "possible_birth_dates": [
    "1991-05-26",
    "1992-05-26"
  ]
```

### `possible_emails`

<table>
  <tr>
    <th>Description</th>
    <td>Email addresses associated with this person that have a lower level of confidence.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

This field uses the same format as the [`emails`](#emails) field.

<Callout icon="💡" theme="default">
  ### Sort Order

  Possible emails are sorted by `last_seen`, `first_seen`, `email`, all in reverse order (most recent first, Z→A):

  1. `last_seen` (most recent first)
  2. `first_seen` (most recent first)
  3. `email` (Z→A)
</Callout>

#### Example

```json
  "possible_emails": [
    {
      "address": "sean@peopledatalabs.com",
      "type": null,
      "first_seen": "2021-06-13",
      "last_seen": "2021-06-13",
      "num_sources": 2
    }
  ]
```

### `possible_location_names`

<table>
  <tr>
    <th>Description</th>
    <td>Locations associated with this person that have a lower level of confidence.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

This field uses the same format as the [`location_names`](#location_names) field.

Possible locations are inferred based on phone area codes, university location, and other associations.

<Callout icon="💡" theme="default">
  ### Sort Order

  Possible locations are sorted by `first_seen`, `last_seen`, `location.name`, all in reverse order (most recent first, Z→A):

  1. `first_seen` (most recent first)
  2. `last_seen` (most recent first)
  3. `location.name` (Z→A)
</Callout>

#### Example

```json
  "possible_location_names": [
    "berkeley, california, united states",
    "san francisco, california, united states"
  ]
```

### `possible_phones`

<table>
  <tr>
    <th>Description</th>
    <td>Phone numbers associated with this person that have a lower level of confidence.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

This field uses the same format as the [`phones`](#phones) field.

<Callout icon="💡" theme="default">
  ### Sort Order

  Possible phones are sorted by `num_sources`, `last_seen`, `first_seen`,  all in reverse order and using the E.164 format (highest first, most recent first):

  1. `num_sources` (highest first)
  2. `last_seen` (most recent first)
  3. `first_seen`(most recent first)
</Callout>

#### Example

```json
  "possible_phones": [
    {
      "number": "+15558675309",
      "first_seen": "2021-06-13",
      "last_seen": "2021-06-13",
      "num_sources": 2
    }
  ]
```

### `possible_profiles`

<table>
  <tr>
    <th>Description</th>
    <td>Social profiles associated with this person that have a lower level of confidence.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

This field uses the same format as the [`profiles`](#profiles) field.

<Callout icon="💡" theme="default">
  ### Sort Order

  Possible profiles are sorted first by return status codes (200 > unknown > 404). The array is then sorted by number of profiles globally, `last_seen`, `first_seen`, `username`, `id`, all in reverse order (highest first, most recent first, Z→A):

  1. Status Codes:
     * Profiles with 200 return status codes are first
     * Profiles with unknown return status codes come next
     * Profiles with 404 return status codes are placed last
  2. Number of profiles globally (highest first)
  3. `last_seen` (most recent first)
  4. `first_seen` (most recent first)
  5. `username` (Z→A)
  6. `id` (Z→A)
</Callout>

#### Example

```json
  "possible_profiles": [
    {
      "network": "linkedin",
      "id": "145991517",
      "url": "linkedin.com/in/seanthorne",
      "username": "seanthorne",
      "first_seen": "2021-06-13",
      "last_seen": "2021-06-13",
      "num_sources": 2
    }
  ]
```

### `possible_street_addresses`

<table>
  <tr>
    <th>Description</th>
    <td>Addresses associated with this person that have a lower level of confidence.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

This field uses the same format as the [`street_addresses`](#street_addresses) field.

<Callout icon="💡" theme="default">
  ### Sort Order

  Possible street addresses are sorted by `first_seen`, `last_seen`, `location.name`, `location.street_address`, `location.address_line_2`, all in reverse order (most recent first, Z→A):

  1. `first_seen` (most recent first)
  2. `last_seen` (most recent first)
  3. `location.name` (Z→A)
  4. `location.street_address` (Z→A)
  5. `location.address_line_2` (Z→A)
</Callout>

#### Example

```json
  "possible_street_addresses": [
    {
      "name": "berkeley, california, united states",
      "locality": "berkeley",
      "metro": "san francisco, california",
      "region": "california",
      "country": "united states",
      "continent": "north america",
      "street_address": "455 fake st",
      "address_line_2": "apartment 12",
      "postal_code": "94704",
      "geo": "37.87,-122.27",
      "first_seen": "2021-06-13",
      "last_seen": "2021-06-13",
      "num_sources": 2
    }
  ]
```

## Social Presence

We currently cover person social profiles on our [Canonical Profile Networks](https://docs.peopledatalabs.com/docs/profile-networks). All profiles we've found for a person will be added to the [`profiles`](#profiles) list.

Each social profile URL has one or more standard formats that we parse and turn into a standard PDL format for that social URL. We invalidate profiles that have non-valid person stubs (for example, `linkedin.com/company`), and we also have a blacklist of usernames that we know are invalid.

We do not validate if a URL is valid (that is, whether you can access it) because doing this at scale is considered a Direct Denial of Service (DDoS) attack and/or a form of crawling. This is highly discouraged! We try to mitigate invalid URLs as much as possible by using Entity Resolution (Merging) to link URLs together and then tagging the primary URL at the top level for key networks.

### `facebook_friends`

<table>
  <tr>
    <th>Description</th>
    <td>The number of Facebook friends the person has.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (>= 0)</code></td>
  </tr>
</table>

#### Example

```json
  "facebook_friends": 3912
```

### `facebook_id`

<table>
  <tr>
    <th>Description</th>
    <td>The person's Facebook profile ID based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "facebook_id": "1089351304"
```

### `facebook_url`

<table>
  <tr>
    <th>Description</th>
    <td>The person's Facebook profile URL based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "facebook_url": "facebook.com/deseanthorne"
```

### `facebook_username`

<table>
  <tr>
    <th>Description</th>
    <td>The person's Facebook profile username based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "facebook_username": "deseanthorne"
```

### `github_url`

<table>
  <tr>
    <th>Description</th>
    <td>The person's GitHub profile URL based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "github_url": "github.com/deseanathan_thornolotheu"
```

### `github_username`

<table>
  <tr>
    <th>Description</th>
    <td>The person's GitHub profile username based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "github_username": "deseanathan_thornolotheu"
```

### `linkedin_connections`

<table>
  <tr>
    <th>Description</th>
    <td>The number of LinkedIn connections the person has.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (>= 0)</code></td>
  </tr>
</table>

#### Field Details

Typically between 0-500.

#### Example

```json
  "linkedin_connections": 432
```

### `linkedin_id`

<table>
  <tr>
    <th>Description</th>
    <td>The person's LinkedIn profile ID. This is null when no values in the "profiles" array are active.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "linkedin_id": "145991517"
```

### `linkedin_url`

<table>
  <tr>
    <th>Description</th>
    <td>The person's current LinkedIn profile URL. This is null when no values in the "profiles" array are active.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "linkedin_url": "linkedin.com/in/seanthorne"
```

### `linkedin_username`

<table>
  <tr>
    <th>Description</th>
    <td>The person's LinkedIn profile username. This is null when no values in the "profiles" array are active.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "linkedin_username": "seanthorne"
```

### `profiles`

<table>
  <tr>
    <th>Description</th>
    <td>Social profiles associated with the person.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

Each profile associated with the person will be added to this list as its own object.

| Field         | Data Type                                                                | Description                                                                                                                                   |
| ------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`          | `String`                                                                 | The profile ID (format varies based on social network).                                                                                       |
| `first_seen`  | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this entity was first associated with the Person record.                                                                        |
| `last_seen`   | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this entity was last associated with the Person record.                                                                         |
| `network`     | `Enum (String)`                                                          | The social network the profile is on. Must be one of our [Canonical Profile Networks](https://docs.peopledatalabs.com/docs/profile-networks). |
| `num_sources` | `Integer (> 0)`                                                          | The number of sources that have contributed to the association of this entity with the Person record.                                         |
| `url`         | `String`                                                                 | The profile URL.                                                                                                                              |
| `username`    | `String`                                                                 | The profile username.                                                                                                                         |

<Callout icon="💡" theme="default">
  ### Sort Order

  Profiles are sorted with the primary profiles listed first (facebook, linkedin, twitter, and github, in that order). The rest of the array is then sorted by status codes (200 > unknown > 404), number of profiles globally, `last_seen`, `first_seen`, `username`, `id`, all in reverse order (highest first, most recent first, Z→A):

  1. Primary profiles first
     1. Facebook
     2. LinkedIn
     3. Twitter
     4. Github
  2. Status Codes:
     * Profiles with 200 return status codes are first
     * Profiles with unknown return status codes come next
     * Profiles with 404 return status codes are placed last
  3. Number of profiles globally (highest first)
  4. `last_seen` (most recent first)
  5. `first_seen` (most recent first)
  6. `username` (Z→A)
  7. `id` (Z→A)
</Callout>

#### Example

```json
  "profiles": [
    {
      "network": "linkedin",
      "id": "145991517",
      "url": "linkedin.com/in/seanthorne",
      "username": "seanthorne",
      "first_seen": "2017-06-02",
      "last_seen": "2019-07-18",
      "num_sources": 17
    }
  ]
```

### `twitter_url`

<table>
  <tr>
    <th>Description</th>
    <td>The person's Twitter profile URL based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "twitter_url": "twitter.com/seanthorne5"
```

### `twitter_username`

<table>
  <tr>
    <th>Description</th>
    <td>The person's Twitter profile username based on source agreement.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Example

```json
  "twitter_username": "seanthorne5"
```

## Work History

### `certifications`

<table>
  <tr>
    <th>Description</th>
    <td>Any certifications the person has.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

The certifications listed are based on user input, we do not verify them.

| Field          | Data Type                                                                | Description                                  |
| -------------- | ------------------------------------------------------------------------ | -------------------------------------------- |
| `end_date`     | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The expiration date of the certification.    |
| `name`         | `String`                                                                 | Certification name                           |
| `organization` | `String`                                                                 | The organization awarding the certification. |
| `start_date`   | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date the certification was awarded.      |

<Callout icon="💡" theme="default">
  ### Sort Order

  Certifications are sorted first by `start_date`, then by `end_date` and finally by `name`, all in reverse order (most recent first, Z→A):

  1. `start_date` (most recent first)
  2. `end_date` (most recent first)
  3. `name` (Z→A)
</Callout>

#### Example

```json
  "certifications": [
    {
      "name": "machine learning certification",
      "organization": "coursera",
      "start_date": "2022-03",
      "end_date": "2023-04"
    }
  ]
```

### `experience`

<table>
  <tr>
    <th>Description</th>
    <td>The person's work experience.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

The experience object that is tagged as `experience.is_primary = True` is copied over to the flattened `job_` fields (see [Current Job](#current-job) and [Current Company](#current-company)).

Each work experience object contains the following fields:

| Field                           | Data Type                                                                | Description                                                                                                             |
| ------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| [`company`](#experiencecompany) | `Object`                                                                 | The company where the person worked.                                                                                    |
| `end_date`                      | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date the person left the company. If the person is still working for the company, will be `null`.                   |
| `first_seen`                    | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this entity was first associated with the Person record.                                                  |
| `last_seen`                     | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this entity was last associated with the Person record.                                                   |
| `is_primary`                    | `Boolean`                                                                | Whether this is the person's current job or not. If `true`, this experience will be used to populate the `job_` fields. |
| `location_names`                | `Array [String]`                                                         | Locations where the person has worked while with this company (if different from the company HQ).                       |
| `num_sources`                   | `Integer (> 0)`                                                          | The number of sources that have contributed to the association of this entity with the Person record.                   |
| `start_date`                    | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date the person started at the company.                                                                             |
| `summary`                       | `String`                                                                 | User-inputted summary of their work experience.                                                                         |
| [`title`](#experiencetitle)     | `Object`                                                                 | The person's job title while at the company.                                                                            |

<Callout icon="💡" theme="default">
  ### Sort Order

  Experience entries are sorted with the primary experience first. The remaining entries are then sorted by `start_date`, `end_date`, `company.name`, and `title.name`, all in reverse order (most recent first, Z→A):

  1. Primary Experience (`is_primary = True` )
  2. `start_date` (most recent first)
  3. `end_date` (most recent first)
  4. `company.name` (Z→A)
  5. `title.name` (Z→A)
</Callout>

##### `experience.company`

The fields in `experience.company` map to the corresponding fields in our [Company Schema](https://docs.peopledatalabs.com/docs/company-schema). The same parsing and formatting logic apply.

| Field          | Sub Field        | Data Type        | Description                                                                                                                                                                                              |
| -------------- | ---------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `facebook_url` |                  | `String`         | The company's [Facebook URL](https://docs.peopledatalabs.com/docs/company-schema#facebook_url)                                                                                                           |
| `founded`      |                  | `Integer (> 0)`  | The [founding year](https://docs.peopledatalabs.com/docs/company-schema#founded) of the company.                                                                                                         |
| `id`           |                  | `String`         | The company's [PDL ID](https://docs.peopledatalabs.com/docs/company-schema#id)                                                                                                                           |
| `industry`     |                  | `Enum (String)`  | The self-identified [industry](https://docs.peopledatalabs.com/docs/company-schema#industry) of the company. Must be one of the [Canonical Industries](https://docs.peopledatalabs.com/docs/industries). |
| `linkedin_id`  |                  | `String`         | The company's [LinkedIn ID](https://docs.peopledatalabs.com/docs/company-schema#linkedin_id)                                                                                                             |
| `linkedin_url` |                  | `String`         | The company's [LinkedIn URL](https://docs.peopledatalabs.com/docs/company-schema#linkedin_url)                                                                                                           |
| `location`     |                  | `Object`         | The location of the company's headquarters. See [Common Location Fields](https://docs.peopledatalabs.com/docs/data-types#common-location-fields) for detailed field descriptions.                        |
|                | `address_line_2` | `String`         |                                                                                                                                                                                                          |
|                | `continent`      | `Enum (String)`  |                                                                                                                                                                                                          |
|                | `country`        | `Enum (String)`  |                                                                                                                                                                                                          |
|                | `geo`            | `String`         |                                                                                                                                                                                                          |
|                | `locality`       | `String`         |                                                                                                                                                                                                          |
|                | `metro`          | `Enum (String)`  |                                                                                                                                                                                                          |
|                | `name`           | `String`         |                                                                                                                                                                                                          |
|                | `postal_code`    | `String`         |                                                                                                                                                                                                          |
|                | `region`         | `String`         |                                                                                                                                                                                                          |
|                | `street_address` | `String`         |                                                                                                                                                                                                          |
| `name`         |                  | `String`         | The [company name](https://docs.peopledatalabs.com/docs/company-schema#name), cleaned and standardized.                                                                                                  |
| `raw`          |                  | `Array [String]` | Raw company name.                                                                                                                                                                                        |
| `size`         |                  | `Enum (String)`  | The self-reported [company size range](https://docs.peopledatalabs.com/docs/company-schema#size). Must be one of our [Canonical Company Sizes](https://docs.peopledatalabs.com/docs/company-sizes).      |
| `ticker`       |                  | `String`         | The [company ticker](https://docs.peopledatalabs.com/docs/company-schema#type). This field will only have a value if the company's `type` is `public`.                                                   |
| `twitter_url`  |                  | `String`         | The company's [Twitter URL](https://docs.peopledatalabs.com/docs/company-schema#twitter_url)                                                                                                             |
| `type`         |                  | `Enum (String)`  | The [company type](https://docs.peopledatalabs.com/docs/company-schema#type). Must be one of our [Canonical Company Types](https://docs.peopledatalabs.com/docs/company-types).                          |
| `website`      |                  | `String`         | The company's [primary website](https://docs.peopledatalabs.com/docs/company-schema#website), cleaned and standardized.                                                                                  |

##### `experience.title`

See the corresponding [Current Job](#current-job) fields for more details on the information included and formatting of these fields.

| Field      | Data Type               | Description                                                                                          |
| ---------- | ----------------------- | ---------------------------------------------------------------------------------------------------- |
| `levels`   | `Array [Enum (String)]` | [Canonical Job Title Levels](https://docs.peopledatalabs.com/docs/job-title-levels).                 |
| `name`     | `String`                | The cleaned job title.                                                                               |
| `raw`      | `Array [String]`        | Raw job title input.                                                                                 |
| `role`     | `Enum (String)`         | One of the [Canonical Job Roles](https://docs.peopledatalabs.com/docs/job-title-roles).              |
| `sub_role` | `Enum (String)`         | One of the [Canonical Job Sub Roles](https://docs.peopledatalabs.com/docs/job-title-subroles).       |
| `class`    | `Enum (String)`         | One of the [Canonical Job Classes](https://docs.peopledatalabs.com/docs/job-title-class-post-v271) . |

<Callout icon="💡" theme="default">
  ### Sort Order (`experience.title.levels`)

  Title levels are sorted from most important to least important based on the following ranking:

  1. `cxo` (first)
  2. `owner`
  3. `vp`
  4. `director`
  5. `partner`
  6. `senior`
  7. `manager`
  8. `entry`
  9. `training`
  10. `unpaid` (last)
</Callout>

#### Example

```json
  "experience": [
    {
      "company": {
        "name": "people data labs",
        "size": "11-50",
        "id": "peopledatalabs",
        "founded": 2015,
        "industry": "computer software",
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
        },
        "linkedin_url": "linkedin.com/company/peopledatalabs",
        "linkedin_id": "18170482",
        "facebook_url": "facebook.com/peopledatalabs",
        "twitter_url": "twitter.com/peopledatalabs",
        "website": "peopledatalabs.com",
        "ticker": null,
        "type": "private",
        "raw": [
          "people data labs"
        ],
      },
      "location_names": ["san francisco, california, united states"],
      "end_date": null,
      "start_date": "2015-03",
      "title": {
        "name": "chief executive officer and co-founder",
        "raw": [
          "co-founder &amp; ceo",
          "co-founder & ceo",
          "co-founder and chief executive officer"
        ],
        "role": "operations",
        "sub_role": "executive",
        "class": "general_and_administrative"
        "levels": [
          "cxo",
          "owner"
        ],
      },
      "is_primary": true,
      "summary": "worked on the \"search analytics\" team to understand our users better",
      "first_seen": "2018-10-11",
      "last_seen": "2022-11-15",
      "num_sources": 17
    },
  ]
```

### `headline`

<table>
  <tr>
    <th>Description</th>
    <td>The brief headline associated with a person profile.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The self-written headline tied to the person profile (often a LinkedIn headline).

The summary is lowercased, but otherwise kept as-is from the raw source.

#### Example

```json
  "headline": "senior data engineer at people data labs"
```

### `industry`

<table>
  <tr>
    <th>Description</th>
    <td>The most relevant industry for this person based on their work history.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Enum (String)</code></td>
  </tr>
</table>

#### Field Details

A person's industry is determined based on their tagged personal industries and the industries of the companies that they have worked for.

The value will be one of our [Canonical Industries](https://docs.peopledatalabs.com/docs/industries).

#### Example

```json
  "industry": "computer software"
```

### `inferred_years_experience`

<table>
  <tr>
    <th>Description</th>
    <td>The person's inferred years of total work experience.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (0 - 100)</code></td>
  </tr>
</table>

#### Field Details

The value will be between 0 and 100.

#### Example

```json
  "inferred_years_experience": 7
```

### `interests`

<table>
  <tr>
    <th>Description</th>
    <td>The person's self-reported interests.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

Each interest is cleaned (lowercased, stripped of whitespace, etc.). We don't have a canonical list of interests but we remove profanity and do some basic cleaning.

<Callout icon="💡" theme="default">
  ### Sort Order

  Interests are sorted alphabetically (from A→Z)
</Callout>

#### Example

```json
  "interests": [
    "data",
    "software"
  ]
```

### `job_history`

<table>
  <tr>
    <th>Description</th>
    <td>Additional professional positions that may have been removed or changed on resumes.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[Object]</code></td>
  </tr>
</table>

#### Field Details

Any additional job history information PDL has that is not included in the [`experience`](#experience) field.

Usually these are positions that have been removed or changed on resumes.

| Field          | Data Type                                                                | Description                                                                                      |
| -------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| `company_id`   | `String`                                                                 | [PDL Company ID](https://docs.peopledatalabs.com/docs/company-schema#id)                         |
| `company_name` | `String`                                                                 | [Company Name](https://docs.peopledatalabs.com/docs/company-schema#name)                         |
| `first_seen`   | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this experience was first associated with this record.                             |
| `last_seen`    | [`String (Date)`](https://docs.peopledatalabs.com/docs/data-types#dates) | The date that this experience was last associated with this record.                              |
| `num_sources`  | `Integer (> 0)`                                                          | The number of sources that have contributed to the association of this profile with this record. |
| `title`        | `String`                                                                 | [Job Title](#job_title) at this company.                                                         |

<Callout icon="💡" theme="default">
  ### Sort Order

  Job history entries are sorted by `start_date`, `end_date`, `company.name`, and `title.name`, all in reverse order (most recent first, Z→A):

  1. `start_date` (most recent first)
  2. `end_date` (most recent first)
  3. `company.name` (Z→A)
  4. `title.name` (Z→A)
</Callout>

#### Example

```json
  "job_history": [
    {
      "company_id": "OMdETRug8CpuRDWGkhQ35wx8CvVk",
      "company_name": "auntie annes",
      "title": "food service supervisor",
      "first_seen": "2016-05-17",
      "last_seen": "2020-05-30",
      "num_sources": 12
    }
  ]
```

### `skills`

<table>
  <tr>
    <th>Description</th>
    <td>The person's self-reported skills.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Array \[String]</code></td>
  </tr>
</table>

#### Field Details

Each skill is cleaned (lowercased, stripped of whitespace, etc.). We do not always strip punctuation because it can be relevant for some skills (ex: `"c++"` vs `"c"`).

We do not do any canonicalization, so `"java"` and `"java 8.0"` are considered separate skills. For this reason, we encourage our customers to use fuzzy text matching with the `skills` field.

<Callout icon="💡" theme="default">
  ### Sort Order

  Skills are sorted alphabetically (from A→Z)
</Callout>

#### Example

```json
  "skills": [
    "entrepreneurship"
  ]
```

### `summary`

<table>
  <tr>
    <th>Description</th>
    <td>User-inputted personal summary.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

The self-written summary tied to the person profile (often a LinkedIn summary).

The summary is lowercased, but otherwise kept as-is from the raw source.

#### Example

```json
  "summary": "growth-hacker and digital nomad"
```

***

# PDL Record Information & Metadata

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

This field currently exists in [Person Enrichment API](https://docs.peopledatalabs.com/docs/person-enrichment-api) responses.

Note: This number corresponds to the [data release number](https://docs.peopledatalabs.com/changelog), not the API release number.

#### Example

```json
  "dataset_version": "19.2"
```

### `first_seen`

<table>
  <tr>
    <th>Description</th>
    <td>The date when this record was first created in our data.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><a href="https://docs.peopledatalabs.com/docs/data-types#dates"><code>String (Date)</code></a></td>
  </tr>
</table>

#### Example

```json
  "first_seen": "2017-06-02"
```

### `num_records`

<table>
  <tr>
    <th>Description</th>
    <td>The number of unique raw records contributing to this specific PDL profile.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (> 0)</code></td>
  </tr>
</table>

#### Example

```json
  "num_records": 420
```

### `num_sources`

<table>
  <tr>
    <th>Description</th>
    <td>The number of unique sources contributing to this specific PDL profile.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>Integer (> 0)</code></td>
  </tr>
</table>

#### Example

```json
  "num_sources": 72
```

### operation\_id

<table>
  <tr>
    <th>Description</th>
    <td>An identifier for an operation in a Data License delivery, used for troubleshooting.</td>
  </tr>

  <tr>
    <th>Data Type</th>
    <td><code>String</code></td>
  </tr>
</table>

#### Field Details

This field exists only in [Data License](https://docs.peopledatalabs.com/docs/data-license) deliveries, and allows PDL employees to identify the timestamp and operations performed on the internal data in order to return a record in a delivery.

#### Example

```json
  "operation_id": "acee3bde2e1a2cb7e75c57b80d5b7bc2d5de5b02e7ea51f91304c28df77251dc"
```

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