import os

from dotenv import load_dotenv
from flask import request, Blueprint
from twilio.twiml.messaging_response import MessagingResponse

from exceptions.Exceptions import ProgramError
from services.OperatorService import OperatorService

load_dotenv()

sms_route = Blueprint('sms', __name__)
operator = OperatorService(os.environ['FAUNS'])


@sms_route.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    resp = MessagingResponse()

    print(number)
    print(message_body)

    try:
        response = operator.handle(message_body, number)
        print(response)
        resp.message(response)
    except ProgramError as e:
        print(e)
        resp.message(f'Something went wrong: {e}')

    return str(resp)
