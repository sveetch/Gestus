# -*- coding: utf-8 -*-
"""
Data models
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _

ENVIRONMENT_KIND_CHOICES = (
    ('integration', _('Integration')),
    ('production', _('Production')),
)

class Egg(models.Model):
    """
    Egg model
    """
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    name = models.CharField(_('name'), unique=True, blank=False, max_length=50)
    package = models.CharField(_('package name'), unique=True, blank=False, max_length=50)
    url = models.CharField(_('url'), blank=True, max_length=255)
    summary = models.TextField(_('summary'), blank=True)
    description = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.package
    
    class Meta:
        verbose_name = _("egg")
        verbose_name_plural = _("eggs")

class EggVersion(models.Model):
    """
    Egg version model
    """
    created = models.DateTimeField(_('created'), auto_now_add=True)
    name = models.CharField(_('name'), blank=False, max_length=20)
    egg = models.ForeignKey(Egg, blank=False, related_name='versions')

    def __unicode__(self):
        return "{eggname}={version}".format(eggname=self.egg.package, version=self.name)
    
    class Meta:
        verbose_name = _("egg version")
        verbose_name_plural = _("eggs versions")

class Website(models.Model):
    """
    Website model
    """
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    name = models.CharField(_('name'), unique=True, blank=False, max_length=100)
    description = models.TextField(_('description'), blank=True)
    enabled = models.BooleanField(_('enabled'), default=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _("website")
        verbose_name_plural = _("websites")

class WebsiteEnvironment(models.Model):
    """
    Website environment model
    """
    website = models.ForeignKey(Website, blank=False, related_name='environments')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    name = models.CharField(_('name'), choices=ENVIRONMENT_KIND_CHOICES, blank=False, max_length=50)
    url = models.CharField(_('url'), blank=True, max_length=255)
    server = models.CharField(_('server'), blank=False, max_length=100)
    enabled = models.BooleanField(_('enabled'), default=True)
    eggs = models.ManyToManyField(EggVersion, blank=True)
    
    def __unicode__(self):
        return "{website} {env}".format(website=self.website.name, env=self.name)
    
    def get_used_eggs(self):
        return self.eggs.all().select_related().order_by('egg__name')
    
    class Meta:
        verbose_name = _("website environment")
        verbose_name_plural = _("websites environments")
