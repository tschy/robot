from src.leg_ik import LegIK

# Initialize the leg with your lengths (10cm, 10cm)
leg = LegIK(l1=10.0, l2=10.0, min_angles=(0, 0), max_angles=(180, 180))

# Let's test a sweep of positions to see if the math holds up
# Testing x from 5 to 15, keeping y at 10
for x in range(-20, 21):
    for y in range(-20, 21):
        try:
            hip, knee = leg.calculate_angles(x, y)
            print(f"Target ({x}, {y}) -> Hip: {hip:.1f}°, Knee: {knee:.1f}°)")
            #print(f"Target ({x}, {y}) -> Hip: {hip:.1f}°, Knee: {knee:.1f}° - {180-knee:.1f}")
        except ValueError as e:
            #print(f"Target ({x}, {y}) -> Out of reach: {e}")
            pass
