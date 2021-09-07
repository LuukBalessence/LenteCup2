from django.contrib import admin

# Register your models here.
from luukopen21 import models

@admin.register(models.GolfProfiel)
class GolfProfielAdmin(admin.ModelAdmin):
    list_display = ("naam", "ehcp", "huurset", "buggy", "preluukopen", "verradergame", "instemronde", "immuniteitraad", "immuniteitverraad", "opmerking")
    list_editable = ("ehcp", "verradergame", "instemronde", "immuniteitraad", "immuniteitverraad")

@admin.register(models.BaanProfiel)
class BaanProfielAdmin(admin.ModelAdmin):
    list_display = ("naam", "adres", "telefoon")

@admin.register(models.TeeKleur)
class TeeKleurAdmin(admin.ModelAdmin):
    list_display = ("pk", "kleur")

@admin.register(models.GolfBaanProfiel)
class GolfBaanProfielAdmin(admin.ModelAdmin):
    list_display = ("naam", "aantalholes", "sr", "cr", "par", "baan", "teekleur")

@admin.register(models.Hole)
class HolesAdmin(admin.ModelAdmin):
    list_display = ("golfbaan", "hole_nr", "par", "strokeindex", "afstand")

@admin.register(models.Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("naam", "dag", "starttijd", "golfbaan")
