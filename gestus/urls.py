# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls import *

from gestus.views import Index

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
)

"""
Urls map for API with Django REST Framework if installed
"""
try:
    from rest_framework.urlpatterns import format_suffix_patterns
except ImportError:
    pass
else:
    from gestus.rest import views

    rest_urlpatterns = format_suffix_patterns(patterns('gestus.rest.views',
        url(r'^rest/$', 'api_root'),
        
        url(r'^rest/websites/$', views.WebsiteList.as_view(), name='api-website-list'),
        url(r'^rest/websites/(?P<pk>\d+)/$', views.WebsiteDetail.as_view(), name='api-website-detail'),
        
        url(r'^rest/environments/$', views.WebsiteEnvironmentList.as_view(), name='api-environment-list'),
        url(r'^rest/environments/(?P<pk>\d+)/$', views.WebsiteEnvironmentDetail.as_view(), name='api-environment-detail'),
        
        url(r'^rest/eggs/$', views.EggList.as_view(), name='api-egg-list'),
        url(r'^rest/eggs/(?P<pk>\d+)/$', views.EggDetail.as_view(), name='api-egg-detail'),
    ))

    urlpatterns = rest_urlpatterns + urlpatterns
