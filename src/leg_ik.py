import math

class LegIK:
    def __init__(self,
                 l1: float,
                 l2: float,

    ):
        if l1 <= 0 or l2 <= 0:
            raise ValueError("Leg segment lengths must be greater than zero.")
        self.l1 = float(l1)
        self.l2 = float(l2)

    def calculate_angles(self,
                         x: float,
                         y: float) \
            -> tuple[float, float]:

        x, y = float(x), float(y)

        dist_sq = x ** 2 + y ** 2
        dist = math.sqrt(dist_sq)

        # Knee angle (theta2) interior
        cos_theta2 =  ((self.l1**2 + self.l2**2 - dist_sq) /
                       (2 * self.l1 * self.l2))

        # Prevent overflow through rounding errors
        theta2 = math.acos(max(-1.0, min(1.0, cos_theta2)))

        # Hip angle (theta1)
        cos_alpha = ((self.l1 ** 2 + dist_sq - self.l2 ** 2) /
                     (2 * self.l1 * dist))
        theta1 = (math.atan2(y, x) +
                  math.acos(max(-1.0, min(1.0, cos_alpha))))

        h_deg, k_deg = math.degrees(theta1), math.degrees(theta2)

        return h_deg, k_deg

    def calculate_angles_with_constraints(self,
                                          x,
                                          y)\
            -> tuple[float | None, float | None]:

        if x == 0 and y == 0: # TODO replace 0,0 with appropriate values
            return 0.0, 0.0 # Skip the center point

        # 2. Call the engine
        try:
            return self.calculate_angles(x, y)
        except ValueError:
            # Handle "out of reach" logic here
            return None, None
"""
constraints:


TODO
- hip angle measured from where?
- Separate math/constraints manager/translation to servo commands



TODO LATER 
- legs should be bend in neutral position
"""