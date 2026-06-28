import time
import sys
from scripts.movement_controller import MovementController
from src.servo_controller import ServoController



def main():
    """Main execution loop for moving the robot leg
    (supports Host vs RPi modes)."""
    # Check if '--prod' was passed in the terminal arguments
    is_prod = "--prod" in sys.argv
    simulate_mode = not is_prod

    """Main execution loop for moving the physical robot leg."""

    servo_driver = ServoController.from_config(simulate=simulate_mode)

    pilot = MovementController(servo_driver)

    print(f"Robot system initialized. Mode: "
          f"{'REAL HARDWARE (RPi)' if is_prod else 'SIMULATION (Host PC)'}")

    # 2. Define a simple operational path (sequence of XY coordinates)
    path_targets = [
        (0.0, 110.0),  # Target 1: Neutral (should result in ~90°)
        (20.0, 90.0),  # Target 2: Slight forward and up
        (0.0, 110.0),  # Target 3: Return to Neutral
        (20.0, 90.0),  # Target 4: Slight backward and up
        (0.0, 130.0)  # Target 5: Extend further down
    ]
    # 3. Execution Loop
    for idx, (target_x, target_y) in enumerate(path_targets):

        pilot.move_to_coordinate(target_x, target_y)

        print("Hardware commands transmitted successfully.")

        # Wait for hardware to physically complete the move
        time.sleep(1.0)


if __name__ == "__main__":
    main()