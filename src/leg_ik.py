import math



class LegIK:
    def __init__(self,
                 l1: float,
                 l2: float,
                 min_angles : tuple[float | int, float | int] =(0, 0),
                 max_angles : tuple[float | int, float | int] =(180, 180)
    ):
        self.l1 = float(l1)
        self.l2 = float(l2)
        self.min_h, self.min_k = min_angles
        self.max_h, self.max_k = max_angles

    def calculate_angles(self, x: float,
                         y: float) -> tuple[float, float]:

        x, y = float(x), float(y)
        # Law of Cosines
        dist_sq = x ** 2 + y ** 2
        dist = math.sqrt(dist_sq)

        # Knee angle (theta2) interior
        cos_theta2 =  (self.l1**2 + self.l2**2 - dist_sq) / (2 * self.l1 * self.l2)

        theta2 = math.acos(max(-1.0, min(1.0, cos_theta2))) # Clamp for safety

        # Hip angle (theta1)
        cos_alpha = (self.l1 ** 2 + dist_sq - self.l2 ** 2) / (2 * self.l1 * dist)
        theta1 = math.atan2(y, x) + math.acos(max(-1.0, min(1.0, cos_alpha)))

        h_deg, k_deg = math.degrees(theta1), math.degrees(theta2)

        # Apply constraints
        if not (self.min_h <= h_deg <= self.max_h) or not (self.min_k <= k_deg <= self.max_k):
            raise ValueError("Target reachable but outside of physical servo limits.")

        return h_deg, k_deg


"""
constraints:

 # Ensure we don't divide by zero

 # Target not reachable: too close to hip, leg too thick, etc., define and account 
 for unreachable zones
    if dist < 0.1:
        raise ValueError("Target too close to hip (Singularity).")

 # Check reachability
    if dist > (self.l1 + self.l2) or dist < abs(self.l1 - self.l2):
        raise ValueError("Target coordinate is out of reach.")    


TODO
- hip angle measured from where?
- Separate math/constraints manager/translation to servo commands



TODO LATER 
- legs should be bend in neutral position
"""