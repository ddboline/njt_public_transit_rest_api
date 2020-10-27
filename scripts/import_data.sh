#!/bin/bash

TMPDIR=`mktemp -d`

cd $TMPDIR

mkdir -p rail_data/ bus_data/

unzip -x /rest_api/data/rail_data.zip -d rail_data/
unzip -x /rest_api/data/bus_data.zip -d bus_data/

for TYPE in rail bus;
do
    for TABLE in agency calendar_dates routes stops stop_times trips;
    do
        echo "create table"
        psql $DATABASE_URL < /rest_api/sql/${TYPE}_${TABLE}.sql
        echo "fill table ${TYPE}_${TABLE}"
        cat ${TYPE}_data/${TABLE}.txt | psql $DATABASE_URL -c "COPY ${TYPE}_${TABLE} FROM STDIN WITH (FORMAT CSV, HEADER true, DELIMITER ',')"
        echo "table ${TYPE}_${TABLE} filled"
    done
done

cd ~/
rm -rf $TMPDIR
