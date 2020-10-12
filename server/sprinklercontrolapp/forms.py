from django import forms
from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer, IrrigationPlan

class SprinklerForm(forms.ModelForm):
    class Meta:
        model = Sprinkler
        fields = ['label', 'description', 'power', 'mode']


class WeeklyTimersForm(forms.ModelForm):
    class Meta:
        model = WeeklyRepeatingTimer
        fields = '__all__'

class IrrigationPlanForm(forms.ModelForm):
    class Meta:
        model = IrrigationPlan
        fields = '__all__'