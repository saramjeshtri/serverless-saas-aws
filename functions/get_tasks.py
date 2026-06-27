import json
import os
import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('TABLE_NAME', 'tasks'))

        user_id = event['requestContext']['authorizer']['claims']['sub']

        result = table.scan(
            FilterExpression=Attr('user_id').eq(user_id)
        )
        tasks = result.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(tasks)
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }