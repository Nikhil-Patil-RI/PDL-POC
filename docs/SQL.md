

# Input Parameters - Person Search API

## Required Parameters

You **must** provide either the [`query`](#query) or the [`sql`](#sql) parameter (but not both) to receive a successful response. We recommend using the Elasticsearch `query` parameter for most use cases.

When you execute an API request, the query runs directly against our [Person Dataset](https://docs.peopledatalabs.com/docs/stats) without any cleaning or preprocessing. This means that you have a *lot* of freedom to explore the dataset and return the perfect records for your particular use case. It also means that you will need to understand the available fields to make successful queries.

Use the field descriptions on the [Person Schema](https://docs.peopledatalabs.com/docs/fields) and the underlying [Elasticsearch Mapping](https://docs.peopledatalabs.com/docs/elasticsearch-mapping) to help write better queries.

To help you identify how to best query for specific sub-entities (schools, companies, and locations), we offer a suite of [Cleaner APIs](https://docs.peopledatalabs.com/docs/cleaner-apis).

We also provide a free [Query Builder Tool](https://docs.peopledatalabs.com/docs/query-builder-tool) to help write and test Elasticsearch queries for our Search APIs.

### `api_key`

| Type     | Description          | Default | Example |
| :------- | :------------------- | :------ | :------ |
| `String` | Your secret API key. |         |         |

Your API Key **must** be included in either the request header or the `api_key` parameter. For more information about request authentication, see the [Authentication](https://docs.peopledatalabs.com/docs/authentication) page.

***

## Optional Parameters

### `query`

| Type     | Description                                                                                                                                                                                                                                        | Example                                                   |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------- |
| `Object` | An [Elasticsearch (v7.7) query](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl.html) involving our [person fields](https://docs.peopledatalabs.com/docs/fields).  \n  \nSee our underlying [Elasticsearch Mapping](https://docs.peopledatalabs.com/docs/elasticsearch-mapping) for reference. | `"query": "term": "job_company_name": "people data labs"` |

#### **Elasticsearch Query Limitations**

The `query` value should align directly with the [Elasticsearch DSL](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl.html).

We accept the following Elasticsearch query types:

* [term](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-term-query.html)
* [terms](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-terms-query.html)
* [exists](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-exists-query.html)
* [bool](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-bool-query.html)
* [match](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-match-query.html)
* [range](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-range-query.html)
* [match\_phrase](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-match-query-phrase.html)
* [wildcard](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-wildcard-query.html)
* [prefix](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-prefix-query.html)
* [match\_all](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl-match-all-query.html)

We've disabled most specialized options, such as boosting and custom scoring, and we do not allow aggregations.

Any array in a query (such as a `terms` array) will have a hard limit of 1000 elements. If a request goes over this limit, it will fail.

### `sql `

| Type     | Description                                                                                                                                       | Example                                                          |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------- |
| `String` | A SQL query of the format: `SELECT * FROM person WHERE XXX`, where XXX is a standard SQL boolean query involving our [person fields](https://docs.peopledatalabs.com/docs/fields). | `SELECT * FROM person WHERE job_company_name='people data labs'` |

#### **SQL Query Limitations**

We execute SQL queries using [Elasticsearch SQL](https://www.elastic.co/what-is/elasticsearch-sql).

We accept any SQL query that translates to the [above Elasticsearch query types](#elasticsearch-query-limitations) through the [ES SQL translate API](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/sql-translate.html).

We will ignore any use of column selections or the `LIMIT` keyword.

We limit the number of wildcard terms (using `LIKE` with `%`) to 20 per request. If a request goes over this limit, it will fail.

You must use subfields rather than top-level fields when making SQL queries. For example, `SELECT * FROM person WHERE experience IS NOT NULL` will fail but `SELECT * FROM person WHERE experience.title.name IS NOT NULL` will behave as expected.

### `size`

| Type      | Description                                                                                                  | Default | Example |
| :-------- | :----------------------------------------------------------------------------------------------------------- | :------ | :------ |
| `Integer` | The maximum number of matched records to return for this query if they exist. Must be between `1` and `100`. | `1`     | `100`   |

### `scroll_token`

| Type     | Description                                                                                                                  | Default | Example         |
| :------- | :--------------------------------------------------------------------------------------------------------------------------- | :------ | :-------------- |
| `String` | Each search API response returns a `scroll_token`. Include it in the next request to fetch the next `size` matching records. |         | `104$14.278746` |

A `scroll_token` returns in every [Person Search API response](https://docs.peopledatalabs.com/docs/output-response-person-search-api#scroll_token) and serves as a placeholder or bookmark for the last record received. For queries with more results than can fit in a single API response (see the [`size`](#size) field), use the `scroll_token` to get the next batch of results.

For example, if you send a query to the Person Search API that has 10,000 matches, you will need multiple API calls to retrieve all the records. The `scroll_token` represents how far along you are in that list of records.

Generally, the way to use `scroll_token` is:

1. Send a query to the Person Search API.
2. Get a response back containing one batch of records as well as a `scroll_token` response value (if you have already retrieved all the available records in this batch, then the `scroll_token` value will be `null`).
3. Use the same query from Step 1 and the `scroll_token` you just received to make another request to the Person Search API.
4. Get another response back with the next batch of records and a new `scroll_token` value.
5. Repeat steps 3 and 4 until you have received the desired number of records or until you receive a 404 status code because pagination is complete and the `scroll_token` key is missing from the response.

For a detailed working example of this process, see the following code example: [Bulk Retrieval](https://docs.peopledatalabs.com/docs/examples-person-search-api#bulk-retrieval).

### `dataset`

| Type            | Description                                                                                      | Default  | Example |
| :-------------- | :----------------------------------------------------------------------------------------------- | :------- | :------ |
| `Enum (String)` | Specifies which [dataset(s)](https://docs.peopledatalabs.com/docs/datasets#list-of-slice-datasets) the API should search against. | `resume` | `all`   |

You can input multiple datasets by separating each with a comma.

Valid dataset names are:

* `all`
* `resume`
* `email`
* `phone`
* `mobile_phone`
* `street_address`
* `consumer_social`
* `developer`

See [Person Stats](https://docs.peopledatalabs.com/docs/datasets) for details about each dataset.

You can exclude dataset(s) by using `-` as the first character. Entering `-` will exclude all of the comma-separated datasets following the character and needs to be entered only once. For example, `"all,-phone,consumer_social"` will include search results from every dataset except the phone and consumer\_social datasets.

### `titlecase`

| Type      | Description                                                                                                                           | Default | Example |
| :-------- | :------------------------------------------------------------------------------------------------------------------------------------ | :------ | :------ |
| `Boolean` | All text in API responses returns as lowercase by default. Setting `titlecase` to `true` will titlecase any records returned instead. | `false` | `true`  |

### `data_include`

| Type     | Description                                                               | Default | Example                      |
| :------- | :------------------------------------------------------------------------ | :------ | :--------------------------- |
| `String` | A comma-separated string of fields that you want the response to include. |         | `"full_name,emails.address"` |

### `pretty`

| Type      | Description                                                                               | Default | Example |
| :-------- | :---------------------------------------------------------------------------------------- | :------ | :------ |
| `Boolean` | Whether the output should have [human-readable](http://jsonprettyprint.net/) indentation. | `false` | `true`  |