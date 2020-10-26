from flask_testing import TestCase
from flask import Flask
from urllib.parse import urlencode

from rest_api import get_app


class BaseTestCase(TestCase):
    def create_app(self):
        app = get_app()
        app.config["TESTING"] = True
        return app


class TestRestApi(BaseTestCase):
    def test_schedules(self):
        parameters = {
            "origin_station_id": 2,
            "coordinates": {"latitude": 41.2, "longitude": 63.4},
            "destination_station_id": 2,
        }
        response = self.client.get(f"/schedules?{urlencode(parameters)}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["next_schedules"]), 3)
