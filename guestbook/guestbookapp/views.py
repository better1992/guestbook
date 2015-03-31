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
		guestbookName = self.request.GET.get('guestbookName',
											  AppConstants().get_default_guestbookName)
		cursor = self.request.GET.get("cursor", None)
		greetings, next_cursor, more = Greeting.get_latest(guestbookName, 20, cursor)

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
			'guestbookName': guestbookName
		}

		return template_values


class SignForm(forms.Form):
	guestbookName = forms.CharField(
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
		guestbookName = form.cleaned_data['guestbookName']
		if Greeting.put_from_dict(form.cleaned_data):
			return redirect("/?guestbookName=" + guestbookName)
		else:
			return render_to_response(self.template_name, {'error': 'Have something wrong!'},
									  RequestContext(self.request))


class GreetingEditView(FormView):
	template_name = "edit.html"
	form_class = SignForm

	def get_initial(self):
		initial = super(GreetingEditView, self).get_initial()

		greeting_id = self.request.GET.get("id")
		guestbookName = self.request.GET.get("guestbookName")
		if guestbookName:
			greeting = Greeting.get_greeting(guestbookName, greeting_id)
			initial["guestbookName"] = guestbookName
			initial["greeting_message"] = greeting.content
			try:
				initial["greeting_id"] = int(greeting_id)
			except ValueError:
				raise ValueError('ID of greeting is not a number!')
		return initial

	def form_valid(self, form):
		guestbookName = form.cleaned_data['guestbookName']
		if Greeting.edit_greeting(form.cleaned_data):
			return redirect("/?guestbookName=" + guestbookName)
		else:
			return render_to_response(self.template_name,
									  {'error': 'Have something wrong!'},
									  RequestContext(self.request))


class GreetingDeleteView(View):
	def get(self, request):
		dictionary = request.GET
		guestbookName = dictionary.get("guestbookName")
		if Greeting.delete_greeting(dictionary):
			return render_to_response('main_page.html',
									  {'error': 'Have something wrong!'},
									  RequestContext(self.request))
		else:
			return redirect("/?guestbookName=" + guestbookName)


class DojoView(TemplateView):
	template_name = 'dojo.html'

	def get_context_data(self):
		guestbookName = self.request.GET.get('guestbookName',
											  AppConstants().get_default_guestbookName)
		#cursor = self.request.GET.get("cursor", None)
		#greetings, next_cursor, more = Greeting.get_latest(guestbookName, 20, cursor)

		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'

		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'isAdmin': users.is_current_user_admin(),
			'currentUser': users.get_current_user(),
		    'guestbookName': guestbookName
		}

		return template_values
