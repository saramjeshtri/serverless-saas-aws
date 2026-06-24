locals {
  table_name = aws_dynamodb_table.tasks.name
  lambda_role_arn = aws_iam_role.lambda_role.arn
  runtime = "python3.12"
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda-basic-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attach basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole"
}

# Attach DynamoDB policy
resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

# Lambda function - create_task
resource "aws_lambda_function" "create_task" {
  filename      = "${path.module}/../functions/create_task.zip"
  function_name = "create-task"
  role          = local.lambda_role_arn
  handler       = "create_task.lambda_handler"
  runtime       = local.runtime

  environment {
    variables = {
      TABLE_NAME = local.table_name
    }
  }
}

# Lambda function - get_tasks
resource "aws_lambda_function" "get_tasks" {
  filename      = "${path.module}/../functions/get_tasks.zip"
  function_name = "get-tasks"
  role          = local.lambda_role_arn
  handler       = "get_tasks.lambda_handler"
  runtime       = local.runtime

  environment {
    variables = {
      TABLE_NAME = local.table_name
    }
  }
}

# Lambda function - get_task
resource "aws_lambda_function" "get_task" {
  filename      = "${path.module}/../functions/get_task.zip"
  function_name = "get-task"
  role          = local.lambda_role_arn
  handler       = "get_task.lambda_handler"
  runtime       = local.runtime

  environment {
    variables = {
      TABLE_NAME = local.table_name
    }
  }
}

# Lambda function - update_task
resource "aws_lambda_function" "update_task" {
  filename      = "${path.module}/../functions/update_task.zip"
  function_name = "update-task"
  role          = local.lambda_role_arn
  handler       = "update_task.lambda_handler"
  runtime       = local.runtime

  environment {
    variables = {
      TABLE_NAME = local.table_name
    }
  }
}

# Lambda function - delete_task
resource "aws_lambda_function" "delete_task" {
  filename      = "${path.module}/../functions/delete_task.zip"
  function_name = "delete-task"
  role          = local.lambda_role_arn
  handler       = "delete_task.lambda_handler"
  runtime       = local.runtime

  environment {
    variables = {
      TABLE_NAME = local.table_name
    }
  }
}