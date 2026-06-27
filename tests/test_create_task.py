import json
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'functions'))

from create_task import lambda_handler

@patch('create_task.boto3')
def test_create_task_success(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    event = {
        'body': json.dumps({'title': 'Test task', 'description': 'Test'}),
        'requestContext': {'authorizer': {'claims': {'sub': 'user-123'}}}
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 201
    body = json.loads(result['body'])
    assert body['title'] == 'Test task'
    assert body['user_id'] == 'user-123'
    assert 'task_id' in body

@patch('create_task.boto3')
def test_create_task_missing_title(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    event = {
        'body': json.dumps({'description': 'No title here'}),
        'requestContext': {'authorizer': {'claims': {'sub': 'user-123'}}}
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 400
    body = json.loads(result['body'])
    assert 'error' in body