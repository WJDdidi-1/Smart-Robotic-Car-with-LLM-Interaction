"""A closed loop you can watch, with no hardware attached.

The sentence goes through the same parser the dialogue layer uses; the action
becomes a target; the controllers drive a simulated differential-drive base
around an obstacle. Run it with:

    python -m apps.demo

Exit code is 0 only if the car arrives and never touches the obstacle, which is
what makes it usable as a smoke test.
"""
import math

from intent.parser import parse
from nav.avoid import AvoidController
from nav.go_to import GoTo
from sim.car import Car, Pose
from sim.world import Obstacle, World


def run(sentence="Hey car, come here.", target=Pose(1.2, 0.0), steps=600, dt=0.05):
    intent = parse(sentence)
    if intent.action != "GOTO_USER":
        return {"action": intent.action, "arrived": False, "reason": "not a motion request"}

    world = World([Obstacle(0.62, 0.10, 0.14)])
    car = Car()
    go_to, avoid = GoTo(), AvoidController()
    closest = math.inf

    for step in range(steps):
        v, w, arrived = go_to.control(car.pose, target)
        if arrived:
            return {
                "action": intent.action,
                "arrived": True,
                "steps": step,
                "pose": car.pose,
                "clearance": closest,
            }
        av, aw = avoid.control(world, car.pose)
        if av == 0.0 and aw != 0.0:
            v, w = av, aw  # blocked: turn in place before trying to drive on
        else:
            v, w = min(v, av), w + aw
        car.step(v, w, dt=dt)
        closest = min(closest, min(car.pose.distance_to(o) - o.radius for o in world.obstacles))

    return {
        "action": intent.action,
        "arrived": False,
        "reason": "ran out of steps",
        "pose": car.pose,
        "clearance": closest,
    }


def main():
    result = run()
    print(f"action: {result['action']}")
    print(f"arrived: {result['arrived']}")
    if result.get("steps") is not None:
        print(f"steps: {result['steps']}")
    print(f"pose: ({result['pose'].x:.2f}, {result['pose'].y:.2f}, {result['pose'].theta:.2f})")
    print(f"closest clearance: {result['clearance']:.3f} m")
    ok = result["arrived"] and result["clearance"] > 0
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
