import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.title("Interactive Plotly Dashboard")

# Load dataset
df = pd.read_csv("TB_Burden_Country.csv")


##############             1. MAP               ####################
# Create a placeholder for the subheader
map_subheader_placeholder = st.empty()

# Sidebar to select region
selected_Region = st.selectbox("Select Region", ["EMR", "EUR", "AFR", "WPR", "AMR", "SEA"])

# Update the subheader dynamically after the region is selected
map_subheader_placeholder.subheader(f"1. Geo-Spatial Visualization for {selected_Region}")

# Filter the dataset for the selected region
filtered_data = df[df["Region"] == selected_Region]

# Select metric to visualize (Incidence, Mortality, or Detection Rate)
metric_options = [
    "Estimated incidence (all forms) per 100 000 population",
    "Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population",
    "Case detection rate (all forms), percent"
]
selected_metric = st.selectbox("Select Metric", metric_options)

# Create the scatter geo plot
geo_fig = px.scatter_geo(
    filtered_data,
    locations="ISO 3-character country/territory code",  # Use the 3-letter country code (ISO)
    color=selected_metric,  # Color by selected metric (Incidence, Mortality, or Detection Rate)
    hover_name="Country or territory name",  # Hover over country name
    size="Estimated total population number",  # Size by population
    projection="natural earth",  # Choose a map projection
    labels={"Estimated total population number": "Population"},
)

# Update layout for the map
geo_fig.update_layout(
    height=600, 
    width=800,
    coloraxis_colorbar_title=selected_metric  # Set color bar title to metric name
)

# Display the plot
st.plotly_chart(geo_fig)


##############             2. Bar               ####################


df_cleaned = df[["Region","Estimated prevalence of TB (all forms) per 100 000 population"]]
avg_tb_incidence = df_cleaned.groupby('Region')['Estimated prevalence of TB (all forms) per 100 000 population'].mean().reset_index()

# Sort by average TB incidence in descending order (highest first)
avg_tb_incidence_sorted = avg_tb_incidence.sort_values('Estimated prevalence of TB (all forms) per 100 000 population', ascending=False)

# Plot horizontal bar chart using Plotly
fig = px.bar(
    avg_tb_incidence_sorted,
    x='Estimated prevalence of TB (all forms) per 100 000 population',
    y='Region',
    orientation='h',  # Horizontal bar chart
    title='Average TB Incidence by Region',
    labels={'Estimated incidence (all forms) per 100 000 population': 'Average TB Incidence (per 100K)', 'Region': 'Region'}
)

st.subheader("2. Average TB Incidence by Region")
st.plotly_chart(fig)



##############             3. Line               ####################


df['Region'] = df['Region'].str.strip().str.title()
df['Country or territory name'] = df['Country or territory name'].str.strip().str.title()

# Handle missing values (you can decide what to do with missing values)
df_cleaned = df.dropna(subset=['Country or territory name', 'Estimated incidence (all forms) per 100 000 population', 'Year'])

# Create a placeholder for the subheader
subheader_placeholder = st.empty()

# Streamlit dropdown menu for selecting a country
country = st.selectbox(
    "Select a Country",
    options=df_cleaned['Country or territory name'].unique(),
    index=0  # Default to the first country in the list
)

# Update the subheader dynamically after the country is selected
subheader_placeholder.subheader(f"3. TB Incidence Trend for {country} Over Time")

# Filter the data for the selected country
country_data = df_cleaned[df_cleaned['Country or territory name'] == country]

# Plot the line graph showing the TB incidence for the selected country
fig = px.line(
    country_data,
    x='Year',
    y='Estimated incidence (all forms) per 100 000 population',
    title=f"TB Incidence Trend in {country}",
    labels={'Year': 'Year', 'Estimated incidence (all forms) per 100 000 population': 'TB Incidence (per 100K)'},
    line_shape='linear'  # Creates a smooth line for the trend
)

# Display the plot
st.plotly_chart(fig)


##############             4. Pie chart               ####################

# Create a placeholder for the subheader
pie_subheader_placeholder = st.empty()

# Handle missing values (you can decide what to do with missing values)
df['Region'] = df['Region'].str.strip().str.title()
df['Country or territory name'] = df['Country or territory name'].str.strip().str.title()
df_cleaned = df.dropna(subset=['Year', 'Estimated incidence (all forms) per 100 000 population', 
                               'Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population'])

# Filter the data for a specific country or overall (you can select a country here)
country = st.selectbox(
    "Select a Country",
    options=df_cleaned['Country or territory name'].unique(),
    index=0,  # Default to the first country
    key="country1_selectbox"
)

# Update the subheader dynamically after the country is selected
pie_subheader_placeholder.subheader(f"4. TB Incidence vs Mortality for {country} (Pie Chart)")

# Filter the data for the selected country
country_data = df_cleaned[df_cleaned['Country or territory name'] == country]

# Get the range of years available for the selected country
years = country_data['Year'].unique()
min_year = years.min()
max_year = years.max()

# Add a slider to choose the year
selected_year = st.slider(
    "Select a Year", 
    min_value=min_year, 
    max_value=max_year, 
    value=max_year  # Default to the most recent year
)

# Filter the data for the selected year
year_data = country_data[country_data['Year'] == selected_year]

# Sum of TB incidence and mortality for the selected year
total_incidence = year_data['Estimated incidence (all forms) per 100 000 population'].sum()
total_mortality = year_data['Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population'].sum()

# Prepare data for the pie chart
labels = ['TB Incidence', 'TB Mortality']
values = [total_incidence, total_mortality]

# Create a pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])

# Update layout for the pie chart
fig.update_layout(
    title=f"Proportion of TB Incidence vs Mortality in {country} for {selected_year}",
    template="plotly_white"
)

# Display the plot in Streamlit
st.plotly_chart(fig)



##############             5. Scatter plot               ####################

# Create a placeholder for the subheader
scatter_subheader_placeholder = st.empty()

df['Country or territory name'] = df['Country or territory name'].str.strip().str.title()

# Drop rows with missing year or metric values
df_cleaned = df.dropna(subset=[
    'Year',
    'Estimated incidence (all forms) per 100 000 population',
    'Estimated prevalence of TB (all forms) per 100 000 population',
    'Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population'
])

# Dropdown for country selection
selected_country = st.selectbox(
    "Select a Country",
    df_cleaned['Country or territory name'].unique(),
    key="country2_selectbox"
)

# Radio button for metric selection
metric_option = st.radio(
    "Select a TB Metric to Visualize",
    ["Incidence", "Prevalence", "Mortality"]
)

# Update the subheader dynamically after the country and metric are selected
scatter_subheader_placeholder.subheader(f"5. {metric_option} of TB in {selected_country}")

# Filter data for selected country
country_data = df_cleaned[df_cleaned['Country or territory name'] == selected_country]

# Map selection to column names
metric_columns = {
    "Incidence": "Estimated incidence (all forms) per 100 000 population",
    "Prevalence": "Estimated prevalence of TB (all forms) per 100 000 population",
    "Mortality": "Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population"
}

selected_column = metric_columns[metric_option]

# Create scatter plot
fig = px.scatter(
    country_data,
    x="Year",
    y=selected_column,
    title=f"{metric_option} of TB in {selected_country} Over Time",
    labels={selected_column: f"{metric_option} per 100K population"},
    trendline="ols"
)

# Display the plot
st.plotly_chart(fig)