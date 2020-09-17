from django import forms
from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer

class SprinklerForm(forms.ModelForm):
    class Meta:
        model = Sprinkler
        fields = ['label', 'location', 'power', 'enabled']

        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Textarea(attrs={'style': 'resize: none','rows': '3','class': 'form-control'}),
            'power': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'enabled': forms.CheckboxInput(attrs={'class': 'form-control'})
        }

class WeeklyTimersForm(forms.ModelForm):
    class Meta:
        model = WeeklyRepeatingTimer
        fields = ['label', 'description', 'timestart', 'timestop', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', "sprinklers"]

        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'timestart': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'timestop': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'monday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'tuesday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'wednesday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'thursday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'friday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'saturday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'sunday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'sprinklers': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
