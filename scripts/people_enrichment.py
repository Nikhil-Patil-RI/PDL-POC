import json

from peopledatalabs import PDLPY

# Create a client, specifying your API key
CLIENT = PDLPY(
    api_key="03e3bfc62ab0429ca47f85407fbfd3df3bd35c3644eb616c2688ef33d932aea9",
)

# Create a parameters JSON object
PARAMS = {"company": "people data labs", "pdl_id": "M4lBKgWVh1SxhtBsrksSVw_0000"}

# Pass the parameters object to the Person Enrichment API
json_response = CLIENT.person.enrichment(**PARAMS).json()

# Check for successful response
if json_response["status"] == 200:
    record = json_response["data"]

    # Print selected fields
    print(
        record["work_email"],
        record["full_name"],
        record["job_title"],
        record["job_company_name"],
    )

    print(f"Successfully enriched profile with PDL data.")

    # Save enrichment data to JSON file
    with open("my_pdl_enrichment.jsonl", "w") as out:
        out.write(json.dumps(record) + "\n")
else:
    print("Enrichment unsuccessful. See error and try again.")
    print("error:", json_response)
