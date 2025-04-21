import json
import os
from pathlib import Path
from datetime import datetime

# Automatically find the root dir (two levels up from this utils file)
ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / 'results/raw'
FIG_DIR = ROOT_DIR / 'results/figures'
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

now = datetime.now().strftime("%m%d-%H%M")

def save_raw(sim, label):
    filename = f'{label}_{now}.json'
    filepath = RAW_DIR / filename
    sim.to_json(filepath)
    print(f"Simulation results saved to {filepath}")

def save_plots(fig, label):
  filename = f'{label}_{now}.png'
  filepath = FIG_DIR / filename
  fig.savefig(filepath)
  print(f"Simulation plot saved to {filepath}")