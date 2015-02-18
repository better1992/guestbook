from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django import forms
from google.appengine.api import users
import time
from guestbookapp.models import Greeting, Guestbook, DEFAULT_GUESTBOOK_NAME

import urllib



class MainView(TemplateView):
	template_name = "main_page.html"
	
	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greetings = Greeting.get_latest(guestbook_name, 10)
		# greeting = Greeting()
		# greetings = greeting.get_latest(guestbook_name,10)
	
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
			'guestbook_name': guestbook_name
		}

		return template_values;


class SignForm(forms.Form):
	guestbook_name = forms.CharField(
		label="Guestbook Name",
		max_length=10,
		required=True,
		widget=forms.TextInput()
	)
	greeting_message = forms.CharField(
		label = "Greeting Massage",
		max_length=50,
		required=True,
		widget=forms.Textarea()
	)
	

class SignView(FormView):
	template_name = "greeting.html"
	form_class = SignForm
	def form_valid(self, form):
		time.sleep(0.01)
		return redirect("/?guestbook_name="+Greeting.put_from_dict(form.cleaned_data))
	
