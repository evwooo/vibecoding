import pyautogui
import time
import random

def main():
    """
    This script prevents the computer from going into sleep mode by periodically
    moving the mouse, clicking at its original position, and pressing the spacebar.
    """
    print("Anti-AFK script started. Press Ctrl+C to stop.")
    pyautogui.FAILSAFE = False

    # Get the initial mouse position.
    original_x, original_y = pyautogui.position()

    try:
        while True:
            # Move the mouse to a random position on the screen.
            screen_width, screen_height = pyautogui.size()
            random_x = random.randint(0, screen_width - 1)
            random_y = random.randint(0, screen_height - 1)
            
            pyautogui.moveTo(random_x, random_y, duration=0.5)
            
            # Return to the original position to click.
            pyautogui.moveTo(original_x, original_y, duration=0.5)
            pyautogui.click()
            
            # Press the spacebar.
            pyautogui.press('space')
            
            # Wait for a random interval between 10 and 30 seconds.
            sleep_duration = random.randint(10, 30)
            print(f"Next action in {sleep_duration} seconds...")
            time.sleep(sleep_duration)
            
    except KeyboardInterrupt:
        print("\nAnti-AFK script stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()