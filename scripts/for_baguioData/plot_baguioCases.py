import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data/baguio_cases.csv')  

# Convert 'dates_discovery' to datetime format
data['dates_discovery'] = pd.to_datetime(data['dates_discovery'])

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(data['dates_discovery'], data['cases'], label='Cases', color='darkslateblue')
# plt.xlabel('Date')
plt.ylabel('Cases')
plt.title('COVID-19 Cases in Baguio Over Time')
# plt.xticks(rotation=45)
# plt.grid(True)
plt.tight_layout()
# plt.legend()

# Show the plot
plt.show()
