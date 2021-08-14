from django.contrib import admin

# Register your models here.
from luukopen21 import models

@admin.register(models.GolfProfiel)
class GolfProfielAdmin(admin.ModelAdmin):
    list_display = ("naam", "ehcp", "huurset", "buggy", "preluukopen", "opmerking")
    list_editable = ("ehcp", "preluukopen", "opmerking")

@admin.register(models.BaanProfiel)
class BaanProfielAdmin(admin.ModelAdmin):
    list_display = ("naam", "plaats")

@admin.register(models.TeeKleur)
class TeeKleurAdmin(admin.ModelAdmin):
    list_display = ("pk", "kleur")

@admin.register(models.GolfBaanProfiel)
class GolfBaanProfielAdmin(admin.ModelAdmin):
    list_display = ("naam", "aantalholes", "sr", "cr", "par", "baan", "teekleur")

@admin.register(models.Holes)
class HolesAdmin(admin.ModelAdmin):
    list_display = ("golfbaan", "hole_nr", "par", "strokeindex", "afstand")