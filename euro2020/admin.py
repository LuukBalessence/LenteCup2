from django.contrib import admin
from django import forms

from euro2020 import models
from .forms import MatchForm, GoalInlineFormSet
from .models import Goal, Match, Team


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "order", "openforbid")
    list_editable = ("openforbid", "openforbid")


@admin.register(models.GamePhase)
class GamePhaseAdmin(admin.ModelAdmin):
    list_display = ("gamephase", "allowbidding", "allowauction", "allowlineup", "allowfiring")
    list_editable = ("allowbidding", "allowauction", "allowlineup", "allowfiring")


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "position", "number", "country")
    list_filter = ("country",)


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country")


class GoalInline(admin.TabularInline):
    formset = GoalInlineFormSet
    model = Goal
    fk_name = "match"
    extra = 2
    fields = ("player", "minute", "type", "phase")


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    form = MatchForm
    list_display = (
        "stage",
        "start",
        "home",
        "away",
        "location",
        "has_started",
        "has_ended",
    )
    list_editable = ("has_started", "has_ended")

    def add_view(self, request, form_url='', extra_context=None):
        # when we add a match, we don't show the players because we don't know the countries yet
        # also, no GoalInlines because we don't know the countries.
        self.exclude = ("players",)
        self.inlines = []
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # when we change a match, we already know the countries so we include the players
        # and the GoalInlines to keep track of the goals.
        self.exclude = None
        match = Match.objects.filter(pk=object_id)
        if match.has_started:
            self.inlines = [
                GoalInline,
            ]
        else:
            self.inlines = []
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "betcoins")
    list_editable = ("betcoins", "betcoins")


@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        "leaguename",
        "maxparticipants",
    )


@admin.register(models.Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "home",
        "away",
        "type",
        "phase",
        "minute",
    )
    list_filter = ("match",)

    def home(self, obj):
        return obj.match.home

    def away(self, obj):
        return obj.match.away

    ordering = (
        "match",
        "phase",
        "minute",
    )


@admin.register(models.Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "player",
        "playerbid",
        "assigned",
        "bidcomment",
    )
    list_filter = ("team",)