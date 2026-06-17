import math

class LegIK:
    def __init__(self,
                 l1: float,
                 l2: float,
                 # min_angles : tuple[float | int, float | int] =(0, 0),
                 # max_angles : tuple[float | int, float | int] =(180, 180)
    ):
        self.l1 = float(l1)
        self.l2 = float(l2)
        # self.min_h, self.min_k = min_angles
        # self.max_h, self.max_k = max_angles

    def calculate_angles(self,
                         x: float,
                         y: float) \
            -> tuple[float, float]:

        x, y = float(x), float(y)

        dist_sq = x ** 2 + y ** 2
        dist = math.sqrt(dist_sq)
        #
        # if dist < 0.001:
        #     # Return a safe default (e.g., fully retracted or extended)
        #     return 0.0, 180.0

        # Knee angle (theta2) interior
        cos_theta2 =  (self.l1**2 + self.l2**2 - dist_sq) / (2 * self.l1 * self.l2)

        # Prevent overflow through rounding errors
        theta2 = math.acos(max(-1.0, min(1.0, cos_theta2)))

        # Hip angle (theta1)
        cos_alpha = (self.l1 ** 2 + dist_sq - self.l2 ** 2) / (2 * self.l1 * dist)
        theta1 = math.atan2(y, x) + math.acos(max(-1.0, min(1.0, cos_alpha)))

        h_deg, k_deg = math.degrees(theta1), math.degrees(theta2)

        return h_deg, k_deg

    def calculate_angles_with_constraints(self,
                                          x,
                                          y)\
            -> tuple[float | None, float | None]:
        # 1. Handle the singularity/zero case
        if (x**2 + y**2) < 0.001:
            return 0.0, 0.0 # TODO replace 0,0 with appropriate values

        if x == 0 and y == 0: # TODO replace 0,0 with appropriate values
            return 0.0, 0.0 # Skip the center point

        if self.l1 == 0 or self.l2 == 0 :
            return 0.0, 0.0



        # 2. Call the engine
        try:
            return self.calculate_angles(x, y)
        except ValueError:
            # Handle "out of reach" logic here
            return None, None
"""
constraints:

 # Target not reachable: too close to hip, leg too thick, etc., define and account 
 for unreachable zones
 

TODO
- hip angle measured from where?
- Separate math/constraints manager/translation to servo commands



TODO LATER 
- legs should be bend in neutral position
"""