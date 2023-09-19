from flask import Flask, request, jsonify
from google.cloud import datastore
import vertexai
from vertexai.language_models import TextGenerationModel
import json, datetime, time, requests
from google.cloud import storage
import os


from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize Vertex AI


# Load the pre-trained text generation model
model = TextGenerationModel.from_pretrained("text-bison@001")

@app.route('/service/product/all_products', methods=['GET'])
def get_all_products():
    try:
        

        # Create a Datastore client
        client = datastore.Client()

        # Define the kind from which you want to fetch the records
        kind = "MasterData"

        # Create a query to fetch the record with the specified product_id
        query = client.query(kind=kind)

        # Fetch the entities that match the query
        results = list(query.fetch())

        if not results:
            return f"No record found.", 404

        # Convert the entity to a dictionary
        records = [dict(result) for result in results]

        # Return the JSON response
        return json.dumps(records)

    except Exception as e:
        error_message = f"Error occurred: {e}"
        return jsonify(error=error_message), 500


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


@app.route('/service/product/id', methods=['POST'])
def get_product_by_id():
    try:
        # Get the product_id from the query parameters in the HTTP request
        product_id = request.json['product_id']

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
    

@app.route('/service/celebrity/celebrity_id', methods=['POST'])
def get_celebrity_by_id():
    try:
        # Get the product_id from the query parameters in the HTTP request
        celebrity_id = request.json['celebrity_id']

        if not celebrity_id:
            return "celebrity_id not provided.", 400

        # Create a Datastore client
        client = datastore.Client()

        # Define the kind from which you want to fetch the records
        kind = "celebrity"

        # Create a query to fetch the record with the specified product_id
        query = client.query(kind=kind)
        query.add_filter('celebrity_id', '=', celebrity_id)

        # Fetch the entities that match the query
        results = list(query.fetch())

        if not results:
            return f"No record found with Product ID: {celebrity_id}", 404

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



@app.route('/service/product/recommendation', methods=['POST'])
def get_recommended_products():

    try:
        datastore_client = datastore.Client()

        request_json = request.get_json()
        if not request_json:
            return jsonify({'error': 'Invalid JSON'}), 400

        query = datastore_client.query(kind='MasterData')

        occasion = request_json.get('Occasion', '').lower()
        if occasion:
            query.add_filter('ocassion', '=', occasion)  # Adjusted property name here

        demographics = request_json.get('Demographics', {})
        gender = demographics.get('gender', '').lower()
        if gender:
            query.add_filter('gender', '=', gender)

        color = request_json.get('color', '').lower()
        if color:
            query.add_filter('color', '=', color)

        material = request_json.get('material', '').lower()
        if material:
            query.add_filter('material', '=', material)

        pattern = request_json.get('pattern', '').lower()
        if pattern:
            query.add_filter('pattern', '=', pattern)

        results = query.fetch()
        product_ids = [result['product_ID'] for result in results]
        return jsonify({'product_ids': product_ids})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/service/ai/summarize', methods=['POST'])
def summarize():

    # Initialize Vertex AI
    vertexai.init(project=os.environ.get("PROJECT_ID"), location=os.environ.get("LOCATION"))

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:
        summary = request.json['content']
        print(type(summary))
        json= '''{
            "age": 35,
        "gender": "female",
        "income": "high",
        "occupation": "professional",
        "tone of text": "friendly"
        "location": "urban"
        }'''
        
        # Test POST request
        prompt = summary

        # Text generation parameters
        parameters = {
            "max_output_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

        # Generate text using the model
        response = model.predict(prompt, **parameters)
        summarized_text = response.text

        return jsonify({"summary": summarized_text})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/service/ai/promotion', methods=['POST'])
def generate_promotion_text():


    # Initialize Vertex AI
    vertexai.init(project=os.environ.get("PROJECT_ID"), location=os.environ.get("LOCATION"))

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:

        json_example = '''{
            "promotion_text": "This is a sample text."
        }'''
        
        summary = request.json['content']
        
        prompt = summary + f" Read the above passage and create a promotion advertisement banner text as one liner for the clothing."


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

        return jsonify({"summary": promotion_text}),200

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/service/ai/promotion_evaluation', methods=['POST'])
def evaluate_promotion_text():


    # Initialize Vertex AI
    vertexai.init(project=os.environ.get("PROJECT_ID"), location=os.environ.get("LOCATION"))

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:

        json_example = """
        {
            
            "promotion tone": "friendly",
            "emotion": "positive",
            "season": "fall",
            "occasion": "wedding"
        }
            """
        
        promotion_text = request.json['promotion_text']
        
        prompt = "You are the marketing campaign consultant, Review the following text in the triple quotes and give the tone, emotion ,season and occasion from the "+ promotion_text +"  and return the value as json attributes, for any missing value, mention as null  and give response structured like this  sample json   " + json_example


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

        return jsonify({"summary": evaluation_metric}),200

    except Exception as e:
        return jsonify({"error": str(e)})
    


conversation_history = []

@app.route('/service/ai/fashionqna', methods=['POST'])
def fashion_advisor():
    # Initialize Vertex AI
    vertexai.init(project=os.environ.get("PROJECT_ID"), location=os.environ.get("LOCATION"))

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")
    try:
        data = request.json
        user_question = data.get('question', '')

        # Add the user's question to the conversation history
        conversation_history.append(f"User: {user_question}")

        # Construct the conversation history prompt with clear context
        conversation_prompt = "\n".join(conversation_history)
        conversation_prompt += "\nFashion Advisor: "

        # Text generation parameters
        parameters = {
            "max_output_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

        # Generate a response using the model and conversation prompt
        response = model.predict(conversation_prompt, **parameters)
        answer = response.text

        # Append the bot's response to the conversation history
        conversation_history.append(f"Fashion Advisor: {answer}")

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)})



@app.route('/service/ai/magazine_qna', methods=['POST'])
def magazine_qna():

    # Initialize Vertex AI
    vertexai.init(project=os.environ.get("PROJECT_ID"), location=os.environ.get("LOCATION"))

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:
        data = request.json

        # Validate the input data
        user_question = data.get('question', '')
        if not user_question:
            return jsonify({"error": "Missing or empty 'question' field in the request."}), 400

        article = data.get('article', '')
        articles = data.get('articles', '')

        # Create a conversation context with the user's question and article text
        conversation = f"User: {user_question}\nArticle: {article}\nArticles: {articles}"

        # Text generation parameters
        parameters = {
            "max_output_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

        # Generate text using the model
        response = model.predict(conversation, **parameters)
        answer = response.text

        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": "An error occurred while processing the request."}), 500    



@app.route('/service/ai/demographic_json', methods=['POST'])
def generate_demographic_json():


    # Initialize Vertex AI
    vertexai.init(project=os.environ.get("PROJECT_ID"), location=os.environ.get("LOCATION"))

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:
        chat = request.json['chat']
        occasion_demographics = """
        {
            "Occasion": "wedding",
            "color": "black",
            "material": "silk",
            "pattern": "solid",
            "Demographics": {
                "Budget": {
                "Min": 150,
                "Max": 200
                },
                "gender": "men",
                "Style": "Classic and Elegant"
            }
        }
            """
        # Test POST request
        prompt = chat + "Give the User Occasion and demographics from this conversation in JSON format." + occasion_demographics + "Don't give color. and gender can be only from (boys,girls,women and men)"

        # Text generation parameters
        parameters = {
            "max_output_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

        # Generate text using the model
        response = model.predict(prompt, **parameters)
        demographic_json = response.text

        return jsonify({"summary": demographic_json}),200

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/service/ai/product_type', methods=['POST'])
def get_product_type():


    # Initialize Vertex AI
    vertexai.init(project=os.environ.get("PROJECT_ID"), location=os.environ.get("LOCATION"))

    # Load the pre-trained text generation model
    model = TextGenerationModel.from_pretrained("text-bison@001")

    try:
        article_text = request.json['article_text']

        product_demographics = """
        {"products": ["sample product name"]}
        """
        # Test POST request
        prompt = article_text + "Provide recommended products only  names  without image links mentioned in the above article in valid Json format without the indentation like this :" + product_demographics

        # Text generation parameters
        parameters = {
            "max_output_tokens": 256,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }

        # Generate text using the model
        response = model.predict(prompt, **parameters)
        product_type = response.text

        return jsonify(product_type),200

    except Exception as e:
        return jsonify({"error": str(e)})        


@app.route('/service/store_conversation', methods=['POST'])
def store_conversation():
    try:
        client = datastore.Client()
        # Generate a unique key using a timestamp
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
        chat_id = f"user_{formatted_datetime}"

        # Parse incoming conversation data from JSON in the request body
        conversation_data = request.get_json()
        user_consent = conversation_data.get('user_consent', True)  # Default to True if not provided
        appointment_required = conversation_data.get('appointment_required', True)  # Default to True if not provided

        # Create a new conversation entity with the generated key
        conversation_entity = datastore.Entity(client.key('Conversation', chat_id))
        conversation_entity['chat_id'] = chat_id # Store the generated key as a property
        conversation_entity['chat'] = conversation_data['conversation']
        conversation_entity['user_consent'] = user_consent
        conversation_entity['appointment_required'] = appointment_required
        conversation_entity['created_at'] = current_datetime
        

        # Save the conversation entity to Datastore
        client.put(conversation_entity)

        response = {
            "status": "success",
            "message": "Conversation stored successfully",
            "chat_id": chat_id
        }
        return jsonify(response), 200
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return jsonify(response), 500    


@app.route('/service/get_articles', methods=['POST'])
def get_articles():
    request_json = request.get_json()
    if not request_json or 'magazine_id' not in request_json:
        return 'Invalid request', 400

    magazine_id = request_json['magazine_id']
    bucket_name = 'drzz_gen_ai_magazine'
    blob_prefix = f'magazine_{magazine_id}/'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=blob_prefix)

    articles = []
    for blob in blobs:
        article_content = blob.download_as_text()
        articles.append(article_content)

    return json.dumps(articles)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
