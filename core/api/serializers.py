from rest_framework.serializers import ModelSerializer
from core.models import Trip

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'