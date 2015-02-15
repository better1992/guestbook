from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django import forms
from google.appengine.api import users
import time
from guestbookapp.models import Greeting, Guestbook,guestbook_key, DEFAULT_GUESTBOOK_NAME

import urllib



class MainView(TemplateView):
    template_name = "main_page.html"
    
    def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		#greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings_query = Greeting.query().order(-Greeting.date)
		greetings = greetings_query.fetch(10)
	
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
		
		self.add_greeting(form)	
		time.sleep(0.5)
		return redirect("main")
	
    def add_greeting(self, form):
		guestbook_name = form.cleaned_data["guestbook_name"]
		guestbook_query = Guestbook.query()
		guestbooks = guestbook_query.fetch()
		greeting = Greeting(parent=guestbook_key(guestbook_name))
		guestbook = None
		for temp in guestbooks:
			if temp.name == guestbook_name:
				guestbook = temp
				break
		if guestbook is None:
			guestbook = Guestbook()
			guestbook.name = guestbook_name
			guestbook.put()
    	
		if users.get_current_user():
			greeting.author = users.get_current_user()
    
		greeting.content = form.cleaned_data["greeting_message"]
		greeting.guestbook = guestbook
		greeting.put()
		
	
