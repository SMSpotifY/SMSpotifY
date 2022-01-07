import os
from dotenv import load_dotenv
from exceptions.Exceptions import ProgramError
from services.OperatorService import OperatorService
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

# SETUP

file = 'tekore.cfg'
fauna_secret = os.environ['FAUNA_SECRET']
operator = OperatorService(file, fauna_secret)

# Web App

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
	number = request.form['From']
	message_body = request.form['Body']
	resp = MessagingResponse()

	try:
		response = operator.handle(message_body, number)
		resp.message(response)
	except ProgramError as e:
		resp.message(f'Something went wrong: {e}')

	return str(resp)

if __name__ == '__main__':
	app.run()