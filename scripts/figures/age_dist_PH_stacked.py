import covasim as cv
import matplotlib.pyplot as plt
import numpy as np

# --- Covasim Data ---
covasim_age_data = cv.data.country_age_data.data['Philippines']
covasim_age_groups = list(covasim_age_data.keys())
covasim_population = list(covasim_age_data.values())

# --- Your Fine Data ---
fine_age_groups = [
    '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
    '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+'
]
fine_population = [
    11066707, 11266823, 11080715, 10459186, 9969846, 9172896, 8120568, 7179320,
    6491312, 5571168, 4941712, 4124118, 3367223, 2393521, 1575398, 930610, 955920
]

# --- Group fine into coarse ---
coarse_population = []
for i in range(0, 16, 2):
    summed = fine_population[i] + fine_population[i+1]
    coarse_population.append(summed)
coarse_population.append(fine_population[-1])  # 80+

# --- Plotting ---
x_coarse = np.arange(len(coarse_population))  # positions 0 to 8

plt.figure(figsize=(16, 8))

# Plot Covasim coarse bars
plt.bar(x_coarse + 0.2, covasim_population, width=0.4, label='Covasim Data', color='cornflowerblue')

# Plot stacked fine bars
bottoms = np.zeros_like(x_coarse, dtype=int)
for i in range(0, 16, 2):
    coarse_idx = i // 2
    plt.bar(coarse_idx - 0.2, fine_population[i], width=0.4, bottom=bottoms[coarse_idx], color='darkorchid', label='PSA Data (lower bracket)' if i==0 else "")
    bottoms[coarse_idx] += fine_population[i]

    plt.bar(coarse_idx - 0.2, fine_population[i+1], width=0.4, bottom=bottoms[coarse_idx], color='darkslateblue', label='PSA Data (upper bracket)' if i==0 else "")
    bottoms[coarse_idx] += fine_population[i+1]

# Last bar (80+)
plt.bar(8 - 0.2, fine_population[-1], width=0.4, color='darkslateblue')

# X ticks
xtick_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
plt.xticks(x_coarse, xtick_labels)

# Labels
plt.title('Age Distribution in the Philippines: Summed Actual Data (stacked) vs Covasim')
plt.xlabel('Age Group')
plt.ylabel('Population')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
