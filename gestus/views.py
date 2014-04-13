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

class Index(LoginRequiredMixin, generic.TemplateView):
    """
    Project index
    """
    template_name = "gestus/index.html"
    
    def get(self, request, *args, **kwargs):
        context = {}#'website_list' : Website.objects.all().order_by('-created')}
        return self.render_to_response(context)
