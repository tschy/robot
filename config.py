import json

# This code runs only once when this module is first imported
with open('config/servo_calibration.json', 'r') as f:
    data = json.load(f)

# Expose the data as a variable
SERVOS = data['servos']

#print(f"DEBUG: Available keys in JSON are: {list(data.keys())}") # Add this

with open('config/test_leg_config.json',  'r') as f:
    data = json.load(f)

# Expose the data as a variable
DIMENSIONS = data["dimensions"]
SERVO_LIMITS = data["servo_limits"]
OFFSETS = data["offsets"]
#print(f"DEBUG: Available keys in JSON are: {list(data.keys())}") # Add this