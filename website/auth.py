
# Import required modules
from flask import Flask, render_template, request, Blueprint, url_for, redirect, session, flash
from google.cloud import datastore
import bcrypt
import os


# Create a Flask app
auth = Blueprint('auth', __name__)

# Initialize Datastore client
datastore_client = datastore.Client()


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data from request
        name = request.form['name']
        user_id = request.form['email']
        email = request.form['email']
        user_role = request.form['user_role']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        # Check if password and confirm password match
        if password != confirm_password:
            return 'Password and Confirm Password do not match', 400

        # Check if user already exists in Datastore
        query = datastore_client.query(kind='User')
        query.add_filter('email', '=', email)
        existing_users = query.fetch()

        if len(list(existing_users)) > 0:
            flash('User with this email already exist','danger')
            return redirect('/signup')

        # Hash the password

        # Save new user to Datastore
        user_key = datastore_client.key('User', user_id)
        user = datastore.Entity(key=user_key)
        user['name'] = name
        user['email'] = email
        user['user_id'] = user_id
        user['user_role'] = user_role
        
        user['password'] = hashed_password.decode('utf-8')
        datastore_client.put(user)
        
        flash("Account Created Successfully!", "success")
        return redirect('/login')

    else:
        if "email" in session:
            flash("Already Logged In!", "info")

            return redirect('/poker_master_landing')
            
        
        # Render the signup page for GET request
        return render_template('signup_page.html')


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    
        if request.method == 'POST':
            email = request.form['email']
            new_password = request.form['new_password']

            # Check if email and new password are provided
            if not email or not new_password:
                return 'Email and new password are required', 400

            # Query Datastore to check if email exists
            query = datastore_client.query(kind='User')
            query.add_filter('email', '=', email)
            result = list(query.fetch())  # Convert query result to list

            # If a user with the given email is found
            if len(result) > 0:
                user = result[0]

                # Update user's password in Datastore
                
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user['password'] = hashed_password.decode('utf-8')                            
                datastore_client.put(user)

                return redirect('/login')
            
            else:
                flash("No account exist with this email","error")
                return redirect('/reset_password')

        else:
            return render_template('reset_password.html')
   
# Initialize Google Cloud Datastore client
datastore_client = datastore.Client()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get email and password from form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not email:
            flash('Please enter your email', 'error')
            return redirect('/login')
        if not password:
            flash('Please enter your password', 'error')
            return redirect('/login')

        # Query Datastore for user with matching email
        query = datastore_client.query(kind='CustomerData')
        query.add_filter('Email', '=', email)
        result = list(query.fetch(limit=1))

        if result:
            # User found, retrieve user information
            user = result[0]
            stored_password = user['Password']  # Retrieve the stored password from the dataset

            # Validate password
            if password == stored_password:
                # Passwords match, log in user
                session['customer_id'] = user['Customer_ID']
                session['first_name'] = user['First_Name']
                session['last_name'] = user['Last_Name']

                # Assuming you have a user role field in your dataset
                # user_role = user['User_Role']
                # You can adjust the role logic here

                return redirect('/homepage')  # Replace with the appropriate route
            else:
                # Incorrect password
                flash('Incorrect password', 'danger')
                return redirect('/login')
        else:
            # User not found
            flash('Incorrect email', 'danger')
            return redirect('/login')
    else:
        # Render login page
        if 'customer_id' in session:
            return redirect('/homepage')  # Replace with the appropriate route
        return render_template('login.html')

@auth.route('/logout')
def logout():
    # Logout logic here
    session.clear()
    return redirect('/login')






 
