from flask import jsonify, request, render_template
from flask import Blueprint, render_template, url_for, request, session, redirect, Flask, jsonify, flash, make_response
from google.cloud import datastore
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from colorthief import ColorThief
from google.cloud import storage, vision
from werkzeug.utils import secure_filename
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


BASE_URL = "https://drzz-services-kcvokjzgdq-nw.a.run.app"

@views.route('/')
def home():
    return redirect('/home')






# Function to fetch products with pagination
def fetch_products(page, per_page):
    
    endpoint = '/service/product/all_products'
    api_url = f'{BASE_URL}{endpoint}'

    response = requests.get(api_url)  # Replace with your actual API URL
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
    endpoint = '/service/product/id'
    api_url = f"{BASE_URL}{endpoint}"
    response = requests.post(api_url,json={"product_id": product_id})
    product_data = response.json()

    return render_template('product_description.html', product=product_data)







def fetch_products_styleme():
    endpoint = '/service/product/all_products'
    api_url = f"{BASE_URL}{endpoint}"
    response = requests.get(api_url)  # Replace with your actual API URL
    products = response.json()
    return products[:3]


@views.route('/conversation')
def conversation():
     
    products = fetch_products_styleme() 
     
    return render_template('conversation.html', products=products)







def ask_question_from_fashion(data):
    try:
        
        endpoint = '/service/ai/fashionqna'
        api_url = f"{BASE_URL}{endpoint}"
        payload = {
            'question': data
            
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json().get('answer', 'Sorry, I couldn\'t find an answer.')
    except requests.exceptions.RequestException as e:
        # Handle the exception and return an error response
        return 'An error occurred while communicating with the chatbot.'
# Initialize an empty list to store the conversation
#conversation_list = []
 
@views.route('/stylemeqna', methods=['POST'])
def styleme_qna():
    # Get the magazine_id from the session
    conversation_list = []
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'error': 'Empty question.'}), 400
    prompt = "\n".join(user_question) + "\n\n You are a Fashion advisor read user_question above and give response as a real Fashion advisor would give ."
    chat = convert_conversation_list_to_plain_text(conversation_list)
    data = {"content": prompt}
    
    answer = ask_question_from_fashion(data)
        
    conversation_list.append({'User': user_question, 'Fashion Advisor': answer})
    #print(conversation_list)
    # Return the answer as a JSON response
    return jsonify({'answer': answer})



def get_products_by_ids(product_ids):
    try:
        # Make a POST request to the cloud function for each product ID
        product_details = []
        print(product_ids)
        for product_id in product_ids['product_ids']:
            print(product_id)

            endpoint = '/service/product/id'
            api_url = f"{BASE_URL}{endpoint}"
            response = requests.post(api_url, json={"product_id": product_id})
            
            if response.status_code == 200:
                response_data = response.json()  # Parse the response JSON
                product_details.append(response_data)
            else:
                # Handle the error response if needed
                print(f"Failed to fetch details for product ID {product_id}: {response.status_code}")

        return product_details

    except Exception as e:
        return {
            "message": str(e)
        }    

# Define the URL of the second Cloud Run service




def convert_conversation_list_to_plain_text(conversation_list):
  """
  Converts a conversation list to plain text.

  Args:
    conversation_list: A list of conversation objects.

  Returns:
    A string of plain text representing the conversation.
  """

  plain_text = ""
  for conversation in conversation_list:
    plain_text += f"User: {conversation['User']}\n"
    plain_text += f"Fashion Advisor: {conversation['Fashion Advisor']}\n"
    print(plain_text)
  return plain_text



@views.route('/styleme', methods=['POST', 'GET'])
def styleme():
    if request.method == 'POST':
        try:
            request_data = request.get_json()
            conversation_list = request_data.get('conversation')
            chat = convert_conversation_list_to_plain_text(conversation_list)
            conversation = parse_conversation(chat)
            chat_conversation = {"conversation": conversation}
            
            response_message = store_conversation_in_datastore(chat_conversation)

            data = {"chat": chat}
            endpoint = '/service/ai/demographic_json'
            api_url = f"{BASE_URL}{endpoint}"

            response_post = requests.post(api_url, json=data)

            if response_post.status_code == 200:
                summary_dict = json.loads(response_post.json().get("summary", "{}"))
                product_ids = get_product_by_json_summary(summary_dict)
                products = get_products_by_id(product_ids)
                session['products'] = products
                

                # Return products and product details as JSON
                return jsonify(products=products)

        except Exception as e:
            print("Error:", str(e))

        # If any error occurs or no products are found, return an empty JSON
        return jsonify(products=[])

    else:
        products = fetch_products_styleme()
        return render_template('styleme.html', products=products)
        


# Function to get articles for a magazine
def get_articles(magazine_id):
    try:
        endpoint = '/service/get_articles'
        api_url = f"{BASE_URL}{endpoint}"
        response = requests.post(api_url, json={'magazine_id': magazine_id})
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle the exception and return an error response
        return None

# Function to ask a question to the chatbot
def ask_question(user_question, magazine_id, articles):
    try:
        endpoint = '/service/ai/magazine_qna'
        api_url = f"{BASE_URL}{endpoint}"
        payload = {
            'question': user_question,
            'articles': articles,
            'magazine_id': magazine_id
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json().get('answer', 'Sorry, I couldn\'t find an answer.')
    except requests.exceptions.RequestException as e:
        # Handle the exception and return an error response
        return 'An error occurred while communicating with the chatbot.'


# Flask route for the magazine page
@views.route('/magazine')
def magazine():
    return render_template('magazine.html')

# Flask route to get articles for a specific magazine
@views.route('/magazine/<magazine_id>')
def magazines(magazine_id):
    # Store the magazine_id in the session
    session['magazine_id'] = magazine_id

    articles = get_articles(magazine_id)
    if articles is None:
        return jsonify({'error': 'An error occurred while fetching articles.'}), 500

    return render_template('magazine.html', articles=articles)

# Flask route to handle user questions
@views.route('/qna', methods=['POST'])
def qna():
    # Get the magazine_id from the session
    magazine_id = session.get('magazine_id')

    if magazine_id is None:
        return jsonify({'error': 'Magazine ID not found in the session.'}), 400

    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'error': 'Empty question.'}), 400

    articles = get_articles(magazine_id)
    if articles is None:
        return jsonify({'error': 'An error occurred while fetching articles.'}), 500

    answer = ask_question(user_question, magazine_id, articles)

    # Return the answer as a JSON response
    return jsonify({'answer': answer})


'''@views.route('/qna', methods=['POST'])
def qna():
    user_question = request.json.get('question')

    # Sample response - you should replace this with your actual logic
    answer = "This is a sample answer to your question: " + user_question

    # Return the answer as JSON
    return jsonify({'answer': answer})'''







    
datastore_client= datastore.Client()
@views.route('/marketing')
def marketing():
    if 'chat_id' in session:

        chat_id = session.get('chat_id')
        client = datastore.Client()

        conversation_entity = client.get(client.key('Conversation', chat_id))
        
        if conversation_entity:
            # Get the summary from the conversation entity
            summary = conversation_entity.get("summary", "No summary available.")
        

        data = {"content": summary}
        
        # json_metrics = fetchCustomerMetrics()
        endpoint = '/service/ai/promotion'
        api_url = f"{BASE_URL}{endpoint}"

        response_post = requests.post(api_url, json=data)
        if response_post.status_code == 200:
            response_data = response_post.json()
            response = response_data.get("summary", "No summary available.")
            
            session['promo'] = response
           
          
            return render_template('marketing.html',text_part=response,summary=summary)
        
        else:
            print("POST Request Failed!")
            print(response_post.text)

    else:
            summary = "Session is not present. Please add some script in StyleMe first."
            return render_template('marketing.html',summary=summary)


# Initialize the Google Cloud Storage client
storage_client = storage.Client()
bucket_name = 'drzz_gen_ai_image_upload'  # Replace with your GCS bucket name

'''from typing import Sequence

from google.cloud import vision


def analyze_image_from_uri(
    image_uri: str,
    feature_types: Sequence,
) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = image_uri
    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)
    print(response)
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
     vision.Feature.Type.LABEL_DETECTION,
    # vision.Feature.Type.TEXT_DETECTION,
    # vision.Feature.Type.DOCUMENT_TEXT_DETECTION,
    # vision.Feature.Type.SAFE_SEARCH_DETECTION,
     #vision.Feature.Type.IMAGE_PROPERTIES,
    # vision.Feature.Type.CROP_HINTS,
     #vision.Feature.Type.WEB_DETECTION,
     #vision.Feature.Type.PRODUCT_SEARCH,
    # vision.Feature.Type.OBJECT_LOCALIZATION,
]

response = analyze_image_from_uri(image_uri, features)
print_labels(response)

image_uri = "gs://photodrzz/photo/-473Wx593H-443007260-pink-MODEl6.jpg"
features = [vision.Feature.Type.OBJECT_LOCALIZATION]

response = analyze_image_from_uri(image_uri, features)
print_objects(response)'''


@views.route('/product_label', methods=['POST','GET'])
def product_label():
    if request.method == 'POST':

        uploaded_image = request.files['file']
        if uploaded_image:
            # Ensure the filename is secure (prevents directory traversal attacks)
            filename = secure_filename(uploaded_image.filename)
            # Upload the image to GCS
            image_blob = upload_image_to_gcs(uploaded_image, filename)
            # Analyze the image using its GCS URI
            image_uri = f'gs://{bucket_name}/{image_blob.name}'
            features = [vision.Feature.Type.LABEL_DETECTION,vision.Feature.Type.IMAGE_PROPERTIES]
            response = analyze_image_from_uri(image_uri, features)
            
            labels = [label.description for label in response.label_annotations]
            print(labels)
            return render_template('productlabel.html', labels=labels)
    else:
        return render_template('productlabel.html')


        

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
        features = [vision.Feature.Type.WEB_DETECTION,vision.Feature.Type.LABEL_DETECTION]
       
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
    print(response)
    return response
    





def get_visual_similar_images(response):
    visually_similar_images = []
    if response.web_detection and response.web_detection.visually_similar_images:
        for image in response.web_detection.visually_similar_images:
            visually_similar_images.append(image.url)
          
    return visually_similar_images[:4]



def chat_summary():

    client = datastore.Client()

    chat_id = session.get('chat_id')
    conversation_entity = client.get(client.key('Conversation', chat_id))
    if conversation_entity:
        # Extract the conversation messages
        chat_messages = [message["message"] for message in conversation_entity["chat"]]
    # Create the prompt for summarization
    prompt = "\n".join(chat_messages) + "\n\nFrom this conversation create summary for fashion advisor so that it will be easy to understand the user needs."

    data = {"content": prompt}

    endpoint = '/service/ai/summarize'
    api_url = f"{BASE_URL}{endpoint}"

    response_post = requests.post(api_url, json=data)
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
    return render_template('chathistory.html', products=products, summary = summary)

def fetch_products_lookalike():
    endpoint = '/service/product/all_products'
    api_url = f"{BASE_URL}{endpoint}"
    response = requests.get(api_url)
    products = response.json()
    return products[:3]  # Return only the first three products

@views.route('/lookalike')
def lookalike():
    products = fetch_products_lookalike()

    return render_template('upload.html', products=products)




def fetch_products_men(page, per_page):

    gender = "men"  # API parameter in uppercase
    
    endpoint = '/service/product/gender'
    api_url = f"{BASE_URL}{endpoint}?gender={gender}"
    response = requests.get(api_url)
    
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
    endpoint = '/service/product/gender'
    api_url = f"{BASE_URL}{endpoint}?gender={gender}"
    response = requests.get(api_url)
    
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
    endpoint = '/service/product/gender'
    api_url = f"{BASE_URL}{endpoint}?gender={gender}"
    response = requests.get(api_url)
    
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
    endpoint = '/service/product/gender'
    api_url = f"{BASE_URL}{endpoint}?gender={gender}"
    response = requests.get(api_url)
    
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
    
    endpoint = '/service/product/ocassion'
    api_url = f"{BASE_URL}{endpoint}?ocassion={ocassion}"
    response = requests.get(api_url)
    
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
    endpoint = '/service/product/ocassion'
    api_url = f"{BASE_URL}{endpoint}?ocassion={ocassion}"
    response = requests.get(api_url)
    
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
    endpoint = '/service/product/ocassion'
    api_url = f"{BASE_URL}{endpoint}?ocassion={ocassion}"
    response = requests.get(api_url)
    
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
    endpoint = '/service/product/ocassion'
    api_url = f"{BASE_URL}{endpoint}?ocassion={ocassion}"
    response = requests.get(api_url)
    
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
    endpoint = '/service/product/ocassion'
    api_url = f"{BASE_URL}{endpoint}?ocassion={ocassion}"
    response = requests.get(api_url)
    
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
    endpoint = '/service/product/ocassion'
    api_url = f"{BASE_URL}{endpoint}?ocassion={ocassion}"
    response = requests.get(api_url)
    
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
    
    endpoint = '/service/product/description'
    api_url = f"{BASE_URL}{endpoint}?query={search_query}"
    response = requests.get(api_url)
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
        endpoint = '/service/store_conversation'
        api_url = f"{BASE_URL}{endpoint}"
        response = requests.post(api_url, json=conversation_data)

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
        #print(summary)
        #print(type(summary))
        # Make a POST request to the cloud function
        endpoint = '/service/product/recommendation'
        api_url = f"{BASE_URL}{endpoint}"
        response = requests.post(api_url, json = summary)

        #print(response)
        response_data = response.json()  # Parse the response JSON
        #print(response_data)
        return response_data
        
        
    except Exception as e:
        return {
            "message": str(e)
        }
    
def get_products_by_id(product_ids):
    try:
        # Make a POST request to the cloud function for each product ID
        product_details = []
        print(product_ids)
        for product_id in product_ids['product_ids']:
            print(product_id)

            endpoint = '/service/product/id'
            api_url = f"{BASE_URL}{endpoint}"
            response = requests.post(api_url, json={"product_id": product_id})
            
            if response.status_code == 200:
                response_data = response.json()  # Parse the response JSON
                product_details.append(response_data)
            else:
                # Handle the error response if needed
                print(f"Failed to fetch details for product ID {product_id}: {response.status_code}")

        return product_details

    except Exception as e:
        return {
            "message": str(e)
        }    




@views.route('/promo_analysis', methods=['GET'])
def promo_analysis():

    promo = session.get('promo')
    # Find the index of the colon ":" after the target text
    start_index = promo.find("**Promotion advertisement banner text:**") + len("**Promotion advertisement banner text:**")

    # Extract the string after the colon
    result = promo[start_index:].strip()

    print(result)

    data = {"promotion_text": result}

    endpoint = '/service/ai/promotion_evaluation'
    api_url = f"{BASE_URL}{endpoint}"
    response_post = requests.post(api_url, json=data)
    if response_post.status_code == 200:
        response_data = response_post.json()
        summary = response_data.get("summary", "No summary available.")
        print(type(summary))

    products = session.get('products')

    return render_template('promo_analysis.html', text_part = promo, summary=summary ,products=products[:3])

