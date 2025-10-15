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


import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configuration and Global Variables ---

# Set the page layout to wide for better visualization display
st.set_page_config(layout="wide")

# Define the URL for the dataset
URL = 'https://raw.githubusercontent.com/intannajwa20/EC2024/refs/heads/main/law_faculty_data.csv'

# Define column keys mapping to actual DataFrame column names.
# NOTE: These column names MUST exactly match the headers in your CSV file.
COLUMNS = {
    # Existing Columns from previous request
    'GENDER': 'Gender',
    'RANK': 'Faculty_Rank',
    'DEPARTMENT': 'Department',
    'EXPERIENCE': 'Years_of_Service',
    
    # New Columns from user request
    'ACADEMIC_YEAR': 'Bachelor  Academic Year in EU',
    'SSC_GPA': 'S.S.C (GPA)',
    'HSC_GPA': 'H.S.C (GPA)',
    'COACHING': 'Did you ever attend a Coaching center?',
    'HSC_MEDIUM': 'H.S.C or Equivalent study medium',
    'EXPECTATION_RESOURCE': 'Q3 [What was your expectation about the University as related to quality of resources?]',
    'EXPECTATION_ENVIRONMENT': 'Q4 [What was your expectation about the University as related to quality of learning environment?]',
    'EXPECTATION_MET': 'Q5 [To what extent your expectation was met?]',
    'BEST_ASPECTS': 'Q6 [What are the best aspects of the program?]'
}


# --- Data Loading Function ---

@st.cache_data
def load_data(data_url):
    """Loads and caches the DataFrame from a URL with basic cleaning."""
    st.info(f"Attempting to load data from: {data_url}")
    try:
        df = pd.read_csv(data_url, encoding='latin1')
        st.success("Data loaded successfully!")
        
        # Data Cleaning/Preparation for visualizations
        for col_name in COLUMNS.values():
            if col_name in df.columns:
                # Handle leading/trailing spaces in string columns
                if df[col_name].dtype == 'object':
                    df[col_name] = df[col_name].str.strip().replace('', np.nan).fillna('Unknown/Missing')

        # Convert GPA/Experience to numeric, coercing errors to NaN
        for key in ['SSC_GPA', 'HSC_GPA', 'EXPERIENCE']:
            if COLUMNS[key] in df.columns:
                df[COLUMNS[key]] = pd.to_numeric(df[COLUMNS[key]], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error loading data. Please check the URL and file format. Error: {e}")
        return pd.DataFrame()


# --- Visualization Functions (Plotly Express) ---

def plot_gender_distribution(df):
    """Visualization 1: Pie Chart of Gender Distribution."""
    gender_col = COLUMNS['GENDER']
    if gender_col not in df.columns: return st.warning(f"Column '{gender_col}' not found.")
    
    gender_counts = df[gender_col].value_counts().reset_index(name='Count')
    gender_counts.columns = ['Gender', 'Count']

    fig = px.pie(
        gender_counts, values='Count', names='Gender',
        title='1. Distribution of Faculty Gender',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_rank_distribution(df):
    """Visualization 2: Bar Chart of Faculty Rank Counts."""
    rank_col = COLUMNS['RANK']
    if rank_col not in df.columns: return st.warning(f"Column '{rank_col}' not found.")

    rank_counts = df[rank_col].value_counts().reset_index(name='Count')

    fig = px.bar(
        rank_counts, x=rank_counts.columns[0], y='Count',
        title='2. Count of Faculty by Academic Rank',
        color='Count',
        color_continuous_scale=px.colors.sequential.Teal,
        labels={rank_counts.columns[0]: "Academic Rank"}
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_academic_year_distribution(df):
    """New Visualization 3: Bar Chart of Academic Year Distribution."""
    year_col = COLUMNS['ACADEMIC_YEAR']
    if year_col not in df.columns: return st.warning(f"Column '{year_col}' not found.")
    
    # Value counts and sort index (like original pandas plot)
    year_counts = df[year_col].value_counts().sort_index().reset_index(name='Number of Students')
    year_counts.columns = ['Academic Year', 'Number of Students']

    fig = px.bar(
        year_counts,
        x='Academic Year',
        y='Number of Students',
        title='3. Distribution of Academic Years',
        color='Number of Students',
        color_continuous_scale=px.colors.sequential.Blues,
        text='Number of Students' # Display count on bars
    )
    fig.update_layout(xaxis={'categoryorder':'category ascending'})
    st.plotly_chart(fig, use_container_width=True)


def plot_gpa_histograms(df):
    """New Visualization 4: Dual Histograms of SSC and HSC GPA."""
    ssc_col = COLUMNS['SSC_GPA']
    hsc_col = COLUMNS['HSC_GPA']
    
    if ssc_col not in df.columns or hsc_col not in df.columns: 
        return st.warning(f"Columns '{ssc_col}' or '{hsc_col}' not found for GPA plots.")
    
    # Plotly figures are created separately, then combined into a container
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("4a. S.S.C (GPA) Distribution")
        fig_ssc = px.histogram(
            df.dropna(subset=[ssc_col]), x=ssc_col,
            title='S.S.C (GPA)',
            marginal="box",
            color_discrete_sequence=['lightgreen']
        )
        fig_ssc.update_layout(xaxis_title="S.S.C (GPA)", yaxis_title="Frequency")
        st.plotly_chart(fig_ssc, use_container_width=True)

    with col2:
        st.subheader("4b. H.S.C (GPA) Distribution")
        fig_hsc = px.histogram(
            df.dropna(subset=[hsc_col]), x=hsc_col,
            title='H.S.C (GPA)',
            marginal="box",
            color_discrete_sequence=['salmon']
        )
        fig_hsc.update_layout(xaxis_title="H.S.C (GPA)", yaxis_title="Frequency")
        st.plotly_chart(fig_hsc, use_container_width=True)


def plot_coaching_attendance(df):
    """New Visualization 5: Pie Chart of Coaching Center Attendance."""
    coaching_col = COLUMNS['COACHING']
    if coaching_col not in df.columns: return st.warning(f"Column '{coaching_col}' not found.")
    
    coaching_counts = df[coaching_col].value_counts().reset_index(name='Count')
    coaching_counts.columns = ['Attended Coaching Center', 'Count']

    fig = px.pie(
        coaching_counts, values='Count', names='Attended Coaching Center',
        title='5. Distribution of Coaching Center Attendance',
        color_discrete_sequence=['gold', 'lightskyblue']
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_hsc_medium(df):
    """New Visualization 6: Bar Chart of H.S.C Study Mediums."""
    medium_col = COLUMNS['HSC_MEDIUM']
    if medium_col not in df.columns: return st.warning(f"Column '{medium_col}' not found.")
    
    medium_counts = df[medium_col].value_counts().reset_index(name='Number of Students')

    fig = px.bar(
        medium_counts,
        x=medium_counts.columns[0], y='Number of Students',
        title='6. Distribution of H.S.C Study Mediums',
        color='Number of Students',
        color_continuous_scale=px.colors.sequential.Teal,
        labels={medium_counts.columns[0]: "H.S.C Study Medium"}
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_expectation_ratings(df):
    """New Visualization 7: Bar Charts for Expectation Ratings."""
    exp_cols = [
        COLUMNS['EXPECTATION_RESOURCE'],
        COLUMNS['EXPECTATION_ENVIRONMENT'],
        COLUMNS['EXPECTATION_MET'],
        COLUMNS['BEST_ASPECTS'] # Note: This last one is descriptive, not a rating
    ]

    st.subheader("7. University Expectation and Satisfaction Ratings")
    
    # Create a 2x2 grid for the four plots
    cols = st.columns(2)

    for i, col in enumerate(exp_cols):
        if col not in df.columns:
            cols[i % 2].warning(f"Column '{col}' not found for expectation plot.")
            continue
            
        # Get counts and ensure categories are treated as strings for sorting
        counts = df[col].astype(str).value_counts().sort_index().reset_index(name='Frequency')

        # Use the column title without the question part for a cleaner plot
        clean_title = col.split('[')[1].replace(']', '') if '[' in col else col
        
        fig = px.bar(
            counts, 
            x=counts.columns[0], y='Frequency', 
            title=clean_title, 
            color_discrete_sequence=['lightblue']
        )
        fig.update_layout(xaxis_title='Response/Rating', yaxis_title='Frequency')
        cols[i % 2].plotly_chart(fig, use_container_width=True)


# --- Main Streamlit App Logic ---

def main():
    st.title("🏛️ Law Faculty Data Analysis Dashboard")
    st.markdown("---")

    # Load data using the globally defined URL
    law_df = load_data(URL)

    if law_df.empty:
        st.stop() # Stop the script if data loading failed

    # Display Data Head
    st.subheader("📊 Data Preview")
    st.dataframe(law_df.head(5))
    st.markdown("---")

    st.header("📈 Key Faculty Visualizations")

    # Grouping related visualizations
    
    st.subheader("Faculty Demographics and Experience")
    col1, col2 = st.columns(2)
    with col1:
        plot_gender_distribution(law_df)
    with col2:
        plot_rank_distribution(law_df)
    
    st.markdown("---")
    
    st.subheader("Academic Background")
    plot_academic_year_distribution(law_df)
    
    plot_gpa_histograms(law_df) # This function creates its own 2-column layout
    
    col3, col4 = st.columns(2)
    with col3:
        plot_coaching_attendance(law_df)
    with col4:
        plot_hsc_medium(law_df)

    st.markdown("---")
    
    # Expectation/Survey data is grouped
    plot_expectation_ratings(law_df)


if __name__ == "__main__":
    main()

