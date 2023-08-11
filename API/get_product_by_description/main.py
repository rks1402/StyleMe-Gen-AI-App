from flask import Flask, request, jsonify
from google.cloud import datastore
from google.oauth2 import service_account
import json

app = Flask(__name__)


@app.route('/get_product_by_description', methods=['GET'])
def get_product_by_description():
    try:
        search_query = request.args.get('query')

        if not search_query:
            return "Search query not provided.", 400

        client = datastore.Client()
        kind = "MasterData"

        # Fetch all records from the Datastore
        all_records = list(client.query(kind=kind).fetch())

        matching_records = []

        # Iterate through each record and apply matching logic
        for record in all_records:
            if all(
                term in record['color'].lower() or
                term in record['material'].lower() or
                term in record['product_category'].lower() or
                term in record['ocassion'].lower() or
                term in record['fit'].lower() or
                term in record['pattern'].lower() or
                term in record['gender'].lower() or
                term in record['brand'].lower() or
                term in record['description'].lower() or
                term in record['product_name'].lower()
                for term in search_query.split()
            ):
                matching_records.append(record)

        if not matching_records:
            return f"No matching products found for query: {search_query}", 404

        records = [dict(result) for result in matching_records]
        return json.dumps(records)

    except Exception as e:
        error_message = f"Error occurred: {e}"
        return jsonify(error=error_message), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
