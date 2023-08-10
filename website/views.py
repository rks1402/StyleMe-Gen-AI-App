from flask import jsonify, request
from flask import Blueprint, render_template, url_for, request, session, redirect, Flask, jsonify, flash
from google.cloud import datastore
import json
import datetime
import hashlib
import random
import string
import os
from google.cloud import storage
from google.cloud import datastore
import requests

views = Blueprint('views', __name__)




@views.route('/')
def home():
    return redirect('/homepage')

# API route to fetch products
@views.route('/product')
def fetch_products():
    response = requests.get('https://full-iqcjxj5v4a-el.a.run.app/get_all_product')  # Replace with your actual API URL
    products = response.json()
    return products

# Route to render HTML page and display products
@views.route('/homepage')
def homepage():
    products = fetch_products()  # Fetch products using the API
    return render_template('homepage.html', products=products)


@views.route('/styleme')
def styleme():
    # ... (rest of your code)

    # Render the template and pass the fetched records
    return render_template('styleme.html')


@views.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        # Modify the filename to include the poker_board_id
        filename = file.filename
        # Upload the file to Google Cloud Storage
        client = storage.Client()
        bucket_name = 'uploaded-cloth'  # Replace with your bucket name
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_file(file)

        flash('File uploaded successfully!', 'success')
        return redirect('/')

    flash('No File is Selected.', 'danger')
    return redirect('/')

