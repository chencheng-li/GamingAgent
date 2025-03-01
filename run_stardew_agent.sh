#!/bin/bash

# Ensure API keys are set
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ] && [ -z "$GEMINI_API_KEY" ]; then
    echo "Warning: No API key environment variables detected. Please set at least one of the following environment variables:"
    echo "  export ANTHROPIC_API_KEY=your_key_here"
    echo "  export OPENAI_API_KEY=your_key_here"
    echo "  export GEMINI_API_KEY=your_key_here"
    exit 1
fi

# Default parameters
API_PROVIDER="anthropic"
MODEL_NAME="claude-3-7-sonnet-20250219"
POLICY="mixed"

# If Anthropic API key isn't set but others are, adjust defaults
if [ -z "$ANTHROPIC_API_KEY" ]; then
    if [ -n "$OPENAI_API_KEY" ]; then
        API_PROVIDER="openai"
        MODEL_NAME="gpt-4o"
    elif [ -n "$GEMINI_API_KEY" ]; then
        API_PROVIDER="gemini"
        MODEL_NAME="gemini-1.5-pro"
    fi
fi

# Print welcome message
echo "======================================================"
echo "   Stardew Valley AI Game Agent Launcher"
echo "======================================================"
echo "Usage tips:"
echo "1. Make sure you've manually started Stardew Valley"
echo "2. Use fullscreen or windowed mode to ensure game window is visible"
echo "3. Press Ctrl+C at any time to stop the agent"
echo ""
echo "Current configuration:"
echo "- API Provider: $API_PROVIDER"
echo "- Model: $MODEL_NAME"
echo "- Policy: $POLICY"
echo "======================================================"

# Ask user to confirm
read -p "Start the agent with the above configuration? (y/n): " CONFIRM

if [[ $CONFIRM != "y" && $CONFIRM != "Y" ]]; then
    echo "Launch cancelled."
    exit 0
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run the game agent - set PYTHONPATH to correctly import modules
PYTHONPATH="$SCRIPT_DIR" python "$SCRIPT_DIR/games/stardew_valley/stardew_agent.py" --api_provider $API_PROVIDER --model_name $MODEL_NAME --policy $POLICY 