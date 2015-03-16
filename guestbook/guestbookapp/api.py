import json
import datetime
from django.http import HttpResponse
from django.views.generic import FormView
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.http import Http404

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
    form_class = SignForm

    # handle GET request: get list messages and return as JSON
    def get(self, *args, **kwargs):
        cursor = self.request.GET.get("cursor", None)
        guestbook_name = kwargs.get("guestbook_name")
        try:
            greetings, next_cursor, more = Greeting.get_latest(guestbook_name, 20, cursor)
        except StandardError:
            return Http404
        lst_greeting = []
        for greeting in greetings:
            item = {
                'id': str(greeting.key.id()),
                'author': str(greeting.author),
                'content': greeting.content,
                'date': str(greeting.date)
            }
            lst_greeting.append(item)

        data = {
            "guestbook_name": guestbook_name,
            "greetings": lst_greeting,
            "more": more,
            "next_cursor": str(next_cursor.urlsafe())
        }
        self.object = data
        return super(GreetingService, self).get(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.object

    # handle POST request: create message and return HttpStatus code
    def post(self, request, *args, **kwargs):
        return super(GreetingService, self).post(self, request, *args, **kwargs)

    @staticmethod
    def form_valid(form):
        guestbook_name = form.cleaned_data.get('guestbook_name')
        dict_parameter = {
            'guestbook_name': guestbook_name,
            'greeting_message': form.cleaned_data.get('greeting_message')
        }
        if Greeting.put_from_dict(dict_parameter):
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)

    @staticmethod
    def form_invalid():
        return HttpResponse(status=400)


class GreetingManageService(JSONResponseMixin, BaseDetailView, FormView):
    form_class = SignForm

    # handle GET request: get a message and return HttpStatus code
    def get_object(self):
        greeting_id = self.kwargs.get("id")
        guestbook_name = self.kwargs.get("guestbook_name")

        greeting = Greeting.get_greeting(guestbook_name, greeting_id)
        if greeting is None:
            return Http404

        data = {
            "greeting_id": str(greeting_id),
            "content": greeting.content,
            "date": str(greeting.date),
            "updated_by": str(greeting.author),
            "guestbook_name": guestbook_name
        }
        return data

    # handle PUT request: Edit a message and return HttpStatus code
    def put(self, request):
        request.POST = json.loads(request.body)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid()

    def form_valid(self, form):
        if users.get_current_user():
            updated_by = users.get_current_user().nickname()
        else:
            updated_by = None
        dict_parameter = {
            'guestbook_name': self.kwargs.get("guestbook_name"),
            'greeting_id': self.kwargs.get("greeting_id"),
            'content': form.cleaned_data["greeting_message"],
            'updated_by': updated_by,
            'updated_day': str(datetime.datetime.now().date())
        }

        if Greeting.edit_greeting(dict_parameter):
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)

    @staticmethod
    def form_invalid():
        return HttpResponse(status=400)

    # handle DELETE request: Delete a message and return HttpStatus code
    @staticmethod
    def delete(**kwargs):
        dict_parameter = {
            'greeting_id': kwargs.get("greeting_id"),
            'guestbook_name': kwargs.get("guestbook_name")
        }

        if Greeting.delete_greeting(dict_parameter):
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
