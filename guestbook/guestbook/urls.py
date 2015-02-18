from django.conf.urls import patterns, include, url
<<<<<<< HEAD
from django.contrib import admin
from guestbookapp.views import MainView,SignView,GreetingEditView
=======

>>>>>>> origin/feature/django-refactoring
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'guestbook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


	url(r"^$", include('guestbookapp.urls')),
	url(r'^guestbookapp/', include('guestbookapp.urls'))

	# url(r'^sign/$', sign_post),
) 
