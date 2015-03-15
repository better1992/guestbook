from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django import forms
from django.core.context_processors import csrf
from django.template import RequestContext

from google.appengine.api import users

from models import Greeting, AppConstants


class MainView(TemplateView):
    template_name = "main_page.html"

    def get_context_data(self):
        guestbook_name = self.request.GET.get('guestbook_name',
                                              AppConstants().get_default_guestbook_name)
        cursor = self.request.GET.get("cursor", None)
        greetings, next_cursor, more = Greeting.get_latest(guestbook_name, 20, cursor)

        if users.get_current_user():
            url = users.create_logout_url(self.request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.get_full_path())
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            'isAdmin': users.is_current_user_admin(),
            'currentUser': users.get_current_user(),
            'guestbook_name': guestbook_name
        }

        return template_values


class SignForm(forms.Form):
    guestbook_name = forms.CharField(
        label="Guestbook Name",
        max_length=10,
        required=True,
        widget=forms.TextInput()
    )
    greeting_message = forms.CharField(
        label="Greeting Massage",
        max_length=50,
        required=True,
        widget=forms.Textarea()
    )
    greeting_id = forms.CharField(max_length=2000, widget=forms.HiddenInput, required=False)


class SignView(FormView):
    template_name = "greeting.html"
    form_class = SignForm

    def form_valid(self, form):
        guestbook_name = form.cleaned_data['guestbook_name']
        if Greeting.put_from_dict(form.cleaned_data):
            return redirect("/?guestbook_name=" + guestbook_name)
        else:
            return render_to_response(self.template_name,
                                      {'error': 'Have something wrong!'},
                                      RequestContext(self.request))


class GreetingEditView(FormView):
    template_name = "edit.html"
    form_class = SignForm

    def get_initial(self):
        initial = super(GreetingEditView, self).get_initial()

        greeting_id = self.request.GET.get("id")
        guestbook_name = self.request.GET.get("guestbook_name")
        if guestbook_name:
            greeting = Greeting.get_greeting(guestbook_name, greeting_id)
            initial["guestbook_name"] = guestbook_name
            initial["greeting_message"] = greeting.content
            try:
                initial["greeting_id"] = int(greeting_id)
            except ValueError:
                raise ValueError('ID of greeting is not a number!')
        return initial

    def form_valid(self, form):
        guestbook_name = form.cleaned_data['guestbook_name']
        if Greeting.edit_greeting(form.cleaned_data):
            return redirect("/?guestbook_name=" + guestbook_name)
        else:
            return render_to_response(self.template_name,
                                      {'error': 'Have something wrong!'},
                                      RequestContext(self.request))


class GreetingDeleteView(View):

    def get(self, request):
        dictionary = request.GET
        guestbook_name = dictionary.get("guestbook_name")
        if Greeting.delete_greeting(dictionary):
            return render_to_response('main_page.html',
                                      {'error': 'Have something wrong!'},
                                      RequestContext(self.request))
        else:
            return redirect("/?guestbook_name=" + guestbook_name)