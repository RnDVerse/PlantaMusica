import streamlit as st
import pandas as pd
import altair as alt
from sklearn.metrics import r2_score
import numpy as np
import os
from io import StringIO

st.set_page_config(page_title="Correlation and Plotting", page_icon="📈")

st.markdown("# Correlation and Plotting")
st.sidebar.header("Analysis Settings")

# Define the relative path to the file
data_file_path = os.path.join('data', 'day_full_df.csv')

if not os.path.exists(data_file_path):
    st.error("File not found. Please check the file path.")
    st.stop()

# Upload .csv file or use default
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Optionally set the column names if required
    df.columns = ['Day', 'Air Temp Low (°C)', 'Air Temp Mean (°C)', 'Air Temp High (°C)', 'Air Humid Low (%)',
                  'Air Humid Mean (%)', 'Air Humid High (%)', 'Water Temp Low (°C)', 'Water Temp Mean (°C)',
                  'Water Temp High (°C)', 'Water Humid Low (°C)', 'Water Humid Mean (°C)',
                  'Water Humid High (%)', 'Canopy Coverage (cm²)', 'Water Consumption (mL)', 'Seed Count']
else:
    df = pd.read_csv(data_file_path)
    # Convert columns to numeric and handle NaNs
    # df['Air Temp Mean (°C)'] = pd.to_numeric(df['Air Temp Mean (°C)'], errors='coerce')
    # df['Canopy Coverage (cm²)'] = pd.to_numeric(df['Canopy Coverage (cm²)'], errors='coerce')
    # df.dropna(inplace=True)



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


# Dynamic column selection setup
default_x_column = 0
default_y_column = 1
if 'Air Temp Mean (°C)' in df.columns and 'Canopy Coverage (cm²)' in df.columns:
    default_x_column = df.columns.get_loc('Air Temp Mean (°C)')
    default_y_column = df.columns.get_loc('Canopy Coverage (cm²)')

x_column = st.sidebar.selectbox('Select X axis column:', df.columns, index=default_x_column)
y_column = st.sidebar.selectbox('Select Y axis column:', df.columns, index=default_y_column)


# Sidebar configuration for polynomial degree
degree = st.sidebar.slider('Select the polynomial degree:', 1, 10, 3)

# Perform polynomial fitting
try:
    coefficients = np.polyfit(df[x_column], df[y_column], degree)
    polynomial = np.poly1d(coefficients)
except Exception as e:
    st.error(f"Failed to fit polynomial: {str(e)}")
    st.stop()

# Generate x values for plotting the fit curve
min_x = df[x_column].min()
max_x = df[x_column].max()
x_fit = np.linspace(min_x, max_x, 100)
y_fit = polynomial(x_fit)

# Prepare data for plotting
plot_df = pd.DataFrame({
    'X': df[x_column],
    'Y': df[y_column],
    'Fit': polynomial(df[x_column])
})

# Adjust domain dynamically based on the data
x_min, x_max = plot_df['X'].min(), plot_df['X'].max()
y_min, y_max = plot_df['Y'].min(), plot_df['Y'].max()

# Apply this new domain to the chart
points = alt.Chart(plot_df).mark_point(color='green', opacity=0.5, size=100).encode(
    x=alt.X('X:Q', title=x_column, scale=alt.Scale(domain=[x_min, x_max])),
    y=alt.Y('Y:Q', title=y_column, scale=alt.Scale(domain=[y_min, y_max])),
    tooltip=[alt.Tooltip('X:Q'), alt.Tooltip('Y:Q')]
)

fit_line = alt.Chart(plot_df).mark_line(color='blue', size=3).encode(
    x='X:Q',
    y='Fit:Q'
)



# Combine charts
chart = points + fit_line
st.altair_chart(chart, use_container_width=True)

# Calculate the R-squared value
r_squared = r2_score(df[y_column], polynomial(df[x_column]))
st.write(f"Polynomial equation: {polynomial}")
st.write(f"$R^2$: {r_squared:.3f}")

# # For Debug
# st.write(df[x_column][:3])
# st.write(df[y_column][:3])

# # Print or visualize the DataFrame to ensure it's structured and populated as expected
# st.write("Plot DataFrame head:", plot_df.head())
# st.write("Plot DataFrame description:", plot_df.describe())  # Gives statistical summary which can hint at issues





# Button to rerun the app (triggers a rerun of the script)
if st.button("Re-run"):
    st.experimental_rerun()