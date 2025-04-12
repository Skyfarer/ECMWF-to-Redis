import json
import boto3

client = boto3.client('lambda')

def lambda_handler(event, context):
    # List of different event payloads
    events = [
        {"forecast_interval": "0h"},
        {"forecast_interval": "6h"},
        {"forecast_interval": "12h"},
        {"forecast_interval": "18h"},
        {"forecast_interval": "24h"},
        {"forecast_interval": "30h"},
        {"forecast_interval": "36h"},
        {"forecast_interval": "42h"},
        {"forecast_interval": "48h"},
        {"forecast_interval": "54h"},
        {"forecast_interval": "60h"},
        {"forecast_interval": "66h"}
    ]

    responses = []
    
    for idx, payload in enumerate(events):
        try:
            response = client.invoke(
                FunctionName='start-ecmwf-fetch',
                InvocationType='Event',  # Asynchronous execution
                Payload=json.dumps(payload)
            )
            responses.append({
                "payload": payload,
                "status": response['StatusCode'],
                "request_id": response['ResponseMetadata']['RequestId']
            })
        except Exception as e:
            responses.append({
                "payload": payload,
                "error": str(e)
            })
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "invocations": responses,
            "parent_request_id": context.aws_request_id
        })
    }
