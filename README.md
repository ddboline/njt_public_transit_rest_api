### agilis_backend_interview_take_home

# Installation instructions:

Clone this repository:

```bash
git clone https://github.com/ddboline/agilis_backend_interview_take_home.git
cd agilis_backend_interview_take_home/
```

Next you need to download the data files from NJT and place them in the data/ directory:

```bash
wget https://www.njtransit.com/rail_data.zip -O ./data/rail_data.zip
wget https://www.njtransit.com/bus_data.zip -O bus_data.zip
```

You'll need to install [docker-compose](https://docs.docker.com/compose/), you can then bring up the application and import the transit data using the following:
```bash
docker-compose up -d --build
docker-compose run rest_api /rest_api/import_data.sh
```

You can run tests using:
```bash
docker-compose run rest_api /rest_api/run_tests.sh
```

# Usage instructions:

To use the api, send a POST containing at minimum the following fields:
```
origin_station_id
```


You can test the api by posting to the api e.g.:
```bash
curl -H "Content-Type: application/json" -X POST -d '{"origin_station_id": 87,"coordinates":[40.7252116,-74.305729],"destination_station_id": 105}' http://0.0.0.0:5000/schedules
```

Which will return the first 10 results (sorted by arrival time):
```bash
{"next_schedules":[{"departure":"2020-10-27T12:01:00","route":"TRENTON TRANSIT CENTER","stop_name":"NEW YORK PENN STATION","transit_mode":"rail"},{"departure":"2020-10-27T12:06:00","route":"70 NEWARK PENN STATION-Exact Fare","stop_name":"MILLBURN AVE AT LACKAWANNA PL","transit_mode":"bus"},{"departure":"2020-10-27T12:12:00","route":"NEW YORK PENN STATION","stop_name":"NEW YORK PENN STATION","transit_mode":"rail"},{"departure":"2020-10-27T12:17:00","route":"GLADSTONE","stop_name":"MILLBURN","transit_mode":"rail"},{"departure":"2020-10-27T12:17:00","route":"NEW YORK PENN STATION","stop_name":"NEW YORK PENN STATION","transit_mode":"rail"},{"departure":"2020-10-27T12:21:00","route":"NEW YORK PENN STATION","stop_name":"NEW YORK PENN STATION","transit_mode":"rail"},{"departure":"2020-10-27T12:26:00","route":"70 NEWARK PENN STATION-Exact Fare","stop_name":"MILLBURN AVE AT LACKAWANNA PL","transit_mode":"bus"},{"departure":"2020-10-27T12:26:00","route":"DOVER","stop_name":"MILLBURN","transit_mode":"rail"},{"departure":"2020-10-27T12:29:00","route":"MSU","stop_name":"NEW YORK PENN STATION","transit_mode":"rail"},{"departure":"2020-10-27T12:35:00","route":"NEW YORK PENN STATION","stop_name":"NEW YORK PENN STATION","transit_mode":"rail"}],"token":"MjMzMDYwMTkzNDM5ODc4MDQxNQ"}
```

The next 10 results can be obtained by calling get and using the token included in the results:
```bash
curl -H "Content-Type: application/json" -X GET http://0.0.0.0:5000/schedules?token=MjMzMDYwMTkzNDM5ODc4MDQxNQ
```
