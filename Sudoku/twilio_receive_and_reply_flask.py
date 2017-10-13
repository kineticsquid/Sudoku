# This is a copy of welcome.py in JKsTwilioApp project

import os
from flask import Flask, jsonify, request, redirect
from twilio.twiml.messaging_response import MessagingResponse, Message, Body, Redirect
import json

app = Flask(__name__)

@app.route('/')
def WelcomeToMyapp():
    return 'Welcome again to my Twilio app running on Bluemix!'

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    try:
        account_sid = "ACefa1096c033ccd122b24a0480cfb21c5"
        auth_token = "4d965a0c6fd26c27070ccf849f817ac4"

        request_headers = str(request.headers)
        request_data = str(request.data)
        incoming_number = request.form['From']
        incoming_message = request.form['Body']

        print('Request data: \n%s\n' % request_data)
        print('Request headers: \n%s\n' % request_headers)

        response = MessagingResponse()
        response.message('%s from %s' % (incoming_message, incoming_number))

        print(response)

        return str(response)
    except Exception as error:
        return {"error": str(error)}

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
