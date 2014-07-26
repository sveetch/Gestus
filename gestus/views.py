# -*- coding: utf-8 -*-
"""
Views
"""
import base64

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.views import generic

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from gestus.models import Website, WebsiteEnvironment, Egg, EggVersion

LAST_MODIFIED_WEBSITES_MAX = 12
LAST_MODIFIED_ENVIRONMENT_MAX = 12
LAST_MODIFIED_EGGS_MAX = 12
TOPRANK_SERVERS_MAX = 6

INDEX_LIST_MAX = 24


class EnvironmentServerMixin(object):
    """
    A mixin to contain the base queryset to use to get a distinct server list 
    used in environments
    """
    def get_server_queryset(self, filter_kwargs={}):
        return WebsiteEnvironment.objects.filter(**filter_kwargs).values("server").annotate(num_environment=models.Count("pk")).order_by('-num_environment')
    
    def get_server_list(self):
        servers = self.get_server_queryset()
        for item in servers:
            item['hash64'] = base64.urlsafe_b64encode(item['server'])
        return servers


class Index(LoginRequiredMixin, EnvironmentServerMixin, generic.TemplateView):
    """
    Gestus index to display data resumes
    """
    template_name = "gestus/index.html"
    
    def get_server_queryset(self, *args, **kwargs):
        return super(Index, self).get_server_queryset(*args, **kwargs)[:TOPRANK_SERVERS_MAX]
        
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context.update({
            'website_list' : Website.objects.all().order_by('-modified', 'name')[0:LAST_MODIFIED_WEBSITES_MAX],
            'environment_list' : WebsiteEnvironment.objects.all().select_related().order_by('-modified', 'name')[0:LAST_MODIFIED_ENVIRONMENT_MAX],
            'eggs_list' : Egg.objects.all().order_by('-modified', 'name')[0:LAST_MODIFIED_EGGS_MAX],
            #'server_list' : self.get_server_queryset()[:TOPRANK_SERVERS_MAX],
            'server_list' : self.get_server_list(),
        })
        return context


class CommonIndexBase(LoginRequiredMixin, generic.ListView):
    paginate_by = INDEX_LIST_MAX
    
    def get_queryset(self):
        return self.model.objects.all().order_by('name')


class WebsiteIndex(CommonIndexBase):
    model = Website
    template_name = "gestus/website_index.html"

class WebsiteDetail(LoginRequiredMixin, generic.DetailView):
    model = Website
    template_name = "gestus/website_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(WebsiteDetail, self).get_context_data(**kwargs)
        
        envs = self.object.environments.all().values_list('id', flat=True)
        
        # TODO: does this need to be distincted ?
        used_eggs = EggVersion.objects.filter(websiteenvironment__in=envs).select_related().order_by('egg__name')
        
        context.update({
            'used_eggs': used_eggs
        })
        return context


class EnvironmentIndex(CommonIndexBase):
    model = WebsiteEnvironment
    template_name = "gestus/environment_index.html"
    
    def get_queryset(self):
        return super(EnvironmentIndex, self).get_queryset().select_related()

class EnvironmentDetail(LoginRequiredMixin, generic.DetailView):
    model = WebsiteEnvironment
    template_name = "gestus/environment_detail.html"


class EggIndex(CommonIndexBase):
    model = Egg
    template_name = "gestus/egg_index.html"

class EggDetail(LoginRequiredMixin, generic.DetailView):
    model = Egg
    template_name = "gestus/egg_detail.html"


class ServerIndex(LoginRequiredMixin, EnvironmentServerMixin, generic.TemplateView):
    """
    List all knowed server for environments
    """
    template_name = "gestus/server_index.html"
    
    def get_server_list(self):
        servers = self.get_server_queryset()
        for item in servers:
            item['hash64'] = base64.urlsafe_b64encode(item['server'])
        return servers
    
    def get_context_data(self, **kwargs):
        context = super(ServerIndex, self).get_context_data(**kwargs)
        context.update({
            'server_list' : self.get_server_list(),
        })
        return context

class ServerDetail(LoginRequiredMixin, EnvironmentServerMixin, generic.TemplateView):
    """
    Server details
    """
    template_name = "gestus/server_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(ServerDetail, self).get_context_data(**kwargs)
        
        hostname = base64.urlsafe_b64decode(str(kwargs['hash64']))
        
        servers = self.get_server_queryset(filter_kwargs={'server': hostname})
        if not servers:
            raise Http404('There is no entry for server: {0}'.format(hostname) )
        
        context.update({
            'server' : servers[0],
            'environment_list' : WebsiteEnvironment.objects.filter(server=hostname).order_by('-modified', 'name').select_related(),
        })
        return context
