from flask import Flask, request, jsonify
from google.cloud import datastore
import json

app = Flask(__name__)

@app.route('/get_record', methods=['GET'])
def get_record_by_product_id():
    try:
        # Get the product_id from the query parameters in the HTTP request
        product_id = request.args.get('product_id')

        if not product_id:
            return "Product ID not provided.", 400

        # Create a Datastore client
        client = datastore.Client()

        # Define the kind from which you want to fetch the records
        kind = "MasterData"

        # Create a query to fetch the record with the specified product_id
        query = client.query(kind=kind)
        query.add_filter('product_ID', '=', product_id)

        # Fetch the entities that match the query
        results = list(query.fetch())

        if not results:
            return f"No record found with Product ID: {product_id}", 404

        # Convert the entity to a dictionary
        record = dict(results[0])

        # Return the JSON response
        return jsonify(record)
       
    except Exception as e:
        error_message = f"Error occurred: {e}"
        return jsonify(error=error_message), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
