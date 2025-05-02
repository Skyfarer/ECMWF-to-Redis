#!/bin/bash
echo "Copying data from S3"
aws s3 cp s3://hf-grib/${FORECAST_INTERVAL}.grib2 .
echo "Parsing Grib to text file"
grib_get_data -p date,shortName -w shortName=2t/2d/10u/10v/tp ${FORECAST_INTERVAL}.grib2 > data.txt
echo "Copying data to Redis"
node insert_data.js data.txt
echo "Done"
exit $?
