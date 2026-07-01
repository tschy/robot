import math


def calculate_forward_kinematics(
        servo_hip: float,
        servo_knee: float,
        l1: float,
        l2: float
) -> tuple[float, float]:
    """
    Calculates the (X, Y) coordinate of the foot given the physical
    servo angles.
    Assumes 90 degrees is straight down for both joints.

    l1: Thigh length
    l2: Shin length
    """
    # 1. Reverse the physical servo mapping back to geometric angles
    # (in degrees)
    h_deg = servo_hip - 90
    k_deg = 180 - (90 - servo_knee)

    # 2. Convert angles to radians
    theta1 = math.radians(h_deg)
    theta2 = math.radians(k_deg)

    # 3. Calculate Knee position relative to Hip origin (0,0)
    knee_x = l1 * math.cos(theta1)
    knee_y = l1 * math.sin(theta1)

    # 4. Calculate Foot position relative to Knee position
    # The absolute angle of the shin in the world coordinate system is
    # (theta1 + theta2 - pi)
    shin_angle = theta1 + theta2 - math.pi

    foot_x = knee_x + l2 * math.cos(shin_angle)
    foot_y = knee_y + l2 * math.sin(shin_angle)

    return round(foot_x, 4), round(foot_y, 4)