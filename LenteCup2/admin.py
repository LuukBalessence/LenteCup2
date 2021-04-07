from django.contrib import admin
from LenteCup2 import models
from .forms import WeekForm, ScoresForm, GameSettingsForm


@admin.register(models.GameSettings)
class WeekAdmin(admin.ModelAdmin):
    form = GameSettingsForm
    list_display = ["tourstarttime"]


@admin.register(models.Week)
class WeekAdmin(admin.ModelAdmin):
    form = WeekForm
    list_display = ["week", "openforscoring", "maxpoints"]


@admin.register(models.Scores)
class ScoresAdmin(admin.ModelAdmin):
    form = ScoresForm
    list_display = ['user', 'week', 'score', 'qualifying', 'finalscore']


@admin.register(models.Speler)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ['rank', 'first_name', 'last_name', 'position']
    list_editable = ['position']

@admin.register(models.GekozenSpelers)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ['user', 'speler', 'eindplaats', 'punten']