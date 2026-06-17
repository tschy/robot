# Translation Only. Map (θ IK )→ Servo PWM.

from adafruit_servokit import ServoKit

class ServoController:
    def __init__(self,
                 limits: dict[str, tuple[float, float]],
                 offsets: dict[str, float],
                 channels: int = 16):
        self.kit = ServoKit(channels=channels)

        # Physical calibration offsets (degrees)
        # Adjust these once you attach the legs to the servos
        self.offsets = offsets

        # Safe operating range for 9g servos (degrees)
        self.limits = limits

    def clamp_joint_angle(self, angle: float, joint_type: str):
        """Enforces safety limits for a specific joint."""
        min_angle, max_angle = self.limits[joint_type]
        return max(min_angle, min(max_angle, angle))

    def move_leg(self, hip_angle, knee_angle):
        """Processes angles,
        applies offsets/clamping,
        and moves hardware."""
        # 1. Apply offset + clamp for hip
        safe_hip = (self.clamp_joint_angle(
            hip_angle + self.offsets["hip"], "hip"))

        # 2. Apply offset + clamp for knee
        safe_knee = (self.clamp_joint_angle(
            knee_angle + self.offsets["knee"], "knee"))

        # 3. Write to hardware
        self.kit.servo[0].angle = safe_hip
        self.kit.servo[1].angle = safe_knee