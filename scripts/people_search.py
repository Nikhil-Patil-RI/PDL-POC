import requests, json

# Set your API key
API_KEY = "eb5fd98c3bb01250388c9a75f6aab8d6b8479b8a7c19e31ef8e4f51e9e77adde"

# Set the Person Search API URL
PDL_URL = "https://api.peopledatalabs.com/v5/person/search"

# Set headers
HEADERS = {"Content-Type": "application/json", "x-api-key": API_KEY}

# Create a parameters JSON object
PARAMS = {
    "sql": "SELECT * FROM person WHERE linkedin_url ='linkedin.com/in/nikhil-patil1008'"
}

# Pass the parameters object to the Person Search API
response = requests.get(PDL_URL, headers=HEADERS, params=PARAMS).json()

# Check for successful response
if response["status"] == 200:
    data = response["data"]
    # Write out each profile found to file
    with open("my_pdl_search.jsonl", "w") as out:
        for record in data:
            out.write(json.dumps(record) + "\n")
    print(f"Successfully grabbed {len(data)} records from PDL.")
    print(f"{response['total']} total PDL records exist matching this query.")
else:
    print(
        "NOTE: The carrier pigeons lost motivation in flight. See error and try again."
    )
    print("Error:", response)
