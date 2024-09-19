import os
from google.cloud import dialogflow_v2 as dialogflow
from flask import Flask, request, jsonify
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument

app = Flask(__name__)

# Set your Google Cloud Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "insert json file location here"

# Dialogflow project ID
DIALOGFLOW_PROJECT_ID = 'insert project id here'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

# Route for receiving user queries and sending them to Dialogflow
@app.route('/query', methods=['POST'])
def query_dialogflow():
    try:
        user_input = request.json.get('text')
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

        # TextInput dialogflow query
        text_input = dialogflow.types.TextInput(text=user_input, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)

        bot_reply = response.query_result.fulfillment_text
        return jsonify({"response": bot_reply})
    
    except InvalidArgument as e:
        return jsonify({"response": "Sorry, something went wrong"}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
