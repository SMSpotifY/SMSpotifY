import os
from dotenv import load_dotenv
from exceptions.Exceptions import ProgramError
from services.OperatorService import OperatorService
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

# SETUP

fauna_secret = os.environ['FAUNA_SECRET']
operator = OperatorService(fauna_secret)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_auth_info = (account_sid, auth_token)

# Web App

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
	number = request.form['From']
	message_body = request.form['Body']
	resp = MessagingResponse()

	try:
		response = operator.handle(message_body, number)
		print(response)
		resp.message(response)
	except ProgramError as e:
		print(e)
		resp.message(f'Something went wrong: {e}')

	return str(resp)

if __name__ == '__main__':
	app.run()