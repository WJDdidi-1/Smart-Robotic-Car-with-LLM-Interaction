"""Differential-drive kinematics.

The car is a point with a heading. `step` integrates one control period with a
unicycle model, which is what a two-wheel platform with a caster behaves like at
low speed:

    x += v * cos(theta) * dt
    y += v * sin(theta) * dt
    theta += w * dt

Keeping this separate from the hardware bridge means the navigation code can be
tested on a laptop, and the same controller runs against the real base.
"""
from dataclasses import dataclass
import math


@dataclass
class Pose:
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0

    def distance_to(self, other):
        return math.hypot(other.x - self.x, other.y - self.y)

    def heading_to(self, other):
        return math.atan2(other.y - self.y, other.x - self.x)


class Car:
    """A point-mass unicycle with a speed and turn-rate limit."""

    def __init__(self, pose=None, max_speed=0.6, max_turn=2.0):
        self.pose = pose or Pose()
        self.max_speed = max_speed
        self.max_turn = max_turn
        self.path = [self.pose]

    def clamp(self, v, w):
        return (
            max(-self.max_speed, min(self.max_speed, v)),
            max(-self.max_turn, min(self.max_turn, w)),
        )

    def step(self, v, w, dt=0.05):
        v, w = self.clamp(v, w)
        self.pose.x += v * math.cos(self.pose.theta) * dt
        self.pose.y += v * math.sin(self.pose.theta) * dt
        self.pose.theta = _wrap(self.pose.theta + w * dt)
        self.path.append(Pose(self.pose.x, self.pose.y, self.pose.theta))
        return self.pose


def _wrap(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle
