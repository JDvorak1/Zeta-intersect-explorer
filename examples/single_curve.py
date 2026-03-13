import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import zetaExplorer

starting_point = (-4, 0)

# Explore the curves
down_search = zetaExplorer.run("columbusSearch", starting_point=starting_point, direction="down")
up_search   = zetaExplorer.run("columbusSearch", starting_point=starting_point, direction="up")

results = down_search + up_search

# Zeta interpolation
results = zetaExplorer.run("circleSearch", seed_results=results)

results.to_csv("intersections.csv")
results.plot_intersects()