from flask import Flask, request, json
from datetime import date, datetime, timedelta, time
from departures import connect_to_db, get_closest_stop_id, get_upcoming_departures


def get_app():
    app = Flask(__name__)

    @app.route("/schedules", methods=["POST"])
    def schedules():
        payload = request.json

        origin_station_id = int(payload["origin_station_id"])
        coordinates = payload["coordinates"]
        latitude = float(coordinates[0])
        longitude = float(coordinates[1])

        destination_station_id = int(payload["destination_station_id"])

        con = connect_to_db()

        stops = set(
            [origin_station_id, destination_station_id]
            + get_closest_stop_id(con, "bus", latitude, longitude)
            + get_closest_stop_id(con, "rail", latitude, longitude)
        )

        print(stops)

        start_datetime = datetime.now()
        end_datetime = start_datetime + timedelta(hours=2)

        dates = [start_datetime.date()]
        start_times = [f"{start_datetime.hour:02}:00:00"]
        end_times = [f"{start_datetime.hour+2:02}:00:00"]

        if start_datetime.hour < 5:
            dates.append((start_datetime - timedelta(days=1)).date())
            start_times = [f"{start_datetime.hour+24:02}:00:00"]
            end_times = [f"{start_datetime.hour+26:02}:00:00"]
        elif end_datetime.hour < 5:
            dates.append((start_datetime - timedelta(days=1)).date())
            start_times = [f"24:00:00"]
            end_times = [f"{end_datetime.hour+26:02}:00:00"]

        departures = set()

        for stop_id in stops:
            for (date, start_time, end_time) in zip(dates, start_times, end_times):
                for stop_type in "rail", "bus":
                    for (arrival_time, _, route_type, stop_name) in get_upcoming_departures(
                        con, stop_type, start_time, end_time, stop_id, date
                    ):
                        if route_type == 0:
                            transit_mode = "light_rail"
                        elif route_type == 2:
                            transit_mode = "rail"
                        else:
                            transit_mode = "bus"
                        departures.add(
                            (transit_mode, arrival_time, stop_name)
                        )

        departures = [
            {"transit_mode": transit_mode, "departure": arrival_time, 'stop_name': stop_name}
            for (transit_mode, arrival_time, stop_name) in departures
        ]

        # mock_response = {
        #     "next_schedules": [
        #         {"transit_mode": "rail", "departure": "2019-11-04 16:19:09.383766"},
        #         {"transit_mode": "bus", "departure": "2019-11-04 17:19:09.459871"},
        #         {
        #             "transit_mode": "light_rail",
        #             "departure": "2019-11-04 18:50:09.543232",
        #         },
        #     ]
        # }

        return json.jsonify({'next_schedules': departures})

    return app


if __name__ == "__main__":
    get_app().run(host="0.0.0.0", port=5000)
