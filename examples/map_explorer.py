import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import zetaExplorer

starting_point = (-10, 0)

# Explore the map
results = zetaExplorer.run("circleSearch", starting_point=starting_point, radius_range=(5,10),rounds=50,precision=250)
# Finer search
results = zetaExplorer.run("circleSearch", seed_results=results,radius_range=(0.25,0.5),rounds=25,precision=250)

results.plot_intersects()