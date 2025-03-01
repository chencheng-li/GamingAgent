import time
import os
import pyautogui
import numpy as np
from datetime import datetime
import random

from tools.utils import encode_image, log_output, extract_python_code
from tools.serving.api_providers import anthropic_completion, openai_completion, gemini_completion

def worker_short_term(thread_id, offset, system_prompt, api_provider, model_name):
    """
    Short-term worker thread: Responsible for handling immediate game actions, such as movement, tool usage, interaction with objects, etc.
    1) Sleeps for 'offset' seconds before starting (to stagger start times)
    2) Continuously takes screenshots, calls AI API, and executes the returned code
    """
    all_response_time = []

    time.sleep(offset)
    print(f"[Thread {thread_id} - SHORT TERM] Starting after {offset}s delay...")

    short_prompt = (
        f"Analyze the current state of Stardew Valley game and generate PyAutoGUI code to control the character's actions for the next 2-3 seconds.\n"
        "Your goal is to execute the most suitable action based on the current state, such as crop care, resource collection, or interacting with NPCs.\n\n"

        "### Basic Control:\n"
        "- WASD: Move up, down, left, or right\n"
        "- Left mouse button: Use handheld tool/interact with items\n"
        "- Number keys 1-12: Switch between item slots\n"
        "- E: Open inventory\n"
        "- F: Eat the current selected food\n"
        "- C: Open crafting menu\n"
        "- ESC: Open game menu/close window\n\n"

        "### Game State Recognition:\n"
        "- Top right corner displays current time and energy\n"
        "- Bottom displays item slots\n"
        "- Recognize current location (farm/town/mine, etc.)\n"
        "- Notice ongoing activities (planting/fishing/mining, etc.)\n\n"

        "### Task Priority:\n"
        "1. Urgent tasks (low energy replenishment/time approaching return)\n"
        "2. Daily tasks (watering/harvesting/animal care)\n"
        "3. Resource collection (gathering/mining/woodcutting)\n"
        "4. Social activities (giving gifts/participating in events)\n\n"

        "### Output Format:\n"
        "- Output only Python code for PyAutoGUI\n"
        "- Add brief comments for each action\n"
    )

    try:
        while True:
            screen_width, screen_height = pyautogui.size()
            region = (0, 0, screen_width, screen_height)
            screenshot = pyautogui.screenshot(region=region)

            thread_folder = f"cache/stardew/thread_{thread_id}"
            os.makedirs(thread_folder, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(thread_folder, f"screenshot_{timestamp}.png")
            screenshot.save(screenshot_path)

            start_time = time.time()
            
            # Prepare message to send to AI
            user_message = (
                f"Current game screenshot. Analyze current state and execute suitable action. \n"
                f"Notice current time, energy, and location, to decide the best action plan."
            )

            # Choose API based on provider
            if api_provider == "anthropic":
                response = anthropic_completion(
                    system_prompt=system_prompt, 
                    model_name=model_name,
                    base64_image=encode_image(screenshot_path),
                    prompt=short_prompt
                )
            elif api_provider == "openai":
                response = openai_completion(
                    system_prompt=system_prompt, 
                    model_name=model_name,
                    base64_image=encode_image(screenshot_path),
                    prompt=short_prompt
                )
            elif api_provider == "gemini":
                response = gemini_completion(
                    system_prompt=system_prompt, 
                    model_name=model_name,
                    base64_image=encode_image(screenshot_path),
                    prompt=short_prompt
                )
            else:
                raise ValueError(f"Unknown API provider: {api_provider}")
            
            end_time = time.time()
            response_time = end_time - start_time
            all_response_time.append(response_time)
            
            print(f"[Thread {thread_id} - SHORT TERM] Response time: {response_time:.2f}s")
            
            # Record output
            log_output(thread_id, response, "stardew")
            
            # Extract and execute code
            code_to_run = extract_python_code(response)
            
            try:
                exec(code_to_run)
            except Exception as e:
                print(f"[Thread {thread_id} - SHORT TERM] Error executing code: {e}")
                time.sleep(1)  # Error pauses briefly
                
            # Control time between screenshots
            time.sleep(35.0)  # Original value was 0.5s
            
    except KeyboardInterrupt:
        print(f"[Thread {thread_id} - SHORT TERM] Interrupted.")
    except Exception as e:
        print(f"[Thread {thread_id} - SHORT TERM] Error: {e}")

def worker_long_term(thread_id, offset, system_prompt, api_provider, model_name):
    """
    Long-term worker thread: Responsible for strategic decision-making and long-term planning, such as seasonal planning, financial management, relationship development, etc.
    1) Sleeps for 'offset' seconds before starting (to stagger start times)
    2) Takes screenshots at a lower frequency, calls AI API to analyze game state and provide long-term strategy recommendations
    """
    all_response_time = []

    time.sleep(offset)
    print(f"[Thread {thread_id} - LONG TERM] Starting after {offset}s delay...")

    long_prompt = (
        f"Analyze the current state of Stardew Valley game and develop long-term planning strategy.\n"
        "Your goal is to analyze current game progress and state, and provide planning suggestions for the next few days or the entire season.\n\n"

        "### Strategic Consideration:\n"
        "- Current season and weather\n"
        "- Farm development status and layout\n"
        "- Available funds and resources\n"
        "- Community center progress\n"
        "- Skill level and unlocked content\n"
        "- NPC relationship status\n\n"

        "### Long-term Planning Points:\n"
        "- Seasonal crop planning\n"
        "- Infrastructure investment (building, tool upgrades, etc.)\n"
        "- Skill development priority\n"
        "- Community center donation plan\n"
        "- Social relationship development\n\n"

        "### Output Format:\n"
        "1. Game state analysis\n"
        "2. Long-term goal setting\n"
        "3. Short-term implementation plan\n"
        "4. Execute code (control character to view necessary information or execute key actions)\n"
    )

    try:
        while True:
            screen_width, screen_height = pyautogui.size()
            region = (0, 0, screen_width, screen_height)
            screenshot = pyautogui.screenshot(region=region)

            thread_folder = f"cache/stardew/thread_{thread_id}"
            os.makedirs(thread_folder, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(thread_folder, f"screenshot_{timestamp}.png")
            screenshot.save(screenshot_path)

            start_time = time.time()
            
            # Choose API based on provider
            if api_provider == "anthropic":
                response = anthropic_completion(
                    system_prompt=system_prompt, 
                    model_name=model_name,
                    base64_image=encode_image(screenshot_path),
                    prompt=long_prompt
                )
            elif api_provider == "openai":
                response = openai_completion(
                    system_prompt=system_prompt, 
                    model_name=model_name,
                    base64_image=encode_image(screenshot_path),
                    prompt=long_prompt
                )
            elif api_provider == "gemini":
                response = gemini_completion(
                    system_prompt=system_prompt, 
                    model_name=model_name,
                    base64_image=encode_image(screenshot_path),
                    prompt=long_prompt
                )
            else:
                raise ValueError(f"Unknown API provider: {api_provider}")
            
            end_time = time.time()
            response_time = end_time - start_time
            all_response_time.append(response_time)
            
            print(f"[Thread {thread_id} - LONG TERM] Response time: {response_time:.2f}s")
            
            # Record output
            log_output(thread_id, response, "stardew")
            
            # Extract and execute code (if any)
            code_to_run = extract_python_code(response)
            
            try:
                if code_to_run and len(code_to_run) > 10:  # Ensure code is not empty
                    exec(code_to_run)
            except Exception as e:
                print(f"[Thread {thread_id} - LONG TERM] Error executing code: {e}")
                
            # Long-term planning thread sleeps for longer
            time.sleep(random.uniform(80, 100))  # Original value was random.uniform(10, 15)
            
    except KeyboardInterrupt:
        print(f"[Thread {thread_id} - LONG TERM] Interrupted.")
    except Exception as e:
        print(f"[Thread {thread_id} - LONG TERM] Error: {e}")