from django.contrib import admin
from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer

# Register your models here.
class SprinklerAdmin (admin.ModelAdmin):
    pass
admin.site.register(Sprinkler, SprinklerAdmin)


class WeeklyRepeatingTimerAdmin (admin.ModelAdmin):
    pass
admin.site.register(WeeklyRepeatingTimer, WeeklyRepeatingTimerAdmin)
