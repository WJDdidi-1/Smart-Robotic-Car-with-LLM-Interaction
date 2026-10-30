import math

import pytest

from sim.car import Car, Pose
from sim.world import Obstacle, World


def test_straight_line_moves_along_heading():
    car = Car()
    car.step(0.4, 0.0, dt=0.5)
    assert car.pose.x == pytest.approx(0.2, abs=1e-9)
    assert car.pose.y == pytest.approx(0.0, abs=1e-9)
    assert car.pose.theta == pytest.approx(0.0, abs=1e-9)


def test_turn_in_place_changes_heading_only():
    car = Car()
    car.step(0.0, 1.0, dt=1.0)
    assert car.pose.x == pytest.approx(0.0, abs=1e-9)
    assert car.pose.theta == pytest.approx(1.0, abs=1e-9)


def test_heading_wraps_instead_of_growing_without_bound():
    car = Car()
    for _ in range(20):
        car.step(0.0, 1.0, dt=1.0)
    assert -math.pi <= car.pose.theta <= math.pi


def test_commands_are_clamped_to_the_base_limits():
    car = Car(max_speed=0.3, max_turn=1.0)
    v, w = car.clamp(5.0, -9.0)
    assert (v, w) == (0.3, -1.0)


def test_pose_geometry():
    here, there = Pose(0.0, 0.0), Pose(3.0, 4.0)
    assert here.distance_to(there) == pytest.approx(5.0)
    assert here.heading_to(there) == pytest.approx(math.atan2(4.0, 3.0))


def test_range_to_sees_an_obstacle_ahead():
    world = World([Obstacle(1.0, 0.0, 0.1)])
    pose = Pose(0.0, 0.0, 0.0)
    assert world.range_to(pose, 0.0) == pytest.approx(0.9, abs=0.02)


def test_range_to_reports_max_range_when_nothing_is_there():
    world = World([])
    assert world.range_to(Pose(), 0.0, max_range=1.2) == pytest.approx(1.2)
