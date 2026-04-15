import math
import re
BEST_KNOWN = {
    # Small
    "A-n80-k10": 1763.00,
    "F-n72-k4": 237.00,
    "E-n101-k14": 1067.00,
    "F-n135-k7": 1162.00,
    "M-n151-k12": 1015.00,

    # Medium
    "Golden_18": 995.13,
    "CMT10": 1395.85,
    "Tai150b": 2727.03,
    "Tai385": 24366.41,
    "Golden_3": 10997.80,

    # Large
    "Li_21": 16212.83,
    "X-n502-k39": 69226.00,
    "Loggi-n601-k42": 347046.00,
    "XL-n1701-k562": 521136.00,
    "XL-n2541-k121": 146390.00,
}

K_REFERENCE = {
    # Small
    "A-n80-k10": 10,
    "F-n72-k4": 4,
    "E-n101-k14": 14,
    "F-n135-k7": 7,
    "M-n151-k12": 12,

    # Medium
    "Golden_18": 27,
    "CMT10": 18,
    "Tai150b": 14,
    "Tai385": 46,
    "Golden_3": 9,

    # Large
    "Li_21": 10,
    "X-n502-k39": 39,
    "Loggi-n601-k42": 42,
    "XL-n1701-k562": 562,
    "XL-n2541-k121": 121,
}


class Instance:
    def __init__(self, name, capacity, coords, demands, depot):
        self.name = name
        self.capacity = capacity
        self.coords = coords
        self.demands = demands
        self.depot = depot
        self.best_known = BEST_KNOWN.get(self.name)
        self.k_ref = K_REFERENCE.get(self.name)

    def distance(self, i, j):
        x1, y1 = self.coords[i]
        x2, y2 = self.coords[j]
        return math.hypot(x1 - x2, y1 - y2)

    def calculate_cost(self, routes):
        total_cost = 0.0

        for route in routes:
            if not route:
                continue

            current = self.depot
            for node in route:
                total_cost += self.distance(current, node)
                current = node

            total_cost += self.distance(current, self.depot)

        return total_cost

    def calculate_penalized_cost(self, routes):
        cost = self.calculate_cost(routes)
        k_used = len(routes)

        if self.k_ref is None or self.best_known is None:
            return cost

        alpha = 0.005 * self.best_known
        beta = 0.02 * self.best_known

        penalty_less = alpha * max(0, self.k_ref - k_used)
        penalty_more = beta * max(0, k_used - self.k_ref)

        return cost + penalty_less + penalty_more

    def calculate_gap(self, solution_cost):
        if self.best_known is None or self.best_known == 0:
            return None
        return 100.0 * abs(solution_cost - self.best_known) / self.best_known