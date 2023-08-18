from flask import Flask, request, jsonify
from google.cloud import datastore
import json


app = Flask(__name__)


@app.route('/product/ocassion', methods=['GET'])
def get_products():
    client = datastore.Client()
    # Get the occasion parameter from the request arguments
    ocassion = request.args.get('ocassion')
    if not ocassion:
        return jsonify({'error': 'Missing occasion parameter'}), 400

    # Query the GCP Datastore for products with the given occasion
    query = client.query(kind='MasterData')
    query.add_filter('ocassion', '=', ocassion)
    results = list(query.fetch())

    if not results:
        return "No records found.", 404

        # Convert the entities to a list of dictionaries
    records = [dict(result) for result in results]

        # Return the JSON response
    return json.dumps(records)

if __name__ == '__main__':
    app.run()