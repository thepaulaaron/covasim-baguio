import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define a function to plot a heatmap for each variant
def plot_contact_matrix(df, ax, title, vmin=None, vmax=None):
    # Set age group labels (5-year intervals from 0-4 to 75+)
    age_labels = [
        '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
        '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75+'
    ]
    
    # Set the columns and index to the age labels
    df.columns = age_labels
    df.index = age_labels

    # Transpose the matrix: contacting age group (originally rows) becomes x-axis (patterned to original Prem data)
    df = df.T  
    
    # Reverse the order of the rows to make sure the matrix starts from the lowest (y-axis)
    df = df[::-1]

    # Calculate the min and max values for the current data
    data_min = df.min().min()
    data_max = df.max().max()

      # # Print the min and max values for reference
      # print(f"{title} - Min: {data_min}, Max: {data_max}")

    # If no vmin and vmax are provided, calculate them from the data
    if vmin is None or vmax is None:
      vmin = data_min  # Use the minimum value for vmin
      vmax = data_max  # Use the maximum value for vmax

    # Manually tweak the vmin and vmax for more sensitive color gradients
    # Adjust the range to zoom in on specific data ranges if needed
    vmin = vmin  # Adjust this value for sensitivity
    vmax = vmax  # Adjust this value for sensitivity

    # Plot the heatmap with a white-to-blue color gradient
    sns.heatmap(df, annot=False, cmap="Blues", xticklabels=True, yticklabels=True, vmin=vmin, vmax=vmax, ax=ax)
    
    # Custom ticks for both axes (0, 5, 10, 15, ..., 75)
    custom_ticks_x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    custom_ticks_y = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
    
    # Set the title and labels for axes
    ax.set_title(title)
    ax.set_xlabel("Contacting Age Group")
    ax.set_ylabel("Contacted Age Group")
    
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

# Results:
# Contact Matrix - All - Min: 0.13937, Max: 9.44356
# Contact Matrix - Home - Min: 0.1288, Max: 0.91398
# Contact Matrix - Others - Min: 0.0045, Max: 4.77255
# Contact Matrix - School - Min: 0.0, Max: 5.14493
# Contact Matrix - Work - Min: 0.0, Max: 0.72452

# Manually define the vmin and vmax values based on the data characteristics or your preference

# # No adjustment of vmin and vmax
# vmin_all, vmin_all, vmin_home, vmax_all, vmax_home, vmin_others, vmax_others, vmin_school, vmax_school, vmin_work, vmax_work = None, None, None, None, None, None, None, None, None, None, None

# 10th percentile of the minimum values in the matrix
# 90th percentile of the maximum values in the matrix

vmin_all = df_all.quantile(0.10).min()
vmax_all = df_all.quantile(0.90).max() 

vmin_home = df_home.quantile(0.10).min() 
vmax_home = df_home.quantile(0.90).max() 

vmin_others = df_others.quantile(0.10).min()
vmax_others = df_others.quantile(0.90).max()

vmin_school = df_school.quantile(0.10).min()
vmax_school = df_school.quantile(0.90).max()

vmin_work = df_work.quantile(0.10).min()
vmax_work = df_work.quantile(0.90).max()

# Create a subplot to plot all variants in one page
fig, axs = plt.subplots(3, 2, figsize=(15, 12))

# Plot each matrix on the respective axis with manually adjusted vmin and vmax
plot_contact_matrix(df_all, axs[0, 0], "Contact Matrix - All", vmin_all, vmax_all)
plot_contact_matrix(df_home, axs[0, 1], "Contact Matrix - Home", vmin_home, vmax_home)
plot_contact_matrix(df_others, axs[1, 0], "Contact Matrix - Others", vmin_others, vmax_others)
plot_contact_matrix(df_school, axs[1, 1], "Contact Matrix - School", vmin_school, vmax_school)
plot_contact_matrix(df_work, axs[2, 0], "Contact Matrix - Work", vmin_work, vmax_work)

# Remove the empty subplot
fig.delaxes(axs[2, 1])

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
