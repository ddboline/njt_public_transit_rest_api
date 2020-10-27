import json
from datetime import datetime
from flask_testing import TestCase
from flask import Flask
from urllib.parse import urlencode

from rest_api import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app


class TestRestApi(BaseTestCase):
    def test_schedules(self):
        payload = {
            "start_time": datetime(2020, 10, 20, 13, 12, 00).isoformat(),
            "origin_station_id": 2,
            "coordinates": [40.762027, -74.2958287],
            "destination_station_id": 2,
        }
        response = self.client.post("/schedules", json=payload)
        self.assertEqual(response.status_code, 200)
        print(json.dumps(response.json, indent=1))
        self.assertEqual(len(response.json["next_schedules"]), 10)
        print(response.json["next_schedules"][0])
        self.assertEqual(
            response.json["next_schedules"][0],
            {
                "departure": "2020-10-20T13:07:00",
                "route": "EGG HARBOR",
                "stop_name": "ABSECON",
                "transit_mode": "rail",
            },
        )
        token = response.json['token']

        print(token)

        response = self.client.get(f"/schedules?token={token}")

        self.assertEqual(len(response.json["next_schedules"]), 7)
