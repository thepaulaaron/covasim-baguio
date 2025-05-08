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
        # Plot cumulative counts
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
        
        # Define color map for all states
        color_map = {
            'susceptible': 'blue',
            'exposed': 'yellow',
            'infectious': 'red',
            'infectious_asym': 'orange',
            'infectious_sym': 'darkred',
            'recovered': 'green',
            'dead': 'violet'
        }
        
        # Cumulative counts plot
        for state in self.tracked_states:
            ax1.plot(self.t, self.tracked_states[state], 
                    label=state.replace('_', ' ').title(), 
                    color=color_map[state])

        ax1.legend()
        ax1.set_xlabel('Day')
        ax1.set_ylabel('People')
        ax1.set_title('Cumulative Counts')
        ax1.set_ylim(bottom=0)
        ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

        # Daily counts plot
        for state in self.tracked_states:
            daily_counts = [0] + [self.tracked_states[state][i] - self.tracked_states[state][i-1] 
                                for i in range(1, len(self.tracked_states[state]))]
            
            ax2.plot(self.t, daily_counts, 
                    label=f'Daily {state.replace("_", " ").title()}', 
                    color=color_map[state], 
                    alpha=0.7)

        ax2.legend()
        ax2.set_xlabel('Day')
        ax2.set_ylabel('Daily New Cases')
        ax2.set_title('Daily Counts')
        ax2.set_ylim(bottom=0)
        ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

        plt.tight_layout()
        plt.show()
        return

BAGUIO_population_hh = 366358

sim = cv.Sim(
        # Setters
        pop_size = 500,
        pop_type = 'hybrid',
        location = 'Philippines',
        # pop_infected = 100,  # default
        n_days=180, 

        # Baguio-calibrated Parameters
        # beta = 0.01042,
        rel_death_prob = 0.05180,

        analyzers=store_seir(label='seir'))
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
    total = S + E + I + D
    print(f"{t}\t{S:,}\t{E:,}\t{I:,} ({I_asymp}+{I_symp}) \t{R:,}\t{D:,}\t{total:,}")


seir.plot()
