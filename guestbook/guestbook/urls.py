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

<<<<<<< HEAD
    url(r'^admin/', include(admin.site.urls)),
	url(r"^$", MainView.as_view(),name="main"),
	url(r"^sign/$", SignView.as_view(),name="sign"),
	# url(r"^delete/$", GreetingDeleteView.as_view(),name="delete"),
	url(r"^edit/$", GreetingEditView.as_view(), name='edit'),
=======
	url(r"^$", include('guestbookapp.urls')),
	url(r'^guestbookapp/', include('guestbookapp.urls'))
>>>>>>> origin/feature/django-refactoring
	# url(r'^sign/$', sign_post),
) 
