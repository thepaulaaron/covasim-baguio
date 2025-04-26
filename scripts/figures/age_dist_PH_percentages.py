import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
import covasim as cv

# 1. Load Covasim age data
covasim_data = cv.data.country_age_data.data['Philippines']

# 2. Your fine-grained actual data
actual_fine_population = np.array([
    11066707, 11266823, 11080715, 10459186, 9969846, 9172896,
    8120568, 7179320, 6491312, 5571168, 4941712, 4124118,
    3367223, 2393521, 1575398, 930610, 955920
])

actual_fine_labels = [
    '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', 
    '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', 
    '60-64', '65-69', '70-74', '75-79', '80+'
]

# 3. Coarse-grain the actual data to match Covasim brackets
# Map fine to coarse: (0-9), (10-19), (20-29), etc.

actual_coarse_population = np.array([
    actual_fine_population[0] + actual_fine_population[1],    # 0-9
    actual_fine_population[2] + actual_fine_population[3],    # 10-19
    actual_fine_population[4] + actual_fine_population[5],    # 20-29
    actual_fine_population[6] + actual_fine_population[7],    # 30-39
    actual_fine_population[8] + actual_fine_population[9],    # 40-49
    actual_fine_population[10] + actual_fine_population[11],  # 50-59
    actual_fine_population[12] + actual_fine_population[13],  # 60-69
    actual_fine_population[14] + actual_fine_population[15],  # 70-79
    actual_fine_population[16]                               # 80+
])

# 4. Get Covasim coarse data into matching format
covasim_coarse_population = np.array([
    covasim_data['0-9'],
    covasim_data['10-19'],
    covasim_data['20-29'],
    covasim_data['30-39'],
    covasim_data['40-49'],
    covasim_data['50-59'],
    covasim_data['60-69'],
    covasim_data['70-79'],
    covasim_data['80+']
])

coarse_labels = [
    '0-9', '10-19', '20-29', '30-39', '40-49', 
    '50-59', '60-69', '70-79', '80+'
]

# 5. Normalize to percentages
covasim_total = np.sum(covasim_coarse_population)
actual_total = np.sum(actual_coarse_population)

covasim_percentages = (covasim_coarse_population / covasim_total) * 100
actual_percentages = (actual_coarse_population / actual_total) * 100

# 6. Plot side-by-side
x = np.arange(len(coarse_labels))  # label locations
width = 0.35  # width of the bars

fig, ax = plt.subplots(figsize=(16, 8))

rects1 = ax.bar(x - width/2, covasim_percentages, width, label='Covasim', color='cornflowerblue')
rects2 = ax.bar(x + width/2, actual_percentages, width, label='Actual', color='darkslateblue')

# Labels and title
ax.set_ylabel('Percentage of Total Population (%)')
ax.set_xlabel('Age Groups')
ax.set_title('Age Distribution Percentages: Covasim vs Actual (Normalized)')
ax.set_xticks(x)
ax.set_xticklabels(coarse_labels)
ax.legend()

# Annotate bars with values
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()
plt.show()

# # 7. Statistical Test: Chi-squared

# # Rescale covasim to match actual total
# covasim_scaled = covasim_coarse_population * (actual_coarse_population.sum() / covasim_coarse_population.sum())

# # Chi-squared test
# chi2_stat, p_value = chisquare(f_obs=actual_coarse_population, f_exp=covasim_scaled)
# print(f"\nChi-Squared Statistic = {chi2_stat:.2f}")
# print(f"P-Value = {p_value:.4f}")

# if p_value < 0.05:
#     print("❌ Statistically significant difference between distributions.")
# else:
#     print("✅ No statistically significant difference — distributions are similar.")

# 8. Calculate Error Metrics

# Differences
differences = covasim_percentages - actual_percentages

# Mean Absolute Error (MAE)
mae = np.mean(np.abs(differences))

# Root Mean Squared Error (RMSE)
rmse = np.sqrt(np.mean(differences**2))

print(f"\nMean Absolute Error (MAE): {mae:.4f}%")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}%")
