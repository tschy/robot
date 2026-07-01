from config import SERVOS
from config import SERVO_LIMITS, OFFSETS


class ServoController:
    def __init__(self,
                 limits: dict[str, tuple[float, float]],
                 offsets: dict[str, float],
                 servos: dict[str, float],
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

            servo_0_config = SERVOS["0"]
            
            self.kit.servo[0].set_pulse_width_range(
                servo_0_config["min_pulse"],
                servo_0_config["max_pulse"],
            )

            print("[PRODUCTION MODE] ServoController initialized \n "
                  "                  with hardware connection.")

            print(f"[PRODUCTION MODE] min_pulse {servo_0_config['min_pulse']},\n "
                  f"                  max_pulse {servo_0_config['max_pulse']}.")

        else:
            print("[SIMULATION MODE] ServoController initialized \n "
                  "                 without physical hardware connection.")

    @classmethod
    def from_config(cls, simulate: bool = True):
        # 2. The class "keeps" the details here
        return cls(
            limits=SERVO_LIMITS,
            offsets=OFFSETS,
            servos= SERVOS,
            simulate=simulate
        )

    def secure_joint_angle(self, angle: float, joint_type: str):
        """Enforces safety limits for a specific joint."""

        min_angle, max_angle = self.limits[joint_type]

        # Debug: See what the math is asking for BEFORE the clamp
        if angle < min_angle or angle > max_angle:
            print(f"[DEBUG] CLAMP TRIGGERED: Requested {angle:.1f}°, "
                  f"clamping to [{min_angle}, {max_angle}]")


        return max(min_angle, min(max_angle, angle))

    def move_joint(self, hip_angle, knee_angle):
        """Processes angles, applies offsets/clamping, and moves
        hardware or simulates it."""
        # Apply offset + clamp for hip
        safe_hip = self.secure_joint_angle(
            hip_angle + self.offsets["hip"], "hip"
        )

         # Apply offset + clamp for knee
        safe_knee = self.secure_joint_angle(
            knee_angle + self.offsets["knee"], "knee"
        )

        # Branch execution based on environment mode
        if self.simulate:
            print(
                f"[SIMULATION PWM] Sending Signals -> \n"
                f"    Channel 0 (Hip): {safe_hip:.1f}°\n"
                f"    Channel 1 (Knee): {safe_knee:.1f}°"
            )
        else:
            print(f"[DEBUG] Final command to hardware -> Hip: {safe_hip}°, Knee: {safe_knee}°")
            self.kit.servo[0].angle = safe_hip
            self.kit.servo[1].angle = safe_knee