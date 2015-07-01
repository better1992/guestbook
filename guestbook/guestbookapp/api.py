import json
import datetime
from django.http import HttpResponse
from django.views.generic import FormView
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.http import Http404, QueryDict

from google.appengine.api import users

from models import Greeting
from views import SignForm

class JSONResponseMixin(object):
	def render_to_response(self, context, **response_kwargs):
		return self.get_json_response(self.convert_context_to_json(context), **response_kwargs)

	def get_json_response(self, content, **httpresponse_kwargs):
		return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

	def convert_context_to_json(self, context):
		return json.dumps(context)


class GreetingService(JSONResponseMixin, BaseListView, FormView):

	# handle GET request: get list messages and return as JSON
	def get_queryset(self):
		cursor = self.request.GET.get("cursor", None)
		guestbook_name = self.kwargs.get("guestbook_name")

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
	def post(self, request, *args, **kwargs):
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

	# @staticmethod
	# def form_valid(form):
	# 	guestbook_name = form.cleaned_data.get('guestbook_name')
	# 	dict_parameter = {
	# 		'guestbook_name': guestbook_name,
	# 		'greeting_message': form.cleaned_data.get('greeting_message')
	# 	}
	# 	if Greeting.put_from_dict(dict_parameter):
	# 		return HttpResponse(status=204)
	# 	else:
	# 		return HttpResponse(status=404)
	#
	# @staticmethod
	# def form_invalid():
	# 	return HttpResponse(status=400)


class GreetingManageService(JSONResponseMixin, BaseDetailView, FormView):

	# handle GET request: get a message and return HttpStatus code
	def get_object(self):
		greeting_id = self.kwargs.get("id")
		guestbook_name = self.kwargs.get("guestbook_name")

		greeting = Greeting.get_greeting(guestbook_name, greeting_id)
		if greeting is None:
			return Http404

		data = greeting.to_dict()
		data['guestbook_name'] = guestbook_name
		return data

	# handle PUT request: Edit a message and return HttpStatus code
	def put(self, request, *args, **kwargs):
		try:
			json_object = json.loads(request.body)
		except ValueError:
			# invalid json
			request.PUT = QueryDict(request.body)
		else:
			# valid json
			request.PUT = json.loads(request.body)

		dict_parameter = {
			'guestbook_name': self.kwargs.get("guestbook_name"),
			'greeting_id': self.kwargs.get("id"),
			'greeting_message': request.PUT.get("greeting_message"),
			'updated_by': request.PUT.get('updated_by'),
		}

		if Greeting.edit_greeting(dict_parameter):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)


	# handle DELETE request: Delete a message and return HttpStatus code
	def delete(self, request, *args, **kwargs):
		dict_parameter = {
			'id': kwargs.get("id"),
			'guestbook_name': kwargs.get("guestbook_name")
		}

		if Greeting.delete_greeting(dict_parameter):
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)
