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
<<<<<<< HEAD
		#greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings_query = Greeting.query().order(-Greeting.date)
		greetings = greetings_query.fetch(10)
		guestbooks = Guestbook.query().fetch()
		
=======
		greetings = Greeting.get_latest(guestbook_name, 10)
		# greeting = Greeting()
		# greetings = greeting.get_latest(guestbook_name,10)
	
>>>>>>> origin/feature/django-refactoring
		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'

		template_values = {
			'greetings': greetings,
			'guestbooks': guestbooks,
			'url': url,		
			'url_linktext': url_linktext,
<<<<<<< HEAD
			'isAdmin' : users.is_current_user_admin(),
			'currentUser' : users.get_current_user(),
=======
			'guestbook_name': guestbook_name
>>>>>>> origin/feature/django-refactoring
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
<<<<<<< HEAD
    template_name = "greeting.html"
    form_class = SignForm
	
    def form_valid(self, form):
		self.add_greeting(form)	
		time.sleep(0.5)
		return redirect("main")
	
    def add_greeting(self, form):
		guestbook_name = form.cleaned_data["guestbook_name"]
		guestbooks = Guestbook.query(Guestbook.name==guestbook_name).get()
		greeting = Greeting()
			
		if guestbooks is None:
			guestbook = Guestbook()
			guestbook.name = guestbook_name
			guestbook.put()
		else:
			guestbook = guestbooks
    	
		if users.get_current_user():
			greeting.author = users.get_current_user()
    
		greeting.content = form.cleaned_data["greeting_message"]
		greeting.guestbook = guestbook
		greeting.put()
	
class GreetingEditView(FormView):
    template_name = "edit.html"
    form_class = SignForm
    
    def get_initial(self):
		initial = super(GreetingEditView, self).get_initial()
		
		greeting_id = self.request.GET.get("id")
		greeting = Greeting.query(Greeting.key==ndb.Key("Greeting", int(greeting_id))).get()
		#greeting = greeting.filter(Greeting.key == ndb.Key("Greeting", greeting_id)).get()
		
		initial["guestbook_name"] = greeting.guestbook.name
		initial["greeting_message"] = greeting.content
		initial["greeting_id"] = int(greeting_id)
		
		return initial
=======
	template_name = "greeting.html"
	form_class = SignForm
	def form_valid(self, form):
		time.sleep(0.01)
		return redirect("/?guestbook_name="+Greeting.put_from_dict(form.cleaned_data))
>>>>>>> origin/feature/django-refactoring
	
    def form_valid(self, form):
		self.edit_greeting(form)	
		time.sleep(0.5)
		return redirect('main')
	
    def edit_greeting(self, form):
    	greeting_id = form.cleaned_data["greeting_id"]
    	greeting_content = form.cleaned_data["greeting_message"]
    	guestbook_name = form.cleaned_data["guestbook_name"]
    	
    	guestbook = Guestbook.query(Guestbook.name == guestbook_name).get()
    	if guestbook is None:
			guestbook = Guestbook()
			guestbook.name = guestbook_name
			guestbook.put()
        greeting = Greeting.query(Greeting.key==ndb.Key("Greeting", int(greeting_id))).get()
        greeting.content = greeting_content
        greeting.guestbook = guestbook
        greeting.put()


