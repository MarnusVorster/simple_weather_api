from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch


class WeatherLookupViewSetTestCase(TestCase):
    """Test WeatherLookupViewSet."""

    mock_weather_hourly_data = [
        {
            'temp': 10.0
        }
    ]
    mock_city = 'Some_city'
    mock_period = 1

    @patch("apps.weather_lookup.viewsets.fetch_lat_lon_from_city")
    @patch("apps.weather_lookup.viewsets.fetch_weather_data")
    def test_search_weather_data(self, mocked_city_lookup_object,
                                 mocked_weather_object):
        """Test the positive flow of search endpoint"""
        mocked_city_lookup_object.return_value = self.mock_weather_hourly_data
        mocked_weather_object.return_value = (1, 1)
        client = APIClient()
        payload = {
            'city': self.mock_city,
            'period': self.mock_period
        }
        response = client.get('/weather_lookup/search/', payload)
        assert response.status_code == 200
