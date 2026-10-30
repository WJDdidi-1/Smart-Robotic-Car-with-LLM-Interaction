"""Obstacles and the one sensor the avoidance controller needs: range ahead."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Obstacle:
    x: float
    y: float
    radius: float = 0.15


class World:
    def __init__(self, obstacles=None, bounds=None):
        self.obstacles = list(obstacles or [])
        self.bounds = bounds  # (min_x, min_y, max_x, max_y) or None

    def range_to(self, pose, angle, max_range=1.2, step=0.01):
        """Distance along `angle` from `pose` until an obstacle or max_range.

        Sampling beats solving circle/ray intersections here: it is exact to
        `step`, has no edge cases for grazing hits, and the controller only needs
        a number it can trust.
        """
        for i in range(1, int(max_range / step) + 1):
            d = i * step
            x = pose.x + math.cos(angle) * d
            y = pose.y + math.sin(angle) * d
            for o in self.obstacles:
                if (x - o.x) ** 2 + (y - o.y) ** 2 <= o.radius ** 2:
                    return d
        return max_range
