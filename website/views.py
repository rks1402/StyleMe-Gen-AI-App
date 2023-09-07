from flask import jsonify, request, render_template
from flask import Blueprint, render_template, url_for, request, session, redirect, Flask, jsonify, flash, make_response
from google.cloud import datastore
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from colorthief import ColorThief
import io
import json
import datetime
import hashlib
import random
import string
import os
import google.generativeai as palm
from google.cloud import storage
from google.cloud import datastore
import requests
from typing import Sequence
import re

views = Blueprint('views', __name__)




@views.route('/')
def home():
    return redirect('/home')






# Function to fetch products with pagination
def fetch_products(page, per_page):
    response = requests.get('https://full-iqcjxj5v4a-el.a.run.app/get_all_product')  # Replace with your actual API URL
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products


# Route to render HTML page and display products with pagination
@views.route('/home')
def homepage():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)





# Existing routes and functions...

@views.route('/product/<string:product_id>')
def product_details(product_id):
    api_url = f"https://fetch-iqcjxj5v4a-el.a.run.app/get_record?product_id={product_id}"
    response = requests.get(api_url)
    product_data = response.json()

    return render_template('product_description.html', product=product_data)







def fetch_products_styleme():
    response = requests.get('https://full-iqcjxj5v4a-el.a.run.app/get_all_product')  # Replace with your actual API URL
    products = response.json()
    return products[:3]


@views.route('/styleme')
def styleme():

    products = fetch_products_styleme() 
     
    return render_template('styleme.html', products=products)

@views.route('/magazine')
def magazine():  

    return render_template('magazine.html')

CLOUD_FUNCTION_URL = 'https://asia-south1-gen-ai-app.cloudfunctions.net/get-articles'

@views.route('/magazine/<magazine_id>')
def magazines(magazine_id):
    response = requests.post(CLOUD_FUNCTION_URL, json={'magazine_id': magazine_id})
    articles = response.json()

    return render_template('magazine.html', articles=articles)


# Initialize the Datastore client
datastore_client = datastore.Client()

# def fetchCustomerMetrics():
#     try:
#         customer_id = "C001"
#         print(customer_id)
#         if not customer_id:
#             return 'Missing customerId parameter', 400

#         query = datastore_client.query(kind='metric')  
#         # Add a filter to fetch data specific to the provided customer ID
#         query.add_filter('customer_id', '=', customer_id)

#         entities = list(query.fetch())
        
#         return entities
#     except Exception as e:
#         return str(e), 500

# def fetch_products_with_discount(discount_value):
#     try:
#         # Create a client to interact with Google Cloud Datastore
#         client = datastore.Client()

#         # Define the kind (entity type) in Datastore
#         kind = "MasterData"

#         # Define a query to filter products with a specific discount
#         query = client.query(kind=kind)
#         query.add_filter("discount", "=", str(discount_value))

#         # Print the query being executed
#         print(f"Executing query: {query}")

#         # Execute the query and fetch matching products
#         matching_products = list(query.fetch())

#         # Print the number of matching products
#         print(f"Found {len(matching_products)} matching products")

#         return matching_products
#     except Exception as e:
#         print(f"Error fetching products: {str(e)}")
#         return []



    
datastore_client= datastore.Client()
@views.route('/marketing')
def marketing():
    if 'chat_id' in session:
        API_URL = "https://summary-gen-ai-api-hmvyexj3oa-el.a.run.app/summarize"

        chat_id = session.get('chat_id')
        client = datastore.Client()

        conversation_entity = client.get(client.key('Conversation', chat_id))
        
        if conversation_entity:
            # Get the summary from the conversation entity
            summary = conversation_entity.get("summary", "No summary available.")
        
    
        
        json= '''{
            "age": 35,
        "gender": "female",
        "income": "high",
        "occupation": "professional",
        "tone of text": "friendly"
        "location": "urban"
        }'''
        
        # Test POST request
        prompt = summary + f" Read the above passage and create a promotion advertisement banner text as one liner for the clothing, return the user data in JSON format like this."
        data = {"content": prompt}
        
        # json_metrics = fetchCustomerMetrics()

        response_post = requests.post(API_URL, json=data)
        if response_post.status_code == 200:
            response_data = response_post.json()
            response = response_data.get("summary", "No summary available.")
            pattern = r'({.*})\s+(.+)'
            match = re.search(pattern, response, re.DOTALL)

            if match:
                json_part = match.group(1)
                text_part = match.group(2)
            
            
            session['promo'] = text_part
           
          
            return render_template('marketing.html', json_part=json_part,text_part=text_part,summary=summary)
        
        else:
            print("POST Request Failed!")
            print(response_post.text)

    else:
            summary = "Session is not present. Please add some script in StyleMe first."
            return render_template('marketing.html',summary=summary)
    

"""@views.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        # Modify the filename to include the poker_board_id
        filename = file.filename
        # Upload the file to Google Cloud Storage
        client = storage.Client()
        bucket_name = 'upload_imagwa'  # Replace with your bucket name
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_file(file)

        flash('File uploaded successfully!', 'success')
        return redirect('/lookalike')

    flash('No File is Selected.', 'danger')
    return redirect('/lookalike')"""

"""def analyze_image(image_file):
    # Initialize the Vision API client
    client = vision_v1.ImageAnnotatorClient()

    # Read the image content from the uploaded file
    image_content = image_file.read()

    # Create a Vision API image object from the content
    image = types.Image(content=image_content)

    # Perform label detection using Vision API
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    # Use colorthief to get the dominant color
    color_thief = ColorThief(io.BytesIO(image_content))
    dominant_color = color_thief.get_color(quality=1)

    # Create a JSON output with analysis results
    analysis_result = {
        "labels": labels,
        "dominant_color": dominant_color
    }

    return analysis_result"""



'''from typing import Sequence

from google.cloud import vision


def analyze_image(
    image_uri: str,
    feature_types: Sequence,
) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = image_uri
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)
   
    return response



def print_labels(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for label in response.label_annotations:
        print(
            f"{label.score:4.0%}",
            f"{label.description:5}",
            sep=" | ",
        )

def print_objects(response: vision.AnnotateImageResponse):
    print("=" * 80)
    for obj in response.localized_object_annotations:
        nvertices = obj.bounding_poly.normalized_vertices
        print(
            f"{obj.score:4.0%}",
            f"{obj.name:15}",
            f"{obj.mid:10}",
            ",".join(f"({v.x:.1f},{v.y:.1f})" for v in nvertices),
            sep=" | ",
        )
        
image_uri = "gs://photodrzz/photo/13000072a.jpg"
features = [
    # vision.Feature.Type.OBJECT_LOCALIZATION,
    # vision.Feature.Type.FACE_DETECTION,
    # vision.Feature.Type.LANDMARK_DETECTION,
    # vision.Feature.Type.LOGO_DETECTION,
    # vision.Feature.Type.LABEL_DETECTION,
    # vision.Feature.Type.TEXT_DETECTION,
    # vision.Feature.Type.DOCUMENT_TEXT_DETECTION,
    # vision.Feature.Type.SAFE_SEARCH_DETECTION,
     #vision.Feature.Type.IMAGE_PROPERTIES,
    # vision.Feature.Type.CROP_HINTS,
     #vision.Feature.Type.WEB_DETECTION,
     #vision.Feature.Type.PRODUCT_SEARCH,
    # vision.Feature.Type.OBJECT_LOCALIZATION,
]

response = analyze_image(image_uri, features)


image_uri = "gs://photodrzz/photo/-473Wx593H-443007260-pink-MODEl6.jpg"
features = [vision.Feature.Type.OBJECT_LOCALIZATION]

response = analyze_image(image_uri, features)




from flask import Flask, request, render_template
from google.cloud import vision
from google.cloud import storage
import tempfile

# Initialize your Flask app
app = Flask(__name__)

# Define your Google Cloud Storage bucket name
bucket_name = "uploaded-cloth"

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

# Your analyze_image and print_objects functions (as defined earlier)

@views.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        # Get the uploaded file
        uploaded_file = request.files["file"]

        if uploaded_file:
            # Create a temporary file to store the uploaded image
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                uploaded_file.save(temp_file.name)
            
            # Upload the image to the Google Cloud Storage bucket
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(uploaded_file.filename)
            blob.upload_from_filename(temp_file.name)

            # Get the public URL of the uploaded image
            image_uri = f"gs://{bucket_name}/{uploaded_file.filename}"

            # Use the analyze_image function with the uploaded image URI
            features = [vision.Feature.Type.OBJECT_LOCALIZATION]
            response = analyze_image(image_uri, features)

            # You can do something with the response here (e.g., print_objects)
            # For example, print detected objects:
            print_objects(response)

            return jsonify(response)  # You'll need to import jsonify from flask


    return render_template("upload.html")  # Create an HTML template for the upload page
'''






from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage, vision
from werkzeug.utils import secure_filename



# Initialize the Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'uploaded-cloth'  # Replace with your GCS bucket name



@views.route('/upload', methods=['POST'])
def upload():
    # Handle the uploaded image
    uploaded_image = request.files['file']
    if uploaded_image:
        # Ensure the filename is secure (prevents directory traversal attacks)
        filename = secure_filename(uploaded_image.filename)
        # Upload the image to GCS
        image_blob = upload_image_to_gcs(uploaded_image, filename)
        # Analyze the image using its GCS URI
        image_uri = f'gs://{bucket_name}/{image_blob.name}'
        features = [vision.Feature.Type.WEB_DETECTION]
        response = analyze_image_from_uri(image_uri, features)
        original_image_url = image_blob.public_url
        visually_similar_images = get_visual_similar_images(response)
        return render_template('upload.html', original_image_url=original_image_url, visually_similar_images=visually_similar_images)

def upload_image_to_gcs(uploaded_image, filename):
    # Create a blob in the GCS bucket with the provided filename
    bucket = storage_client.bucket(bucket_name)
    image_blob = bucket.blob(filename)
    # Upload the image file to the blob
    image_blob.upload_from_string(uploaded_image.read(), content_type=uploaded_image.content_type)
    return image_blob

def analyze_image_from_uri(image_uri: str, feature_types: list) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)
    return response

def get_visual_similar_images(response):
    visually_similar_images = []
    if response.web_detection and response.web_detection.visually_similar_images:
        for image in response.web_detection.visually_similar_images:
            visually_similar_images.append(image.url)
          
    return visually_similar_images[:4]









def chat_summary():

    client = datastore.Client()

    API_URL = "https://summary-gen-ai-api-hmvyexj3oa-el.a.run.app/summarize"
    chat_id = session.get('chat_id')
    conversation_entity = client.get(client.key('Conversation', chat_id))
    if conversation_entity:
        # Extract the conversation messages
        chat_messages = [message["message"] for message in conversation_entity["chat"]]
    # Create the prompt for summarization
    prompt = "\n".join(chat_messages) + "\n\nFrom this conversation create summary for fashion advisor so that it will be easy to understand the user needs."

    data = {"content": prompt}

    response_post = requests.post(API_URL, json=data)
    if response_post.status_code == 200:
        response_data = response_post.json()
        summary = response_data.get("summary", "No summary available.")

         # Update the conversation entity with the generated summary
        conversation_entity["summary"] = summary
        client.put(conversation_entity)  # Save the updated entity
        
        return summary
    else:
        print("POST Request Failed!")
        print(response_post.text)

@views.route('/chathistory')
def chathistory():    
    if 'chat_id' in session :
        summary = chat_summary()
    else:
        summary = "chat on style me to see summary."    
    
    if 'products' in session :
        products = session.get('products')
    else:
        products = fetch_products_lookalike()
    return render_template('chathistory.html', products=products[:3], summary = summary)

def fetch_products_lookalike():
    response = requests.get('https://full-iqcjxj5v4a-el.a.run.app/get_all_product')
    products = response.json()
    return products[:3]  # Return only the first three products

@views.route('/lookalike')
def lookalike():
    products = fetch_products_lookalike()

    return render_template('upload.html', products=products)




def fetch_products_men(page, per_page):

    gender = "men"  # API parameter in uppercase
    url = f"https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender={gender}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/men')
def fetch_men_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_men(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)



def fetch_products_women(page, per_page):
    gender = "women"  # API parameter in uppercase
    url = f"https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender={gender}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/women')
def fetch_women_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_women(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)



def fetch_products_boys(page, per_page):
    gender = "boys"  # API parameter in uppercase
    url = f"https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender={gender}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/boys')
def fetch_boys_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_boys(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)



def fetch_products_girls(page, per_page):
    gender = "girls"  # API parameter in uppercase
    url = f"https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender={gender}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/girls')
def fetch_girls_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_girls(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)





def fetch_products_wedding(page, per_page):
    ocassion = "wedding"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/wedding')
def fetch_wedding_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_wedding(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)




def fetch_products_party(page, per_page):
    ocassion = "party"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/party')
def fetch_party_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_party(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)



def fetch_products_casual(page, per_page):
    ocassion = "casual"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/casual')
def fetch_casual_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_casual(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)




















def fetch_products_birthday(page, per_page):
    ocassion = "birthday"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/birthday')
def fetch_birthday_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_birthday(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)





def fetch_products_formal(page, per_page):
    ocassion = "formal"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/formal')
def fetch_formal_data():
    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_formal(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)



def fetch_products_vacation(page, per_page):
    ocassion = "vacation"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products

@views.route('/vacation')
def fetch_vacation_data():

    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_products_vacation(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)



def fetch_search_dataa(page, per_page):
    search_query = request.args.get('query')
    print(search_query)  # API parameter in uppercase
    url = f"https://get-product-by-description-hmvyexj3oa-el.a.run.app/get_product_by_description?query={search_query}"
    
    response = requests.get(url)
    products = response.json()

    total_products = len(products)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = products[start_idx:end_idx]

    return paginated_products, total_products



@views.route('/search')
def fetch_search_data():

    page = request.args.get('page', default=1, type=int)  # Get the requested page number from the URL
    per_page = 8 # Number of products per page

    products, total_products = fetch_search_dataa(page, per_page)  # Fetch products using the API

    total_pages = (total_products + per_page - 1) // per_page  # Calculate the total number of pages

    return render_template('homepage.html', products=products, page=page, per_page=per_page, total_pages=total_pages)

# Function to create simple text into desired JSON format.
def parse_conversation(text):
    lines = text.strip().split('\n')
    conversation = []
    sender = None
    current_message = []

    for line in lines:
        line = line.strip()
        if line.startswith('User:'):
            if sender and current_message:
                conversation.append({"sender": sender, "message": ' '.join(current_message)})
            sender = 'user'
            current_message = [line[len('User:'):].strip()]
        elif line.startswith('Fashion Assistant:'):
            if sender and current_message:
                conversation.append({"sender": sender, "message": ' '.join(current_message)})
            sender = 'bot'
            current_message = [line[len('Fashion Assistant:'):].strip()]
        else:
            current_message.append(line)

    if sender and current_message:
        conversation.append({"sender": sender, "message": ' '.join(current_message)})

    return conversation

# Function to take the JSON chat and store into datastore
def store_conversation_in_datastore(conversation_data):
    try:
        # Make a POST request to the cloud function
        response = requests.post("https://asia-south1-gen-ai-app.cloudfunctions.net/chat_to_datastore", json=conversation_data)

        if response.status_code == 200:
            response_data = response.json()  # Parse the response JSON
            chat_id = response_data.get("chat_id")  # Extract the entity key
            
            if chat_id:
                response_message = {
                    "message": "Conversation sent and stored successfully",
                    "chat_id": chat_id  # Include the entity key in the response
                }
                session['chat_id'] = chat_id
                print(session['chat_id'])
            else:
                response_message = {
                    "message": "Conversation sent and stored successfully"
                }
            
            return response_message
        else:
            return {
                "message": f"Error sending conversation: {response.text}"
            }
    except Exception as e:
        return {
            "message": str(e)
        }
    
def get_product_by_json_summary(summary):
    try:
        print(type(summary))
        # Make a POST request to the cloud function
        response = requests.post("https://asia-south1-gen-ai-app.cloudfunctions.net/get-product-by-ocassion-and-demographics", json = summary)

        print(response)
        response_data = response.json()  # Parse the response JSON
        print(response_data)
        return response_data
        
        
    except Exception as e:
        return {
            "message": str(e)
        }
    
def get_products_by_id(product_ids):
    try:
        
        
        # Make a POST request to the cloud function
        response = requests.post("https://asia-south1-gen-ai-app.cloudfunctions.net/get-products-by-id", json = product_ids)

        print(response)
        response_data = response.json()  # Parse the response JSON
        print(response_data)
        return response_data
        
        
    except Exception as e:
        return {
            "message": str(e)
        }    

@views.route('/submit_chat', methods=['POST'])
def submit_chat():
    API_URL = "https://summary-gen-ai-api-hmvyexj3oa-el.a.run.app/summarize"

    chat = request.form['chat']
    conversation = parse_conversation(chat)
    chat_conversation = {"conversation": conversation}  # Removed the jsonify call here

    response_message = store_conversation_in_datastore(chat_conversation)

    #return jsonify({"message": response_message})
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
    data = {"content": prompt}

    response_post = requests.post(API_URL, json=data)
    if response_post.status_code == 200:
        response_data = response_post.json()
        summary = response_data.get("summary", "No summary available.")
        try:
            summary_dict = json.loads(summary)
            print(summary_dict)  # This should now be a dictionary
            product_ids = get_product_by_json_summary(summary_dict)
            # Rest of your code
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
        #return summary
        #return product_ids  # Return the product_ids as JSON response
        print(product_ids)
        print(type(product_ids))
        products = get_products_by_id(product_ids)
        session['products'] = products
        #return products
        return render_template('styleme.html', products=products)
    
    else:
        print("POST Request Failed!")
        print(response_post.text)


@views.route('/promo_analysis', methods=['GET'])
def promo_analysis():

    promo = session.get('promo')

    API_URL = "https://summary-gen-ai-api-hmvyexj3oa-el.a.run.app/summarize"

    #return jsonify({"message": response_message})
    sample = """
    {
        
        "promotion tone": "friendly",
        "emotion": "positive",
        "season": "fall",
        "occasion": "wedding"
    }
        """
    # Test POST request
    prompt = "You are the marketing campaign consultant, Review the following text in the triple quotes and give the tone, emotion ,season and occasion from the text and return the value as son attributes. for any missing value, mention as null  " + promo + "sample json like  " + sample
    data = {"content": prompt}

    response_post = requests.post(API_URL, json=data)
    if response_post.status_code == 200:
        response_data = response_post.json()
        summary = response_data.get("summary", "No summary available.")
        print(type(summary))

    products = session.get('products')

    return render_template('promo_analysis.html', text_part = promo, summary=summary ,products=products[:3])

     
