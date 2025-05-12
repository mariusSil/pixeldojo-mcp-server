#!/bin/bash
# Development installation script for PixelDojo MCP server

# Check for Python >= 3.11
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher is required (found $python_version)"
    echo "Please install a compatible Python version and try again."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies and package in development mode
echo "Installing package in development mode..."
pip install -e .

# Check if PIXELDOJO_API_KEY is set
if [ -z "$PIXELDOJO_API_KEY" ]; then
    echo ""
    echo "NOTE: PIXELDOJO_API_KEY environment variable is not set."
    echo "Before using the server, set your API key with:"
    echo "export PIXELDOJO_API_KEY=your_api_key_here"
fi

echo ""
echo "✅ Installation complete! You can now run the server with:"
echo "pixeldojo-mcp"
echo ""
echo "For testing with Windsurf, follow the instructions in WINDSURF_INTEGRATION.md"
