import streamlit as st
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

# Set the page title
st.set_page_config(page_title="Interactive Plotly Dashboard", layout="wide")


# Heading
st.title("Interactive Plotly Dashboard")
st.write("This dashboard displays four different Plotly graphs for data visualization.")

# Subheading for Scatter Plot
st.subheader("1. Scatter Plot")
# Generate sample data for scatter plot
scatter_data = px.data.iris()
scatter_fig = px.scatter(scatter_data, x="sepal_width", y="sepal_length", color="species",
                          title="Scatter Plot of Sepal Dimensions")
st.plotly_chart(scatter_fig, use_container_width=True)

# Subheading for Line Chart
st.subheader("2. Line Chart")
# Generate sample data for line chart

# Dropdown menu for selecting line type
line_type = st.selectbox("Select Line Type", ["Solid", "Dashed", "Dotted"])
if line_type == "Solid":
    line_style = "solid"
elif line_type == "Dashed":
    line_style = "dash"
else:
    line_style = "dot"

# Radio button for selecting function 
funlist = ["sin", "cos"]
fun = st.radio("Select Function", funlist)
x = np.linspace(0, 10, 100)
if fun == "sin":
    y = np.sin(x)
else:
    y = np.cos(x)

line_fig = go.Figure()
line_fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sine Wave', line=dict(dash=line_style)))
line_fig.update_layout(title="Line Chart of Sine Wave", xaxis_title="X", yaxis_title="sin(X)")
st.plotly_chart(line_fig, use_container_width=True)

# Subheading for Bar Chart
st.subheader("3. Bar Chart")
# Generate sample data for bar chart
bar_data = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Values": [23, 45, 56, 78]
})

# Radio button for selecting bar color
bar_color = st.radio("Select Bar Color", ["Blue", "Green", "Red"])
if bar_color == "Blue":
    color = "blue"
elif bar_color == "Green":
    color = "green"
else:
    color = "red"

bar_fig = px.bar(bar_data, x="Category", y="Values", title="Bar Chart of Categories", color_discrete_sequence=[color])
# bar_fig.update_layout(xaxis_title="Category", yaxis_title="Values")
st.plotly_chart(bar_fig, use_container_width=True)

# Subheading for Pie Chart
st.subheader("4. Pie Chart")
# Generate sample data for pie chart
pie_data = pd.DataFrame({
    "Labels": ["Apple", "Banana", "Cherry", "Date"],
    "Values": [30, 20, 25, 25]
})

# Selectbox for selecting pie chart items
pie_items = st.multiselect("Select Pie Chart Items", ["Apple", "Banana", "Cherry", "Date"])
pie_data = pie_data[pie_data["Labels"].isin(pie_items)]

st.write("Selected Items: ", pie_items)

pie_fig = px.pie(pie_data, names="Labels", values="Values", title="Pie Chart of Fruits")
st.plotly_chart(pie_fig, use_container_width=True)