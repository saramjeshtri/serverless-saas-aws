# serverless-saas-aws

Serverless task management API on AWS. Users authenticate via Cognito and can only access their own tasks. Infrastructure managed with Terraform.

## Stack

- **Compute:** AWS Lambda (Python 3.12)
- **API:** API Gateway + Cognito authorizer
- **Database:** DynamoDB
- **Auth:** Cognito User Pool
- **IaC:** Terraform

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /tasks | Create a task |
| GET | /tasks | Get your tasks |
| GET | /tasks/{task_id} | Get a task by ID |
| PUT | /tasks/{task_id} | Update a task |
| DELETE | /tasks/{task_id} | Delete a task |

All endpoints require a valid Cognito JWT token in the `Authorization` header.

## Live API

Base URL: `https://lliax9894k.execute-api.us-east-1.amazonaws.com/dev`

To test the API you need a Cognito token. Register and login using the Authentication section below, then use the token in the Usage examples.

## Deploy

```bash
cd infrastructure
terraform init && terraform apply
```

## Authentication

```bash
# Register
aws cognito-idp sign-up \
  --client-id $CLIENT_ID \
  --username you@example.com \
  --password YourPassword1! \
  --user-attributes Name=email,Value=you@example.com

# Login
aws cognito-idp initiate-auth \
  --client-id $CLIENT_ID \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=you@example.com,PASSWORD=YourPassword1!

# Use the IdToken from the response
curl -H "Authorization: $ID_TOKEN" $API_URL/tasks
```

## Usage

```bash
# Create task
curl -X POST $API_URL/tasks \
  -H "Authorization: $ID_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "task title", "description": "task description"}'

# Get all tasks
curl -H "Authorization: $ID_TOKEN" $API_URL/tasks

# Update task
curl -X PUT $API_URL/tasks/{task_id} \
  -H "Authorization: $ID_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Delete task
curl -X DELETE $API_URL/tasks/{task_id} \
  -H "Authorization: $ID_TOKEN"
```

## Requirements

- AWS CLI configured
- Terraform >= 1.0