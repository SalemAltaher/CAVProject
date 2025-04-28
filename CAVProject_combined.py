import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# https://cavproject-53pkhuxf8phqrbdpm9mzuv.streamlit.app/
# This is the link for visiting the page online

@st.cache_data
def load_data():
    return pd.read_csv("TB_Burden_Country.csv")

df = load_data()




# Filters
st.sidebar.title("Filters")

# Region
regions = st.sidebar.multiselect("Select Region(s):", df["Region"].dropna().unique(), default=df["Region"].dropna().unique())

# Year
years = st.sidebar.slider("Select Year Range:", int(df["Year"].min()), int(df["Year"].max()), (1990, 2013))

# Country
countries = st.sidebar.multiselect(
    "Select Country(s):",
    df["Country or territory name"].dropna().unique()
)

filtered = df[df["Region"].isin(regions) & df["Year"].between(years[0], years[1])]
if countries:
    filtered = filtered[filtered["Country or territory name"].isin(countries)]





st.title("Tuberculosis Global Visualization Dashboard")


st.caption("EMR: Middle East")
st.caption("EUR: Europe")
st.caption("AFR: Africa")
st.caption("WPR: East Asia")
st.caption("AMR: South/North America")
st.caption("SEA: South Asia")

st.markdown("---")

# 1
st.subheader("1. TB Prevalence Over Time")
metric = st.selectbox("Select Metric to Track Over Time:", [
    "Estimated number of incident cases (all forms)",
    "Estimated prevalence of TB (all forms) per 100 000 population"
])
line_fig = px.line(
    filtered,
    x="Year",
    y=metric,
    color="Country or territory name",
    title=f"{metric} Over Time"
)
st.plotly_chart(line_fig, use_container_width=True)

st.markdown("---")

# 2
st.subheader("2. TB Deaths by Region")
if len(regions) >= 2:

    bar_data = filtered.groupby("Region")["Estimated number of deaths from TB (all forms, excluding HIV)"].sum().reset_index()

    bar_fig = px.bar(
        bar_data,
        x="Region",
        y="Estimated number of deaths from TB (all forms, excluding HIV)",
        color="Region",
        title="Total TB Deaths by Region"
    )
    st.plotly_chart(bar_fig, use_container_width=True)
else:
    st.info("Please select two or more regions from the sidebar to view this chart.")


st.markdown("---")

# 3
st.subheader("3. TB-HIV Co-Infection by Region")
pie_data = filtered.groupby("Region")["Estimated incidence of TB cases who are HIV-positive"].sum().reset_index()
pie_fig = px.pie(pie_data, names="Region", values="Estimated incidence of TB cases who are HIV-positive",
                 title="TB-HIV Co-Infection Share by Region", hole=0.4)
pie_fig.update_traces(textinfo="percent+label")
st.plotly_chart(pie_fig, use_container_width=True)

st.markdown("---")

# 4
st.subheader("4. Population vs TB Incidence")

scatter_data = filtered.dropna(subset=["Estimated incidence of TB cases who are HIV-positive"])

scatter_fig = px.scatter(
    scatter_data,
    x="Estimated total population number",
    y="Estimated number of incident cases (all forms)",
    color="Country or territory name",
    size="Estimated incidence of TB cases who are HIV-positive",
    title="Population vs TB Incidence"
)
st.plotly_chart(scatter_fig, use_container_width=True)

st.markdown("---")

# 5
st.subheader("5. Case Detection Rate Map")

color_options = st.radio("Select Chart Color Theme", ["Viridis", "Cividis", "Blues", "Reds"])
color_scale = "Viridis" if color_options == "Viridis" else color_options.lower()

map_fig = px.choropleth(
    filtered,
    locations="Country or territory name",
    locationmode="country names",
    color="Case detection rate (all forms), percent",
    hover_name="Country or territory name",
    color_continuous_scale=color_scale,
    title="Case Detection Rate (%) by Country"
)
map_fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(map_fig, use_container_width=True)

st.markdown("---")


# 7
st.subheader("6. TB Incidence vs Mortality for Selected Country")

if countries:
    for country_pie in countries:
        country_data_pie = df[(df["Country or territory name"] == country_pie) & (df["Year"].between(years[0], years[1]))]

        total_incidence = country_data_pie['Estimated incidence (all forms) per 100 000 population'].sum()
        total_mortality = country_data_pie['Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population'].sum()

        labels = ['TB Incidence', 'TB Mortality']
        values = [total_incidence, total_mortality]

        pie_country_fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        pie_country_fig.update_layout(title=f"TB Incidence vs Mortality in {country_pie} ({years[0]}–{years[1]})", template="plotly_white")
        st.plotly_chart(pie_country_fig, use_container_width=True)
else:
    st.info("Please select at least one country from the sidebar to view the pie chart.")

st.markdown("---")

# 8
st.subheader("7. TB Metric Trend Over Time for a Country")

# Ensure at least one country is selected from the sidebar
if countries:
    # Use the first selected country from the sidebar filter
    selected_country_trend = countries[0]

    # Radio button for metric selection
    metric_option_trend = st.radio("Select Metric to Trend", ["Incidence", "Prevalence", "Mortality"])

    # Map metric options to column names
    metric_columns = {
        "Incidence": "Estimated incidence (all forms) per 100 000 population",
        "Prevalence": "Estimated prevalence of TB (all forms) per 100 000 population",
        "Mortality": "Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population"
    }
    selected_metric_trend = metric_columns[metric_option_trend]

    # Filter data for the selected country
    country_trend_data = df[df["Country or territory name"] == selected_country_trend]

    # Create scatter plot
    scatter_trend_fig = px.scatter(
        country_trend_data,
        x="Year",
        y=selected_metric_trend,
        title=f"{metric_option_trend} of TB in {selected_country_trend} Over Time",
        trendline="ols",
        labels={selected_metric_trend: f"{metric_option_trend} per 100K"}
    )

    # Display the plot
    st.plotly_chart(scatter_trend_fig, use_container_width=True)
else:
    st.info("Please select at least one country from the sidebar to view the trend.")

st.markdown("---")

# 9


# 10
st.subheader("8. TB Mortality-HIV positive over time")

if countries:
    country_trend_data = df[df["Country or territory name"].isin(countries) & df["Year"].between(years[0], years[1])]

    for country in countries:
        country_data = country_trend_data[country_trend_data["Country or territory name"] == country]

        if not country_data.empty:
            line_trend_fig = px.line(
                country_data.melt(
                    id_vars="Year", 
                    value_vars=[
                        "Estimated mortality of TB cases who are HIV-positive, per 100 000 population",
                        "Estimated mortality of TB cases who are HIV-positive, per 100 000 population, low bound",
                        "Estimated mortality of TB cases who are HIV-positive, per 100 000 population, high bound"
                    ]
                ),
                x="Year",
                y="value",
                color="variable",  # color by metric
                labels={"value": "Rate per 100K", "variable": "TB Metric"},
                title=f"TB Metrics Trend in {country} Over Time"
            )

            st.plotly_chart(line_trend_fig, use_container_width=True)

else:
    st.info("Please select at least one country from the sidebar to view the trend.")

st.markdown("---")
st.subheader("9. Sunburst")
sunburst_data = filtered.dropna(subset=["Estimated number of incident cases (all forms)"])

sunburst_fig = px.sunburst(
    sunburst_data,
    path=["Region", "Country or territory name"],
    values="Estimated number of incident cases (all forms)",
    color="Region",
    title="Sunburst: TB Incidence by Region and Country"
)

st.plotly_chart(sunburst_fig, use_container_width=True)

st.markdown("---")


# 10
st.subheader("10. Average TB Prevalence by Region")
avg_tb_incidence = df.groupby('Region')['Estimated prevalence of TB (all forms) per 100 000 population'].mean().reset_index()
avg_tb_incidence_sorted = avg_tb_incidence.sort_values('Estimated prevalence of TB (all forms) per 100 000 population', ascending=False)

bar_fig2 = px.bar(
    avg_tb_incidence_sorted,
    x='Estimated prevalence of TB (all forms) per 100 000 population',
    y='Region',
    orientation='h',
    title='Average TB Prevalence by Region'
)
st.plotly_chart(bar_fig2, use_container_width=True)

st.markdown("---")
st.caption("Done by")
st.caption("- Omar Al-Marzouqi")
st.caption("- Abdulla Al-Marzouqi")
st.caption("- Mohammed Al-Shamsi")
st.caption("- Salem Al-Taher")
