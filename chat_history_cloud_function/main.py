from google.cloud import datastore
from flask import jsonify, request

# Create a Datastore client
client = datastore.Client()

def store_conversation(request):
    try:
        # Parse incoming conversation data from JSON in the request body
        conversation_data = request.get_json()

        # Create a new conversation entity
        conversation_entity = datastore.Entity(client.key('Conversation'))
        conversation_entity['conversation'] = conversation_data['conversation']

        # Save the conversation entity to Datastore
        client.put(conversation_entity)

        response = {
            "status": "success",
            "message": "Conversation stored successfully"
        }
        return jsonify(response), 200
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return jsonify(response), 500
