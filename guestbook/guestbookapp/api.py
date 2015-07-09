import json

from django.http import HttpResponse, QueryDict
from django.views.generic import FormView
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from services import GreetingService


class JSONResponseMixin(object):
	def render_to_response(self, context, **response_kwargs):
		return self.get_json_response(self.convert_context_to_json(context), **response_kwargs)

	def get_json_response(self, content, **httpresponse_kwargs):
		return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

	def convert_context_to_json(self, context):
		return json.dumps(context)


class GreetingCollectionView(JSONResponseMixin, BaseListView, FormView):
	# handle GET request: get list messages and return as JSON
	def get_queryset(self):
		cursor = self.request.GET.get("cursor", None)
		guestbook_name = self.kwargs.get("guestbook_name")
		return GreetingService.list(guestbook_name=guestbook_name, cursor=cursor)

	# handle POST request: create message and return HttpStatus code
	def post(self, request, **kwargs):
		try:
			json_object = json.loads(request.body)
		except ValueError:
			# invalid json
			request.POST = QueryDict(request.body)
		else:
			# valid json
			request.POST = json_object
		content = request.POST.get('greeting_message')
		guestbook_name = kwargs.get('guestbook_name')
		return GreetingService.create(guestbook_name=guestbook_name, content=content)


class GreetingSingleView(JSONResponseMixin, BaseDetailView, FormView):
	# handle GET request: get a message and return HttpStatus code
	def get_object(self, request, **kwargs):
		greeting_id = kwargs.get("id")
		guestbook_name = kwargs.get("guestbook_name")
		return GreetingService.get(guestbook_name=guestbook_name, pk=greeting_id)

	# handle PUT request: Edit a message and return HttpStatus code
	def put(self, request, **kwargs):
		try:
			json_object = json.loads(request.body)
		except ValueError:
			# invalid json
			request.PUT = QueryDict(request.body)
		else:
			# valid json
			request.PUT = json.loads(request.body)
		guestbook_name = kwargs.get("guestbook_name")
		greeting_id = kwargs.get("id")
		content = request.PUT.get("greeting_message")
		return GreetingService.update(guestbook_name=guestbook_name, content=content,
										pk=greeting_id)

	# handle DELETE request: Delete a message and return HttpStatus code
	def delete(self, request, *args, **kwargs):
		id = kwargs.get("id"),
		guestbook_name = kwargs.get("guestbook_name")
		return GreetingService.delete(guestbook_name=guestbook_name, pk=id[0])
