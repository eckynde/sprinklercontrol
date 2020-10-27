from sprinklercontrolapp.models import Sprinkler, SprinklerPoweredHistory
import pytz
from datetime import datetime

def setPowerstate(id, power):

    try:
        sprinkler = Sprinkler.objects.get(pk=id)
    except Sprinkler.DoesNotExist:
        return
    
    if sprinkler.power != power:
        Sprinkler.objects.filter(pk=id).update(power=power)
        SprinklerPoweredHistory.objects.create(sprinkler=sprinkler, timeofevent=datetime.now(tz=pytz.timezone("Europe/Berlin")), powered=power)


    # if db.power = power then
    #   do nothing
    # else
    #   DB updaten
    #   History schreiben

    # add to history
    



