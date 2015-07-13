from django.views.generic import TemplateView

from google.appengine.api import users

from models import AppConstants


class DojoView(TemplateView):
	template_name = 'dojo.html'

	def get_context_data(self):
		guestbook_name = self.request.GET.get('guestbook_name',
											AppConstants().get_default_guestbook_name)

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
			'guestbook_name': guestbook_name
		}

		return template_values
