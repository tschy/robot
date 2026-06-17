from src.leg_ik import LegIK
import matplotlib.pyplot as plt
import numpy as np

leg = LegIK(l1=10.0, l2=10.0)

def display_knee_hip_angles():
    # CALCULATE LIST OF VALUES
    # Initialize the leg with your lengths (10cm, 10cm)


    for x in range(-20, 21):
        for y in range(-20, 21):

            try:
                hip, knee = leg.calculate_angles_with_constraints(x, y)
                print(f"Target ({x}, {y}) -> Hip: {hip:.1f}°, Knee: {knee:.1f}°)")
                #print(f"Target ({x}, {y}) -> Hip: {hip:.1f}°, Knee: {knee:.1f}° - {180-knee:.1f}")
            except ValueError as e:
                #print(f"Target ({x}, {y}) -> Out of reach: {e}")
                pass


# DISPLAY HEAT MAP SHOWING KNEE ANGLES
def display_knee_angle_heat_map():
    # Define the grid
    x_range = np.linspace(-20, 20, 41)
    y_range = np.linspace(-20, 20, 41)
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.full(X.shape, np.nan) # Fill with NaN for unreachable points

    # Fill the grid with knee angles
    for i in range(len(x_range)):
        for j in range(len(y_range)):
            x, y = x_range[i], y_range[j]
            try:
                # We only care about the knee angle
                _, knee = leg.calculate_angles_with_constraints(x, y)
                Z[j, i] = knee # Note: j,i order for matrix indexing
            except ValueError:
                pass # Keep as NaN

    # Plotting the "Full Picture"
    plt.figure(figsize=(8.0, 6.0))  # type: ignore
    plt.imshow(Z, extent=(-20, 20, -20, 20), origin='lower', cmap='viridis')
    plt.colorbar(label='Knee Angle (Degrees)')
    plt.title("Full Workspace Knee Angle Heatmap")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.show()




# DISPLAY LEG POSITONS FOR GIVEN VALUES
def display_leg_positions():
    # Hardcode your 10 concrete coordinates right here
    targets = [
        (10.0, 5.0),
        (12.0, -3.0),
        (5.0, 14.0),
        (15.0, 0.0),
        (8.0, -8.0),
        (7.0, 11.0),
        (-2.0, 10.0),
        (11.0, 7.0),
        (13.0, -6.0),
        (4.0, 4.0),

        (20.0, 0.0),
        (-15.0, 11.0),
        (-19.0, 6.0),

        # --- Quadrant 1 (Top-Right) ---
        (7.0, 7.0),    # Standard reaching up and right

        # --- Quadrant 2 (Top-Left) ---
        (-5.0, 8.0),   # Reaching back and up

        # --- Quadrant 3 (Bottom-Left) ---
        (-6.0, -6.0),  # Reaching back and down

        # --- Quadrant 4 (Bottom-Right) ---
        (8.0, -5.0),   # Standard walking/support step stance

        # --- Fully Stretched Links (Max Extension = 20.0) ---
        (20.0, 0.0),   # Stretched straight out to the right
        (0.0, 20.0),   # Stretched straight up
        (-20.0, 0.0),  # Stretched straight out to the left
        (0.0, -20.0),  # Stretched straight down
        (14.14, 14.14),# Stretched completely diagonally (45 degrees)

        # --- Boundary Test ---
        (19.9, 0.0),    # Almost fully extended (99.5% capacity)

        # --- Quadrant 4 (Bottom-Right: Main walking workspace) ---
        (5.0, -5.0),  # Shallow step down and forward
        (10.0, -8.0),  # Reaching low out to the right
        (12.0, -12.0),  # Deep crouched step forward

        # --- Quadrant 3 (Bottom-Left: Rear support/push-off zone) ---
        (-5.0, -5.0),  # Shallow trailing step backward
        (-10.0, -8.0),  # Reaching low out to the left
        (-12.0, -12.0),  # Deep crouched step backward

        # --- Straight Down Axis ---
        (0.0, -10.0),  # Mid-retraction (leg completely bent in half pointing down)
        (0.0, -15.0),  # Standard neutral standing drop

        # --- Fully Stretched Links (Max Extension = 20.0 in lower hemisphere) ---
        (0.0, -20.0),  # Stretched dead straight down
        (14.14, -14.14),  # Stretched completely diagonally down-right (45 degrees)

        (20.0, 0.0),       # Hip: 0.0°   | Knee: 180.0° (Straight Right)
        (19.98, 1.01),     # Hip: 2.9°   | Knee: 180.0°
        (18.79, 6.84),     # Hip: 20.0°  | Knee: 180.0°
        (14.14, 14.14),    # Hip: 45.0°  | Knee: 180.0° (Straight Diagonal Up-Right)
        (14.14, -14.14)    # Hip: -45.0° | Knee: 180.0° (Straight Diagonal Down-Right)
    ]
    plt.figure(figsize=(8.0, 8.0))  # type: ignore

    # Colors to differentiate between the different target results
    colors = plt.cm.tab10(np.linspace(0, 1, len(targets)))

    for idx, (target_x, target_y) in enumerate(targets):
        hip_deg, knee_deg = leg.calculate_angles_with_constraints(target_x, target_y)

        if hip_deg is None or knee_deg is None:
            print(f"Target {idx+1} ({target_x}, {target_y}) is out of reach! Skipping.")
            continue

        hip_rad = np.radians(hip_deg)
        hip_x, hip_y = 0.0, 0.0

        knee_x = leg.l1 * np.cos(hip_rad)
        knee_y = leg.l1 * np.sin(hip_rad)

        knee_world_rad = hip_rad + np.radians(knee_deg) - np.pi
        foot_x = knee_x + leg.l2 * np.cos(knee_world_rad)
        foot_y = knee_y + leg.l2 * np.sin(knee_world_rad)

        color = colors[idx]
        # Draw the physical configuration
        plt.plot([hip_x, knee_x, foot_x], [hip_y, knee_y, foot_y],
                 color=color, linewidth=2, marker='o', markersize=6,
                 alpha=0.7, label=f'Target {idx+1}: ({target_x}, {target_y})')

        # Draw the expected target coordinate
        plt.scatter(target_x, target_y, color=color, marker='x', s=100, zorder=5)

    max_reach = leg.l1 + leg.l2
    plt.xlim(-max_reach - 2, max_reach + 2)
    plt.ylim(-max_reach - 2, max_reach + 2)

    plt.axhline(0, color='black', linewidth=1.0)
    plt.axvline(0, color='black', linewidth=1.0)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    plt.title("End Result Configurations for Target List")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    display_knee_hip_angles()
    display_knee_angle_heat_map()
    display_leg_positions()

