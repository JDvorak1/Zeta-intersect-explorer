# zetaExplorer

**zetaExplorer** maps the intersections where the real and imaginary parts of the Riemann zeta function are equal — all points *s* in the complex plane where Re(ζ(s)) = Im(ζ(s)). It can chart broad regions of these intersections, follow the complicated curves they form deep into the complex plane, and focus a search on any rectangular region of interest.

Three algorithms are available: a **circle search** that fans outward from a seed point to document big or small details, a **box search** that confines the circle search to a user-defined rectangular region, and a **Columbus search** that follows a single continuous curve as far as you set it to go.

---

## Why this tool exists

The intersections where Re(ζ(s)) = Im(ζ(s)) are not scattered randomly — they form individual, continuous curves that run through the complex plane. zetaExplorer is built to collect data on those curves: mapping their shapes, tracing them individually, and surveying specific regions in detail.

The goal behind that data collection is to find equations that describe individual curves. An equation that correctly describes one of these curves would, by definition, produce points where Re(ζ(s)) = Im(ζ(s)) when fed into the zeta function. If enough of those equations could be found and understood, they could bring us closer to a numerical resolution of the Riemann hypothesis.

---

## Contents

- [The Riemann-zeta fingerprint](#the-riemann-zeta-fingerprint)
- [The zeta egg](#the-zeta-egg)
- [Single curves](#single-curves)
- [Box search](#box-search)
- [Installation](#installation)
- [API reference](#api-reference)
- [File structure](#file-structure)

---

## The Riemann-zeta fingerprint

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

## Box search

The **box search** (`boxSearch`) runs a circle search constrained to a rectangular region of the complex plane defined by two corner points. Random circles are placed uniformly within the box, making it easy to survey a specific area without the search drifting outside it.

This is useful when you want to focus on a known region — for example, the critical strip around Re(s) = 1/2 where the non-trivial zeros of the Riemann zeta function are located.

![Zeta zeros along the critical line](figures/zeta%20zeros.png)

Produced with [`examples/box_search_critical_line.py`](examples/box_search_critical_line.py):

```python
import zetaExplorer

# Explore the strip around the critical line Re(s) = 1/2
# Box: Re(s) from 0 to 1.5, Im(s) from 10 to 28
results = zetaExplorer.run(
    "boxSearch",
    box_start=(0, 10),
    box_end=(1.5, 28),
    num_circles=200,
    radius_range=(0.75, 1.5),
    precision=250,
)

# Finer search
results = zetaExplorer.run("circleSearch", seed_results=results,
                            radius_range=(0.25, 0.35), iterations=50, precision=250)

results.plot_intersects(show_critical_line=True)
```

---

## Installation

```bash
pip install git+https://github.com/JDvorak1/Zeta-intersect-explorer.git
```

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

#### `"boxSearch"` — constrained area search

Places circles randomly within a rectangular region defined by two corner points and records all intersection crossings found within it.

```python
zetaExplorer.run(
    "boxSearch",
    box_start=(0, 10),      # bottom-left corner (Re, Im)
    box_end=(1.5, 28),      # top-right corner (Re, Im)
    num_circles=200,         # number of random circles to place
    radius_range=(0.75, 1.5),
    precision=250,
)
```

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
├── map_explorer.py              — broad fingerprint map
├── eggsplorer.py                — closed egg structure near (-2, 0)
├── single_curve.py              — single-branch Columbus trace
└── box_search_critical_line.py  — box search along the critical strip
figures/
├── fingerprint 0.png
├── fingerprint1.png
├── fingerprint 2.png
├── the zeta egg.png
├── single curve algo.png
├── zero line.png
└── zeta zeros.png
```
