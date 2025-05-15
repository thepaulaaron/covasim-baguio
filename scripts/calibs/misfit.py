import pandas as pd
import numpy as np
import covasim as cv

# Load the CSV
df = pd.read_csv("data/baguio_raw.csv", parse_dates=['date'])

# Set 'date' as index and ensure continuous daily date range
df = df.set_index('date').sort_index()
full_index = pd.date_range(start=df.index.min(), end=df.index.max())
df = df.reindex(full_index, fill_value=0)
df.index.name = 'date'

# Extract series
cases = df['cases'].values
deaths = df['deaths'].values

# Apply 7-day centered rolling average smoothing
def smooth(data, window=7):
    return pd.Series(data).rolling(window=window, center=True).mean().to_numpy()

smoothed_cases = smooth(cases)
smoothed_deaths = smooth(deaths)

def get_covasim_results(sim):
    """Extract cases and deaths from Covasim simulation results"""
    dates = sim.results['date']
    cases = sim.results['new_infections'].values  # Convert to numpy array
    deaths = sim.results['new_deaths'].values     # Convert to numpy array
    
    # Create a DataFrame with the same date range as our observations
    sim_df = pd.DataFrame({'cases': cases, 'deaths': deaths}, index=dates)
    sim_df = sim_df.reindex(full_index, fill_value=0)
    
    return sim_df['cases'].values, sim_df['deaths'].values

def compute_misfit(obs_cases, model_cases, obs_deaths, model_deaths):
    M_diag = np.max(obs_cases) if np.max(obs_cases) != 0 else 1
    M_death = np.max(obs_deaths) if np.max(obs_deaths) != 0 else 1

    print(f"Normalizers: M_diag = {M_diag:.2f}, M_death = {M_death:.2f}")
    print(f"Observed cases max: {np.max(obs_cases):.2f}, Simulated cases max: {np.max(model_cases):.2f}")
    print(f"Observed deaths max: {np.max(obs_deaths):.2f}, Simulated deaths max: {np.max(model_deaths):.2f}")
    
    J = np.sum(np.abs(obs_cases - model_cases) / M_diag +
               np.abs(obs_deaths - model_deaths) / M_death)
    return J

def calculate_simulation_misfit(sim):
    """Calculate misfit between Covasim simulation and smoothed observations"""
    # Get simulation results
    sim_cases, sim_deaths = get_covasim_results(sim)
    
    # Ensure no NaNs in smoothed version
    valid_idx = ~np.isnan(smoothed_cases) & ~np.isnan(smoothed_deaths)
    
    # Use only valid indices for comparison
    smooth_cases_valid = smoothed_cases[valid_idx]
    smooth_deaths_valid = smoothed_deaths[valid_idx]
    sim_cases_valid = sim_cases[valid_idx]
    sim_deaths_valid = sim_deaths[valid_idx]
    
    # Calculate misfit
    J = compute_misfit(smooth_cases_valid, sim_cases_valid,
                      smooth_deaths_valid, sim_deaths_valid)
    
    return J

# Example usage:
# sim = cv.Sim(...)  # Your Covasim simulation
# misfit = calculate_simulation_misfit(sim)
# print(f"Misfit between smoothed data and simulation: {misfit:.4f}")
