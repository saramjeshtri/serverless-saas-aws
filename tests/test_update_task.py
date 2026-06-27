import json
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'functions'))

from update_task import lambda_handler

@patch('update_task.boto3')
def test_update_task_success(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    mock_table.get_item.return_value = {
        'Item': {
            'task_id': 'abc-123',
            'user_id': 'user-123',
            'title': 'Old title',
            'status': 'pending'
        }
    }

    mock_table.update_item.return_value = {
        'Attributes': {
            'task_id': 'abc-123',
            'user_id': 'user-123',
            'title': 'Old title',
            'status': 'completed'
        }
    }

    event = {
        'pathParameters': {'task_id': 'abc-123'},
        'body': json.dumps({'status': 'completed'}),
        'requestContext': {'authorizer': {'claims': {'sub': 'user-123'}}}
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 200

@patch('update_task.boto3')
def test_update_task_wrong_user(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    mock_table.get_item.return_value = {
        'Item': {
            'task_id': 'abc-123',
            'user_id': 'different-user',
            'title': 'Task',
            'status': 'pending'
        }
    }

    event = {
        'pathParameters': {'task_id': 'abc-123'},
        'body': json.dumps({'status': 'completed'}),
        'requestContext': {'authorizer': {'claims': {'sub': 'user-123'}}}
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 403

@patch('update_task.boto3')
def test_update_task_no_fields(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    mock_table.get_item.return_value = {
        'Item': {
            'task_id': 'abc-123',
            'user_id': 'user-123',
            'title': 'Task',
            'status': 'pending'
        }
    }

    event = {
        'pathParameters': {'task_id': 'abc-123'},
        'body': '{}',
        'requestContext': {'authorizer': {'claims': {'sub': 'user-123'}}}
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 400