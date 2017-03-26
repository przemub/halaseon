from django.contrib import admin

from .models import Sonda, Pomiar

class SondaAdmin(admin.ModelAdmin):
    list_display = ['położenie', 'ostatni_pomiar']
    search_fields = ['położenie']

class PomiarAdmin(admin.ModelAdmin):
    list_display = ['wynikf', 'sonda', 'data']
    list_filter = ['sonda', 'data']

admin.site.register(Sonda, SondaAdmin)
admin.site.register(Pomiar, PomiarAdmin)

