# encoding: utf8

import json
import os
from datetime import date

import boto3
from botocore.exceptions import ClientError

sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

DYNAMODB_TABLE = 'important_dates'

NO_TOPIC = '<none>'
sns_topic = os.environ.get('SNS_TOPIC_ARN', NO_TOPIC)


def send_sms_message(message, topic):
    print("Sending message: '{}' to topic {}".format(message, topic))
    if topic == NO_TOPIC:
        print("dry run, no messages sent")
        response = {}
    else:
        response = sns.publish(
            TopicArn=topic,
            Message=message
        )
    return response


def lambda_handler(event, context):
    """Check if there is an entry in the 'important_dates' table for today (format is '<day>-<month'). If one
    is found, retrieve the element 'label' of the entry and publish it to the SNS topic given by the environment
    variable 'SNS_TOPIC_ARN'.

    This lambda is designed to be triggered at least once a day (several time a day is better,
    just in case the messages are overlooked)
    """
    date_table = dynamodb.Table(DYNAMODB_TABLE)

    today = date.today()

    table_key = "{:02d}-{:02d}".format(today.day, today.month)

    try:
        print("Looking for item '{}'".format(table_key))
        response = date_table.get_item(
            TableName='important_dates',
            Key={'date': table_key},
            AttributesToGet=[
                'label',
            ],
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response.get('Item')
        if item:
            send_sms_message(item['label'], sns_topic)
        else:
            print("Nothing important happened today")
