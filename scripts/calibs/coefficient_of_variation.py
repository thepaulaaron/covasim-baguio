import pandas as pd

# Load the data
df = pd.read_csv("data/baguio_raw.csv")

# Optional: convert date column to datetime if needed
df['date'] = pd.to_datetime(df['date'])

# Extract the daily case and death series
daily_cases = df['cases']
daily_deaths = df['deaths']

# Compute CV for cases
mean_cases = daily_cases.mean()
std_cases = daily_cases.std()
cv_cases = std_cases / mean_cases

# Compute CV for deaths
mean_deaths = daily_deaths.mean()
std_deaths = daily_deaths.std()
cv_deaths = std_deaths / mean_deaths

# Print results
print(f"Cases - Mean: {mean_cases:.2f}, Std Dev: {std_cases:.2f}, CV: {cv_cases:.4f}")
print(f"Deaths - Mean: {mean_deaths:.2f}, Std Dev: {std_deaths:.2f}, CV: {cv_deaths:.4f}")
