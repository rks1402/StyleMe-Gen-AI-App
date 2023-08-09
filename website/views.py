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