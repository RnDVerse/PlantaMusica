import altair as alt
import pandas as pd
import streamlit as st
import os 
from io import StringIO

st.set_page_config(page_title="Extract Environment Condition", page_icon="🌍")
st.markdown("# Environment Condition")
st.sidebar.header("Environment Related Data")
st.write(
    """Upload or insert your environment data and inspect the relationship here. Choose the X and Y axis from the sidebar.  """
)

# Define the relative path to the file
data_file_path = os.path.join('data', 'day_full_df.csv')

# Option to upload .csv file or use default
uploaded_file = st.sidebar.file_uploader("Upload your CSV file containing environment data", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv(data_file_path)

# Option for manual data entry
st.sidebar.header("Or enter data manually:")
data_string = st.sidebar.text_area("Enter CSV data (expand the space as needed for visibility):", "Property_1,Property_2\n20,10\n25,15")
if st.sidebar.button('Load Data & Plot'):
    
    data_io = StringIO(data_string)
    df = pd.read_csv(data_io)
    
# Convert DataFrame to CSV string for download
csv = df.to_csv(index=False)
st.sidebar.download_button(
   label="Download CSV",
   data=csv,
   file_name='environment_data.csv',
   mime='text/csv')

# Sidebar configuration for selecting columns
default_x_column = df.columns.get_loc('Air Temp Mean (°C)') if 'Air Temp Mean (°C)' in df.columns else 0
default_y_column = df.columns.get_loc('Water Temp Mean (°C)') if 'Water Temp Mean (°C)' in df.columns else 0

x_column = st.sidebar.selectbox('Select X axis column:', df.columns, index=default_x_column)
y_column = st.sidebar.selectbox('Select Y axis column:', df.columns, index=default_y_column)

# Prepare data for plotting
plot_df = pd.DataFrame({
    'X': df[x_column],
    'Y': df[y_column]
})

# Adjust domain dynamically based on the data
x_min, x_max = plot_df['X'].min(), plot_df['X'].max()
y_min, y_max = plot_df['Y'].min(), plot_df['Y'].max()

# Create the chart
points = alt.Chart(plot_df).mark_point(color='orange', opacity=0.5, size=100).encode(
    x=alt.X('X:Q', title=x_column, scale=alt.Scale(domain=[x_min, x_max])),
    y=alt.Y('Y:Q', title=y_column, scale=alt.Scale(domain=[y_min, y_max])),
    tooltip=[alt.Tooltip('X:Q'), alt.Tooltip('Y:Q')]
)

st.altair_chart(points, use_container_width=True)
