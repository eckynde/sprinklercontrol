from rest_framework import serializers 
from sprinklercontrolapp.models import Sprinkler
 
 
class SprinklerSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Sprinkler
        fields = ('id',
                  'label',
                  'description',
                  'power',
                  'enabled')