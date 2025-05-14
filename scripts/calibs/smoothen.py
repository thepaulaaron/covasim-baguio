import pandas as pd

file_path = 'data/baguio_raw.csv'
df_raw = pd.read_csv(file_path, parse_dates=['date'])

# Apply 7-day moving average smoothing to 'cases' and 'deaths' using rolling window
df_smoothed = df_raw.copy()
df_smoothed['cases'] = df_smoothed['cases'].rolling(window=7, center=True).mean()
df_smoothed['deaths'] = df_smoothed['deaths'].rolling(window=7, center=True).mean()

# Drop rows with NaN (caused by rolling window at the edges)
df_smoothed.dropna(inplace=True)

# Save the smoothed version for Covasim
smoothed_file_path = 'data/baguio_smoothed.csv'
df_smoothed.to_csv(smoothed_file_path, index=False)

print(f'Smoothed data saved at: {smoothed_file_path}')
