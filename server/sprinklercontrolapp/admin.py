from django.contrib import admin
from sprinklercontrolapp.models import Sprinkler, Restriction, Error, SprinklerError, WaterQuantity, GeneralSetting, Irrigation

# Register your models here.
class SprinklerAdmin (admin.ModelAdmin):
    pass
admin.site.register(Sprinkler, SprinklerAdmin)


class SprinklerErrorAdmin (admin.ModelAdmin):
    pass
admin.site.register(SprinklerError, SprinklerErrorAdmin)


class RestrictionAdmin (admin.ModelAdmin):
    pass
admin.site.register(Restriction, RestrictionAdmin)


class ErrorAdmin (admin.ModelAdmin):
    pass
admin.site.register(Error, ErrorAdmin)


class WaterQuantityAdmin (admin.ModelAdmin):
    pass
admin.site.register(WaterQuantity, WaterQuantityAdmin)


class GeneralSettingAdmin (admin.ModelAdmin):
    pass
admin.site.register(GeneralSetting, GeneralSettingAdmin)


class IrrigationAdmin (admin.ModelAdmin):
    pass
admin.site.register(Irrigation, IrrigationAdmin)

