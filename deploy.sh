#!/bin/bash

# Pharma Intelligence API - Deployment Script
# Usage: ./deploy.sh [build|start|stop|restart|logs|status]

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Build the Docker images
build() {
    log_info "Building Docker images..."
    docker-compose build --no-cache
    log_success "Docker images built successfully!"
}

# Start the services
start() {
    log_info "Starting services..."
    docker-compose up -d
    log_success "Services started successfully!"
    log_info "API will be available at: http://localhost:8000"
    log_info "API documentation at: http://localhost:8000/docs"
    log_info "Health check at: http://localhost:8000/health"
    echo ""
    log_info "Waiting for API to be ready..."
    sleep 5
    status
}

# Stop the services
stop() {
    log_info "Stopping services..."
    docker-compose down
    log_success "Services stopped successfully!"
}

# Restart the services
restart() {
    log_info "Restarting services..."
    stop
    start
}

# Show logs
logs() {
    log_info "Showing logs (Ctrl+C to exit)..."
    docker-compose logs -f
}

# Show status
status() {
    log_info "Checking service status..."
    echo ""
    docker-compose ps
    echo ""
    
    # Check API health
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        log_success "API is healthy and responding!"
        echo ""
        log_info "Testing API endpoints..."
        curl -s http://localhost:8000/health | jq '.' 2>/dev/null || curl -s http://localhost:8000/health
    else
        log_warning "API is not responding yet. Check logs with: ./deploy.sh logs"
    fi
}

# Clean up
clean() {
    log_warning "This will remove all containers, images, and volumes. Are you sure? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log_info "Cleaning up..."
        docker-compose down -v --rmi all
        log_success "Cleanup complete!"
    else
        log_info "Cleanup cancelled."
    fi
}

# Main script
check_docker

case "$1" in
    build)
        build
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    clean)
        clean
        ;;
    *)
        echo "Pharma Intelligence API - Deployment Script"
        echo ""
        echo "Usage: ./deploy.sh [command]"
        echo ""
        echo "Commands:"
        echo "  build      Build Docker images"
        echo "  start      Start the services"
        echo "  stop       Stop the services"
        echo "  restart    Restart the services"
        echo "  logs       Show service logs"
        echo "  status     Show service status"
        echo "  clean      Remove all containers, images, and volumes"
        echo ""
        echo "Quick start:"
        echo "  ./deploy.sh build    # First time only"
        echo "  ./deploy.sh start    # Start the API"
        echo ""
        exit 1
        ;;
esac
