

# Reference - Company Search API

The Company Search API is perfect for finding specific segments of companies that you need to power your projects and products. It gives you direct access to our full [Company Dataset](https://docs.peopledatalabs.com/docs/company-fields). There are many degrees of freedom, which allow you to find any kind of company with a single query.

# Endpoint

The endpoint for the Company Search API is `https://api.peopledatalabs.com/v5/company/search`.

# Company Search API Access and Billing

We charge **per record retrieved**. Each company record in the `data` array in the response counts as one credit against your total package.

# Requests

See [Authentication](https://docs.peopledatalabs.com/docs/authentication) and [Requests](https://docs.peopledatalabs.com/docs/requests) to learn how to input requests. We recommend using a JSON object to capture request parameters and will do so in the examples.

# Rate Limiting

The current default rate limit is 10 requests per minute.

# Input Parameters

> 📘 For More Details, See [Input Parameters - Company Search API](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api)
>
> You can also click on the individual parameter names in the table below to view more information on them.

| Parameter Name                                                                                          | Description                                                                                                                                                                                                                                                                                                                                                                     | Default | Example                                               |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ----------------------------------------------------- |
| [`query`](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api#query)               | An [Elasticsearch (v7.7) query](https://www.elastic.co/guide/en/elasticsearch/reference/7.7/query-dsl.html). See our underlying [Elasticsearch mapping](#full-field-mapping) for reference.                                                                                                                                                                                     |         | `{"query": {"term": {"name": "people data labs"}}}`   |
| [`sql`](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api#sql)                   | An SQL query of the format: `SELECT * FROM company WHERE XXX`, where XXX is a standard SQL boolean query involving our [company fields](https://docs.peopledatalabs.com/docs/company-fields). We will ignore any use of column selections or the LIMIT keyword.                                                                                                                                                  |         | `SELECT * FROM company WHERE name='people data labs'` |
| [`size`](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api#size)                 | The batch size or the maximum number of matched records to return for this query if they exist. Must be between `1` and `100`.                                                                                                                                                                                                                                                  | `1`     | `100`                                                 |
| [`from`](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api#from)                 | **\[LEGACY] The `from` field is not recommended for use and will not be supported long term. Use the `scroll_token` field instead** An offset value for paginating between batches, which can be a number between `0` and `9999`. We will execute pagination for a maximum of 10,000 records per query. **NOTE: YOU CANNOT USE `FROM` WITH `SCROLL_TOKEN` IN THE SAME REQUEST**. | `0`     | `0`, `100`, `200` ...                                 |
| [`scroll_token`](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api#scroll_token) | An offset key for paginating between batches. Unlike the legacy `from`, you can use this parameter for any number of records. Each Company Search API response returns a `scroll_token`, which you can use to fetch the next `size` records.                                                                                                                                    | `None`  | `104$14.278746`                                       |
| [`titlecase`](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api#titlecase)       | All text in API responses returns as lowercase by default. Setting `titlecase` to `true` will titlecase the person data in `200` responses.                                                                                                                                                                                                                                     | `false` | `true`                                                |
| [`pretty`](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api#pretty)             | Whether the output should have [human-readable](http://jsonprettyprint.net/) indentation.                                                                                                                                                                                                                                                                                       | `false` | `true`                                                |
| [`api_key`](https://docs.peopledatalabs.com/docs/input-parameters-company-search-api#api_key)           | Your secret API key (**Note**: you can also provide this in the request header instead, as shown on the [Authentication](https://docs.peopledatalabs.com/docs/authentication) page).                                                                                                                                                                                                                             |         |                                                       |

# Output Response

We will return an HTTP response code of `200` for any valid request, regardless of whether records were found for your query or not. For that reason, pay close attention to the `total` value in your response object to understand query success. Each company record in the `data` array of the response counts as a single credit against your total package. The responses in the output are sorted by profile completeness.

## Response Fields

> 📘 For More Details, See [Output Response - Company Search API](https://docs.peopledatalabs.com/docs/output-response-company-search-api)
>
> You can also click the field names in the table below to view more information as well.

| Field                                                                                                  | Description                                                                                                            | Type             |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ---------------- |
| [`status`](https://docs.peopledatalabs.com/docs/output-response-company-search-api#status)             | The response code. See a description of our [error codes](errors).                                                     | `Integer`        |
| [`data`](https://docs.peopledatalabs.com/docs/output-response-company-search-api#data)                 | The company response objects that match the input query (see the [example company record](https://docs.peopledatalabs.com/docs/example-company-record). | `Array (Object)` |
| [`total`](https://docs.peopledatalabs.com/docs/output-response-company-search-api#total)               | The number of records matching a given `query` or `sql` input.                                                         | `Integer`        |
| [`scroll_token`](https://docs.peopledatalabs.com/docs/output-response-company-search-api#scroll_token) | The scroll value, which you can use for further pagination.                                                            | `String`         |

## Response Data Structure

The response from the Company Search API will be in this format:

```json
{
    "status": 200,
    "data": [
        {
          "id": "tnHcNHbCv8MKeLh92946LAkX6PKg",
          "name": "people data labs",
          ...
        },
        ...
    ],
    "total": 6,
    "scroll_token": "13.312621$543927"
}
```

See [Example Company Record](https://docs.peopledatalabs.com/docs/example-company-record) for a full example of the fields included in the `data` object.

## Errors

If the request encounters an error, it will instead return an Error Response in the format described in [Errors](https://docs.peopledatalabs.com/docs/errors).

# Full Field Mapping

See [Elasticsearch Mapping](https://docs.peopledatalabs.com/docs/elasticsearch-mapping-company).

# All Data Field Descriptions

See [Company Schema](https://docs.peopledatalabs.com/docs/company-schema).