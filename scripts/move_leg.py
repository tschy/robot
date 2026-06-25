import json
import time
import sys
from src.leg_ik import LegIK
from src.servo_controller import ServoController
from src.movement_guard import MovementGuard
from config import DIMENSIONS, SERVO_LIMITS, OFFSETS
from config import SERVOS

def load_robot_config(simulate: bool = True) \
        -> tuple[LegIK, ServoController, MovementGuard]:
    """Reads the JSON configuration to initialize core
    components with safe boundaries and calibrations."""

    dims1 = DIMENSIONS["thigh_length"]
    dims2 = DIMENSIONS["shin_length"]

    # Initialize all three core tools
    leg_engine = LegIK(l1=dims1,l2=dims2)

    controller = ServoController(
        limits=SERVO_LIMITS,
        offsets=OFFSETS,
        simulate=simulate)

    guard = MovementGuard(dims1, dims2)

    return leg_engine, controller, guard


def main():
    """Main execution loop for moving the robot leg
    (supports Host vs RPi modes)."""
    # Check if '--prod' was passed in the terminal arguments
    is_prod = "--prod" in sys.argv
    simulate_mode = not is_prod

    """Main execution loop for moving the physical robot leg."""
    # 1. Initialize the system components
    leg_engine, controller, guard = (
        load_robot_config(simulate=simulate_mode))
    print(f"Robot system initialized. Mode: "
          f"{'REAL HARDWARE (RPi)' if is_prod else 'SIMULATION (Host PC)'}")

    # 2. Define a simple operational path (sequence of XY coordinates)
    path_targets = [
        (0.0, -110.0),  # Target 1: Neutral Standing position straight
        # down
        (30.0, -100.0),  # Target 2: Step Forward
        # (Foot moves out and slightly up)
        (-30.0, -100.0),  # Target 3: Step Backward (Foot pushes behind)
        (0.0, -170.0)  # Target 4: Intentional Out-Of-Reach
        # (To test your MovementGuard)
    ]
    # 3. Execution Loop
    for idx, (target_x, target_y) in enumerate(path_targets):
        print(f"\n--- Processing Target {idx + 1}: "
              f"({target_x}, {target_y}) ---")

        # Check if the coordinate is physically
        # reachable before running math
        if not guard.is_reachable(target_x, target_y):
            print(f"[GUARD REJECTION] Target ("
                  f"{target_x}, {target_y}) is out of reach! Skipping.")
            continue

        # Calculate mathematical ideal angles safely
        raw_hip, raw_knee = leg_engine.calculate_angles(target_x, target_y)
        print(f"Calculated Geometry -> Raw Hip: "
              f"{raw_hip:.1f}°")

        # Send raw angles directly to the controller pipeline
        # The controller automatically applies offsets and safety
        # clamps before writing to I2C
        controller.move_leg(raw_hip)
        print("Hardware commands transmitted successfully.")

        # Wait for hardware to physically complete the move
        time.sleep(1.0)


if __name__ == "__main__":
    main()