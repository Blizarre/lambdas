# encoding: utf8

import json

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

DYNAMODB_TABLE = 'important_dates'


def lambda_handler(event, context):
    """Add a new birthday to the 'important_dates' in dynamo_db.

    Important date format is { 'date': '<day>-<month', 'label': '<label_content>' }

    It is triggered by API Gateway and therefore returns
    a proper body with status code and body
    """
    date_table = dynamodb.Table(DYNAMODB_TABLE)

    params = json.loads(event['body'])
    date = params['date']
    label = params['label']

    try:
        date_table.put_item(
            Item={
                'date': date,
                'label': label,
            }
        )
    except ClientError as e:
        status_code = 500
        response_body = {'message': e.response['Error']['Message']}
    else:
        status_code = 200
        response_body = {
            'message': 'Added item',
            'added_date': date,
            'added_label': label
        }
    response = {
        'statusCode': status_code,
        'body': json.dumps(response_body, indent=4)
    }
    return response
