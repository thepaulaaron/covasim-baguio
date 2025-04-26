import covasim as cv
import matplotlib.pyplot as plt
import numpy as np
import time

# PH_POP_household = 108_667_043
PH_POP_household = 1_000_000
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
    print(f"\n✅ populate_ph() took {elapsed:.2f} seconds.")
    return sim

def populate_ph_scaled(n):
    pop_scale = PH_POP_household / n  # Adjust scaling

    start = time.time()

    sim = cv.Sim(
        pop_size=n,
        pop_scale=pop_scale,
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
    print(f"🌏 Virtual simulated population size: {len(sim.people) * sim.pars['pop_scale']:.0f}")

    print(f"\n✅ populate_ph_scaled() took {elapsed:.2f} seconds.")

    return sim

# ----------------------------------------------

if __name__ == '__main__':
    population =  1_000_000
    sim1 = populate_ph(population)

    simulated_agents = 100_000
    sim2 = populate_ph_scaled(simulated_agents)

    # Get data
    ages1 = sim1.people.age
    ages2 = sim2.people.age
    scaled_counts2 = [sim2.pars['pop_scale'] for _ in ages2]

    # Set up side-by-side plot
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot left: No scaling
    axes[0].hist(ages1, bins=30, edgecolor='black', alpha=0.7)
    axes[0].set_title(f"PH Age Distribution\n{len(sim1.people):,.0f} people (No Scaling)", fontsize=13)
    axes[0].set_xlabel("Age", fontsize=11)
    axes[0].set_ylabel("Number of People", fontsize=11)
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Plot right: Scaled
    axes[1].hist(ages2, bins=30, weights=scaled_counts2, edgecolor='black', alpha=0.7, color='skyblue')
    axes[1].set_title(f"PH Age Distribution\n{len(sim2.people) * sim2.pars['pop_scale']:,.0f} people (Scaled)", fontsize=13)
    axes[1].set_xlabel("Age", fontsize=11)
    axes[1].set_ylabel("Scaled Number of People", fontsize=11)
    axes[1].grid(True, linestyle='--', alpha=0.5)

    # Make Y-axis limits same
    max_y = max(axes[0].get_ylim()[1], axes[1].get_ylim()[1])
    axes[0].set_ylim(0, max_y)
    axes[1].set_ylim(0, max_y)

    # Make layout nice
    plt.tight_layout()
    plt.show()
