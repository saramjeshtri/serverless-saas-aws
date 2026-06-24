# Serverless SaaS Backend on AWS

A fully serverless REST API built with AWS Lambda, API Gateway, and DynamoDB.
Infrastructure managed with Terraform.

## Architecture
API Gateway → Lambda → DynamoDB

## Stack

- **Runtime:** Python 3.12
- **Compute:** AWS Lambda
- **API:** AWS API Gateway
- **Database:** AWS DynamoDB
- **IaC:** Terraform
- **Region:** us-east-1

## Endpoints

| Method | Path | Handler |
|--------|------|---------|
| POST | /tasks | create_task |
| GET | /tasks | get_tasks |
| GET | /tasks/{task_id} | get_task |
| PUT | /tasks/{task_id} | update_task |
| DELETE | /tasks/{task_id} | delete_task |

## Usage

```bash
# Deploy
cd infrastructure
terraform init && terraform apply

# Create task
curl -X POST $API_URL/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "task title", "description": "task description"}'

# Get all tasks
curl $API_URL/tasks

# Update task
curl -X PUT $API_URL/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Delete task
curl -X DELETE $API_URL/tasks/{task_id}
```

## Requirements

- AWS CLI configured
- Terraform >= 1.0