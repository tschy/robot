import time
import sys
from src.movement_controller import MovementController
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
        (179.8, 8.8),  # Math Hip: ~5.1°   -> Hardware: ~5.0° (Clamped)
        (178.6, 21.0),  # Math Hip: ~15.1°  -> Hardware: ~5.1°
        (175.5, 47.1),  # Math Hip: ~25.1°  -> Hardware: ~15.1°
        (169.1, 75.6),  # Math Hip: ~35.1°  -> Hardware: ~25.1°
        (159.5, 102.3),  # Math Hip: ~45.1°  -> Hardware: ~35.1°
        (146.9, 126.3),  # Math Hip: ~55.1°  -> Hardware: ~45.1°
        (131.6, 147.1),  # Math Hip: ~65.1°  -> Hardware: ~55.1°
        (113.8, 164.3),  # Math Hip: ~75.1°  -> Hardware: ~65.1°
        (93.9, 177.3),  # Math Hip: ~85.1°  -> Hardware: ~75.1°
        (72.2, 185.5),  # Math Hip: ~95.1°  -> Hardware: ~85.1°
        (49.2, 188.7),  # Math Hip: ~105.1° -> Hardware: ~95.1°
        (25.4, 186.7),  # Math Hip: ~115.1° -> Hardware: ~105.1°
        (1.2, 179.9),  # Math Hip: ~125.1° -> Hardware: ~115.1°
        (-22.7, 167.9),  # Math Hip: ~135.1° -> Hardware: ~125.1°
        (-46.0, 150.9),  # Math Hip: ~145.1° -> Hardware: ~135.1°
        (-68.1, 129.2),  # Math Hip: ~155.1° -> Hardware: ~145.1°
        (-88.7, 103.8),  # Math Hip: ~165.1° -> Hardware: ~155.1°
        (-107.0, 75.5),  # Math Hip: ~175.1° -> Hardware: ~165.1°
        (-122.3, 45.4)  # Math Hip: ~185.1° -> Hardware: ~175.1°
    ]
    # 3. Execution Loop
    for idx, (target_x, target_y) in enumerate(path_targets):

        pilot.move_to_coordinate(target_x, target_y)

        print("Hardware commands transmitted successfully.")

        # Wait for hardware to physically complete the move
        time.sleep(1.0)

if __name__ == "__main__":
    main()