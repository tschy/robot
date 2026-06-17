

# 1. Calculate raw angles from geometry engine
raw_hip, raw_knee = leg_ik.calculate_angles(target_x, target_y)

# 2. Protect hardware by clamping values to physical limits
safe_hip = controller.clamp_joint_angle("hip", raw_hip)
safe_knee = controller.clamp_joint_angle("knee", raw_knee)