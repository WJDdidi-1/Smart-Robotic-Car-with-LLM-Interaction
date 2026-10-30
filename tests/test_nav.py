import math

import pytest

from nav.avoid import AvoidController
from nav.go_to import GoTo
from sim.car import Car, Pose
from sim.world import Obstacle, World


def test_nothing_close_means_drive_straight():
    world = World([])
    v, w = AvoidController().control(world, Pose())
    assert v > 0.3
    assert w == pytest.approx(0.0)


def test_obstacle_ahead_turns_and_slows():
    world = World([Obstacle(0.6, 0.0, 0.15)])
    v, w = AvoidController().control(world, Pose())
    assert v < 0.3
    assert abs(w) > 0.3


def test_obstacle_on_the_left_turns_right():
    world = World([Obstacle(0.41, 0.28, 0.1)])
    _, w = AvoidController().control(world, Pose())
    assert w < 0


def test_car_reaches_a_target_in_front():
    car = Car()
    target = Pose(1.0, 0.0)
    controller = GoTo()
    for _ in range(400):
        v, w, arrived = controller.control(car.pose, target)
        if arrived:
            break
        car.step(v, w, dt=0.05)
    assert controller.control(car.pose, target)[2] is True
    assert car.pose.distance_to(target) <= controller.tolerance


def test_car_turns_toward_a_target_behind_it():
    car = Car()
    target = Pose(-1.0, 0.0)
    controller = GoTo()
    _, w, arrived = controller.control(car.pose, target)
    assert arrived is False
    assert abs(w) > 0.5


def test_arrived_means_zero_command():
    controller = GoTo()
    v, w, arrived = controller.control(Pose(0.0, 0.0), Pose(0.01, 0.0))
    assert (v, w, arrived) == (0.0, 0.0, True)


def test_avoidance_keeps_the_car_out_of_the_obstacle():
    world = World([Obstacle(0.6, 0.0, 0.15)])
    car = Car()
    controller = AvoidController()
    for _ in range(300):
        v, w = controller.control(world, car.pose)
        car.step(v, w, dt=0.05)
        for obstacle in world.obstacles:
            assert car.pose.distance_to(obstacle) > obstacle.radius
