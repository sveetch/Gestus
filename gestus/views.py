# -*- coding: utf-8 -*-
"""
Views
"""
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

INDEX_LIST_MAX = 24

class Index(LoginRequiredMixin, generic.TemplateView):
    """
    Gestus index to display data resumes
    """
    template_name = "gestus/index.html"
    
    def get(self, request, *args, **kwargs):
        context = {
            'website_list' : Website.objects.all().order_by('-modified', 'name')[0:LAST_MODIFIED_WEBSITES_MAX],
            'environment_list' : WebsiteEnvironment.objects.all().order_by('-modified', 'name')[0:LAST_MODIFIED_ENVIRONMENT_MAX],
            'eggs_list' : Egg.objects.all().order_by('-modified', 'name')[0:LAST_MODIFIED_EGGS_MAX]
        }
        return self.render_to_response(context)


class CommonIndexBase(LoginRequiredMixin, generic.ListView):
    paginate_by = INDEX_LIST_MAX
    
    def get_queryset(self):
        return self.model.objects.all().order_by('-modified', 'name')

class WebsiteIndex(CommonIndexBase):
    model = Website
    template_name = "gestus/website_index.html"

class EnvironmentIndex(CommonIndexBase):
    model = WebsiteEnvironment
    template_name = "gestus/environment_index.html"

class EggIndex(CommonIndexBase):
    model = Egg
    template_name = "gestus/egg_index.html"


class WebsiteDetail(LoginRequiredMixin, generic.DetailView):
    model = Website
    template_name = "gestus/website_detail.html"

class EnvironmentDetail(LoginRequiredMixin, generic.DetailView):
    model = WebsiteEnvironment
    template_name = "gestus/environment_detail.html"

class EggDetail(LoginRequiredMixin, generic.DetailView):
    model = Egg
    template_name = "gestus/egg_detail.html"
