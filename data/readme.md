This folder stores the raw, mock, or official data needed to run the simulations.

# Data from Prem et al.
### Reproducing the Contact Matrices

Clone their updated repository for the contact matrices: https://github.com/kieshaprem/synthetic-contact-matrices

Install RStudio, then run the following:

```R
# Load the full dataset
load("C:/.../synthetic-contact-matrices-2.0/output/syntheticmatrices/contact_<variant>.rdata")
```

`<variant>` - all, home, others, school, work

```R
# Access the Philippine data
phl_data <- contact_<variant>[["PHL"]]

# Convert the extracted matrix to a data frame,
# as matrices do not directly support writing to
# CSV without row and column names.

df <- as.data.frame(phl_data)


# Remove column names to export without them
colnames(df) <- NULL

# Write the data to a CSV file without row and column names
write.csv(df, "contact_<variant>_PHL.csv", row.names = FALSE, quote = FALSE)

```