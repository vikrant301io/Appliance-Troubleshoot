# PowerShell script for building and pushing Docker image to ECR
# Usage: .\scripts\build-and-push.ps1 -Region us-east-1 -AccountId YOUR_ACCOUNT_ID -ImageTag latest

param(
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-east-1",
    
    [Parameter(Mandatory=$true)]
    [string]$AccountId,
    
    [Parameter(Mandatory=$false)]
    [string]$ImageTag = "latest"
)

$ErrorActionPreference = "Stop"

$ImageName = "appliance-assistant"
$EcrRepository = "${AccountId}.dkr.ecr.${Region}.amazonaws.com/${ImageName}"

Write-Host "Building Docker image..." -ForegroundColor Green
docker build -t ${ImageName}:${ImageTag} .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Tagging image for ECR..." -ForegroundColor Green
docker tag ${ImageName}:${ImageTag} ${EcrRepository}:${ImageTag}
docker tag ${ImageName}:${ImageTag} ${EcrRepository}:latest

Write-Host "Logging in to ECR..." -ForegroundColor Green
$loginCommand = aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $EcrRepository

if ($LASTEXITCODE -ne 0) {
    Write-Host "ECR login failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Pushing image to ECR..." -ForegroundColor Green
docker push ${EcrRepository}:${ImageTag}
docker push ${EcrRepository}:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Image pushed successfully!" -ForegroundColor Green
Write-Host "Image URI: ${EcrRepository}:${ImageTag}" -ForegroundColor Cyan

