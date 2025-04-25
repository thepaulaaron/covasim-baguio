This folder contains the scripts to run simulations for the project.

##### File: `populate_baguio.py`
###### [20250425-142220] Version
Initializes a Baguio population based on a scaled population from the national PH data (official from [PSA, 2020](https://psa.gov.ph/statistics/population-and-housing/stat-tables)).
- Uses household population instead of total population
- Uses localized Baguio age-sex data, instead of national for more accurate representation
- Uses Covasim's `hybrid` pop_type as a better approximation (no `synthpops` available for location:Philippines)
- TODO:
  - [ ] optimize the age groups for varying different interactions
    - e.g., more household interactions for children, higher school and workplace interactions for young adults, and more household/community interactions for older adults
    - adjust Covasim's parameters such as transmission (beta), severity (severe_prob), and mortality rates (death_prob) for different age group
  - [ ] assess the sex aspect