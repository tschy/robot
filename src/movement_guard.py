# Safety Only. Does this (x,y) exist? Is it within reach?

class MovementGuard:
    def __init__(self, l1, l2):
        self.l1 = float(l1)
        self.l2 = float(l2)

        self.min_r = abs(l1 - l2)
        self.max_r = l1 + l2

    def is_reachable(self, x, y):
        dist_sq = x**2 + y**2
        return ((self.min_r**2 <= dist_sq <= self.max_r**2)
                and dist_sq > 0.001)

    def get_safe_default(self):
        # Return coordinates for a "neutral standing" position
        return 0, -(self.l1 + self.l2) * 0.7


    """
 # Target not reachable: too close to hip, leg too thick, etc., 
 # define and account 
 for unreachable zones
 """