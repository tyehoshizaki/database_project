#!/bin/bash

# Quick activation script for the virtual environment
# Usage: source activate_venv.sh

if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated!"
    echo "📋 Current Python: $(which python)"
    echo "📋 Current pip: $(which pip)"
else
    echo "❌ Virtual environment not found. Run './setup_venv.sh' first."
fi