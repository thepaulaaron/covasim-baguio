import covasim as cv
import numpy as np
import matplotlib.pyplot as plt

def get_baguio_age_distribution():
    """
    Returns the age distribution array for Baguio city.
    Returns:
        numpy.ndarray: Array of ages following Baguio's age distribution
    """
    # --- Prepare custom age distribution for Baguio ---
    age_bins = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24),
                (25, 29), (30, 34), (35, 39), (40, 44), (45, 49),
                (50, 54), (55, 59), (60, 64), (65, 69), (70, 74),
                (75, 79), (80, 100)]

    age_counts = [26573, 28840, 30713, 34527, 39461,
                  35642, 30818, 27658, 23055, 19413,
                  18170, 15460, 12362, 8581, 5461,
                  2985, 3432]

    # Create age array using actual counts
    ages = []
    for (low, high), count in zip(age_bins, age_counts):
        ages.extend(np.random.randint(low, high + 1, count))
    ages = np.array(ages)
    np.random.shuffle(ages)
    
    return ages

if __name__ == "__main__":
    # Get the age distribution
    ages = get_baguio_age_distribution()
    
    # --- Scaled from Baguio AgeHist

        # pop_target = 500_000
        # scaling_factor = pop_target / len(ages)
        # print(f"PopTarget: {pop_target} \t SF: {scaling_factor}")

        # sim2 = cv.Sim(
        #     n_days=365,
        #     pop_size=pop_target,
        #     pop_type='hybrid',
        #     location=None,      # No default location data, so Covasim doesn't overwrite your population
        #     pop_infected=10,
        #     pop_scale=scaling_factor,
        # )
        # sim2.initialize()  # Initialize first to create the sim object
        # sim2.people = cv.make_people(sim=sim2, age=ages, n=len(ages), pop_scale=scaling_factor)  # Now inject custom ages
        # sim2.run()

    # --- Simulation 1: Custom age distribution (Baguio) ---
    sim1 = cv.Sim(
        n_days=365,
        pop_size=len(ages),
        pop_type='hybrid',
        location=None,      # No default location data, so Covasim doesn't overwrite your population
        pop_infected=10,
        pop_scale=1,
    )
    sim1.initialize()  # Initialize first to create the sim object
    sim1.people = cv.make_people(sim=sim1, age=ages, n=len(ages), pop_scale=1)  # Now inject custom ages
    sim1.run()

    # --- Simulation 2: Default Philippines ---
    sim2 = cv.Sim(
        n_days=365,
        pop_size=len(ages),  # Same pop size for fair comparison
        pop_type='hybrid',
        location='philippines',
        pop_infected=10,
        pop_scale=1,
    )
    sim2.initialize()
    sim2.run()

    # --- Plot comparison ---
    plt.figure(figsize=(12,6))
    plt.plot(sim1.results['date'], sim1.results['new_infections'], label='Baguio age dist', color='blue')
    plt.plot(sim2.results['date'], sim2.results['new_infections'], label='Philippines default', color='red')
    plt.title('New Infections: Custom Baguio vs Philippines Default Age Distribution')
    plt.xlabel('Date')
    plt.ylabel('New infections')
    plt.legend()
    plt.grid(True)
    plt.show()

    # --- Print summary stats ---
    print("Summary statistics:")
    print("Custom Baguio ages:")
    print(f"Mean age: {np.mean(sim1.people.age):.2f}")
    print(f"Median age: {np.median(sim1.people.age):.2f}")
    print(f"Population size: {len(sim1.people)}")

    print("\nDefault Philippines ages:")
    print(f"Mean age: {np.mean(sim2.people.age):.2f}")
    print(f"Median age: {np.median(sim2.people.age):.2f}")
    print(f"Population size: {len(sim2.people)}")
