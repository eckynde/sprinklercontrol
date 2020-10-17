from django.contrib import admin
from sprinklercontrolapp.models import Sprinkler, WeeklyRepeatingTimer, Weekday, IrrigationPlan, Preferences

# Register your models here.
class SprinklerAdmin (admin.ModelAdmin):
    pass
admin.site.register(Sprinkler, SprinklerAdmin)


class WeeklyRepeatingTimerAdmin (admin.ModelAdmin):
    pass
admin.site.register(WeeklyRepeatingTimer, WeeklyRepeatingTimerAdmin)


class WeekdayAdmin (admin.ModelAdmin):
    pass
admin.site.register(Weekday, WeekdayAdmin)


class IrrigationPlanAdmin (admin.ModelAdmin):
    pass
admin.site.register(IrrigationPlan, IrrigationPlanAdmin)

class SingletonAdmin(admin.ModelAdmin):
    actions = None
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Preferences)
class PreferencesAdmin(SingletonAdmin):
    pass