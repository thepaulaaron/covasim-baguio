import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV
data = pd.read_csv('data/baguio_cases.csv')
data['dates_discovery'] = pd.to_datetime(data['dates_discovery'])

# Plot cumulative cases
plt.figure(figsize=(18, 6))
plt.plot(data['dates_discovery'], data['cum_cases'], label='Cumulative Cases', color='darkslateblue')

# Define milestones: (start, end, label, color)
milestones = [
    ('2020-03-02', '2020-05-15', 'ECQ', 'red'),
    ('2020-05-16', '2020-05-31', 'GCQ', 'darkred'),
    ('2020-06-01', '2021-01-31', 'MGCQ', 'orange'),
    ('2021-02-01', '2021-10-31', 'GCQ', 'darkred'),
    ('2021-11-01', '2021-12-05', 'AL3', 'gold'),
    ('2021-12-06', '2022-01-09', 'AL2', 'yellowgreen'),
    ('2022-01-10', '2022-02-16', 'AL3', 'gold'),
    ('2022-02-17', '2022-03-01', 'AL2', 'yellowgreen'),
    ('2022-03-02', '2023-07-31', 'AL1', 'lightgreen')
]

# Plot shaded regions and add text labels
for start, end, label, color in milestones:
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    plt.axvspan(start_date, end_date, color=color, alpha=0.3)

    # Add text label in the middle of the shaded region
    middle_date = start_date + (end_date - start_date) / 2
    y_position = data['cum_cases'].max() * 0.7  # Adjust vertical position (80% up)
    plt.text(middle_date, y_position, label,
             horizontalalignment='center', verticalalignment='center',
             fontsize=9, color='black', rotation=90, alpha=0.7)

# Legend only for the main cumulative line
# plt.legend(['Cumulative Cases'], loc='upper left')

# plt.xlabel('Date')
plt.ylabel('Cumulative Cases')
plt.title('COVID-19 Cumulative Cases in Baguio City Over Time with Quarantine Levels')
# plt.xticks(rotation=45)
# plt.grid(True)
plt.tight_layout()

plt.show()
