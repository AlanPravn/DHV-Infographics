import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

def load_data(Education_data):
    """Load data from an Excel file."""
    return pd.read_excel(Education_data)

def filter_data(data, countries, indicators, years):
    """Filter data for specified countries, indicators, and years."""
    return data[(data["Country Name"].isin(countries)) & 
                (data["Indicator Name"].isin(indicators))][['Country Name', 'Indicator Name'] + years]

# Plot 1: Vertical Bar Chart
def plot_vertical_bar_chart(data, ax, title, years):
    """Plot a vertical bar chart for the given data."""
    width = 0.15  # Width of the bars
    num_countries = len(data['Country Name'].unique())
    country_offsets = {country: i * width for i, country in enumerate(data['Country Name'].unique())}

    for country in data['Country Name'].unique():
        country_data = data[data['Country Name'] == country]
        bar_positions = [x + country_offsets[country] for x in range(len(years))]
        ax.bar(bar_positions, country_data.iloc[0][years], width, label=f"{country}: {country_data.iloc[0][years[-1]]}")
    
    ax.set_xticks([r + width * (num_countries / 2) for r in range(len(years))])
    ax.set_xticklabels(years)
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Plot 2: Pie Chart
def plot_pie_chart(data, ax, year, title):
    """Plot a pie chart for a single year."""
    pie_data = data.groupby('Country Name')[year].mean(numeric_only=True)
    wedges, _ = ax.pie(pie_data, startangle=140, colors=sns.color_palette('bright'))
    ax.set_title(title)
    legend_labels = [f'{country}: {value:.2f}' for country, value in pie_data.items()]
    ax.legend(wedges, legend_labels, title="Country: Value", loc='upper left', bbox_to_anchor=(1, 1))

# Plot 3: Horizontal Bar Chart
def plot_horizontal_bar_chart(data, ax, title):
    """Plot a horizontal bar chart for the given data."""
    bar_data = data.groupby('Country Name').mean(numeric_only=True).mean(axis=1)
    bars = ax.barh(bar_data.index, bar_data.values, color=sns.color_palette('muted'))
    ax.set_title(title)
    ax.set_xlabel('Average Value')
    ax.set_ylabel('Country')
    legend_labels = [f'{country}: {value:.2f}' for country, value in bar_data.items()]
    ax.legend(bars, legend_labels, title="Country: Average", loc='upper left', bbox_to_anchor=(1, 1))

# Plot 4: Line Chart
def plot_line_chart(data, ax, title, years):
    """Plot a line chart for the given data."""
    for country in data['Country Name'].unique():
        country_data = data[data['Country Name'] == country]
        ax.plot(years, country_data.iloc[0][years], marker='o', label=f"{country}: {country_data.iloc[0][years[-1]]}")
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.set_ylabel('Value')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Main execution and plotting
file_path = "Education_data.xlsx"
countries = ["Europe & Central Asia", "Ghana", "Malaysia", "Azerbaijan", "Mexico"]
indicators = [
    "Trained teachers in primary education (% of total teachers)", 
    "Primary education, pupils", 
    "School enrollment, primary (% gross)", 
    "School enrollment, primary, female (% gross)"
]
years = [2000, 2001, 2002, 2003, 2004, 2005]

data = load_data(file_path)
filtered_data = filter_data(data, countries, indicators, years)

sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(20, 15))  # Increase the figure size
plot_vertical_bar_chart(filtered_data[filtered_data['Indicator Name'] == indicators[0]], axes[0, 0], indicators[0], years)
plot_pie_chart(filtered_data[filtered_data['Indicator Name'] == indicators[1]], axes[0, 1], 2005, indicators[1])
plot_horizontal_bar_chart(filtered_data[filtered_data['Indicator Name'] == indicators[2]], axes[1, 0], indicators[2])
plot_line_chart(filtered_data[filtered_data['Indicator Name'] == indicators[3]], axes[1, 1], indicators[3], years)


# Adjusting layout
plt.tight_layout()
plt.subplots_adjust(top=0.9)  # Adjust top spacing to accommodate the title

# Stylish box for Name and Student ID information
author_box = dict(boxstyle='round', facecolor='#7FC7D9', alpha=0.5, edgecolor='black')
fig.text(0.82, -0.04, "Name: Alan Praveen Putty Francis Xavier", ha="left", va="bottom", fontsize=14, color='black', bbox=author_box)
fig.text(0.82, -0.01, "Student ID: 22082221", ha="left", va="bottom", fontsize=14, color='black', bbox=author_box)

# Abstract text
abstract_text = ("Public health disparities surfaced (2015-2019) among Argentina, Brazil, Mexico, the Netherlands, and the United Kingdom. "
                 "Argentina saw a health indicator decline but grappled with 15.5% chronic disease mortality in 2019. Brazil faced a high youth mortality rate of 33.9%. "
                 "Contrastingly, the Netherlands and the United Kingdom showcased effective health management, reflected in lower youth mortality and declining chronic disease mortality.")
fig.text(0.5, -0.09, textwrap.fill(abstract_text, width=100), wrap=True, horizontalalignment='center', fontsize=18)

# Custom title
plt.suptitle("A Comparative Evaluation of Public Health Measures", fontsize=22, y=0.95, color='black', ha='center', backgroundcolor='#7FC7D9')

# Save the figure
plt.savefig("22082221.png", dpi=300, bbox_inches='tight', pad_inches=1.0)
