'''
Loading and plotting data
'''

import covasim as cv

pars = dict(
    start_day = '2020-02-01',
    end_day   = '2020-04-11',
    beta      = 0.015,
)
sim = cv.Sim(datafile='baguio_covid_data.csv')
sim.run()
sim.plot(to_plot=['cum_diagnoses'])