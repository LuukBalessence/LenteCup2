from django import forms

from luukopen21.models import GolfProfiel


class AanmeldForm(forms.ModelForm):
    class Meta:
        model = GolfProfiel
        fields = ('naam', 'ehcp', 'buggy', 'huurset', 'preluukopen', 'opmerking')
        widgets = {'naam': forms.TextInput(attrs={'class': "input is-primary"}),
                   'ehcp': forms.NumberInput(attrs={'min': 0, 'max': 54, 'class': "input is-primary"}),
                   'buggy': forms.CheckboxInput(attrs={'class': "checkbox"}),
                   'huurset': forms.CheckboxInput(attrs={'class': "checkbox"}),
                   'preluukopen': forms.CheckboxInput(attrs={'class': "checkbox"}),
                   'opmerking': forms.Textarea(attrs={'class': "input is-primary", 'style': 'height: 6em;'})}
        labels = {
            'naam': 'Voornaam/alias',
            'ehcp': 'Handicap',
            'buggy': 'Buggy nodig?',
            'huurset': 'Huurset nodig?',
            'preluukopen': 'Doet mee aan Pre-Luuk Open?',
            'opmerking': 'Opmerkingen',
        }
        fields_required = ['naam', 'ehcp', 'buggy', 'huurset']

class ScumForm(forms.Form):
    naam1 = forms.CharField(max_length=40, help_text="1e te elimineren golfeer")
    naam2 = forms.CharField(max_length=40, help_text="2e te elimineren golfeer")
