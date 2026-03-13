import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# This is if you want mouse rotation support for windows
import matplotlib
matplotlib.use("TkAgg")

import zetaExplorer

starting_point = (0.5, 14.1347)

results = zetaExplorer.run(
    "circleSearch",
    starting_point=starting_point,
    initial_radius=2.0,
    rounds=6,
    circles_per_round=6,
    radius_range=(0.5, 1.5),
    precision=400,
)

results = zetaExplorer.run(
    "circleSearch",
    seed_results=results,
    radius_range=(0.1, 0.4),
    iterations=30,
    precision=400,
)
results.plot_3d()
