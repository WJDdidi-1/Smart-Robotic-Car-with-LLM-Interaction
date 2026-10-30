"""Reactive obstacle avoidance.

Three range readings — left, centre, right — decide a speed and a turn rate.
This is deliberately the simplest thing that works: the point is a controller
that can be tested, not a planner. When nothing is close it drives straight.
"""
import math


class AvoidController:
    def __init__(self, slow=0.55, stop=0.28, cruise=0.45, turn=1.2, fan=0.6):
        self.slow = slow
        self.stop = stop
        self.cruise = cruise
        self.turn = turn
        self.fan = fan  # half-angle between the centre and side readings

    def read(self, world, pose):
        return (
            world.range_to(pose, pose.theta + self.fan),
            world.range_to(pose, pose.theta),
            world.range_to(pose, pose.theta - self.fan),
        )

    def control(self, world, pose):
        left, centre, right = self.read(world, pose)
        if centre > self.slow and left > self.slow and right > self.slow:
            return self.cruise, 0.0
        if centre < self.stop:
            # Blocked: turn toward the side with more room, in place.
            return 0.0, self.turn if left >= right else -self.turn
        # Something is close: slow down and steer away from it, proportionally.
        # Sign: a blocked *left* reading means turn right (negative w), so the
        # bias is left-minus-right. A dead-on obstacle leaves the two side rays
        # equal, and choosing neither side would drive straight into it, so a
        # tie picks a side instead of holding course.
        bias = (left - right) / max(self.slow, 1e-6)
        if abs(bias) < 0.15:
            bias = 0.5 if left > right else -0.5
        w = max(-self.turn, min(self.turn, bias * self.turn))
        # Turn harder, drive slower: the turn is what keeps the car clear.
        v = self.cruise * max(0.0, centre / self.slow) * (1.0 - 0.5 * min(1.0, abs(bias)))
        return v, w
