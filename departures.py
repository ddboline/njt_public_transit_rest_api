import os
from typing import List, Tuple
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from datetime import date, time, datetime, timedelta

DATABASE_URL = os.environ["DATABASE_URL"]


def connect_to_db() -> Connection:
    engine = create_engine(DATABASE_URL)
    return engine.connect()


def get_closest_stop_id(
    con: Connection, stop_type: str, lat: float, lon: float, limit: int = 1
) -> List[int]:
    query = f"""
        SELECT stop_id
        FROM {stop_type}_stops
        ORDER BY
            abs(stop_lat - {lat}) ^ 2 + abs(stop_lon - {lon}) ^ 2
        LIMIT {limit}
    """

    return [row["stop_id"] for row in con.execute(query)]


def get_upcoming_departures(
    con: Connection,
    stop_type: str,
    start_time: str,
    end_time: str,
    stop_id: int,
    date: date,
) -> List[Tuple[datetime, str, int, str]]:
    query = f"""
        SELECT a.arrival_time, b.trip_headsign, d.route_type, e.stop_name
        FROM {stop_type}_stop_times a
        JOIN {stop_type}_trips b ON a.trip_id = b.trip_id
        JOIN {stop_type}_calendar_dates c ON b.service_id = c.service_id
        JOIN {stop_type}_routes d ON b.route_id = d.route_id
        JOIN {stop_type}_stops e ON a.stop_id = e.stop_id
        WHERE a.stop_id = %s
            AND a.arrival_time >= %s
            AND a.arrival_time <= %s
            AND c.date = %s
    """
    parameters = (stop_id, start_time, end_time, date)

    return [
        (
            convert_arrival_time(date, row["arrival_time"]),
            row["trip_headsign"],
            row["route_type"],
            row['stop_name'],
        )
        for row in con.execute(query, parameters)
    ]


def convert_arrival_time(date: date, time_str: str) -> datetime:
    hour = int(time_str[0:2])
    minute = int(time_str[3:5])
    second = int(time_str[6:9])
    if hour >= 24:
        hour -= 24
        date += timedelta(days=1)
    return datetime.combine(date, time(hour, minute, second))


def test_convert_arrival_time():
    assert convert_arrival_time(date(2020, 10, 12), "25:12:00") == datetime(
        2020, 10, 13, 1, 12
    )
