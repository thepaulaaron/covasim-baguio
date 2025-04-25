import covasim as cv
import networkx as nx
import numpy as np

def summarize_population(sim):
    people = sim.people
    contacts = people.contacts  # Dictionary of contacts per layer

    # General population stats
    print(f"\n📊 Total people generated: {len(people)}")
    print(f"👶 Age range: {min(people.age):.2f} to {max(people.age):.2f}")
    print(f"🧑 Avg age: {people.age.mean():.2f}")
    print(f"👫 Number of males: {(people.sex == 0).sum()}")
    print(f"👭 Number of females: {(people.sex == 1).sum()}")

    # Sample some individuals and print their contacts
    print(f"\n👥 Sample individuals with contacts: (from total {len(people)})")
    sample_indices = np.random.choice(len(people), size=5, replace=False)  # Randomly sample 5 indices
    print(f"Sampled indices: {sample_indices}")
    for i in sample_indices:
        person = people[int(i)]
        print(f"Person {i}:")
        print(f"  Age: {person.age:.2f}")
        print(f"  Sex: {'M' if person.sex == 0 else 'F'}")
        for layer in ['h', 's', 'w', 'c']:  # Household, school, work, and community layers
            p1 = contacts[layer]['p1']
            p2 = contacts[layer]['p2']
            contact_ids = set(p2[p1 == i]) | set(p1[p2 == i])  # Find contact pairs for this person
            print(f"  Contacts - {layer}: {sorted(contact_ids)}")
        print()

    # Optional: Visualize contact layers as graphs using NetworkX
    # for layer in ['h', 's', 'w', 'c']:  # Iterate over each contact layer
    #     layer_contacts = contacts[layer]
    #     G_layer = nx.Graph()
    #     G_layer.add_edges_from(zip(layer_contacts['p1'], layer_contacts['p2']))
    #     print(f"{layer} layer: {G_layer.number_of_edges()} edges")

def make_baguio_population(total_population_baguio=366358, total_population_ph=109035343):
    # Age group data for Baguio (scaled for population size)
    age_groups_baguio = {
        '0-4': 107, '5-9': 110, '10-14': 105, '15-19': 100, '20-24': 97,
        '25-29': 99, '30-34': 99, '35-39': 101, '40-44': 97, '45-49': 97,
        '50-54': 92, '55-59': 89, '60-64': 86, '65-69': 75, '70-74': 74,
        '75-79': 58, '80+': 44
    }
    
    # 1. Scaling Factors based on Baguio vs. Philippines data
    scaling_factor_population = total_population_baguio / total_population_ph
    print(f"Scaling factor for total population: {scaling_factor_population:.4f}")
    
    # 2. Scaling the Household Population
    total_households_ph = 26393906
    total_households_baguio = 100220
    scaling_factor_households = total_households_baguio / total_households_ph
    print(f"Scaling factor for number of households: {scaling_factor_households:.4f}")
    
    # 3. Scaling the Urban Population
    total_urban_population_ph = 58930729
    total_urban_population_baguio = 236926
    scaling_factor_urban_population = total_urban_population_baguio / total_urban_population_ph
    print(f"Scaling factor for urban population: {scaling_factor_urban_population:.4f}")
    
    # 4. Create the synthetic population for Baguio
    sim = cv.Sim(
        pop_size=total_population_baguio,  # Use Baguio's total population size
        pop_type='hybrid',  # Hybrid population type
        location='Philippines',  # Set to Philippines for general location
        label='Baguio City Population Example'
    )
    sim.initialize()

    # 5. Create an age distribution based on the age groups
    age_group_proportions = {group: count / sum(age_groups_baguio.values()) for group, count in age_groups_baguio.items()}
    
    # Create the synthetic population based on the proportions
    ages = []
    for group, proportion in age_group_proportions.items():
        # Determine the age range for this group
        age_range = group.split('-')
        if len(age_range) == 1:  # If the group is 80+, use 80 as the lower bound
            min_age = 80
            max_age = 100
        else:
            min_age = int(age_range[0])
            max_age = int(age_range[1])
        
        # Scale the population for each group and assign ages
        group_population = int(proportion * total_population_baguio)
        ages.extend(np.random.randint(min_age, max_age, size=group_population))

    # Assign ages to the synthetic population
    sim.people.age = np.array(ages)

    # 6. Adjust sex distribution based on the ratio of males to females
    male_ratio = 178966 / total_population_baguio
    num_males = int(male_ratio * total_population_baguio)
    num_females = total_population_baguio - num_males
    sim.people.sex = np.concatenate([np.zeros(num_males), np.ones(num_females)])

    # 7. Applying scaling factors to adjust population characteristics
    sim.pars['pop_size'] = int(total_population_baguio)  # Set the population size for the simulation
    sim.pars['pop_scale'] = scaling_factor_population  # Scale the population according to Baguio

    print(f"\n✅ Population size set for Baguio: {len(sim.people)}")
    summarize_population(sim)  # Summarize the population data for Baguio
    return sim

if __name__ == '__main__':
    sim = make_baguio_population()  # Create Baguio's population with scaling
