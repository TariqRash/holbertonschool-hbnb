#!/bin/bash
# HBnB Database Setup Script
# This script sets up the database with schema and sample data

echo "🗄️  Setting up HBnB database..."

# Create instance directory if it doesn't exist
mkdir -p instance

# Check if database already exists
if [ -f "instance/development.db" ]; then
    echo "⚠️  Database already exists at instance/development.db"
    read -p "Do you want to reset it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old database..."
        rm -f instance/development.db
    else
        echo "❌ Cancelled. Database left unchanged."
        exit 0
    fi
fi

# Create database with schema
echo "📋 Creating database schema..."
sqlite3 instance/development.db < schema.sql

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create schema"
    exit 1
fi

# Load sample data
echo "📦 Loading sample data..."
sqlite3 instance/development.db < seed.sql

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to load sample data"
    exit 1
fi

# Verify setup
echo ""
echo "✅ Database setup complete!"
echo ""
echo "📊 Database contains:"
echo "  - Users: $(sqlite3 instance/development.db 'SELECT COUNT(*) FROM users;')"
echo "  - Places: $(sqlite3 instance/development.db 'SELECT COUNT(*) FROM places;')"
echo "  - Amenities: $(sqlite3 instance/development.db 'SELECT COUNT(*) FROM amenities;')"
echo "  - Reviews: $(sqlite3 instance/development.db 'SELECT COUNT(*) FROM reviews;')"
echo ""
echo "🔐 Login credentials:"
echo "  Admin: admin@hbnb.io / admin1234"
echo "  User: john@example.com / 123456"
echo ""
echo "🚀 You can now run the application with: python3 run.py"
