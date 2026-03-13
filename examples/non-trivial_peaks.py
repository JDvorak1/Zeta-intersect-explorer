import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import mpmath
import zetaExplorer

zeros = [mpmath.zetazero(n) for n in range(1, 4)]

results = None
for z in zeros:
    r = zetaExplorer.run("findMaxReal", starting_point=(float(z.real), float(z.imag)), initial_radius=0.75, iterations=20, verbose=False)
    results = r if results is None else results + r
    print("Peak: ",r.peak_real[0])

results.plot_intersects(show_critical_line=True)
