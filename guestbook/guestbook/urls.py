from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'guestbook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r"^$", include('guestbookapp.urls')),
	url(r'^guestbookapp/', include('guestbookapp.urls'))
	# url(r'^sign/$', sign_post),
) 
