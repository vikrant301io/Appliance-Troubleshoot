#!/bin/bash

# Build and push Docker image to ECR
# Usage: ./scripts/build-and-push.sh <aws-region> <aws-account-id> [image-tag]

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=${2:-""}
IMAGE_TAG=${3:-latest}
IMAGE_NAME="appliance-assistant"
ECR_REPOSITORY="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE_NAME}"

if [ -z "$ACCOUNT_ID" ]; then
    echo "Error: AWS Account ID is required"
    echo "Usage: $0 <aws-region> <aws-account-id> [image-tag]"
    exit 1
fi

echo "Building Docker image..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo "Tagging image for ECR..."
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REPOSITORY}:${IMAGE_TAG}
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REPOSITORY}:latest

echo "Logging in to ECR..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_REPOSITORY}

echo "Pushing image to ECR..."
docker push ${ECR_REPOSITORY}:${IMAGE_TAG}
docker push ${ECR_REPOSITORY}:latest

echo "✅ Image pushed successfully!"
echo "Image URI: ${ECR_REPOSITORY}:${IMAGE_TAG}"

