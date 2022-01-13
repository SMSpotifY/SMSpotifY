import os

from dotenv import load_dotenv

from webapp.WebServer import app

load_dotenv()

# SETUP

account_sid = os.environ['TWILIO_ACCOUNT_SID']
FAUNS = os.environ['FAUNS']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

twilio_auth_info = (account_sid, auth_token)

if __name__ == '__main__':
	app.run(port=8080)