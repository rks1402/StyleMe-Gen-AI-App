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






# API route to fetch products
@views.route('/product')
def fetch_products():
    response = requests.get('https://full-iqcjxj5v4a-el.a.run.app/get_all_product')  # Replace with your actual API URL
    products = response.json()
    return products

# Route to render HTML page and display products
@views.route('/')
def display_products():
    products = fetch_products()  # Fetch products using the API
    return render_template('homepage.html', products=products)


@views.route('/styleme')
def styleme():
    # ... (rest of your code)

    # Render the template and pass the fetched records
    return render_template('styleme.html')



