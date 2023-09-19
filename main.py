import os
from website import create_app

# Get the directory of the current script
#dir_path = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path of the credentials file in the secrets directory
#credentials_path = os.path.join(dir_path, 'secrets', 'credentials.json')

# Set the environment variable to the credentials file path
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path 

# Create and run the Flask app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
