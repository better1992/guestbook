import json

from django.http import HttpResponse
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
		return GreetingService.list(self.request, self.kwargs)

	# handle POST request: create message and return HttpStatus code
	def post(self, request, **kwargs):
		return GreetingService.post(request, **kwargs)


class GreetingSingleView(JSONResponseMixin, BaseDetailView, FormView):

	# handle GET request: get a message and return HttpStatus code
	def get_object(self, request, **kwargs):
		return GreetingService.get(request, **kwargs)

	# handle PUT request: Edit a message and return HttpStatus code
	def put(self, request, **kwargs):
		return GreetingService.put(request, **kwargs)

	# handle DELETE request: Delete a message and return HttpStatus code
	def delete(self, request, *args, **kwargs):
		return GreetingService.delete(**kwargs)
