from django import forms
from django.forms import BaseForm
from models import AppConstants


class SignForm(forms.Form, BaseForm):

	guestbook_name = forms.CharField(
		label="Guestbook Name",
		max_length=10,
		required=True,
		widget=forms.TextInput(attrs={'value': AppConstants().get_default_guestbook_name})
	)
	greeting_message = forms.CharField(
		label="Greeting Massage",
		max_length=10,
		required=True,
		widget=forms.TextInput()
	)
