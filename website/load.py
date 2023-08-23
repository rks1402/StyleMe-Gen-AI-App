"""from google.cloud import datastore

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

    delete_all_entities(project_id, kind)"""

import requests

# Replace this with your deployed Cloud Run URL
API_URL = "https://summary-iqcjxj5v4a-el.a.run.app/summarize"

# Test GET request
response_get = requests.get(API_URL)
print("GET Response:")
print(response_get.text)
print("-" * 30)

# Test POST request
prompt = "FashionAssistant: Welcome! How can I assist you today? User: Hi there! I need some fashion advice for an upcoming job interview. FashionAssistant: Absolutely, Id be delighted to help you find the perfect outfit for your job interview. Could you tell me more about the job interview? User: Its a job interview at a corporate office, so I need a formal outfit. FashionAssistant: Thank you for sharing. To provide you with the best suggestions, could you please share your budget or the price range youre comfortable with for the outfit? User: Im looking for something around $150 to $200. FashionAssistant: Got it, thank you for letting me know. And to help you better, do you prefer classic and elegant styles, or do you like to incorporate modern trends as well? User: I usually lean towards classic and elegant styles. FashionAssistant: Wonderful, thank you! For a corporate job interview, a well-tailored suit or a polished dress would be perfect. Are you thinking of wearing a suit or a dress for the interview? User: Im considering a suit. FashionAssistant: Great choice! A suit exudes professionalism. What color palette are you considering for the suit—classic black, navy, or something else? User: Im thinking of a charcoal gray suit. FashionAssistant: Charcoal Gray is an excellent choice—sophisticated and versatile. Do you prefer a pantsuit or a skirt suit? User: A pantsuit, please. FashionAssistant: Also, to ensure the perfect fit, could you share your size preferences & measurements, or dress size? User: My measurements are [provide measurements] and I wear size S. Give the User Occasion and demographics from this conversation in JSON format."
data = {"content": prompt}

response_post = requests.post(API_URL, json=data)
if response_post.status_code == 200:
    response_data = response_post.json()
    summary = response_data.get("summary", "No summary available.")
    print("POST Response - Summary:")
    print(summary)
else:
    print("POST Request Failed!")
    print(response_post.text)

