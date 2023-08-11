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
    products = fetch_products() 
     
    return render_template('styleme.html', products=products)

@views.route('/upload', methods=['POST'])
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
        return redirect('/')

    flash('No File is Selected.', 'danger')
    return redirect('/')



@views.route('/men')
def fetch_men_data():
    gender = "men"  # API parameter in uppercase
    url = f"https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender={gender}"
    
    response = requests.get(url)
    
    products = response.json()
    
    return render_template('homepage.html', products=products)  # Render a template to display the data

@views.route('/women')
def fetch_women_data():
    gender = "women"  # API parameter in uppercase
    url = f"https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender={gender}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html', products=products)  # Render a template to display the data

@views.route('/boys')
def fetch_boys_data():
    gender = "boys"  # API parameter in uppercase
    url = f"https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender={gender}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html', products=products)  # Render a template to display the data

@views.route('/girls')
def fetch_girls_data():
    gender = "girls"  # API parameter in uppercase
    url = f"https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender?gender={gender}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html',  products=products)  # Render a template to display the data


@views.route('/wedding')
def fetch_wedding_data():
    ocassion = "wedding"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html',  products=products)  # Render a template to display the data


@views.route('/party')
def fetch_party_data():
    ocassion = "party"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html',  products=products)  # Render a template to display the data

@views.route('/casual')
def fetch_casual_data():
    ocassion = "casual"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html',  products=products)  # Render a template to display the data


@views.route('/birthday')
def fetch_birthday_data():
    ocassion = "birthday"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html',  products=products)  # Render a template to display the data


@views.route('/formal')
def fetch_formal_data():
    ocassion = "formal"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html', products=products)  # Render a template to display the data


@views.route('/vacation')
def fetch_vacation_data():
    ocassion = "vacation"  # API parameter in uppercase
    url = f"https://ocassion-iqcjxj5v4a-el.a.run.app/product/ocassion?ocassion={ocassion}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html',  products=products)  # Render a template to display the data


@views.route('/search')
def fetch_search_data():
    search_query = request.args.get('query')  # API parameter in uppercase
    url = f"https://get-product-by-description-hmvyexj3oa-el.a.run.app/get_product_by_description?query={search_query}"
    
    response = requests.get(url)
    products = response.json()
    
    return render_template('homepage.html',  products=products)  # Render a template to display the data
