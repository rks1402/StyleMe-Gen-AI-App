from flask import Flask, request, jsonify
from google.cloud import datastore
from google.oauth2 import service_account

app = Flask(__name__)

# Replace with the path to your JSON key file
key_file = 'secret/credentials.json'
credentials = service_account.Credentials.from_service_account_file(key_file)
client = datastore.Client(credentials=credentials)

@app.route('/products', methods=['GET'])
def get_products():
    # Get the occasion parameter from the request arguments
    ocassion = request.args.get('ocassion')
    if not ocassion:
        return jsonify({'error': 'Missing occasion parameter'}), 400

    # Query the GCP Datastore for products with the given occasion
    query = client.query(kind='MasterData')
    query.add_filter('ocassion', '=', ocassion)
    results = list(query.fetch())

    # Return the results as a JSON object
    return jsonify({'products': results})

if __name__ == '__main__':
    app.run()
