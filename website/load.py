'''from google.cloud import datastore

def delete_all_entities(project_id, kind):
    client = datastore.Client(project_id)
    query = client.query(kind=kind)

    # Retrieve all keys for the specified kind
    keys = [entity.key for entity in query.fetch()]

    # Delete entities in batches of 500 to avoid request size limit
    batch_size = 500
    for i in range(0, len(keys), batch_size):
        batch = client.delete_multi(keys[i:i+batch_size])

    print(f"All entities of kind '{kind}' have been deleted.")

if __name__ == "__main__":
    project_id = "bigquery-390709"  # Replace with your GCP project ID
    kind = "product"  # Replace with the kind name of the entities you want to delete

    delete_all_entities(project_id, kind)
'''
import requests
import json

# Define the URL of your Flask API
api_url = "https://qnamagazine-hmvyexj3oa-el.a.run.app/ask"  # Replace with the actual URL if different

# Define the request data as a Python dictionary
data = {
    "question": "What is the capital of France?",
    "article": "Paris is the capital of France.",
    "articles": "Some additional text."
}

# Convert the data to JSON format
headers = {'Content-type': 'application/json'}
json_data = json.dumps(data)

try:
    # Send a POST request to the API
    response = requests.post(api_url, data=json_data, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        answer = response_data.get('answer', 'No answer received.')

        # Print the answer
        print(f"Answer from API: {answer}")
    else:
        print(f"Request failed with status code {response.status_code}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
