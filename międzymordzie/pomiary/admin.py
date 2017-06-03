from django.contrib import admin

from .models import Sonda, Pomiar, Przerwa

class SondaAdmin(admin.ModelAdmin):
    list_display = ['położenie', 'ostatni_pomiar']
    search_fields = ['położenie']

class PomiarAdmin(admin.ModelAdmin):
    list_display = ['wynikf', 'sonda', 'data']
    list_filter = ['sonda', 'data']

class PrzerwaAdmin(admin.ModelAdmin):
    list_display = ['nazwa_przerwy', 'czas_start', 'czas_koniec']

admin.site.register(Sonda, SondaAdmin)
admin.site.register(Pomiar, PomiarAdmin)
admin.site.register(Przerwa, PrzerwaAdmin)
