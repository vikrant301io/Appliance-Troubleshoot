#!/bin/bash

# Deploy ECS service
# Usage: ./scripts/deploy-ecs.sh <aws-region> <cluster-name> <service-name>

set -e

REGION=${1:-us-east-1}
CLUSTER_NAME=${2:-appliance-assistant-cluster}
SERVICE_NAME=${3:-appliance-troubleshoot-assistant-service}

if [ -z "$CLUSTER_NAME" ] || [ -z "$SERVICE_NAME" ]; then
    echo "Error: Cluster name and service name are required"
    echo "Usage: $0 <aws-region> <cluster-name> <service-name>"
    exit 1
fi

echo "Updating ECS service..."
aws ecs update-service \
    --cluster ${CLUSTER_NAME} \
    --service ${SERVICE_NAME} \
    --force-new-deployment \
    --region ${REGION}

echo "Waiting for service to stabilize..."
aws ecs wait services-stable \
    --cluster ${CLUSTER_NAME} \
    --services ${SERVICE_NAME} \
    --region ${REGION}

echo "✅ Deployment complete!"
echo "Service: ${SERVICE_NAME}"
echo "Cluster: ${CLUSTER_NAME}"

