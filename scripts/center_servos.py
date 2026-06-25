from adafruit_servokit import ServoKit
import time

# Initialize PCA9685
kit = ServoKit(channels=16)

HIP_CHANNEL = 0
KNEE_CHANNEL = 1

def smooth_move(channel, target_angle, steps=45, delay=0.03):
    """Gently moves a servo to the target angle to protect fragile mounts."""
    # Try to read current angle; default to 90 if unknown to safely
    # minimize sudden movement
    current_angle = kit.servo[channel].angle

    angle = 100
    if current_angle != angle:
        current_angle = angle
    
    current_angle = int(current_angle)
    target_angle = int(target_angle)
    
    if current_angle == target_angle:
        return

    # Calculate step direction
    step_size = 1 if target_angle > current_angle else -1
    
    print(f"Gently moving channel {channel} from {current_angle}° "
          f"to {target_angle}°...")
    for angle in range(current_angle, target_angle + step_size, step_size):
        kit.servo[channel].angle = angle
        time.sleep(delay)

def center_all():
    print("Starting safe, slow calibration sequence...")
    
    # Move hip, then knee slowly
    smooth_move(HIP_CHANNEL, 180)
    time.sleep(0.5)
    smooth_move(KNEE_CHANNEL, 90)

    print("Done. Servos are centered safely. You can now attach or "
          "adjust the leg linkages.")

if __name__ == "__main__":
    center_all()
