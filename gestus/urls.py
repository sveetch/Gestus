# -*- coding: utf-8 -*-
"""
Root url's map for application
"""
from django.conf.urls import *

from gestus import views

urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    
    url(r'^websites/$', views.WebsiteIndex.as_view(), name='website-list'),
    url(r'^websites/(?P<pk>\d+)/$', views.WebsiteDetail.as_view(), name='website-detail'),
    
    url(r'^environments/$', views.EnvironmentIndex.as_view(), name='environment-list'),
    url(r'^environments/(?P<pk>\d+)/$', views.EnvironmentDetail.as_view(), name='environment-detail'),
    
    url(r'^eggs/$', views.EggIndex.as_view(), name='egg-list'),
    url(r'^eggs/(?P<pk>\d+)/$', views.EggDetail.as_view(), name='egg-detail'),
    
    url(r'^servers/$', views.ServerIndex.as_view(), name='server-list'),
    url(r'^servers/(?P<hash64>[-=\w]+)/$', views.ServerDetail.as_view(), name='server-detail'),
)

"""
Urls map for API with Django REST Framework if installed
"""
try:
    from rest_framework.urlpatterns import format_suffix_patterns
except ImportError:
    pass
else:
    from gestus.rest import views as api_views

    rest_urlpatterns = format_suffix_patterns(patterns('gestus.rest.views',
        url(r'^rest/$', 'api_root'),
        
        url(r'^rest/websites/$', api_views.WebsiteList.as_view(), name='api-website-list'),
        url(r'^rest/websites/(?P<pk>\d+)/$', api_views.WebsiteDetail.as_view(), name='api-website-detail'),
        
        url(r'^rest/environments/$', api_views.WebsiteEnvironmentList.as_view(), name='api-environment-list'),
        url(r'^rest/environments/(?P<pk>\d+)/$', api_views.WebsiteEnvironmentDetail.as_view(), name='api-environment-detail'),
        
        url(r'^rest/eggs/$', api_views.EggList.as_view(), name='api-egg-list'),
        url(r'^rest/eggs/(?P<pk>\d+)/$', api_views.EggDetail.as_view(), name='api-egg-detail'),
    ))

    urlpatterns = rest_urlpatterns + urlpatterns
