import json
import os
import boto3

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('TABLE_NAME', 'tasks'))

        user_id = event['requestContext']['authorizer']['claims']['sub']
        task_id = event.get('pathParameters', {}).get('task_id')

        if not task_id:
            raise ValueError("task_id is required")

        # Fetch task first to verify ownership
        result = table.get_item(Key={'task_id': task_id})
        task = result.get('Item')

        if not task:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Task not found'})
            }

        if task['user_id'] != user_id:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Forbidden'})
            }

        table.delete_item(Key={'task_id': task_id})

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Task deleted successfully'})
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