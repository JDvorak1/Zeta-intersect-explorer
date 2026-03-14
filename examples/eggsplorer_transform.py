import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import zetaExplorer

results = zetaExplorer.run(
    "boxSearch",
    box_start=(-3, -2),
    box_end=(2, 2),
    radius_range=(0.5, 1),
    precision=250,
    transform_imag=lambda x: 2*x**2, # transforming data before checking itersections 
)

results.plot_intersects()
