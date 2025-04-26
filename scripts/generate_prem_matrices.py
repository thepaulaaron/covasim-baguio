import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define a function to plot a heatmap for each variant
def plot_contact_matrix(df, ax, title):
    # Set age group labels (5-year intervals from 0-4 to 75+)
    age_labels = [
        '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
        '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+'
    ]
    
    # Set the columns and index to the age labels
    df.columns = age_labels
    df.index = age_labels
    
    # Reverse the order of the rows to make sure the matrix starts from the lowest (y-axis)
    df = df[::-1]

    # Plot the heatmap with a white-to-blue color gradient
    sns.heatmap(df, annot=False, cmap="Blues", xticklabels=True, yticklabels=True, ax=ax)
    
    # Custom ticks for both axes (0, 5, 10, 15, ..., 75)
    custom_ticks_x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    custom_ticks_y = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    
    # Set the title and labels for axes
    ax.set_title(title)
    ax.set_xlabel("Contacted Age Group")
    ax.set_ylabel("Contacting Age Group")
    
    # Set the ticks for x and y axes
    ax.set_xticks(range(len(age_labels)))  # Set the position of the ticks (indexes)
    ax.set_xticklabels(custom_ticks_x)  # Set the labels for x-axis as custom ticks

    ax.set_yticks(range(1, len(age_labels)))  # Set the position of the ticks (indexes) for y-axis, excluding 0
    ax.set_yticklabels(custom_ticks_y[::-1])  # Reverse only the labels for y-axis (no data reversal)
    
    # Rotate tick labels for better visibility
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)

# Read the CSV files for each variant
df_all = pd.read_csv("data/from_prem_et_al/contact_all_PHL.csv", header=None)
df_home = pd.read_csv("data/from_prem_et_al/contact_home_PHL.csv", header=None)
df_others = pd.read_csv("data/from_prem_et_al/contact_others_PHL.csv", header=None)
df_school = pd.read_csv("data/from_prem_et_al/contact_school_PHL.csv", header=None)
df_work = pd.read_csv("data/from_prem_et_al/contact_work_PHL.csv", header=None)

# Create a subplot to plot all variants in one page
fig, axs = plt.subplots(3, 2, figsize=(15, 12))

# Plot each matrix on the respective axis
plot_contact_matrix(df_all, axs[0, 0], "Contact Matrix - All")
plot_contact_matrix(df_home, axs[0, 1], "Contact Matrix - Home")
plot_contact_matrix(df_others, axs[1, 0], "Contact Matrix - Others")
plot_contact_matrix(df_school, axs[1, 1], "Contact Matrix - School")
plot_contact_matrix(df_work, axs[2, 0], "Contact Matrix - Work")

# Remove the empty subplot
fig.delaxes(axs[2, 1])

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
