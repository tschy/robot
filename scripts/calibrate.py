import time
from adafruit_servokit import ServoKit


servo_configs = {
    0: {"lower": 700, "upper": 2480},
    1: {"lower": 500, "upper": 2500}
}

# Initialize the kit
kit = ServoKit(channels=16)

# Configure the servo channel (e.g., channel 0)
# Default is 1000 to 2000. We expand to 500-2500 to find the full
# physical limit.


for servo_channel in [0, 1]:

    servo = kit.servo[servo_channel]

    lower_limit = servo_configs[servo_channel]["lower"]
    upper_limit = servo_configs[servo_channel]["upper"]

    servo.set_pulse_width_range(lower_limit, upper_limit)

    print(f"Testing min limit ({lower_limit})...")
    servo.angle = 0
    time.sleep(2)

    print(f"Testing max limit ({upper_limit})...")
    servo.angle = 180
    time.sleep(2)

    print("Returning to center (90)...")
    servo.angle = 90