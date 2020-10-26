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
        payload = {
            "origin_station_id": 2,
            "coordinates": [40.762027, -74.2958287],
            "destination_station_id": 2,
        }
        response = self.client.post("/schedules", json=payload)
        self.assertEqual(response.status_code, 200)
        print(response.json)
        self.assertEqual(len(response.json["next_schedules"]), 3)
