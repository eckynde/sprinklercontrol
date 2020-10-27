from sprinklercontrolapp.models import Sprinkler

def aktivate(args):
    for objs in args:
        Sprinkler.objects.filter(pk=objs).update(power=True)

def deaktivate(args):
    for objs in args:
        Sprinkler.objects.filter(pk=objs).update(power=False)

def controlSmartSprinkler():
    import sprinklercontrolapp.controlSmartSprinkler