from django.conf.urls import patterns, include, url
from django.contrib import admin
from guestbookapp.views import MainView,SignView,GreetingEditView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'guestbook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r"^$", MainView.as_view(),name="main"),
	url(r"^sign/$", SignView.as_view(),name="sign"),
	# url(r"^delete/$", GreetingDeleteView.as_view(),name="delete"),
	url(r"^edit/$", GreetingEditView.as_view(), name='edit'),
	# url(r'^sign/$', sign_post),
) 
