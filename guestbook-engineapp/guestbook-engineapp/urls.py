from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.defaults import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('guestbook.urls')),
)

