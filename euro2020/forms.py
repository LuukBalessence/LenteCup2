from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from euro2020.models import Goal, Player, Match, Bids, Team
from django.utils.translation import gettext_lazy as _


class GoalInlineFormSet(forms.BaseInlineFormSet):
    """
    Goals can only be scored by players that are playing in the parents Match
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        for form in self.forms:
            form.fields['player'].queryset = instance.players.all()

    class Meta:
        model = Goal
        fields = ("__all__")


class AddGoalForm(forms.ModelForm):
    # formulier om een doelpunt toe te voegen
    # op zich is het eenvoudig, we hebben een model en vier velden
    # het match veld is niet nodig want die hebben we toegevoegd toen
    # we het formulier hebben gemaakt in views.add_goal
    # maar... jij gaf aan dat je wilt filteren op speler, alleen de spelers van de spelende
    # landen mogen getoond worden, daarom overriden we de __init__ functie, deze wordt gebruikt
    # voor het initialiseren van het formulier en is dus een prima plek om velden aan te passen.
    # In dit geval willen we het player veld filteren.
    # maar eerst roepen we de init functie van ModelForm aan middel super().__init__
    # hier kun je je later nog in verdiepen, dit heeft te maken met object oriented programming
    # anyway, we willen een OR filter maken met countryhome en countryaway en dat is wat we hier doen
    # de queryset van het player field wordt gefilterd.
    # zie: https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        if instance:
            self.fields["player"].queryset = Player.objects.select_related(
                "country"
            ).filter(Q(country=instance.match.home) | Q(country=instance.match.away))

    class Meta:
        model = Goal
        fields = ["player", "type", "minute", "phase"]


class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        if instance:
            self.fields["players"].queryset = Player.objects.filter(
                country__in=[self.instance.home, self.instance.away]
            )

    class Meta:
        model = Match
        fields = "__all__"
        widgets = {
            'players': FilteredSelectMultiple(verbose_name="players", is_stacked=False)
        }

    def clean(self):
        cleaned_data = super().clean()
        home = cleaned_data.get("home")
        away = cleaned_data.get("away")
        if home and away:
            # check: home and away can't be the same
            if home == away:
                raise ValidationError(
                    {"away": _("A country can't play against itself.")}
                )

class PickLeagueForm(forms.Form):
    leaguename = forms.CharField(widget=forms.Select(
            attrs={'class': 'input is-primary', 'style': 'width: 300px; text-align:right', 'placeholder': '0'}),
                label='', required=False, help_text = "Pick a League")
    secretnumber = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'input is-primary', 'style': 'width: 300px; text-align:right', 'placeholder': '0'})
        , label='', min_value=10000, max_value=99999, required=False, help_text = "Enter a number between 10000 and 99999")

class ChangeFirstNameForm(forms.Form):
    firstname = forms.CharField(max_length=30, help_text="Enter your Name")

class CreateLeagueForm(forms.Form):
    leaguename = forms.CharField(max_length=30, help_text="Enter League Name")

class ChangeTeamNameForm(forms.Form):
    teamname = forms.CharField(max_length=30, help_text="Enter or change your Team Name")


class BidsForm(forms.Form):
    player = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'True'}), label='', required=False)
    playerpk = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'input is-primary is-small', 'style': 'width: 60px;', 'readonly': 'True'}), label='',
                               required=False)
    position = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'True'}), label='', required=False)
    bid = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'input is-primary is-small', 'style': 'width: 60px; text-align:right', 'placeholder': '0'})
        , label='', min_value=0, max_value=2000, required=False, help_text = "Enter a number between 0 and 2000")

    field_order = ['position', 'player']