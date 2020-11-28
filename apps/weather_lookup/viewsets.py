import datetime
from django.http import HttpResponse, Http404
import json
import requests
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import statistics

from apps.weather_lookup.serializers import WeatherLookupSerializer
from simple_weather_api.settings import WEATHER_API_KEY

# Might make this a env var
WEATHER_API_URL = "https://community-open-weather-map.p.rapidapi.com/"


def calculate_final_temperatures(aggregated_temperatures: [dict]) -> dict:
    """
    Calculate the overall min, max, avg and median temps over the period span.
    :param aggregated_temperatures: List of aggregated temperatures
    :return: Consolidated temperatures
    """
    min_temp = min([temp['min'] for temp in aggregated_temperatures])
    max_temp = max([temp['max'] for temp in aggregated_temperatures])
    avg_temp = sum(
        [temp['avg'] for temp in aggregated_temperatures]
    ) / len(aggregated_temperatures)
    temp_list = []
    for temps in aggregated_temperatures:
        temp_list += temps['temp_list']
    median_temp = statistics.median(temp_list)
    return {
        'min': round(min_temp * 2) / 2,
        'max': round(max_temp * 2) / 2,
        'avg': round(avg_temp * 2) / 2,
        'median': round(median_temp * 2) / 2
    }


def calculate_temperatures_from_hourly_data(weather_data: list) -> dict:
    """
    Calculates the min, max, avg temps.
    :param weather_data: List of hourly temps data.
    :return: Dict with min, max and avg temperatures.
    """
    temps = [hour_weather['temp'] for hour_weather in weather_data]
    min_temp = min(temps)
    max_temp = max(temps)
    avg_temp = sum(temps) / len(temps)
    return {
        'min': min_temp,
        'max': max_temp,
        'avg': avg_temp,
        'temp_list': temps
    }


def calculate_dates_from_period(period: int) -> [int]:
    """
    Calculate the dates in UNIX timestamp from period.

    :param period: Days to look back on.
    :return: List of calculated UNIX timestamps
    """
    timestamps = []
    while period > 0:
        timestamp = (datetime.datetime.now() - datetime.timedelta(days=period)).timestamp()
        timestamps.append(timestamp)
        period -= 1
    return timestamps


def fetch_lat_lon_from_city(city: str) -> [float]:
    """
    Fetch the lat and long of a city.

    :param city:  The city to search for.
    :return:
    """
    data = {
        'q': city,
        'cnt': 1
    }
    header_data = {
        'x-rapidapi-key': WEATHER_API_KEY,
        'x-rapidapi-host': 'community-open-weather-map.p.rapidapi.com'
    }
    response = requests.get(
        WEATHER_API_URL + 'find',
        params=data,
        headers=header_data
    )
    if not response.json()['list']:
        raise Http404("Poll does not exist")
    lat = response.json()['list'][0]["coord"]["lat"]
    lon = response.json()['list'][0]["coord"]["lon"]
    return lat, lon


def fetch_weather_data(lat: float, lon: float, timestamp: int) -> dict:
    """
    Method to fetch weather data via API.
    :param lat: Latitude of city.
    :param lon: Longitude of city.
    :param timestamp: The timestamp to fetch weather on in UNIX timestamp format.
    :return: Historical weather data.
    """
    data = {
        'lat': lat,
        'lon': lon,
        'dt': int(timestamp),
        'units': 'metric'
    }
    header_data = {
        'x-rapidapi-key': WEATHER_API_KEY,
        'x-rapidapi-host': 'community-open-weather-map.p.rapidapi.com'
    }
    response = requests.get(
        WEATHER_API_URL + 'onecall/timemachine',
        params=data,
        headers=header_data
    )
    return response.json()['hourly']


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
        print(lat)
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
        return HttpResponse("!!!!!")
