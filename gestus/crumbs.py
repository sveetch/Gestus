from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'index': ugettext_lazy('<i class="icon-satellite"></i> Gestus'),
    'website-list': ugettext_lazy('Website index'),
    'website-detail': ugettext_lazy('{% load i18n %}<small class="subhead">Website</small> {{ website.name }}'),
    'environment-list': ugettext_lazy('Website environment index'),
    'environment-detail': ugettext_lazy('{% load i18n %}<small class="subhead">Website environment</small> {{ websiteenvironment }}'),
    'egg-list': ugettext_lazy('Egg index'),
    'egg-detail': ugettext_lazy('{% load i18n %}<small class="subhead">Egg</small> {{ egg.name }}'),
    'server-list': ugettext_lazy('Server index'),
    'server-detail': ugettext_lazy('{% load i18n %}<small class="subhead">Server</small> {{ server.server }}'),
})