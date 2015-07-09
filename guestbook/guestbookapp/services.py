import json

from django.http import HttpResponse
from django.http import Http404

from models import Greeting, AppConstants

GUESTBOOK_NAME = AppConstants().get_default_guestbook_name

class GreetingService(object):

	# handle GET request: get list messages and return as JSON
	@classmethod
	def list(cls, guestbook_name=GUESTBOOK_NAME, limit=10, cursor=None, **kwargs):

		greetings, next_cursor, more = Greeting.get_latest(guestbook_name, limit, cursor)
		if greetings is None:
			return HttpResponse(status=404)
		lst_greeting = [greeting.to_dict() for greeting in greetings]

		if next_cursor is None:
			next_cursor_url = ''
		else:
			next_cursor_url = str(next_cursor.urlsafe())

		data = {
			"guestbook_name": guestbook_name,
			"greetings": lst_greeting,
			"more": more,
			"next_cursor": next_cursor_url
		}
		return data

	# handle POST request: create message and return HttpStatus code
	@classmethod
	def create(cls, guestbook_name=GUESTBOOK_NAME, content=None, **kwargs):
		import logging
		logging.warning(guestbook_name)
		if content is None:
			return HttpResponse(status=400)
		dict_parameter = {
			'guestbook_name': guestbook_name,
			'greeting_message': content
		}
		if Greeting.put_from_dict(dict_parameter):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	# handle GET request: get a message and return HttpStatus code
	@classmethod
	def get(self, guestbook_name=GUESTBOOK_NAME, pk=None):

		greeting = Greeting.get_greeting(guestbook_name, pk)
		if greeting is None:
			return Http404

		data = greeting.to_dict()
		data['guestbook_name'] = guestbook_name
		return data

	# handle PUT request: Edit a message and return HttpStatus code
	@classmethod
	def update(cls, guestbook_name=GUESTBOOK_NAME, pk=None, content=None, **kwargs):

		dict_parameter = {
			'guestbook_name': guestbook_name,
			'greeting_id': pk,
			'greeting_message': content,
		}

		if Greeting.edit_greeting(dict_parameter):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	# handle DELETE request: Delete a message and return HttpStatus code
	@classmethod
	def delete(cls, guestbook_name=GUESTBOOK_NAME, pk=None):
		dict_parameter = {
			'id': pk,
			'guestbook_name': guestbook_name
		}

		if Greeting.delete_greeting(dict_parameter):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)
