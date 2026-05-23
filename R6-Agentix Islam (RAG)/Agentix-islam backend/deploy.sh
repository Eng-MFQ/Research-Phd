#!/bin/bash

# Server details
SERVER_IP="46.225.80.110"
SERVER_USER="agentix"
REMOTE_DIR="/opt/agentix-islam"

# Ensure remote directory exists with correct ownership
ssh $SERVER_USER@$SERVER_IP "sudo mkdir -p $REMOTE_DIR && sudo chown $SERVER_USER:$SERVER_USER $REMOTE_DIR"

# Sync files
echo "Syncing files to $SERVER_IP..."
rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '.venv' --exclude 'env' --exclude '.idea' ./ $SERVER_USER@$SERVER_IP:$REMOTE_DIR

# Copy .env from existing agentix deployment
echo "Copying .env from /opt/agentix..."
ssh $SERVER_USER@$SERVER_IP "cp /opt/agentix/.env $REMOTE_DIR/.env"

# Deploy
echo "Deploying on server..."
ssh $SERVER_USER@$SERVER_IP "cd $REMOTE_DIR && docker compose up -d --build"

echo "Deployment complete!"
