from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy

site.update({
    'gestus:index': ugettext_lazy('<i class="icon-satellite"></i> Gestus'),
    'gestus:website-list': ugettext_lazy('Website index'),
    'gestus:website-detail': ugettext_lazy('{% load i18n %}<small class="subhead">Website</small> {{ website.name }}'),
    'gestus:environment-list': ugettext_lazy('Website environment index'),
    'gestus:environment-detail': ugettext_lazy('{% load i18n %}<small class="subhead">Website environment</small> {{ websiteenvironment }}'),
    'gestus:egg-list': ugettext_lazy('Egg index'),
    'gestus:egg-detail': ugettext_lazy('{% load i18n %}<small class="subhead">Egg</small> {{ egg.name }}'),
    'gestus:server-list': ugettext_lazy('Server index'),
    'gestus:server-detail': ugettext_lazy('{% load i18n %}<small class="subhead">Server</small> {{ server.server }}'),
})