import random
import csv
import numpy as np
import mpmath
import matplotlib.pyplot as plt

# This is if you want mouse rotation support for windows
import matplotlib
matplotlib.use("TkAgg")

mpmath.mp.dps = 25


def _generate_circle(cx, cy, radius, n):
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    re_arr = cx + radius * np.cos(angles)
    im_arr = cy + radius * np.sin(angles)
    return re_arr, im_arr


_DIRECTION_ANGLES = {
    "north": 90,  "up": 90,
    "south": 270, "down": 270,
    "east":  0,   "right": 0,
    "west":  180, "left": 180,
}

def _generate_arc(cx, cy, radius, n, direction):
    if isinstance(direction, str):
        center_deg = _DIRECTION_ANGLES[direction.lower()]
    else:
        center_deg = float(direction)
    center_rad = np.deg2rad(center_deg)
    start = center_rad - np.pi / 2
    end   = center_rad + np.pi / 2
    angles = np.linspace(start, end, n)
    re_arr = cx + radius * np.cos(angles)
    im_arr = cy + radius * np.sin(angles)
    return re_arr, im_arr


def _compute_zeta(re_arr, im_arr):
    n = len(re_arr)
    zeta_re = np.empty(n)
    zeta_im = np.empty(n)
    for i in range(n):
        s = mpmath.mpc(re_arr[i], im_arr[i])
        z = mpmath.zeta(s)
        zeta_re[i] = float(z.real)
        zeta_im[i] = float(z.imag)
    return zeta_re, zeta_im


def _find_intersections(re_arr, im_arr, zeta_re, zeta_im):
    diff = zeta_re - zeta_im
    crossings = []
    for i in range(len(diff) - 1):
        if diff[i] * diff[i + 1] < 0:
            t = diff[i] / (diff[i] - diff[i + 1])
            re = re_arr[i] + t * (re_arr[i + 1] - re_arr[i])
            im = im_arr[i] + t * (im_arr[i + 1] - im_arr[i])
            crossings.append((re, im))
    return crossings


def _status(msg, verbose):
    if verbose:
        print(f"\r{msg:<80}", end="", flush=True)


class IntersectionResults:
    def __init__(self, points):
        self._re = np.array([p[0] for p in points])
        self._im = np.array([p[1] for p in points])
        self._zeta_avg = None  # computed lazily

    def __add__(self, other):
        combined = list(zip(self._re, self._im)) + list(zip(other._re, other._im))
        return IntersectionResults(combined)

    def __len__(self):
        return len(self._re)

    @property
    def real(self):
        return self._re

    @property
    def imag(self):
        return self._im

    @property
    def zeta_avg(self):
        """Average of Re(zeta(s)) and Im(zeta(s)) at each intersection point."""
        if self._zeta_avg is None:
            zeta_re, zeta_im = _compute_zeta(self._re, self._im)
            self._zeta_avg = (zeta_re + zeta_im) / 2.0
        return self._zeta_avg

    def to_csv(self, path):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Re(s)", "Im(s)","Zeta_result"])
            for re, im, zeta in zip(self._re, self._im, self.zeta_avg):
                writer.writerow([re, im, zeta])

    def plot_intersects(self, show_critical_line=False):
        plt.scatter(self._im, self._re, s=10, alpha=0.7)
        if show_critical_line:
            plt.axhline(y=0.5, color="red", linewidth=1, linestyle="--", label="Critical line Re(s)=½")
            im_min, im_max = self._im.min(), self._im.max()
            zeros_im = []
            # Upper half-plane zeros (positive imaginary part)
            n = 1
            while True:
                z = mpmath.zetazero(n)
                t = float(z.imag)
                if t > im_max:
                    break
                if t >= im_min:
                    zeros_im.append(t)
                n += 1
            # Lower half-plane zeros (negative imaginary part, conjugates)
            n = 1
            while True:
                t = -float(mpmath.zetazero(n).imag)
                if t < im_min:
                    break
                if t <= im_max:
                    zeros_im.append(t)
                n += 1
            if zeros_im:
                plt.scatter(zeros_im, [0.5] * len(zeros_im),
                            s=40, color="red", zorder=5, label=f"Zeta zeros ({len(zeros_im)})")
            plt.legend()
        plt.xlabel("Im(s)")
        plt.ylabel("Re(s)")
        plt.title(f"Riemann Zeta Intersections ({len(self._re)} points)")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_3d(self):
        """3D scatter plot: x=Im(s), y=Re(s), z=zeta_avg."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(self._im, self._re, self.zeta_avg, s=10, alpha=0.7)
        ax.set_xlabel("Im(s)")
        ax.set_ylabel("Re(s)")
        ax.set_zlabel("zeta_avg")
        ax.set_title(f"Riemann Zeta Intersections — 3D ({len(self._re)} points)")
        plt.tight_layout()
        plt.show()


def _run_random_circle_search(
    starting_point=(0.5, 14.135), # First zero on the critical line
    initial_radius=1,
    rounds=5,
    circles_per_round=4,
    iterations=20,         # Steps when running on seed_results
    radius_range=(0.25, 1.0),
    seed_results=None,     # IntersectionResults to continue from instead of generating a seed circle
    verbose=True,
    precision=500):
    if seed_results is not None:
        found = list(zip(seed_results.real, seed_results.imag))
        _status(f"Seeded from existing data: {len(found)} points", verbose)
        for step in range(1, iterations + 1):
            cx, cy = random.choice(found)
            radius = random.uniform(*radius_range)
            re_arr, im_arr = _generate_circle(cx, cy, radius, precision)
            zeta_re, zeta_im = _compute_zeta(re_arr, im_arr)
            crossings = _find_intersections(re_arr, im_arr, zeta_re, zeta_im)
            found.extend(crossings)
            _status(f"Step {step}/{iterations}: {len(crossings)} new | {len(found)} total", verbose)
    else:
        found = []
        cx, cy = starting_point
        re_arr, im_arr = _generate_circle(cx, cy, initial_radius, precision)
        zeta_re, zeta_im = _compute_zeta(re_arr, im_arr)
        crossings = _find_intersections(re_arr, im_arr, zeta_re, zeta_im)
        found.extend(crossings)
        _status(f"Round 0/seed: {len(crossings)} new | {len(found)} total", verbose)
        for round_num in range(1, rounds + 1):
            if not found:
                break
            centers = random.choices(found, k=circles_per_round)
            new_this_round = 0
            for (cx, cy) in centers:
                radius = random.uniform(*radius_range)
                re_arr, im_arr = _generate_circle(cx, cy, radius, precision)
                zeta_re, zeta_im = _compute_zeta(re_arr, im_arr)
                crossings = _find_intersections(re_arr, im_arr, zeta_re, zeta_im)
                found.extend(crossings)
                new_this_round += len(crossings)
            _status(f"Round {round_num}/{rounds}: {new_this_round} new | {len(found)} total", verbose)

    if verbose:
        print()
    return IntersectionResults(found)


def _run_columbus_search(
    starting_point=(0.5, 14.135),  # First zero on the critical line
    initial_radius=1,
    iterations=20,
    radius=None,           # Fixed radius; set to None to use radius_range instead
    radius_range=(0.25, 1.0),
    direction=None,        # Seed shape: None=full circle, or "north"/"south"/"east"/"west" (or degrees)
    seed_results=None,     # IntersectionResults to continue from instead of generating a seed circle
    verbose=True,
    precision=500):
    visited = set()
    sx, sy = starting_point

    if seed_results is not None:
        found = list(zip(seed_results.real, seed_results.imag))
        _status(f"Seeded from existing data: {len(found)} points", verbose)
    else:
        found = []
        if direction is None:
            re_arr, im_arr = _generate_circle(sx, sy, initial_radius, precision)
        else:
            re_arr, im_arr = _generate_arc(sx, sy, initial_radius, precision, direction)
        zeta_re, zeta_im = _compute_zeta(re_arr, im_arr)
        crossings = _find_intersections(re_arr, im_arr, zeta_re, zeta_im)
        found.extend(crossings)
        _status(f"Step 0/seed: {len(crossings)} new | {len(found)} total", verbose)

    for step in range(1, iterations + 1):
        candidates = [p for p in found if p not in visited]
        if not candidates:
            _status(f"Step {step}: all found points visited, stopping.", verbose)
            break
        cx, cy = max(candidates, key=lambda p: (p[0] - sx) ** 2 + (p[1] - sy) ** 2)
        visited.add((cx, cy))

        r = random.uniform(*radius_range) if radius is None else radius
        re_arr, im_arr = _generate_circle(cx, cy, r, precision)
        zeta_re, zeta_im = _compute_zeta(re_arr, im_arr)
        crossings = _find_intersections(re_arr, im_arr, zeta_re, zeta_im)
        found.extend(crossings)

        dist = ((cx - sx) ** 2 + (cy - sy) ** 2) ** 0.5
        _status(f"Step {step}/{iterations}: dist={dist:.3f} | {len(crossings)} new | {len(found)} total", verbose)

    if verbose:
        print()
    return IntersectionResults(found)


def _run_box_search(
    box_start=(0.0, 0.0),    # (re_min, im_min) — lower corner of the box
    box_end=(1.0, 30.0),     # (re_max, im_max) — upper corner of the box
    num_circles=250,
    radius_range=(0.25, 1.0),
    verbose=True,
    precision=250):
    re_min, im_min = box_start
    re_max, im_max = box_end

    found = []
    for i in range(1, num_circles + 1):
        cx = random.uniform(re_min, re_max)
        cy = random.uniform(im_min, im_max)
        radius = random.uniform(*radius_range)
        re_arr, im_arr = _generate_circle(cx, cy, radius, precision)
        zeta_re, zeta_im = _compute_zeta(re_arr, im_arr)
        crossings = _find_intersections(re_arr, im_arr, zeta_re, zeta_im)
        in_box = [(re, im) for re, im in crossings
                  if re_min <= re <= re_max and im_min <= im <= im_max]
        found.extend(in_box)
        _status(f"Circle {i}/{num_circles}: {len(in_box)} kept | {len(found)} total", verbose)

    if verbose:
        print()
    return IntersectionResults(found)


def run(algorithm, **kwargs):
    if algorithm == "circleSearch":
        return _run_random_circle_search(**kwargs)
    elif algorithm == "columbusSearch":
        return _run_columbus_search(**kwargs)
    elif algorithm == "boxSearch":
        return _run_box_search(**kwargs)
    else:
        raise ValueError(f"Unknown algorithm: '{algorithm}'")
