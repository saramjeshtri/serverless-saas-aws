import json
import os
import boto3
import uuid
from datetime import datetime

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('TABLE_NAME', 'tasks'))

        user_id = event['requestContext']['authorizer']['claims']['sub']

        body = json.loads(event.get('body', '{}'))
        title = body.get('title')
        description = body.get('description', '')

        if not title:
            raise ValueError("title is required")

        task = {
            'task_id': str(uuid.uuid4()),
            'user_id': user_id,
            'title': title,
            'description': description,
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat()
        }

        table.put_item(Item=task)

        return {
            'statusCode': 201,
            'body': json.dumps(task)
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }