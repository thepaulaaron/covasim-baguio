import covasim as cv
import matplotlib.pyplot as plt

class store_seir(cv.Analyzer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # This is necessary to initialize the class properly
        self.tracked_states = {
            'susceptible': [],
            'exposed': [],
            'infectious': [],
            'infectious_asym': [],
            'infectious_sym': [],
            'recovered': [],
            'dead': []
        }
        self.t = []
        self.S = []
        self.E = []
        self.I = []
        self.R = []
        return

    def apply(self, sim):
        ppl = sim.people # Shorthand
        self.t.append(sim.t)
        self.tracked_states['susceptible'].append(ppl.susceptible.sum())
        self.tracked_states['exposed'].append(ppl.exposed.sum() - ppl.infectious.sum())
        self.tracked_states['infectious'].append(ppl.infectious.sum())
        self.tracked_states['infectious_asym'].append((sim.people.infectious & ~sim.people.symptomatic).sum())
        self.tracked_states['infectious_sym'].append((sim.people.infectious & sim.people.symptomatic).sum())
        self.tracked_states['recovered'].append(ppl.recovered.sum())
        self.tracked_states['dead'].append(ppl.dead.sum())
        return

    def plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.t, self.tracked_states['susceptible'], label='Susceptible')
        ax.plot(self.t, self.tracked_states['exposed'], label='Exposed')
        ax.plot(self.t, self.tracked_states['infectious'], label='Infectious')
        ax.plot(self.t, self.tracked_states['recovered'], label='Recovered')
        ax.plot(self.t, self.tracked_states['dead'], label='Dead')

        ax.legend()
        ax.set_xlabel('Day')
        ax.set_ylabel('People')

        # Set y-axis to start at 0
        ax.set_ylim(bottom=0)

        # Format y-axis ticks with commas
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

        plt.show()
        return

sim = cv.Sim(pop_size = 500,
            pop_infected = 100, n_days=180, analyzers=store_seir(label='seir'))
sim.run()
seir = sim.get_analyzer('seir') # Retrieve by label

# Explicitly print SEIR counts per day
print("Day\tSUS\tEXP\tINF (asymp+symp)\t\tRCV\tDTH\tTotal")
for t, S, E, I, I_asymp, I_symp, R, D in zip(seir.t, 
                            seir.tracked_states['susceptible'], 
                            seir.tracked_states['exposed'], 
                            seir.tracked_states['infectious'], 
                            seir.tracked_states['infectious_asym'], 
                            seir.tracked_states['infectious_sym'], 
                            seir.tracked_states['recovered'], 
                            seir.tracked_states['dead']):
    total = S + E + I + R + D
    print(f"{t}\t{S:,}\t{E:,}\t{I:,} ({I_asymp}+{I_symp}) \t{R:,}\t{D:,}\t{total:,}")


seir.plot()
