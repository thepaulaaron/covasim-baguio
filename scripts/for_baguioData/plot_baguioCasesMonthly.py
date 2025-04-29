import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data/baguio_cases_monthly.csv')  

# Convert 'dates_discovery' to datetime format
data['month_year'] = pd.to_datetime(data['month_year'])

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(data['month_year'], data['monthly_cases'], label='Monthly Cases', color='darkslateblue')
# plt.xlabel('Date')
plt.ylabel('Cases')
plt.title('COVID-19 Monthly Cases in Baguio Over Time')
# plt.xticks(rotation=45)
# plt.grid(True)
plt.tight_layout()
# plt.legend()

# Show the plot
plt.show()
