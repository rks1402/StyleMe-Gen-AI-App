from flask import Flask, request, jsonify
from google.cloud import datastore
import vertexai
from vertexai.language_models import TextGenerationModel
import json

app = Flask(__name__)

@app.route('/service/product/gender', methods=['GET'])
def get_product_by_gender():
    try:
        # Get the product_id from the query parameters in the HTTP request
        gender = request.args.get('gender')

        if not gender:
            return "gender value not provided.", 400
        
        # Input validation to be added!

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
            return f"No record found for requested gender: {gender}", 404

        # Convert the entity to a dictionary
        records = [dict(result) for result in results]

        # Return the JSON response with response code to be added!
        return json.dumps(records)

       
    except Exception as e:
        error_message = f"Error occurred: {e}"
        return jsonify(error=error_message), 500


@app.route('/service/product/id', methods=['GET'])
def get_product_by_id():
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


@app.route('/service/product/description', methods=['GET'])
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
            search_query_words = search_query.lower().split()  # Split query into words
            if all(
                term in record['search_query'].lower().split()  # Split search_query into words
                for term in search_query_words
            ):
                matching_records.append(record)

        if not matching_records:
            return f"No matching products found for query: {search_query}", 404

        records = [dict(result) for result in matching_records]
        return json.dumps(records)

    except Exception as e:
        error_message = f"Error occurred: {e}"
        return jsonify(error=error_message), 500


@app.route('/service/product/ocassion', methods=['GET'])
def get_products_by_ocassion():
    
    try:
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

    except Exception as e:
        error_message = f"Error occurred: {e}"
        return jsonify(error=error_message), 500



# @app.route('/service/product/recommendation', method=['GET'])
# def get_recommended_products():

    # This function needs to be modified !
    # client = datastore.Client()
    
    # query = client.query(kind='MasterData')
    # request_json = filter_request.get_json()

    # if request_json and 'Occasion' in request_json:
    #     ocassion = request_json['Occasion']
    #     ocassion = ocassion.lower()
    #     query.add_filter('ocassion', '=', ocassion)
    # else:
    #     return f'Data not found'

    # request_json = request.get_json()
    # if request_json and 'Demographics' in request_json:
    #     Demographics = request_json['Demographics']
    #     if 'gender' in 'Demographics':
    #         gender = Demographics['gender']
    #         gender = gender.lower()
    #         query.add_filter('gender', '=', gender)

    # if request_json and 'color' in request_json:
    #     color = request_json['color']
    #     color = color.lower()
    #     query.add_filter('color', '=', color)

    # if request_json and 'material' in request_json:
    #     material = request_json['material']
    #     material = material.lower()
    #     query.add_filter('material', '=', material)

    # if request_json and 'pattern' in request_json:
    #     pattern = request_json['pattern']
    #     pattern = pattern.lower()
    #     query.add_filter('pattern', '=', pattern)

    # results = query.fetch()
    # l=list()
    # for result in results:
    #     l.append(result['product_ID'])
    # result=str(l)
    # result = str(['M01','F01','F02'])
    # return result



@app.route('/service/ai/summarize', methods=['POST'])
def summarize():

    # Initialize Vertex AI
    vertexai.init(project="gen-ai-app", location="us-central1")

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:
        content = request.json['content']
        print(type(content))

        # Text generation parameters
        parameters = {
            "max_output_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

        # Generate text using the model
        response = model.predict(content, **parameters)
        summarized_text = response.text

        return jsonify({"summary": summarized_text})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/service/ai/promotion', methods=['POST'])
def generate_promotion_text():


    # Initialize Vertex AI
    vertexai.init(project="gen-ai-app", location="us-central1")

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:

        json_example = '''{
            "promotion_text": "This is a sample text."
        }'''
        
        occasion = request.json['occasion']
        gender = request.json['gender']
        
        prompt = "You are a creative marketing content writer. Generate marketing advertisement promotion text for the occasion " + occasion + " and gender " + gender + " with happy and excitment tone.Return the result in a json format like this" + json_example


        # Text generation parameters
        parameters = {
            "max_output_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

        # Generate text using the model
        response = model.predict(prompt, **parameters)
        promotion_text = response.text

        return jsonify(promotion_text),200

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/service/ai/promotion_evaluation', methods=['POST'])
def evaluate_promotion_text():


    # Initialize Vertex AI
    vertexai.init(project="gen-ai-app", location="us-central1")

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:

        json_example = '''{
            "promotion_text": "This is a sample text.",
            "tone" : "friendly",
            "is_abusive_language": false,
            "is_adult_content": false
        }'''
        
        promotion_text = request.json['promotion_text']
        
        prompt = "You are a marketing lead content moderator. " + promotion_text + " Review above marketing promotion text and return the result with following attributes such as Tone, is_abusive_language, is_adult_content in a json format like this " + json_example


        # Text generation parameters
        parameters = {
            "max_output_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

        # Generate text using the model
        response = model.predict(prompt, **parameters)
        evaluation_metric = response.text

        return jsonify(evaluation_metric),200

    except Exception as e:
        return jsonify({"error": str(e)})
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
