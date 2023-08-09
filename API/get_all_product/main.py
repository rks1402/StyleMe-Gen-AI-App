from flask import Flask, request, jsonify
from google.cloud import datastore
import json

app = Flask(__name__)

@app.route('/get_by_gender', methods=['GET'])
def get_record_by_gender_category():
    try:
        # Get the product_id from the query parameters in the HTTP request
        gender = request.args.get('gender')

        if not gender:
            return "gender category not provided.", 400

        # Create a Datastore client
        client = datastore.Client()

        # Define the kind from which you want to fetch the records
        kind = "MasterData"

        # Create a query to fetch the record with the specified product_id
        query = client.query(kind=kind)
        query.add_filter('gender', '=', gender)

        # Fetch the entities that match the query
        results = list(query.fetch())

        if not results:
            return f"No record found with Product ID: {gender}", 404

        # Convert the entity to a dictionary
        records = [dict(result) for result in results]

        # Return the JSON response
        return json.dumps(records)

        
       
    except Exception as e:
        error_message = f"Error occurred: {e}"
        return jsonify(error=error_message), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
