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
		dict = self.get_form_kwargs()

		dict['data'] = self.kwargs
		form = self.form_class(**dict)
		if not form.is_valid():
			return HttpResponse(status=400)

		guestbook_name = form.cleaned_data["guestbook_name"]
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

		form = self.get_form(self.form_class)
		if not form.is_valid():
			return HttpResponse(status=400)

		content = form.cleaned_data['greeting_message']
		guestbook_name = form.cleaned_data['guestbook_name']

		return GreetingService.create(guestbook_name=guestbook_name, content=content)


class GreetingSingleView(JSONResponseMixin, BaseDetailView, FormView):
	# handle GET request: get a message and return HttpStatus code
	def get_object(self, request, **kwargs):

		dict = self.get_form_kwargs()
		dict['data'] = kwargs
		form = self.form_class(**dict)
		if not form.is_valid():
			return HttpResponse(status=400)

		greeting_id = kwargs.get("id")
		guestbook_name = kwargs.get("guestbook_name")
		return GreetingService.get(guestbook_name=guestbook_name, pk=greeting_id)

	# handle PUT request: Edit a message and return HttpStatus code
	def put(self, request, **kwargs):
		try:
			json_object = json.loads(request.body)
		except ValueError:
			# invalid json
			request.POST = QueryDict(request.body)
		else:
			# valid json
			request.POST = json_object

		form = self.get_form(self.form_class)
		if not form.is_valid():
			return HttpResponse(status=400)

		greeting_id = form.cleaned_data["id"]
		guestbook_name = form.cleaned_data["guestbook_name"]
		content = form.cleaned_data["greeting_message"]
		updated_by = form.cleaned_data["updated_by"]

		return GreetingService.update(user=updated_by, guestbook_name=guestbook_name,
										content=content, pk=greeting_id)

	# handle DELETE request: Delete a message and return HttpStatus code
	def delete(self, request, *args, **kwargs):

		dict = self.get_form_kwargs()
		dict['data'] = kwargs
		form = self.form_class(**dict)
		if not form.is_valid():
			return HttpResponse(status=400)

		greeting_id = form.cleaned_data["id"]
		guestbook_name = form.cleaned_data["guestbook_name"]
		return GreetingService.delete(guestbook_name=guestbook_name, pk=greeting_id)
