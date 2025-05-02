#!/bin/bash

date_str=$(date -u +"%Y%m%d")
url="s3://ecmwf-forecasts/${date_str}/00z/ifs/0p25/oper/${date_str}000000-${forecast_interval}-oper-fc.grib2"
aws s3 cp --no-sign-request $url .
aws s3 cp "${date_str}000000-${forecast_interval}-oper-fc.grib2" s3://hf-grib/${forecast_interval}.grib2
aws ecs run-task \
  --cluster fargate \
  --task-definition process-ecmwf \
  --launch-type FARGATE \
  --network-configuration '{"awsvpcConfiguration": {"subnets": ["subnet-69cb1121"], "securityGroups": ["sg-57535728"],"assignPublicIp": "ENABLED"}}' \
  --overrides "{\"containerOverrides\": [{\"name\": \"process-ecmwf\", \"environment\": [{\"name\": \"FORECAST_INTERVAL\", \"value\": \"$forecast_interval\"}]}]}"
