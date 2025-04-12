import boto3
import os
import json

def lambda_handler(event, context):
    ecs = boto3.client('ecs')
    
    response = ecs.run_task(
        cluster='fargate',
        launchType='FARGATE',
        taskDefinition='fetch-ecmwf:2',
        count=1,
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-69cb1121'],
                'securityGroups': ['sg-57535728'],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            'containerOverrides': [{
                'name': 'fetch-ecmwf',
                'environment': [
                    {
                        'name': 'LAMBDA_EVENT',
                        'value': json.dumps(event)
                    },
                    {
                        'name': 'forecast_interval',
                        'value': event.get("forecast_interval")
                    }
                ]
            }]
        }
    )
    return response
