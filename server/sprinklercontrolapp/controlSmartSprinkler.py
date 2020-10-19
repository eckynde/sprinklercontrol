from sprinklercontrolapp.models import WeatherCurrent, WeatherForecast, Sprinkler

## "exec(open('sprinklercontrolapp/controlSmartSprinkler.py').read())"

smartSprinklers = Sprinkler.objects.filter(mode='S')

for objs in smartSprinklers:
    print(objs.label)