import covasim as cv
import numpy as np
import optuna as op
import sciris as sc
import pandas as pd
import os
from misfit import calculate_simulation_misfit, smoothed_cases, smoothed_deaths, full_index
from datetime import datetime
import sys
import matplotlib.pyplot as plt

# Output folder for independent period calibrations
OUTPUT_DIR = 'period_calibration_independent'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define intervention periods
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

# play around these params
PERIOD_PARAMS = dict(
    beta=[0.005, 0.007],
    rel_death_prob=[0.5, 0.6],
)

# Base simulation parameters
base_pars = dict(
    pop_size=10e3,
    pop_infected=1,
    location='philippines',
    pop_scale=37,
    pop_type='hybrid',
    rescale=True,
)

def analyze_trials(study, period_name, timestamp):
    """Analyze and visualize trial results"""
    trials_df = pd.DataFrame([
        {
            'trial': t.number,
            'beta': t.params['beta'],
            'rel_death_prob': t.params['rel_death_prob'],
            'misfit': t.value
        }
        for t in study.trials
    ])
    
    # Save raw trial data
    trials_df.to_csv(os.path.join(OUTPUT_DIR, f'trials_{period_name}_{timestamp}.csv'), index=False)
    
    # Create scatter plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Beta vs Misfit
    ax1.scatter(trials_df['beta'], trials_df['misfit'], alpha=0.5)
    ax1.set_xlabel('Beta')
    ax1.set_ylabel('Misfit')
    ax1.set_title('Beta vs Misfit')
    
    # Rel Death Prob vs Misfit
    ax2.scatter(trials_df['rel_death_prob'], trials_df['misfit'], alpha=0.5)
    ax2.set_xlabel('Relative Death Probability')
    ax2.set_ylabel('Misfit')
    ax2.set_title('Relative Death Probability vs Misfit')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f'trial_analysis_{period_name}_{timestamp}.png'))
    plt.close()
    
    # Print summary statistics
    print("\nTrial Analysis Summary:")
    print(f"Number of trials: {len(trials_df)}")
    print("\nBest 5 trials:")
    print(trials_df.nsmallest(5, 'misfit'))
    print("\nParameter ranges for best 5 trials:")
    print(f"Beta range: {trials_df.nsmallest(5, 'misfit')['beta'].min():.6f} to {trials_df.nsmallest(5, 'misfit')['beta'].max():.6f}")
    print(f"Rel death prob range: {trials_df.nsmallest(5, 'misfit')['rel_death_prob'].min():.6f} to {trials_df.nsmallest(5, 'misfit')['rel_death_prob'].max():.6f}")

def calibrate_period(period_name, n_trials):
    if period_name not in INTERVENTION_PERIODS:
        print(f"Error: Period '{period_name}' not found. Available periods: {list(INTERVENTION_PERIODS.keys())}")
        sys.exit(1)

    start_date, end_date = INTERVENTION_PERIODS[period_name]
    print(f"\nCalibrating period: {period_name.upper()} ({start_date} to {end_date})")

    def objective(trial):
        # Suggest parameters
        beta = trial.suggest_float('beta', *PERIOD_PARAMS['beta'])
        rel_death_prob = trial.suggest_float('rel_death_prob', *PERIOD_PARAMS['rel_death_prob'])
        # Set up sim
        period_pars = base_pars.copy()
        period_pars.update({'start_day': start_date, 'end_day': end_date})
        sim = cv.Sim(pars=period_pars)
        sim.update_pars({'beta': beta, 'rel_death_prob': rel_death_prob})
        sim.run(verbose=0)
        # Calculate misfit for this period
        period_misfit = calculate_simulation_misfit(sim)
        return period_misfit

    # Set up Optuna study
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    study_name = f'calib_{period_name}_{timestamp}'
    storage = f'sqlite:///{OUTPUT_DIR}/calib_{period_name}_{timestamp}.db'
    sampler = op.samplers.TPESampler(n_startup_trials=5, n_ei_candidates=12)
    study = op.create_study(
        study_name=study_name,
        storage=storage,
        load_if_exists=False,
        direction='minimize',
        sampler=sampler
    )
    study.optimize(objective, n_trials=n_trials, n_jobs=1)

    # Analyze and visualize results
    analyze_trials(study, period_name, timestamp)

    # Save best parameters and results
    best_params = study.best_params
    best_value = study.best_value
    print(f"Best params for {period_name}: {best_params}, misfit: {best_value:.4f}")
    
    # Save to file
    result = {
        'period': period_name,
        'start_date': start_date,
        'end_date': end_date,
        **best_params,
        'misfit': best_value
    }
    sc.savejson(os.path.join(OUTPUT_DIR, f'best_params_{period_name}_{timestamp}.json'), result, indent=2)
    
    # Save final sim state
    period_pars = base_pars.copy()
    period_pars.update({'start_day': start_date, 'end_day': end_date})
    sim = cv.Sim(pars=period_pars)
    sim.update_pars(best_params)
    sim.run(verbose=0)
    sim.save(os.path.join(OUTPUT_DIR, f'final_sim_{period_name}_{timestamp}.sim'))
    print(f"Saved best parameters and final sim for {period_name} to {OUTPUT_DIR}")

if __name__ == '__main__':
    
    #     if len(sys.argv) != 2:
    #     print("Usage: python calibrate_period_independent.py <period_name>")
    #     print(f"Available periods: {list(INTERVENTION_PERIODS.keys())}")
    #     sys.exit(1)
    
    # period = sys.argv[1]

    # Specify the period to calibrate
    period = 'merged_1'  # You can change this to any period from INTERVENTION_PERIODS
    calibrate_period(period, n_trials=100) 