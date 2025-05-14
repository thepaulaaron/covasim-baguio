import pandas as pd
import matplotlib.pyplot as plt

df_raw = pd.read_csv('data/baguio_raw.csv', parse_dates=['date'])
df_smoothed = pd.read_csv('data/baguio_smoothed.csv', parse_dates=['date'])

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot cases
ax1.plot(df_raw['date'], df_raw['cases'], 'o', alpha=0.3, label='Raw Cases', markersize=3, color='blue')
ax1.plot(df_smoothed['date'], df_smoothed['cases'], '-', label='7-day Moving Average', linewidth=2, color='red')
ax1.set_title('COVID-19 Cases in Baguio City')
ax1.set_ylabel('Number of Cases')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot deaths
ax2.plot(df_raw['date'], df_raw['deaths'], 'o', alpha=0.3, label='Raw Deaths', markersize=3, color='green')
ax2.plot(df_smoothed['date'], df_smoothed['deaths'], '-', label='7-day Moving Average', linewidth=2, color='orange')
ax2.set_title('COVID-19 Deaths in Baguio City')
ax2.set_ylabel('Number of Deaths')
ax2.set_xlabel('Date')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot
plt.savefig('data/smoothed_vs_raw.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'data/smoothed_vs_raw.png'") 