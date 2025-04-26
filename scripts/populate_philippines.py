import covasim as cv
import matplotlib.pyplot as plt
import numpy as np
# import networkx as nx
import concurrent.futures
from tqdm import tqdm 
from collections import Counter

# PH_POP_household = 108_667_043
PH_POP_household = 100_000
PH_POP_total     = 109_035_343

# -------------------------------------------------- #

def summarize_population(sim, scaled=False):
    people = sim.people

    # Age distribution
    ages = people.age
    print("\n📊 Age Distribution (sample):")


    print(np.round(np.percentile(ages,
        # Min, Q1, Median, Q3, Max
        [0, 25, 50, 75, 100]), 1))  

    # # Household size estimation via contact graph
    # household_contacts = sim.people.contacts['h']
    # pairs = list(zip(household_contacts['p1'], household_contacts['p2']))

    # # Build groups from pairwise household contacts
    # G = nx.Graph()
    # G.add_edges_from(pairs)

    # household_sizes = [len(c) for c in nx.connected_components(G)]
    # size_counts = Counter(household_sizes)

    # print("\n🏠 Estimated Household Size Distribution:")
    # for size in sorted(size_counts):
    #     print(f"{size} members: {size_counts[size]} households")

    # Plot age distribution
    plt.figure(figsize=(10, 6))
    plt.hist(ages, bins=30, edgecolor='k', alpha=0.7)

    if scaled:
        plt.title(f"PH Age Distribution (Scaled for {len(sim.people) * sim.pars['pop_scale']:.0f} people)")
    else:
        plt.title(f"PH Age Distribution (For {len(sim.people)})")

    plt.xlabel("Age")
    plt.ylabel("Number of People")
    plt.show()

def populate_ph(n):
    sim = cv.Sim(
        pop_size = n,
        pop_type='hybrid',
        location='Philippines',
        label='Philippines Population Example'
    )
    sim.initialize()
    print(f"\n✅ Population size: {len(sim.people)}")

    summarize_population(sim, False)

    # Show statistics of the people
    # fig = sim.people.plot() 
    return sim

# -------------------------------------------------- #

def populate_ph_scaled(n):
    pop_scale = PH_POP_household / n

    sim = cv.Sim(
        pop_size=n,
        pop_scale=pop_scale,
        rescale=True,
        pop_type='hybrid',
        location='Philippines',
        label='Philippines Population Example'
    )
    sim.initialize()

    print(f"\n✅ Number of agents created: {len(sim.people)}")
    print(f"🌏 Virtual simulated population size: {len(sim.people) * sim.pars['pop_scale']:.0f}")

    # Get the plot of agents' data (age, gender, etc.)
    # Default plot for simulated agents
    # fig = sim.people.plot()

    # Now plotting the age distribution
    print("\n📊 Plotting the population distribution... This may take a moment.")
    summarize_population(sim, True)

    return sim

if __name__ == '__main__':
    # population = 100e3
    # sim = populate_ph(population)

    simulated_agents = 100e3
    sim = populate_ph_scaled(simulated_agents)