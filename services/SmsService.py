from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

class SmsService:
	def __init__(self, twilio_auth_info):
		self.auth = twilio_auth_info
		self.client = Client(twilio_auth_info.0, twilio_auth_info.1)

	def run(self):
		app = Flask(__name__)

		@app.route('/sms', methods=['POST'])
		def sms():
			number = request.form['From']
			message_body = request.form['Body']

			resp = MessagingResponse()
			resp.message('Hello {}, you said: {}'.format(number, message_body))
			return str(resp)
