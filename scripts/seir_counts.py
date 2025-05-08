import covasim as cv
import matplotlib.pyplot as plt
import pandas as pd

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

        # Define visualization data for quarantine periods
        quarantine_vis = [
            # (start_date, end_date, label, color)
            ('2020-03-02', '2020-05-15', 'ECQ', 'red'),
            ('2020-05-16', '2020-05-31', 'GCQ', 'darkred'),
            ('2020-06-01', '2021-01-31', 'MGCQ', 'orange'),
            ('2021-02-01', '2021-10-31', 'GCQ', 'darkred'),
            ('2021-11-01', '2021-12-05', 'AL3', 'gold'),
            ('2021-12-06', '2022-01-09', 'AL2', 'yellowgreen'),
            ('2022-01-10', '2022-02-16', 'AL3', 'gold'),
            ('2022-02-17', '2022-03-01', 'AL2', 'yellowgreen'),
            ('2022-03-02', '2023-07-31', 'AL1', 'lightgreen')
        ]

        # Add vertical lines and annotations for each quarantine period
        for i, (start_date, end_date, label, color) in enumerate(quarantine_vis):
            start_day = (pd.to_datetime(start_date) - pd.to_datetime('2020-03-02')).days
            end_day = (pd.to_datetime(end_date) - pd.to_datetime('2020-03-02')).days
            
            # Add vertical lines
            ax1.axvline(x=start_day, color=color, linestyle='--', alpha=0.5)
            ax1.axvline(x=end_day, color=color, linestyle='--', alpha=0.5)
            ax2.axvline(x=start_day, color=color, linestyle='--', alpha=0.5)
            ax2.axvline(x=end_day, color=color, linestyle='--', alpha=0.5)

            # Add text annotations only at the start of each period
            # Position text at different heights to avoid overlap
            y_pos = ax1.get_ylim()[1] * (0.95 - (i % 3) * 0.05)  # Cycle through 3 different heights
            ax1.text(start_day, y_pos, f'{label} ({start_date})', 
                    rotation=90, va='top', ha='right', alpha=0.7, color=color)

        # Add legend for quarantine levels
        quarantine_legend = [plt.Line2D([0], [0], color=color, linestyle='--', alpha=0.5, label=label)
                           for _, _, label, color in quarantine_vis]
        ax1.legend(handles=quarantine_legend, loc='upper right', title='Quarantine Levels')

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

# Define specific interventions with detailed properties
ecq_start = '2020-03-02'
ecq_end = '2020-05-15'
gcq_start = '2020-05-16'
gcq_end = '2020-05-31'
mgcq_start = '2020-06-01'
mgcq_end = '2021-01-31'
gcq2_start = '2021-02-01'
gcq2_end = '2021-10-31'
al3_start = '2021-11-01'
al3_end = '2021-12-05'
al2_start = '2021-12-06'
al2_end = '2022-01-09'
al3_2_start = '2022-01-10'
al3_2_end = '2022-02-16'
al2_2_start = '2022-02-17'
al2_2_end = '2022-03-01'
al1_start = '2022-03-02'
al1_end = '2023-07-31'

# Create ECQ intervention
ecq_intervention = cv.change_beta(
    days=[ecq_start, ecq_end],
    changes=[0.3, 1.0],  # Reduce transmission to 30% during ECQ, return to normal after
    layers=['h', 's', 'w', 'c']  # Apply to all layers
)

# Create GCQ intervention
gcq_intervention = cv.change_beta(
    days=[gcq_start, gcq_end],
    changes=[0.4, 1.0],  # Reduce transmission to 40% during GCQ, return to normal after
    layers=['h', 's', 'w', 'c']  # Apply to all layers
)

# Create MGCQ intervention
mgcq_intervention = cv.change_beta(
    days=[mgcq_start, mgcq_end],
    changes=[0.5, 1.0],  # Reduce transmission to 50% during MGCQ
    layers=['h', 's', 'w', 'c']
)

# Create second GCQ intervention with all parameters
class GCQ2Intervention(cv.Intervention):
    def __init__(self, start_day, end_day):
        super().__init__()
        self.start_day = start_day
        self.end_day = end_day

    def apply(self, sim):
        if sim.t == self.start_day:
            # Modify disease duration parameters for GCQ2 period
            sim['dur']['inf2rec'] = {'dist': 'normal', 'par1': 100.0, 'par2': 2.0}  # Increase infectious to recovery duration
            sim['dur']['asym2rec'] = {'dist': 'normal', 'par1': 100.0, 'par2': 2.0}  # Increase asymptomatic to recovery duration
            
        elif sim.t == self.end_day:
            # Restore original values
            sim['dur']['inf2rec'] = {'dist': 'normal', 'par1': 10.0, 'par2': 2.0}  # Original infectious to recovery duration
            sim['dur']['asym2rec'] = {'dist': 'normal', 'par1': 8.0, 'par2': 2.0}   # Original asymptomatic to recovery duration

# Create the GCQ2 interventions
gcq2_beta = cv.change_beta(
    days=[gcq2_start, gcq2_end],
    changes=[0.4, 1.0],  # Reduce transmission to 40% during GCQ2
    layers=['h', 's', 'w', 'c']
)

gcq2_disease = GCQ2Intervention(
    start_day=(pd.to_datetime(gcq2_start) - pd.to_datetime('2020-03-02')).days,
    end_day=(pd.to_datetime(gcq2_end) - pd.to_datetime('2020-03-02')).days
)

# Create AL3 intervention
al3_intervention = cv.change_beta(
    days=[al3_start, al3_end],
    changes=[0.6, 1.0],  # Alert Level 3 transmission reduction
    layers=['h', 's', 'w', 'c']
)

# Create AL2 intervention
al2_intervention = cv.change_beta(
    days=[al2_start, al2_end],
    changes=[0.7, 1.0],  # Alert Level 2 transmission reduction
    layers=['h', 's', 'w', 'c']
)

# Create second AL3 intervention
al3_2_intervention = cv.change_beta(
    days=[al3_2_start, al3_2_end],
    changes=[0.6, 1.0],  # Back to AL3 levels
    layers=['h', 's', 'w', 'c']
)

# Create second AL2 intervention
al2_2_intervention = cv.change_beta(
    days=[al2_2_start, al2_2_end],
    changes=[0.7, 1.0],  # Back to AL2 levels
    layers=['h', 's', 'w', 'c']
)

# Create AL1 intervention
al1_intervention = cv.change_beta(
    days=[al1_start, al1_end],
    changes=[0.8, 1.0],  # Most relaxed restrictions
    layers=['h', 's', 'w', 'c']
)

sim = cv.Sim(
        # Setters
        pop_size = 50000,  # Simulate with 50,000 people
        pop_type = 'hybrid',  # Need to specify this for contact layers
        location = 'Philippines',
        # pop_infected = 1,  # Start with 1 infected person
        start_day = '2020-03-02',
        end_day = '2023-07-31',

        # Contact parameters
        contacts = {'h': 3.0, 's': 20, 'w': 20, 'c': 20},  # Average contacts per layer
        beta_layer = {'h': 3.0, 's': 1.0, 'w': 0.6, 'c': 0.3},  # Base transmission rates per layer

        # Baguio-calibrated Parameters
        beta = 0.016,  # Increased from 0.01042 to allow for some spread
        rel_death_prob = 0.05180,

        interventions=[ecq_intervention, gcq_intervention, mgcq_intervention, 
                      gcq2_beta, gcq2_disease, al3_intervention, al2_intervention,
                      al3_2_intervention, al2_2_intervention, al1_intervention],  # Add all interventions
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
