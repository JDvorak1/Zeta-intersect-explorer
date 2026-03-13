import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import zetaExplorer

starting_point = (-2, 0)

# Explore the curves
results =zetaExplorer.run("circleSearch", starting_point=starting_point,radius_range=(0.5,1),rounds=8,circles_per_round=25,precision=250)

results.plot_intersects()
results.plot_3d()