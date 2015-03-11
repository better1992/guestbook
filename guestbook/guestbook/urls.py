from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r"^$", include('guestbookapp.urls')),
                       url(r'^guestbookapp/', include('guestbookapp.urls'))
)
