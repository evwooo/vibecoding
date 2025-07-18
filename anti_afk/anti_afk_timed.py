import pyautogui
import time
import random

def main():
    """
    This script prevents the computer from going into sleep mode by periodically
    moving the mouse, clicking at its original position, and pressing the spacebar.
    It runs for a user-specified duration.
    """
    print("Anti-AFK script started.")
    pyautogui.FAILSAFE = False

    # Get the duration from the user.
    while True:
        try:
            duration_minutes = float(input("Enter the duration in minutes to run the script: "))
            if duration_minutes > 0:
                break
            else:
                print("Please enter a positive number for the duration.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    duration_seconds = duration_minutes * 60
    start_time = time.time()
    end_time = start_time + duration_seconds

    print(f"Script will run for {duration_minutes} minutes.")
    print("Press Ctrl+C to stop the script early.")

    # Get the initial mouse position.
    original_x, original_y = pyautogui.position()

    try:
        while time.time() < end_time:
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
            
            # Check if the next sleep would exceed the end time.
            if time.time() + sleep_duration > end_time:
                # Adjust sleep to finish exactly on time.
                sleep_duration = end_time - time.time()
                if sleep_duration <= 0:
                    break # Exit if no time is left.

            print(f"Next action in {sleep_duration:.2f} seconds...")
            time.sleep(sleep_duration)
            
    except KeyboardInterrupt:
        print("\nAnti-AFK script stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # This will run whether the script finishes naturally or is interrupted.
        if time.time() >= end_time:
             print("\nSpecified duration reached. Anti-AFK script finished.")
        else:
             print("\nAnti-AFK script stopped before duration was reached.")


if __name__ == "__main__":
    main()
