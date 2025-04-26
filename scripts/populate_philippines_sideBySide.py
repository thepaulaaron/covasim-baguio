import covasim as cv
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import time

# Philippine population
PH_POP_household = 300_000
PH_POP_total     = 109_035_343

# ----------------------------------------------

def populate_ph(n):
    start = time.time()
    sim = cv.Sim(
        pop_size=n,
        pop_type='hybrid',
        location='Philippines',
        label='Philippines Population Example'
    )
    sim.initialize()
    end = time.time()
    elapsed = end - start

    print(f"\n✅ Population size: {len(sim.people)}")
    print(f"✅ populate_ph() took {elapsed:.2f} seconds.")
    return sim

def populate_ph_scaled():
  
    # Adjustable scaling:
      # populate_ph_scaled(n: simulated agents)
    # pop_scale = PH_POP_household / n 
    # Note: Use cv.Sim(pop_size=n)

    # Fixed scaling:
      # populate_ph_scaled()
    fixed_pop_scale = 1.5
    pop_size = int(PH_POP_household / fixed_pop_scale)
    # Note: Use cv.Sim(pop_size=pop_size)

    start = time.time()

    sim = cv.Sim(
        pop_size=pop_size,
        pop_scale=fixed_pop_scale,
        rescale=True,
        pop_type='hybrid',
        location='Philippines',
        label='Philippines Population Example (Scaled)'
    )
    sim.initialize()
    
    end = time.time()
    elapsed = end - start

    print(f"\n✅ Number of agents created: {len(sim.people)}")
    print(f"🌏 Population scaling factor: {sim.pars['pop_scale']:.2f}")
    print(f"🌏 Virtual simulated population size: {len(sim.people) * sim.pars['pop_scale']:,.0f}")
    print(f"✅ populate_ph_scaled() took {elapsed:.2f} seconds.")
    return sim

def compare_distributions(ages1, ages2, scaled_counts2, bins=20):
    from scipy.stats import chisquare
    import numpy as np

    # Create histograms (RAW COUNTS)
    hist1, bin_edges = np.histogram(ages1, bins=bins)
    hist2, _ = np.histogram(ages2, bins=bin_edges, weights=scaled_counts2)

    # Normalize histograms
    hist1_norm = hist1 / np.sum(hist1) if np.sum(hist1) > 0 else hist1
    hist2_norm = hist2 / np.sum(hist2) if np.sum(hist2) > 0 else hist2

    # Ensure the total sums match for the chi-square test
    total_hist1 = np.sum(hist1)
    total_hist2 = np.sum(hist2)
    if total_hist1 != total_hist2:
        scale_factor = total_hist1 / total_hist2
        hist2 = hist2 * scale_factor

    # Calculate RMSE between normalized histograms
    rmse = np.sqrt(np.mean((hist1_norm - hist2_norm) ** 2))

    # 🛠️ Perform Chi-square test on RAW COUNTS (not normalized)
    chi2_stat, p_value = chisquare(f_obs=hist1, f_exp=hist2)

    # 📋 Print summary
    print("\n📊 Comparison Summary:")
    print(f"🔹 RMSE between distributions: {rmse:.5f}")
    print(f"🔹 Chi-square statistic: {chi2_stat:.2f}")
    print(f"🔹 p-value: {p_value:.5f}")

    if p_value < 0.05:
        print("⚠️ Significant difference (scaling may introduce bias)")
    else:
        print("✅ No significant difference (scaling seems acceptable)")

    return chi2_stat, p_value, rmse, hist1_norm, hist2_norm, bin_edges


def plot_comparison(hist1_norm, hist2_norm, bins, sim1, sim2):
    """Plot the comparison between two distributions."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot left: No scaling
    axes[0].bar(bins[:-1], hist1_norm, width=1, edgecolor='black', alpha=0.7)
    axes[0].set_title(f"PH Age Distribution\n{len(sim1.people):,.0f} people (No Scaling)", fontsize=13)
    axes[0].set_xlabel("Age", fontsize=11)
    axes[0].set_ylabel("Proportion of People", fontsize=11)
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Plot right: Scaled
    axes[1].bar(bins[:-1], hist2_norm, width=1, edgecolor='black', alpha=0.7, color='skyblue')
    axes[1].set_title(f"PH Age Distribution\n{len(sim2.people) * sim2.pars['pop_scale']:,.0f} people (Scaled)", fontsize=13)
    axes[1].set_xlabel("Age", fontsize=11)
    axes[1].set_ylabel("Scaled Proportion", fontsize=11)
    axes[1].grid(True, linestyle='--', alpha=0.5)

    # Make Y-axis limits same
    max_y = max(axes[0].get_ylim()[1], axes[1].get_ylim()[1])
    axes[0].set_ylim(0, max_y)
    axes[1].set_ylim(0, max_y)

    # Make layout nice
    plt.tight_layout()
    plt.show()

# Main code block
if __name__ == '__main__':
    # Set different simulated population sizes
    population = PH_POP_household
    sim1 = populate_ph(population)

    # simulated_agents = 900e2
    # sim2 = populate_ph_scaled(simulated_agents)
    sim2 = populate_ph_scaled()

    # Extract ages
    ages1 = sim1.people.age
    ages2 = sim2.people.age
    scaled_counts2 = [sim2.pars['pop_scale'] for _ in ages2]

    # Compare distributions
    chi2_stat, p_value, rmse, hist1_norm, hist2_norm, bins = compare_distributions(ages1, ages2, scaled_counts2)

    # Plot comparison
    plot_comparison(hist1_norm, hist2_norm, bins, sim1, sim2)

    # Print the Chi-Square Results
    print(f"\n📊 Chi-Square Test Results: ")
    print(f"Chi-Square Statistic: {chi2_stat:.2f}")
    print(f"P-Value: {p_value:.5f}")
