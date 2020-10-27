# agilis_backend_interview_take_home

Usage instructions:

Clone this repository:

```bash
git clone https://github.com/ddboline/agilis_backend_interview_take_home.git
cd agilis_backend_interview_take_home/
```

Next you need to download the data files from NJT and place them in the data/ directory:

`wget https://www.njtransit.com/rail_data.zip -O ./data/rail_data.zip`
`wget https://www.njtransit.com/bus_data.zip -O bus_data.zip`

You'll need to install [https://docs.docker.com/compose/](docker-compose), you can then bring up the application using:
`PASSWORD=password docker-compose run up -d build`
