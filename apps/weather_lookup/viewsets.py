from django.http import HttpResponse
import json
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.weather_lookup.serializers import WeatherLookupSerializer
from apps.weather_lookup.helpers import calculate_dates_from_period
from apps.weather_lookup.helpers import calculate_final_temperatures
from apps.weather_lookup.helpers import calculate_temperatures_from_hourly_data
from apps.weather_lookup.helpers import fetch_lat_lon_from_city
from apps.weather_lookup.helpers import fetch_weather_data


class WeatherLookupViewSet(GenericViewSet):
    """Viewset for weather lookup."""

    @action(['GET'], detail=False, url_name='search', url_path='search')
    def search_city(self, request):
        """
        Do a weather lookup and return results.

        Accepts 'city' and 'period'(days) params which does a weather history lookup
        and returns some data.
        """
        serializer = WeatherLookupSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        # resolve coords from city
        lat = fetch_lat_lon_from_city(serializer.data.get('city'))
        lon = 1
        # Get timestamps from period
        timestamps = calculate_dates_from_period(serializer.data.get('period'))
        temperatures_list = []
        # Loop through timestamps and fetch weather data
        for timestamp in timestamps:
            weather_data = fetch_weather_data(lat, lon, timestamp)
            # Calculate daily min, max and avg from hourly data
            temp_metrics = calculate_temperatures_from_hourly_data(weather_data)
            temperatures_list.append(temp_metrics)
        final_temperatures = calculate_final_temperatures(temperatures_list)
        return HttpResponse(json.dumps(final_temperatures))

    @action(['GET'], detail=False, url_name='chart', url_path='chart')
    def chart(self, request):
        return HttpResponse("TODO: Add a chart view of the historical weather data!!")
