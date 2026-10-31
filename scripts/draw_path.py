"""Draw docs/demo-path.svg from an actual run of the demo loop.

The figure in the README is not an illustration: it is the poses this script
recorded, so a change to the controllers shows up as a different curve.

    python -m scripts.draw_path
"""
import math
import pathlib

from nav.avoid import AvoidController
from nav.go_to import GoTo
from sim.car import Car, Pose
from sim.world import Obstacle, World


def run():
    target = Pose(1.2, 0.0)
    obstacle = Obstacle(0.62, 0.10, 0.14)
    world = World([obstacle])
    car, go_to, avoid = Car(), GoTo(), AvoidController()
    poses = [(car.pose.x, car.pose.y)]  # copy: car.pose is mutated in place
    closest = math.inf
    for step in range(600):
        v, w, arrived = go_to.control(car.pose, target)
        if arrived:
            return poses, step, closest, obstacle
        av, aw = avoid.control(world, car.pose)
        if av == 0.0 and aw != 0.0:
            v, w = av, aw
        else:
            v, w = min(v, av), w + aw
        car.step(v, w, dt=0.05)
        poses.append((car.pose.x, car.pose.y))
        closest = min(closest, min(car.pose.distance_to(o) - o.radius for o in world.obstacles))
    raise SystemExit("the loop did not arrive; the figure would be misleading")


def svg(poses, steps, closest, obstacle):
    width, padx, top, bottom = 760, 62, 66, 36
    xs = [p[0] for p in poses] + [0.0, 1.2, obstacle.x - obstacle.radius, obstacle.x + obstacle.radius]
    ys = [p[1] for p in poses] + [obstacle.y - obstacle.radius, obstacle.y + obstacle.radius, 0.0]
    minx, maxx = min(xs) - 0.06, max(xs) + 0.06
    miny, maxy = min(ys) - 0.06, max(ys) + 0.06
    scale = (width - 2 * padx) / (maxx - minx)
    height = int(round(top + bottom + (maxy - miny) * scale))
    cx = (minx + maxx) / 2

    def x(value):
        return width / 2 + (value - cx) * scale

    def y(value):
        return top + (maxy - value) * scale

    path = "M " + " L ".join(f"{x(px):.1f} {y(py):.1f}" for px, py in poses)
    grid = []
    for tick in [i / 5 for i in range(-2, 8)]:
        grid.append(f'<line x1="{x(tick):.1f}" y1="{top}" x2="{x(tick):.1f}" y2="{height - bottom}"/>')
    for tick in [i / 5 for i in range(-2, 4)]:
        grid.append(f'<line x1="{padx - 20}" y1="{y(tick):.1f}" x2="{width - padx + 20}" y2="{y(tick):.1f}"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">
  <title id="t">The demo loop, drawn from the run</title>
  <desc id="d">A simulated car drives from the origin to (1.2, 0), steering around one obstacle at (0.62, 0.10) with radius 0.14 m. The line is the {len(poses)} poses the run recorded; the closest clearance was {closest:.3f} m and the green dot is the pose the 8 cm arrival tolerance accepted.</desc>
  <style>
    .grid{{stroke:#eceff3;stroke-width:1}}
    .axis{{font:400 10px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;fill:#98a1ae}}
    .path{{fill:none;stroke:#2f6fed;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}}
    .obs{{fill:#fdecec;stroke:#e06c6c;stroke-width:1.5}}
    .mark{{stroke-width:1.5;fill:#ffffff}}
    .t{{font:600 12px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;fill:#1d2129}}
    .s{{font:400 11px -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;fill:#5b6472}}
    .m{{font:400 10px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#7a8494}}
  </style>
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  <g class="grid">{"".join(grid)}</g>
  <circle class="obs" cx="{x(obstacle.x):.1f}" cy="{y(obstacle.y):.1f}" r="{obstacle.radius * scale:.1f}"/>
  <text class="s" x="{x(obstacle.x) + obstacle.radius * scale + 10:.1f}" y="{y(obstacle.y) + 4:.1f}">obstacle</text>
  <text class="m" x="{x(obstacle.x) + obstacle.radius * scale + 10:.1f}" y="{y(obstacle.y) + 20:.1f}">r = {obstacle.radius} m</text>
  <path class="path" d="{path}"/>
  <circle class="mark" cx="{x(0):.1f}" cy="{y(0):.1f}" r="5" stroke="#2f6fed"/>
  <text class="s" x="{x(0) - 14:.1f}" y="{y(0) + 24:.1f}">start</text>
  <circle class="mark" cx="{x(1.2):.1f}" cy="{y(0):.1f}" r="5" stroke="#2f6fed"/>
  <text class="s" x="{x(1.2) - 18:.1f}" y="{y(0) - 14:.1f}">target</text>
  <circle class="mark" cx="{x(poses[-1][0]):.1f}" cy="{y(poses[-1][1]):.1f}" r="4" stroke="#1f9d63"/>
  <text class="t" x="{padx - 38}" y="28">{steps} steps · 0.05 s each · closest clearance {closest:.3f} m</text>
  <text class="m" x="{padx - 38}" y="46">python -m apps.demo</text>
  <text class="axis" x="{width - padx + 6}" y="{height - 12}">x (m)</text>
  <text class="axis" x="10" y="200">y (m)</text>
</svg>
'''


def main():
    poses, steps, closest, obstacle = run()
    out = pathlib.Path(__file__).resolve().parent.parent / "docs" / "demo-path.svg"
    out.write_text(svg(poses, steps, closest, obstacle))
    print(f"wrote {out} ({len(poses)} poses, {steps} steps, clearance {closest:.3f} m)")


if __name__ == "__main__":
    main()
