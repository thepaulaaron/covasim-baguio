import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Mock data parameters
population = 400000  # Assumed population of Baguio
initial_infected = int(population * 0.01)  # 1% initially infected
days = 365  # Simulate for one year
daily_tests = int(population * 0.1)  # 10% of population tested per day

# Initial mock cases
initial_cases = np.zeros(days)
initial_cases[0] = initial_infected  # All initial cases on day 0

# Simulating daily infection dynamics
def simulate_daily_cases(population, initial_cases, daily_tests, transmission_rate, interventions):
    cases = initial_cases.copy()
    for day in range(1, len(cases)):
        # New cases from previous day's infected people
        new_cases = cases[day - 1] * transmission_rate * (1 - interventions)
        cases[day] = cases[day - 1] + new_cases
        
        # Preventing cases from exceeding population size
        if cases[day] > population:
            cases[day] = population
    
    return cases

# Example of a 50% intervention reduction on transmission
transmission_rate = 0.2  # Rate of infection transmission
interventions = 0.5  # Lockdown or distancing reduces transmission by 50%

# Simulate daily infection numbers
daily_infections = simulate_daily_cases(population, initial_cases, daily_tests, transmission_rate, interventions)

# Convert to a DataFrame for easier visualization
data = pd.DataFrame({
    'Day': np.arange(0, days),
    'Infected': daily_infections
})

# Show a preview of the mock data
print(data.head())

# Plotting the daily infection curve
plt.plot(data['Day'], data['Infected'], label='Infected')
plt.xlabel('Days')
plt.ylabel('Number of Infected People')
plt.title('Mock COVID-19 Infections in Baguio (Simulated)')
plt.legend()
plt.show()