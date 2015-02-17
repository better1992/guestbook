from django.conf.urls import patterns, include, url
from guestbookapp.views import MainView,SignView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'guestbook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r"^$", MainView.as_view(),name="main"),
	url(r'^guestbook/', include('guestbook.urls')),
	# url(r'^sign/$', sign_post),
) 
