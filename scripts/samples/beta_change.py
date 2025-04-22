import covasim as cv
cv.options(jupyter=True, verbose=0) # -> avoid the need for if __name__ == '__main__':

# Define baseline parameters and sim
pars = dict(
    start_day = '2020-03-01',
    end_day   = '2020-06-01',
    pop_type  = 'hybrid',
)

orig_sim = cv.Sim(pars, label='Baseline')

# Define sim with change_beta
schoolClosure = cv.change_beta(days=['2020-04-15', '2020-05-01', '2020-05-15'], changes=[0.2, 1.5, 0.7])

sim = cv.Sim(pars, interventions=schoolClosure, label='With beta changes')

# Run and plot
msim = cv.parallel(orig_sim, sim)
msim.plot()