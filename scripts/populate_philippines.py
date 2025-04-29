import covasim as cv
import matplotlib.pyplot as plt
import numpy as np
# import networkx as nx
import concurrent.futures
from tqdm import tqdm 
from collections import Counter
import time

# PH_POP_household = 108_667_043
PH_POP_household = 100_000
# PH_POP_total     = 109_035_343

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

    # Custom age groups (non-overlapping)
    age_groups = [
        ("0–4", 0, 4),
        ("5–9", 5, 9),
        ("10–14", 10, 14),
        ("15–19", 15, 19),
        ("20–24", 20, 24),
        ("25–29", 25, 29),
        ("30–34", 30, 34),
        ("35–39", 35, 39),
        ("40–44", 40, 44),
        ("45–49", 45, 49),
        ("50–54", 50, 54),
        ("55–59", 55, 59),
        ("60–64", 60, 64),
        ("65–69", 65, 69),
        ("70–74", 70, 74),
        ("75–79", 75, 79),
        ("80+", 80, 120),
    ]

    group_counts = {}
    for label, lower, upper in age_groups:
        count = np.sum((ages >= lower) & (ages <= upper))
        if scaled:
            # Scale the count
            count = count * sim.pars['pop_scale']
        group_counts[label] = count

    # Print group counts
    print("\n📊 Age Group Counts:")
    total = 0
    for label, count in group_counts.items():
        total += count
        percent = (count / total) * 100
        print(f"{label}: {count:,.0f} people ({percent:.2f}%)")

    # Print total count
    print(f"\n🔢 Total Population: {total:,.0f} people")

    # Plotting
    labels = list(group_counts.keys())
    values = list(group_counts.values())

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color='skyblue', edgecolor='k')
    # plt.xticks(rotation=45, ha='right')
    
    if scaled:
        plt.title(f"PH Age Distribution (Scaled for {len(sim.people) * sim.pars['pop_scale']:.0f} people)")
    else:
        plt.title(f"PH Age Distribution (For {len(sim.people)})")

    plt.xlabel("Age")
    plt.ylabel("Number of People")
    plt.tight_layout()
    plt.show()

def populate_ph(n):
    start = time.time()
    sim = cv.Sim(
        pop_size = n,
        pop_type='hybrid',
        location='Philippines',
        label='Philippines Population Example'
    )
    sim.initialize()
    end = time.time()
    elapsed = end - start

    print(f"\n✅ Population size: {len(sim.people)}")
    print(f"✅ populate_ph() took {elapsed:.2f} seconds.")

    summarize_population(sim, False)

    # Show statistics of the people
    # fig = sim.people.plot() 
    return sim

# -------------------------------------------------- #

def populate_ph_scaled(n):
    pop_scale = PH_POP_household / n
    transmuted_pop_size = (n * 1.20)

    start = time.time()
    sim = cv.Sim(
        pop_size=transmuted_pop_size,
        pop_scale=pop_scale,
        rescale=True,
        pop_type='hybrid',
        location='Philippines',
        label='Philippines Population Example',
        verbose=1                          # Enable verbosity for debugging
    )
    sim.initialize()

    # Correct the pop_scale AFTER knowing true len(sim.people)
    true_n = len(sim.people)
    sim['pop_scale'] = PH_POP_household / true_n

    end = time.time()
    elapsed = end - start

    print(f"\n✅ Number of agents created: {true_n}")
    print(f"🌏 Virtual simulated population size: {true_n * sim.pars['pop_scale']:.0f}")
    print(f"🌏 Population scaling factor: {sim.pars['pop_scale']:.2f}")
    print(f"✅ populate_ph_scaled() took {elapsed:.2f} seconds.")

    # Get the plot of agents' data (age, gender, etc.)
    # Default plot for simulated agents
    # fig = sim.people.plot()

    # Now plotting the age distribution
    print("\n📊 Plotting the population distribution... This may take a moment.")
    summarize_population(sim, True)

    return sim

if __name__ == '__main__':
    # population = PH_POP_household
    # sim = populate_ph(population)

    simulated_agents = 100_000
    sim = populate_ph_scaled(simulated_agents)