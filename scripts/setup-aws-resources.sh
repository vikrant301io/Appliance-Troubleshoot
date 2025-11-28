#!/bin/bash

# Setup AWS resources for ECS deployment
# Usage: ./scripts/setup-aws-resources.sh <aws-region> <aws-account-id>

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=${2:-""}
IMAGE_NAME="appliance-assistant"
CLUSTER_NAME="appliance-assistant-cluster"
SERVICE_NAME="appliance-troubleshoot-assistant-service"
LOG_GROUP="/ecs/appliance-troubleshoot-assistant"

if [ -z "$ACCOUNT_ID" ]; then
    echo "Error: AWS Account ID is required"
    echo "Usage: $0 <aws-region> <aws-account-id>"
    exit 1
fi

echo "Setting up AWS resources..."

# Create ECR repository
echo "Creating ECR repository..."
aws ecr create-repository \
    --repository-name ${IMAGE_NAME} \
    --region ${REGION} \
    --image-scanning-configuration scanOnPush=true \
    --encryption-configuration encryptionType=AES256 \
    || echo "Repository already exists"

# Create ECS cluster
echo "Creating ECS cluster..."
aws ecs create-cluster \
    --cluster-name ${CLUSTER_NAME} \
    --region ${REGION} \
    --capacity-providers FARGATE FARGATE_SPOT \
    --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1 \
    || echo "Cluster already exists"

# Create CloudWatch log group
echo "Creating CloudWatch log group..."
aws logs create-log-group \
    --log-group-name ${LOG_GROUP} \
    --region ${REGION} \
    || echo "Log group already exists"

# Create secrets manager secret for OpenAI API key (if not exists)
echo "Creating Secrets Manager secret..."
aws secretsmanager create-secret \
    --name appliance-assistant/openai-api-key \
    --description "OpenAI API Key for Appliance Troubleshoot Assistant" \
    --region ${REGION} \
    --secret-string "{\"apiKey\":\"YOUR_OPENAI_API_KEY_HERE\"}" \
    || echo "Secret already exists (update it manually with: aws secretsmanager put-secret-value)"

echo "✅ AWS resources setup complete!"
echo ""
echo "Next steps:"
echo "1. Update the OpenAI API key in Secrets Manager:"
echo "   aws secretsmanager put-secret-value --secret-id appliance-assistant/openai-api-key --secret-string '{\"apiKey\":\"your-key\"}' --region ${REGION}"
echo ""
echo "2. Build and push Docker image:"
echo "   ./scripts/build-and-push.sh ${REGION} ${ACCOUNT_ID}"
echo ""
echo "3. Create task definition:"
echo "   aws ecs register-task-definition --cli-input-json file://ecs/task-definition.json --region ${REGION}"
echo ""
echo "4. Create ECS service:"
echo "   aws ecs create-service --cli-input-json file://ecs/service-definition.json --region ${REGION}"

