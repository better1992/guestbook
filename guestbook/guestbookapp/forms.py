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
	id = forms.CharField(required=False)
	greeting_message = forms.CharField(
		label="Greeting Massage",
		max_length=10,
		required=False,
		widget=forms.TextInput()
	)
	updated_by = forms.CharField(required=False)