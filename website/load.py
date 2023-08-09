from google.cloud import datastore

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
