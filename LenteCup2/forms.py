from django import forms

from LenteCup2.models import Week, Scores, GekozenSpelers, GameSettings


class GameSettingsForm(forms.ModelForm):

    class Meta:
        model = GameSettings
        fields = "__all__"


class WeekForm(forms.ModelForm):

    class Meta:
        model = Week
        fields = "__all__"


class ScoresForm(forms.ModelForm):

    class Meta:
        model = Scores
        fields = "__all__"


class GekozenSpelersForm(forms.ModelForm):

    class Meta:
        use_required_attribute = False
        model = GekozenSpelers
        fields = "__all__"



class ChangeFirstNameForm(forms.Form):
    firstname = forms.CharField(max_length=30, help_text="Enter your Name")

