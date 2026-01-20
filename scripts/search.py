import json
import os
from dotenv import load_dotenv

load_dotenv()

from peopledatalabs import PDLPY

# Create a client, specifying your API key
CLIENT = PDLPY(
    api_key=os.getenv("PDL_KEY"),
)

# Create a parameters JSON object
PARAMS = {
    "sql": "SELECT * FROM company WHERE industry='computer software'",
    "size": "1",
    "pretty": True,
    "titlecase": True
}

# Pass the parameters object to the Company Search API
response = CLIENT.company.search(**PARAMS).json()

# Check for successful response
if response["status"] == 200:
  data = response['data']
  # Write out each profile found to file
  with open("my_pdl_search.json", "w") as out:
    for record in data:
      out.write(json.dumps(record) + "\n")
  print(f"Successfully grabbed {len(data)} records from PDL.")
  print(f"{response['total']} total PDL records exist matching this query.")
else:
  print("NOTE: The carrier pigeons lost motivation in flight. See error and try again.")
  print("Error:", response)