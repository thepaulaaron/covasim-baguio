import covasim as cv
import matplotlib.pyplot as plt
import numpy as np
# import networkx as nx

def summarize_population(sim):
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
    import matplotlib.pyplot as plt
    plt.hist(ages, bins=30, edgecolor='k', alpha=0.7)
    plt.title("Age Distribution in Hybrid Philippines Population")
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

    summarize_population(sim)

    # Show statistics of the people
    # fig = sim.people.plot() 
    return sim

if __name__ == '__main__':
    population = 200e3
    sim = populate_ph(population)
