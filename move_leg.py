import json
import time
import sys
from src.leg_ik import LegIK
from src.servo_controller import ServoController
from src.movement_guard import MovementGuard


def load_robot_config(config_path: str = "config/test_leg_config.json",
                      simulate: bool = True) \
        -> tuple[LegIK, ServoController, MovementGuard]:
    """Reads the JSON configuration to initialize core
    components with safe boundaries and calibrations."""
    with open(config_path, "r") as file:
        config = json.load(file)

    dims = config["dimensions"]
    limits = config["servo_limits"]
    offsets = config["offsets"]

    # Initialize all three core tools
    leg_engine = LegIK(l1=dims["thigh_length"], l2=dims["shin_length"])
    controller = ServoController(
        limits=limits, offsets=offsets, simulate=simulate)
    guard = MovementGuard(l1=dims["thigh_length"], l2=dims["shin_length"])

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
        (10.0, -8.0),
        (0.0, -15.0),
        (5.0, -5.0),
        (30.0, -30.0) # Intentional out-of-reach target to test the guard
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
              f"{raw_hip:.1f}°, Raw Knee: {raw_knee:.1f}°")

        # Send raw angles directly to the controller pipeline
        # The controller automatically applies offsets and safety
        # clamps before writing to I2C
        controller.move_leg(raw_hip, raw_knee)
        print("Hardware commands transmitted successfully.")

        # Wait for hardware to physically complete the move
        time.sleep(1.0)


if __name__ == "__main__":
    main()