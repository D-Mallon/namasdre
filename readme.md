# Namasdre Project Setup and Deployment Guide

This guide provides step-by-step instructions for setting up, running, and updating the Namasdre project.

## Local Development

1. Start the local development environment:

   ```
   docker compose up --build -d
   ```

   This command builds and starts the Docker containers for the project.

2. To stop the local development environment:
   ```
   docker compose down
   ```

## Deployment

1. Build and push the Docker image:

   ```
   docker buildx build --platform linux/amd64,linux/arm64 -t mallon89/namasdre:v1.0.10 -t mallon89/namasdre:latest --push .
   ```

   This command builds the Docker image for multiple platforms and pushes it to Docker Hub.

2. SSH into the EC2 instance:

   ```
   ssh -i /Users/dmallon/Projects/pemKeys/namasdreKeyPair.pem ubuntu@3.255.167.61
   ```

   Ensure you're in the correct directory (/Users/dmallon/Projects/pemKeys) when running this command.

3. Once connected to the EC2 instance, pull the latest Docker image:

   ```
   docker pull mallon89/namasdre:latest
   ```

4. Run the deployment script:
   ```
   ./set_env_and_run.sh
   ```
   This script sets up the environment and starts the Docker container.

## Updating the Project

1. Make changes to the project locally.

2. Build and push the new Docker image (see step 1 in the Deployment section).

3. SSH into the EC2 instance (see step 2 in the Deployment section).

4. Pull the latest image and restart the container:
   ```
   docker pull mallon89/namasdre:latest
   docker stop namasdre_container
   docker rm namasdre_container
   ./set_env_and_run.sh
   ```

## Copying Files to EC2

To copy files from your local machine to the EC2 instance:

1. Navigate to the pemKeys directory:

   ```
   cd /Users/dmallon/Projects/pemKeys
   ```

2. Use SCP to copy files:
   ```
   scp -i namasdreKeyPair.pem -r /Users/dmallon/Projects/namasdre/* ubuntu@3.255.167.61:~/namasdre_project/
   ```

## Troubleshooting

- If you encounter the error "network with name namasdre_network already exists", you can ignore it if the container starts successfully.
- For issues with static files, ensure that all static files have unique paths across your project.

Remember to replace sensitive information like IP addresses and key paths with placeholders if sharing this README publicly.
