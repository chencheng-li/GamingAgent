#!/usr/bin/env python3
"""
Stardew Valley AI Game Agent Launcher - Python Version
Run this script directly with Python to avoid module import issues
"""

import os
import sys
import subprocess
import argparse

def check_api_keys():
    """Check if API keys are set"""
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')
    gemini_key = os.environ.get('GEMINI_API_KEY')
    
    if not any([anthropic_key, openai_key, gemini_key]):
        print("Warning: No API key environment variables detected. Please set at least one of the following environment variables:")
        print("  export ANTHROPIC_API_KEY=your_key_here")
        print("  export OPENAI_API_KEY=your_key_here")
        print("  export GEMINI_API_KEY=your_key_here")
        return False
    
    # Determine default API provider
    api_provider = "anthropic"
    model_name = "claude-3-7-sonnet-20250219"
    
    if not anthropic_key:
        if openai_key:
            api_provider = "openai"
            model_name = "gpt-4o"
        elif gemini_key:
            api_provider = "gemini"
            model_name = "gemini-1.5-pro"
    
    return api_provider, model_name

def main():
    parser = argparse.ArgumentParser(description="Stardew Valley AI Game Agent Launcher")
    parser.add_argument("--api_provider", type=str, 
                        help="API provider to use (anthropic, openai, gemini)")
    parser.add_argument("--model_name", type=str, 
                        help="Model name to use")
    parser.add_argument("--policy", type=str, default="mixed",
                        choices=["mixed", "short", "long"],
                        help="Agent policy: 'mixed', 'short', or 'long'")
    
    args = parser.parse_args()
    
    # Check API keys
    api_result = check_api_keys()
    if not api_result:
        sys.exit(1)
    
    default_api_provider, default_model_name = api_result
    
    # Use command line arguments or defaults
    api_provider = args.api_provider or default_api_provider
    model_name = args.model_name or default_model_name
    policy = args.policy
    
    # Print welcome message
    print("======================================================")
    print("   Stardew Valley AI Game Agent Launcher (Python Version)")
    print("======================================================")
    print("Usage tips:")
    print("1. Make sure you've manually started Stardew Valley")
    print("2. Use fullscreen or windowed mode to ensure game window is visible")
    print("3. Press Ctrl+C at any time to stop the agent")
    print("")
    print("Current configuration:")
    print(f"- API Provider: {api_provider}")
    print(f"- Model: {model_name}")
    print(f"- Policy: {policy}")
    print("======================================================")
    
    # Ask user to confirm
    confirm = input("Start the agent with the above configuration? (y/n): ")
    if confirm.lower() != 'y':
        print("Launch cancelled.")
        sys.exit(0)
    
    # Get path to the script's root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Method 1: Set environment variables and run as subprocess (similar to bash script method)
    try:
        # Set environment variables
        env = os.environ.copy()
        env['PYTHONPATH'] = script_dir  # Set PYTHONPATH to project root directory
        
        # Prepare command line arguments
        agent_script = os.path.join(script_dir, "games", "stardew_valley", "stardew_agent.py")
        cmd = [
            sys.executable,
            agent_script,
            f"--api_provider={api_provider}",
            f"--model_name={model_name}",
            f"--policy={policy}"
        ]
        
        # Run agent
        print(f"Starting Stardew Valley AI Game Agent...")
        subprocess.run(cmd, env=env, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {e}")
        
        # Method 2: Try running as a Python module
        print("Trying to run as a module...")
        try:
            # Add project root directory to Python path
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)
            
            # Set command line arguments
            sys.argv = [
                sys.argv[0],
                f"--api_provider={api_provider}",
                f"--model_name={model_name}",
                f"--policy={policy}"
            ]
            
            # Import and run
            from games.stardew_valley.stardew_agent import main as stardew_main
            stardew_main()
            
        except ImportError as e:
            print(f"Module import failed: {e}")
            print("Please make sure you're running this script from the project root directory")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nUser interrupted, exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main() 