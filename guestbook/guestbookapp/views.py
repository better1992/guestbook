from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django import forms
from google.appengine.ext import ndb
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
			'isAdmin' : users.is_current_user_admin(),
			'currentUser' : users.get_current_user(),
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
	greeting_id = forms.CharField(max_length=2000, widget=forms.HiddenInput, required=False)

class SignView(FormView):

		template_name = "greeting.html"
		form_class = SignForm
		def form_valid(self, form):
			time.sleep(0.01)
			return redirect("/?guestbook_name="+Greeting.put_from_dict(form.cleaned_data))
	
   
	
class GreetingEditView(FormView):
	template_name = "edit.html"
	form_class = SignForm
	
	def get_initial(self):
		initial = super(GreetingEditView, self).get_initial()
		
		greeting_id = self.request.GET.get("id")
		guestbook_name = self.request.GET.get("guestbook_name")
		if  guestbook_name: 
			greeting = Greeting.get_greeting(guestbook_name,greeting_id)
			initial["guestbook_name"] = guestbook_name
			initial["greeting_message"] = greeting.content
			initial["greeting_id"] = int(greeting_id)
		return initial
	
	def form_valid(self, form):
		time.sleep(0.01)
		return redirect("/?guestbook_name="+Greeting.edit_greeting(form.cleaned_data))
	
  


