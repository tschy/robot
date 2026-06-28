from src.leg_ik import LegIK
from src.movement_guard import MovementGuard
from config import DIMENSIONS

class MovementController:
    def __init__(self, servo_controller):
        self.controller = servo_controller

        dims1 = DIMENSIONS["thigh_length"]
        dims2 = DIMENSIONS["shin_length"]

        # Initialize all three core tools
        self.engine = LegIK(l1=dims1, l2=dims2)
        self.guard = MovementGuard(dims1, dims2)

    def move_to_coordinate(
            self,
            target_x: float,
            target_y: float
    ):
        """Orchestrates the reachability check, math,
        and hardware command."""

        # 1. Guard (Safety Check)
        if not self.guard.is_reachable(target_x, target_y):
            print(f"[GUARD REJECTION] Target ("
                  f"{target_x}, {target_y}"
                  f") out of reach.")
            return False

        print(f"\n--- Processing Target ({target_x}, {target_y}) ---")

        # 2. Geometry (Math Engine)

        hip_angle, knee_angle = self.engine.calculate_angles(
            target_x, target_y
        )

        print(f"Calculated Geometry -> Hip: {hip_angle:.1f}°"
              f", Knee: {knee_angle:.1f}°")

        # 3. Hardware (Servo Driver)
        self.controller.move_joint(hip_angle)

        print(f"Moved to ({target_x}, {target_y}) successfully.")
        return True