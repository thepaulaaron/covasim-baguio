import covasim as cv
import sciris as sc
import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

# Output folder for plots
OUTPUT_DIR = 'period_calibration_independent'
os.makedirs(OUTPUT_DIR, exist_ok=True)

INTERVENTION_PERIODS = {
    'merged_1': ('2020-03-02', '2021-03-02'),

    'ecq': ('2020-03-02', '2020-05-15'),
    'gcq': ('2020-05-16', '2020-05-31'),
    'mgcq': ('2020-06-01', '2021-01-31'),
    'gcq2': ('2021-02-01', '2021-10-31'),
    'al3': ('2021-11-01', '2021-12-05'),
    'al2_1': ('2021-12-06', '2022-01-09'),
    'al3_2': ('2022-01-10', '2022-02-16'),
    'al2_2': ('2022-02-17', '2022-03-01'),
    'al1': ('2022-03-02', '2022-03-15'),
}

base_pars = dict(
    pop_size=10e3,
    pop_infected=1,
    location='philippines',
    pop_scale=37,
    pop_type='hybrid',
    rescale=True,
)

def plot_period(period_name):
    """Run simulation and plot results for a specific period using calibrated parameters"""
    if period_name not in INTERVENTION_PERIODS:
        print(f"Error: Period '{period_name}' not found. Available periods: {list(INTERVENTION_PERIODS.keys())}")
        return

    # Get period dates
    start_date, end_date = INTERVENTION_PERIODS[period_name]
    print(f"\nPlotting period: {period_name.upper()} ({start_date} to {end_date})")

    # Find the most recent calibration results
    param_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(f'best_params_{period_name}_')]
    if not param_files:
        print(f"No calibration results found for period {period_name}")
        return
    
    # Get the most recent file
    latest_file = sorted(param_files)[-1]
    params = sc.loadjson(os.path.join(OUTPUT_DIR, latest_file))
    
    print(f"Using parameters from: {latest_file}")
    print(f"Parameters: beta={params['beta']:.6f}, rel_death_prob={params['rel_death_prob']:.6f}")
    print(f"Misfit: {params['misfit']:.4f}")

    # Set up and run simulation
    period_pars = base_pars.copy()
    period_pars.update({
        'start_day': start_date,
        'end_day': end_date,
        'beta': params['beta'],
        'rel_death_prob': params['rel_death_prob']
    })
    
    sim = cv.Sim(pars=period_pars)
    sim.run(verbose=0)

    # Load raw and smoothed data
    raw_df = pd.read_csv("data/baguio_raw.csv", parse_dates=['date'])
    smoothed_df = pd.read_csv("data/baguio_smoothed.csv", parse_dates=['date'])
    
    # Set date as index for both dataframes
    raw_df = raw_df.set_index('date').sort_index()
    smoothed_df = smoothed_df.set_index('date').sort_index()
    
    # Get the common date range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Filter data for this period using the same date range
    period_raw = raw_df.loc[start_date:end_date]
    period_smoothed = smoothed_df.loc[start_date:end_date]

    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot cases
    ax1.plot(sim.results['date'], sim.results['new_infections'], 'b-', label='Simulated')
    ax1.plot(period_smoothed.index, period_smoothed['cases'], 'r-', label='Observed (Smoothed)')
    ax1.scatter(period_raw.index, period_raw['cases'], color='red', alpha=0.2, label='Observed (Raw)')
    ax1.set_title(f'Daily New Cases - {period_name.upper()}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cases')
    ax1.legend()
    ax1.grid(True)
    
    # Plot deaths
    ax2.plot(sim.results['date'], sim.results['new_deaths'], 'b-', label='Simulated')
    ax2.plot(period_smoothed.index, period_smoothed['deaths'], 'r-', label='Observed (Smoothed)')
    ax2.scatter(period_raw.index, period_raw['deaths'], color='red', alpha=0.2, label='Observed (Raw)')
    ax2.set_title(f'Daily New Deaths - {period_name.upper()}')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Deaths')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    
    # Save plot
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plt.savefig(os.path.join(OUTPUT_DIR, f'plot_{period_name}_{timestamp}.png'))
    print(f"Saved plot to {OUTPUT_DIR}/plot_{period_name}_{timestamp}.png")
    
    # Show plot
    plt.show()

if __name__ == '__main__':
    # Specify the period to plot
    period = 'merged_1'  # Change this to any period from INTERVENTION_PERIODS
    plot_period(period) 