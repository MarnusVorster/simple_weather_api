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
    def test_search_weather_data(self, mocked_weather_object,
                                 mocked_city_lookup_object):
        """Test the positive flow of search endpoint"""
        mocked_weather_object.return_value = self.mock_weather_hourly_data
        mocked_city_lookup_object.return_value = (1, 1)
        client = APIClient()
        payload = {
            'city': self.mock_city,
            'period': self.mock_period
        }
        response = client.get('/weather_lookup/search/', payload)
        assert response.status_code == 200

    def test_search_weather_data_missing_params(self):
        """Test the validation of the payload if both parms is not sent."""
        client = APIClient()
        response = client.get('/weather_lookup/search/')
        assert response.status_code == 400
        assert response.content == \
               b'{"city":["This field is required."],' \
               b'"period":["This field is required."]}'

    def test_search_weather_data_missing_city(self):
        """Test the validation of the payload if city is not sent."""
        client = APIClient()
        payload = {
            'period': self.mock_period
        }
        response = client.get('/weather_lookup/search/', payload)
        assert response.status_code == 400
        assert response.content == b'{"city":["This field is required."]}'

    def test_search_weather_data_missing_period(self):
        """Test the validation of the payload if period is not sent."""
        client = APIClient()
        payload = {
            'city': self.mock_city
        }
        response = client.get('/weather_lookup/search/', payload)
        assert response.status_code == 400
        assert response.content == b'{"period":["This field is required."]}'
