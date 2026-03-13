import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

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
results = zetaExplorer.run("circleSearch", seed_results=results,radius_range=(0.25,0.35),iterations=50,precision=250)

results.plot_intersects(show_critical_line=True)
