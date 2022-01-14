from faunadb import query as q
from faunadb.client import FaunaClient

from operator import itemgetter
from exceptions.Exceptions import UnrecognizedRequestException

from exceptions.Exceptions import MoreThanOneUserFoundException, UserNotFoundException


class FaunaService:
	def __init__(self, FAUNS):
		self.client = FaunaClient(
			secret = FAUNS,
			domain = 'db.us.fauna.com',
			scheme = 'https'
		)

	def handle(self, request):
		request_types = {
			'get_user_by_phone': self.get_user_by_phone_number,
			'get_users': self.get_users,
			'create_user': self.create_new_user
		}

		if request['request_type'] in request_types:
			return request_types[request['request_type']](request['data'])
		else:
			raise UnrecognizedRequestException('This type of request isn\'t recognised :(')

	# returns a list of references to user documents
	def get_users(self):
		result = self.client.query(
			q.paginate(q.match(q.index('all_users')))
		)['data']
		users = []
		for user in result:
			users.append(self.client.query(
				q.get(user)
			)['data'])
		return users

	# returns a users information as a dict
	def get_user_by_phone_number(self, number):
		phone_number = self._normalise_phone_number(number)
		result = self.client.query(
			q.paginate(q.match(q.index('users_by_number'), phone_number))
		)['data']
		if len(result) > 1:
			raise MoreThanOneUserFoundException(f'{len(result)} users found with phone number: {phone_number}')
		elif len(result) < 1:
			raise UserNotFoundException(f'No user was found with phone number: {phone_number}')
		else:
			ref = result[0]
			user_result = self.client.query(
				q.get(ref)
			)
			return user_result['data']

	# registers a new user
	def create_new_user(self, request_data):
		name, number, role = itemgetter('name', 'number', 'role')(request_data)
		result = self.client.query(
			q.create(
				q.collection('users'),
				{'data': {
					'name': name,
					'number': number,
					'role': role
				}}
			)
		)

		return "The following user has been created: {} with the following attributes: {}".format(result['ref'], {name, number, role})

	# adds +1 to the start of phone number if it doesn't already have it
	@staticmethod
	def _normalise_phone_number(number):
		phone_number = number
		if not number.startswith('+1'):
			phone_number = f'+1{number}'
		return phone_number
