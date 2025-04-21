import covasim as cv
import sys
import os

# Add the project root to sys.path so Python can find utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.save_results import save_raw, save_plots

sim = cv.Sim()
sim.run()
fig = sim.plot()
save_raw(sim, "simple")
save_plots(fig, "simple")