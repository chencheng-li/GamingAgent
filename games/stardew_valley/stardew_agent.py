import time
import numpy as np
import concurrent.futures
import argparse
import os

from games.stardew_valley.workers import worker_short_term, worker_long_term

# System prompt content - Designed specifically for Stardew Valley game
system_prompt = (
    "You are an intelligent Stardew Valley game agent. Your task is to analyze the game screen, understand the current game state, "
    "and execute the best actions to manage the farm, develop skills, build social relationships, and complete game tasks."
    "\n\n"
    "Game objectives include but are not limited to:\n"
    "- Develop and optimize the farm (plant crops, raise animals, build facilities)\n"
    "- Complete Community Center donations (collect various items)\n"
    "- Develop friendships and relationships with villagers\n"
    "- Upgrade tools and skills\n"
    "- Explore mines and other areas\n"
    "- Participate in seasonal activities and festivals\n"
    "\n\n"
    "Please make the best decisions based on visual information in the game (time, energy, location, inventory, etc.)."
)

def main():
    """
    Launch the Stardew Valley game agent, supporting short-term and long-term planning threads.
    """
    parser = argparse.ArgumentParser(
        description="Stardew Valley AI Game Agent - Use AI to automate playing Stardew Valley"
    )
    parser.add_argument("--api_provider", type=str, default="anthropic",
                      help="API provider to use (anthropic, openai, gemini)")
    parser.add_argument("--model_name", type=str, default="claude-3-7-sonnet-20250219",
                      help="Model name to use (must have vision capabilities)")
    parser.add_argument("--concurrency_interval", type=float, default=1.0,
                      help="Interval time between starting worker threads (seconds)")
    parser.add_argument("--api_response_latency_estimate", type=float, default=8.0,
                      help="Estimated API response latency time (seconds)")
    parser.add_argument("--policy", type=str, default="mixed", 
                      choices=["mixed", "short", "long"],
                      help="Agent policy: 'mixed', 'short', or 'long'")
    parser.add_argument("--game_path", type=str, 
                      default="/Users/chenchengli/Library/Application Support/Steam/steamapps/common/Stardew Valley/Contents/MacOS/Stardew Valley",
                      help="Path to the Stardew Valley game executable")
    parser.add_argument("--auto_launch", type=bool, default=False,
                      help="Whether to automatically launch the game")

    args = parser.parse_args()

    # Create cache directory
    os.makedirs("cache/stardew", exist_ok=True)

    # If auto-launch is enabled, start the game
    if args.auto_launch and os.path.exists(args.game_path):
        try:
            print(f"Launching game: {args.game_path}")
            os.system(f"open \"{args.game_path}\"")
            print("Waiting for game to start...")
            time.sleep(10)  # Give the game some time to start
        except Exception as e:
            print(f"Error launching game: {e}")
            print("Please start the game manually, then run this script.")
    
    # Calculate number of threads based on latency and interval
    num_threads = max(2, int(args.api_response_latency_estimate / args.concurrency_interval))
    offsets = [i * args.concurrency_interval for i in range(num_threads)]

    print(f"Starting {num_threads} threads using '{args.policy}' policy...")
    print(f"API Provider: {args.api_provider}, Model: {args.model_name}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            if args.policy == "mixed":
                # Mixed policy: one long-term thread, the rest are short-term threads
                if i == 0:
                    executor.submit(worker_long_term, i, offsets[i], system_prompt, args.api_provider, args.model_name)
                else:
                    executor.submit(worker_short_term, i, offsets[i], system_prompt, args.api_provider, args.model_name)
            elif args.policy == "short":
                # Short-term threads only
                executor.submit(worker_short_term, i, offsets[i], system_prompt, args.api_provider, args.model_name)
            elif args.policy == "long":
                # Long-term threads only
                executor.submit(worker_long_term, i, offsets[i], system_prompt, args.api_provider, args.model_name)

        try:
            while True:
                time.sleep(0.25)
        except KeyboardInterrupt:
            print("\nMain thread interrupted. Exiting all threads...")

if __name__ == "__main__":
    main() 