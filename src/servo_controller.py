class ServoController:
    def __init__(self,
                 limits: dict[str, tuple[float, float]],
                 offsets: dict[str, float],
                 channels: int = 16,
                 simulate: bool = True):

        self.simulate = simulate
        self.offsets = offsets
        self.limits = limits

        if not self.simulate:
            # Scoped hardware import to prevent host PC
            # environment crashes
            from adafruit_servokit import ServoKit
            self.kit = ServoKit(channels=channels)
            print("[PRODUCTION MODE] ServoController initialized \n "
                  "                  with hardware connection.")

        else:
            print("[SIMULATION MODE] ServoController initialized \n "
                  "                 without physical hardware connection.")

    def clamp_joint_angle(self, angle: float, joint_type: str):
        """Enforces safety limits for a specific joint."""
        min_angle, max_angle = self.limits[joint_type]
        return max(min_angle, min(max_angle, angle))

    def move_leg(self, hip_angle, knee_angle):
        """Processes angles, applies offsets/clamping, and moves
        hardware or simulates it."""
        # 1. Apply offset + clamp for hip
        safe_hip = self.clamp_joint_angle(
            hip_angle + self.offsets["hip"], "hip"
        )

        # 2. Apply offset + clamp for knee
        safe_knee = self.clamp_joint_angle(
            knee_angle + self.offsets["knee"], "knee"
        )

        # 3. Branch execution based on environment mode
        if self.simulate:
            print(
                f"[SIMULATION PWM] Sending Signals -> \n "
                f"   Channel 0 (Hip): {safe_hip:.1f}° |  \n "
                f"   Channel 1 (Knee): {safe_knee:.1f}°")
        else:
            self.kit.servo[0].angle = safe_hip
            self.kit.servo[1].angle = safe_knee