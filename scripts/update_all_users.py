import os

from faunadb.client import FaunaClient
from faunadb import query as q

def update_all_users():
	client = FaunaClient(os.environ['FAUNS'])
	users = client.query(
		q.paginate(q.match(q.index('all_users')))
	)
	pass

#TODO: write a script that pulls all users in a collection, updates the data to include permissions