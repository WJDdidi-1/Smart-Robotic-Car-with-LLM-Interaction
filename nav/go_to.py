"""Turn-then-drive controller for "come here".

A proportional heading controller plus a speed ramp: it turns first when the
target is behind, then closes the distance. The 8 cm tolerance is roughly the
size of the robot, so "arrived" means it is standing where you are.
"""
import math


class GoTo:
    def __init__(self, tolerance=0.08, max_speed=0.45, gain_turn=1.6, gain_drive=0.9):
        self.tolerance = tolerance
        self.max_speed = max_speed
        self.gain_turn = gain_turn
        self.gain_drive = gain_drive

    def control(self, pose, target):
        distance = pose.distance_to(target)
        if distance <= self.tolerance:
            return 0.0, 0.0, True
        error = _wrap(pose.heading_to(target) - pose.theta)
        w = max(-2.0, min(2.0, error * self.gain_turn))
        # Drive only once roughly facing the target, so the car does not arc.
        v = 0.0 if abs(error) > 0.6 else min(self.max_speed, distance * self.gain_drive)
        return v, w, False


def _wrap(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle
