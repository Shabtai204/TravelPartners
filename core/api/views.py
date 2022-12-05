from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Trip
from .serializers import TripSerializer

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/trips',
        'GET /api/trips/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def get_trips(request):
    trips = Trip.objects.all()
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_trip(request, pk):
    trip = Trip.objects.get(id=pk)
    serializer = TripSerializer(trip, many=False)
    return Response(serializer.data)