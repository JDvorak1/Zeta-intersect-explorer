# zetaExplorer

**zetaExplorer** maps the intersections where the real and imaginary parts of the Riemann zeta function are equal — all points *s* in the complex plane where Re(ζ(s)) = Im(ζ(s)). It can chart broad regions of these intersections, and it can follow the complicated curves they form deep into the complex plane.

Two algorithms are available: a **circle search** that fans outward from a seed point to document big or small details, and a **Columbus search** that follows a single continuous curve as far as you set it to go.

## The fingerprints

Running a broad circle search from a central seed reveals the fingerprint of the Riemann zeta function — the characteristic pattern of intersection points spread across the complex plane.

![Fingerprint map centered near the origin](figures/fingerprint%200.png)

Produced with [`examples/map_explorer.py`](examples/map_explorer.py):

```python
import zetaExplorer

results = zetaExplorer.run("circleSearch", starting_point=(-10, 0),
                           radius_range=(5, 10), rounds=50, precision=250)
# refine
results = zetaExplorer.run("circleSearch", seed_results=results,
                           radius_range=(0.25, 0.5), rounds=25, precision=250)
results.plot_intersects()
```

Each visible curve is a structure of the intersections. Different regions of the complex plane show different structures:

![Fingerprint in the positive imaginary half-plane](figures/fingerprint1.png)

![Fingerprint in the negative imaginary half-plane](figures/fingerprint%202.png)

---

## The zeta egg

Near the trivial zero at (−2, 0) the intersection curve closes into a loop.

![The zeta egg](figures/the%20zeta%20egg.png)

Produced with [`examples/eggsplorer.py`](examples/eggsplorer.py):

```python
import zetaExplorer

results = zetaExplorer.run("circleSearch", starting_point=(-2, 0),
                           radius_range=(0.5, 1.5), rounds=5,
                           circles_per_round=25, precision=500)
results.to_csv("egg_points.csv")
results.plot_intersects()
```

---

## Single curves

The **Columbus search** (`columbusSearch`) works differently from the circle search. Instead of spreading outward in all directions, it always steps toward the point farthest from the starting location — hugging a single branch and following it wherever it leads.

This makes it well-suited for tracing complicated, winding curves inside the Riemann plane without losing the thread.


Curve starting at (-4,0)
![imag zero](figures/zeroline.png)

Produced with [`examples/single_curve.py`](examples/single_curve.py):

```python
import zetaExplorer

starting_point = (-4, 0)

down_search = zetaExplorer.run("columbusSearch", starting_point=starting_point,
                                direction="down")
up_search   = zetaExplorer.run("columbusSearch", starting_point=starting_point,
                                direction="up")

results = down_search + up_search

# optional: fill in gaps with circle search
results = zetaExplorer.run("circleSearch", seed_results=results)

results.to_csv("intersections.csv")
results.plot_intersects()
```
Curve stating at the first zero on the critical line.
![Single curve traced by the Columbus algorithm](figures/single%20curve%20algo.png)


---

## Installation

```bash
pip install mpmath numpy matplotlib
```

Place `zetaExplorer.py` in your project and import it.

---

## API reference

### `zetaExplorer.run(algorithm, **kwargs)`

Runs the chosen algorithm and returns an `IntersectionResults` object.

---

#### `"circleSearch"` — radial fan search

Starts from a seed point, finds intersection crossings on a circle, then places new circles on each crossing and repeats for several rounds. Covers large areas quickly.

```python
zetaExplorer.run(
    "circleSearch",
    starting_point=(0.5, 14.135), # seed location in the complex plane
    seed_radius=1,                 # radius of the initial circle
    rounds=5,                      # number of expansion rounds
    circles_per_round=4,           # new probe circles per round
    radius_range=(0.25, 1.0),      # random radius drawn from this range
    precision=500,                 # sample points per circle
    seed_results=None,             # supply existing results to continue from
)
```

When `seed_results` is provided, `starting_point` and `rounds` are ignored — the search continues by placing random circles on points already found.

---

#### `"columbusSearch"` — single-branch follower

Always extends toward the point most distant from the origin, following one branch of the intersection curve outward.

```python
zetaExplorer.run(
    "columbusSearch",
    starting_point=(0.5, 14.135), # seed location
    initial_radius=1,              # radius of the seed circle or arc
    iterations=20,                 # steps to take
    radius=None,                   # fixed radius; None uses radius_range
    radius_range=(0.25, 1.0),      # random radius range (used when radius=None)
    direction=None,                # seed shape: None=full circle, or "north"/"south"/"east"/"west"/degrees
    seed_results=None,             # supply existing results to continue from
    precision=500,
)
```

`direction` restricts the seed to a half-circle arc, useful for starting two opposite Columbus searches from the same point and combining their results.

---

### `IntersectionResults`

```python
results.real             # numpy array of Re(s) at each intersection
results.imag             # numpy array of Im(s) at each intersection
len(results)             # total intersections found

results.plot_intersects()        # scatter plot (Im on x-axis, Re on y-axis)
results.to_csv("output.csv")     # save as CSV with columns Re(s), Im(s)

combined = results_a + results_b # merge two result sets
```

---

## File structure

```
zetaExplorer.py         — the full tool (single file)
examples/
├── map_explorer.py     — broad fingerprint map
├── eggsplorer.py       — closed egg structure near (-2, 0)
└── single_curve.py     — single-branch Columbus trace
figures/
├── fingerprint 0.png
├── fingerprint1.png
├── fingerprint 2.png
├── the zeta egg.png
├── single curve algo.png
└── zero line.png
```
