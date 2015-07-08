import json

from django.http import HttpResponse
from django.http import Http404, QueryDict

from models import Greeting


class GreetingService(object):

	# handle GET request: get list messages and return as JSON
	@classmethod
	def list(cls, request, kwargs):
		cursor = request.GET.get("cursor", None)
		guestbook_name = kwargs.get("guestbook_name")
		greetings, next_cursor, more = Greeting.get_latest(guestbook_name, 20, cursor)
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
	def post(cls, request, **kwargs):
		try:
			json_object = json.loads(request.body)
		except ValueError:
			# invalid json
			request.POST = QueryDict(request.body)
		else:
			# valid json
			request.POST = json_object

		guestbook_name = kwargs.get('guestbook_name')
		if (guestbook_name is None) | (request.POST.get('greeting_message') is None):
			return HttpResponse(status=400)
		dict_parameter = {
			'guestbook_name': guestbook_name,
			'greeting_message': request.POST.get('greeting_message')
		}

		if Greeting.put_from_dict(dict_parameter):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	# handle GET request: get a message and return HttpStatus code
	@classmethod
	def get(cls, **kwargs):
		greeting_id = kwargs.get("id")
		guestbook_name = kwargs.get("guestbook_name")

		greeting = Greeting.get_greeting(guestbook_name, greeting_id)
		if greeting is None:
			return Http404

		data = greeting.to_dict()
		data['guestbook_name'] = guestbook_name
		return data

	# handle PUT request: Edit a message and return HttpStatus code
	@classmethod
	def put(cls, request, **kwargs):
		try:
			json_object = json.loads(request.body)
		except ValueError:
			# invalid json
			request.PUT = QueryDict(request.body)
		else:
			# valid json
			request.PUT = json.loads(request.body)

		dict_parameter = {
			'guestbook_name': kwargs.get("guestbook_name"),
			'greeting_id': kwargs.get("id"),
			'greeting_message': request.PUT.get("greeting_message"),
			'updated_by': request.PUT.get('updated_by'),
		}

		if Greeting.edit_greeting(dict_parameter):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	# handle DELETE request: Delete a message and return HttpStatus code
	@classmethod
	def delete(cls, **kwargs):
		dict_parameter = {
			'id': kwargs.get("id"),
			'guestbook_name': kwargs.get("guestbook_name")
		}

		if Greeting.delete_greeting(dict_parameter):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)
