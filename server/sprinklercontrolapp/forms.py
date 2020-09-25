from django import forms
from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer

class SprinklerForm(forms.ModelForm):
    class Meta:
        model = Sprinkler
        fields = ['label', 'description', 'power', 'enabled']


class WeeklyTimersForm(forms.ModelForm):
    class Meta:
        model = WeeklyRepeatingTimer
        fields = '__all__'
