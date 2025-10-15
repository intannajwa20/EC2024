import streamlit as st
import pandas as pd
import plotly.express as px

# Define the URL for the dataset
url = 'https://raw.githubusercontent.com/intannajwa20/EC2024/refs/heads/main/law_faculty_data.csv'

# Set up the Streamlit application
st.title("Law Faculty Gender Distribution Analysis")

# --- Data Loading and Display ---

# Load the data from the URL (use st.cache_data for better performance)
@st.cache_data
def load_data(data_url):
    """Loads and caches the DataFrame from a URL."""
    try:
        # Assuming the CSV reading was successful with the previous encoding
        df = pd.read_csv(data_url, encoding='latin1')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on failure

law_df = load_data(url)

# Check if the DataFrame is loaded and not empty
if not law_df.empty:
    # Display the head of the DataFrame as requested in the original code
    st.subheader("Data Preview (First 5 Rows)")
    st.dataframe(law_df.head())

    # --- Plotly Visualization ---

    # Check if the 'Gender' column exists to avoid errors
    if 'Gender' in law_df.columns:
        st.subheader("Distribution of Gender in Law Faculty")

        # 1. Get the counts of each gender (similar to the original logic)
        gender_counts = law_df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']

        # 2. Create the Plotly Pie Chart
        # Plotly Express is generally the simplest way to create standard plots
        fig = px.pie(
            gender_counts,
            values='Count',
            names='Gender',
            title='Distribution of Gender in Law Faculty',
            # Customizing the color sequence (optional)
            color_discrete_sequence=px.colors.qualitative.Pastel 
        )

        # 3. Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("The DataFrame does not contain a 'Gender' column.")

else:
    st.info("Could not load the Law Faculty data. Please check the URL and file format.")

