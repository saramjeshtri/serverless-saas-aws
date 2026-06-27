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

        body = json.loads(event.get('body', '{}'))
        title = body.get('title')
        description = body.get('description')
        status = body.get('status')

        if not any([title, description, status]):
            raise ValueError("at least one field to update is required")

        update_expression = "SET "
        expression_values = {}

        if title:
            update_expression += "title = :title, "
            expression_values[':title'] = title
        if description:
            update_expression += "description = :description, "
            expression_values[':description'] = description
        if status:
            update_expression += "#s = :status, "
            expression_values[':status'] = status

        update_expression = update_expression.rstrip(', ')

        kwargs = {
            'Key': {'task_id': task_id},
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_values,
            'ReturnValues': 'ALL_NEW'
        }

        if status:
            kwargs['ExpressionAttributeNames'] = {'#s': 'status'}

        result = table.update_item(**kwargs)
        updated_task = result.get('Attributes')

        return {
            'statusCode': 200,
            'body': json.dumps(updated_task)
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