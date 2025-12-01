#!/bin/bash

# Virtual Environment Setup Script
# This script creates and activates a Python virtual environment

set -e  # Exit on any error

VENV_NAME="venv"
PYTHON_VERSION="python3"

echo "🐍 Setting up Python virtual environment..."

# Check if Python is installed
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
    echo "📦 Creating virtual environment '$VENV_NAME'..."
    $PYTHON_VERSION -m venv $VENV_NAME
    echo "✅ Virtual environment created successfully!"
else
    echo "📦 Virtual environment '$VENV_NAME' already exists."
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source $VENV_NAME/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📋 Installing requirements from requirements.txt..."
    pip install -r requirements.txt
    echo "✅ Requirements installed successfully!"
else
    echo "📋 No requirements.txt found. You can add dependencies later."
fi

echo ""
echo "🎉 Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment manually, run:"
echo "  source $VENV_NAME/bin/activate"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"
echo ""
echo "To install new packages, activate the environment first, then run:"
echo "  pip install <package_name>"
echo "  pip freeze > requirements.txt  # to save dependencies"