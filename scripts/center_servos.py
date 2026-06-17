from adafruit_servokit import ServoKit
import time

# Initialize PCA9685
kit = ServoKit(channels=16)

# Define which channels your servos are on
HIP_CHANNEL = 0
KNEE_CHANNEL = 1

def center_all():
    print("Centering servos to 90 degrees...")
    # Setting to 90 ensures the servo is at its physical midpoint
    kit.servo[HIP_CHANNEL].angle = 90
    kit.servo[KNEE_CHANNEL].angle = 90

    # Give the hardware a moment to reach the position
    time.sleep(1)
    print("Done. You can now attach the leg linkages.")

if __name__ == "__main__":
    center_all()