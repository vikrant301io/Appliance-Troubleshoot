.PHONY: help build push deploy setup test clean

# Default values
REGION ?= us-east-1
ACCOUNT_ID ?= 
IMAGE_TAG ?= latest
CLUSTER_NAME ?= appliance-assistant-cluster
SERVICE_NAME ?= appliance-troubleshoot-assistant-service

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image locally
	docker build -t appliance-assistant:$(IMAGE_TAG) .

test: ## Run tests locally
	python -m pytest tests/ -v

setup: ## Setup AWS resources (ECR, ECS cluster, etc.)
	@if [ -z "$(ACCOUNT_ID)" ]; then \
		echo "Error: ACCOUNT_ID is required. Usage: make setup ACCOUNT_ID=123456789012"; \
		exit 1; \
	fi
	chmod +x scripts/setup-aws-resources.sh
	./scripts/setup-aws-resources.sh $(REGION) $(ACCOUNT_ID)

push: ## Build and push Docker image to ECR
	@if [ -z "$(ACCOUNT_ID)" ]; then \
		echo "Error: ACCOUNT_ID is required. Usage: make push ACCOUNT_ID=123456789012"; \
		exit 1; \
	fi
	chmod +x scripts/build-and-push.sh
	./scripts/build-and-push.sh $(REGION) $(ACCOUNT_ID) $(IMAGE_TAG)

deploy: ## Deploy/update ECS service
	chmod +x scripts/deploy-ecs.sh
	./scripts/deploy-ecs.sh $(REGION) $(CLUSTER_NAME) $(SERVICE_NAME)

logs: ## View CloudWatch logs
	aws logs tail /ecs/appliance-troubleshoot-assistant --follow --region $(REGION)

status: ## Check ECS service status
	aws ecs describe-services \
		--cluster $(CLUSTER_NAME) \
		--services $(SERVICE_NAME) \
		--region $(REGION) \
		--query 'services[0].{Status:status,Running:runningCount,Desired:desiredCount,Events:events[0:3]}' \
		--output table

clean: ## Remove local Docker images
	docker rmi appliance-assistant:$(IMAGE_TAG) || true

docker-run: ## Run Docker container locally
	docker-compose up --build

docker-stop: ## Stop local Docker container
	docker-compose down

