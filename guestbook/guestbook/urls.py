from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
                       url(r"^$", include('guestbookapp.urls')),
                       url(r'^guestbookapp/', include('guestbookapp.urls'))
)
