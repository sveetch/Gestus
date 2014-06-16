from django.contrib import admin

from .models import Website, WebsiteEnvironment, Egg, EggVersion


class WebsiteEnvironmentInline(admin.StackedInline):
    model = WebsiteEnvironment
    
class WebsiteAdmin(admin.ModelAdmin):
    ordering = ('modified',)
    search_fields = ('name', 'description',)
    list_display = ('name', 'modified', 'enabled')
    inlines = [
        WebsiteEnvironmentInline,
    ]

admin.site.register(Website, WebsiteAdmin)
admin.site.register(WebsiteEnvironment)
admin.site.register(Egg)
admin.site.register(EggVersion)
