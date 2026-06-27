import json
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'functions'))

from get_task import lambda_handler

@patch('get_task.boto3')
def test_get_task_success(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    mock_table.get_item.return_value = {
        'Item': {
            'task_id': 'abc-123',
            'user_id': 'user-123',
            'title': 'Test task',
            'status': 'pending'
        }
    }

    event = {
        'pathParameters': {'task_id': 'abc-123'},
        'requestContext': {'authorizer': {'claims': {'sub': 'user-123'}}}
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['task_id'] == 'abc-123'

@patch('get_task.boto3')
def test_get_task_not_found(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    mock_table.get_item.return_value = {}

    event = {
        'pathParameters': {'task_id': 'fake-id'},
        'requestContext': {'authorizer': {'claims': {'sub': 'user-123'}}}
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 404

@patch('get_task.boto3')
def test_get_task_wrong_user(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    mock_table.get_item.return_value = {
        'Item': {
            'task_id': 'abc-123',
            'user_id': 'different-user',
            'title': 'Test task',
            'status': 'pending'
        }
    }

    event = {
        'pathParameters': {'task_id': 'abc-123'},
        'requestContext': {'authorizer': {'claims': {'sub': 'user-123'}}}
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 403