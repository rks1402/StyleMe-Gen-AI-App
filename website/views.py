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


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return redirect('/homepage')

@views.route('/homepage')
def homepage():
    return render_template('home.html')

@views.route('/stylemepage')
def stylemepage():
    return render_template('stylemepage.html')

@views.route('/upload_image_page')
def upload_image_page():
    return render_template('upload_image.html')

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
        return redirect('/upload_image_page')

    flash('No File is Selected.', 'danger')
    return redirect('/upload_image_page')