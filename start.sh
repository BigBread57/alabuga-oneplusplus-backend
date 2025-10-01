#!/bin/bash

# Alabuga OnePlus+ Backend Quick Start Script
# This script helps you quickly start the project

set -e

echo "🚀 Alabuga OnePlus+ Backend Quick Start"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Ask user what mode to run
echo "Select startup mode:"
echo "1) Quick Start (recommended for first time) - uses pre-built images"
echo "2) Development Mode - builds locally with hot-reload"
echo "3) Production Mode - for production deployment"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting in Quick Start mode..."
        echo ""
        docker-compose -f docker-compose.quickstart.yml up -d
        compose_file="docker-compose.quickstart.yml"
        ;;
    2)
        echo ""
        if [ ! -f .env ]; then
            echo "📝 Creating .env file from .env.example..."
            cp .env.example .env
            echo "✅ .env file created. You can edit it if needed."
        fi
        echo ""
        echo "🔨 Starting in Development mode..."
        echo ""
        docker-compose up -d --build
        compose_file="docker-compose.yml"
        ;;
    3)
        echo ""
        if [ ! -f .env ]; then
            echo "⚠️  .env file not found!"
            echo "📝 Creating .env file from .env.production.example..."
            cp .env.production.example .env
            echo ""
            echo "⚠️  IMPORTANT: Please edit .env file and update:"
            echo "   - DJANGO_SECRET_KEY"
            echo "   - POSTGRES_PASSWORD"
            echo "   - DJANGO_DATABASE_PASSWORD"
            echo "   - DJANGO_SUPERUSER_PASSWORD"
            echo "   - DOMAIN_NAME"
            echo ""
            read -p "Press Enter when you're done editing .env..."
        fi
        echo ""
        echo "🚢 Starting in Production mode..."
        echo ""
        docker-compose -f docker-compose.production.yml up -d
        compose_file="docker-compose.production.yml"
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "⏳ Waiting for services to start..."
sleep 5

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📋 Service Status:"
docker-compose -f "$compose_file" ps
echo ""

if [ "$choice" == "1" ] || [ "$choice" == "2" ]; then
    echo "🎉 Project is ready!"
    echo ""
    echo "📍 Available services:"
    echo "   • Backend API:    http://localhost:8000"
    echo "   • API Swagger:    http://localhost:8000/api/schema/swagger-ui/"
    echo "   • Django Admin:   http://localhost:8000/admin/"
    echo "   • Flower:         http://localhost:5555"
    echo ""
    echo "🔑 Default credentials:"
    echo "   Email:    admin@example.com"
    echo "   Password: admin"
    echo ""
elif [ "$choice" == "3" ]; then
    echo "🎉 Production deployment completed!"
    echo ""
    echo "📍 Your application should be available at:"
    echo "   https://$(grep DOMAIN_NAME .env | cut -d '=' -f2)"
    echo ""
fi

echo "📚 Useful commands:"
echo "   • View logs:          docker-compose -f $compose_file logs -f"
echo "   • Stop services:      docker-compose -f $compose_file down"
echo "   • Restart services:   docker-compose -f $compose_file restart"
echo ""
echo "📖 For more information, see:"
echo "   • QUICKSTART.md - Quick start guide"
echo "   • DEPLOYMENT.md - Production deployment guide"
echo "   • README.md     - General documentation"
echo ""
