#!/bin/sh
aws s3 cp s3://hf-grib/0h.grib2 .
grib_get_data -w shortName=2t 0h.grib2 > data.txt
node insert_geo_points.js data.txt
