from sprinklercontrolapp.models import Sprinkler, SprinklerPoweredHistory
import pytz
from sprinklercontrolapp.uart.main import direct_sprinkler_control
from datetime import datetime

def setPowerstate(id, power):

    try:
        sprinkler = Sprinkler.objects.get(pk=id)
    except Sprinkler.DoesNotExist:
        return
    
    Sprinkler.objects.filter(pk=id).update(power=power)
    direct_sprinkler_control(sprinkler.uuid, power)

    if sprinkler.power != power:
        SprinklerPoweredHistory.objects.create(sprinkler=sprinkler, timeofevent=datetime.now(tz=pytz.timezone("Europe/Berlin")), powered=power)
        



