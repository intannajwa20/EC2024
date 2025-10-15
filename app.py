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

# --- Visualization Functions (Plotly Express) ---

def plot_gender_distribution(df):
    """Visualization 1: Pie Chart of Gender Distribution."""
    if COLUMNS['GENDER'] not in df.columns: return
    
    gender_counts = df[COLUMNS['GENDER']].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    fig = px.pie(
        gender_counts,
        values='Count',
        names='Gender',
        title='1. Distribution of Faculty Gender',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)


def plot_rank_distribution(df):
    """Visualization 2: Bar Chart of Faculty Rank Counts."""
    if COLUMNS['RANK'] not in df.columns: return

    rank_counts = df[COLUMNS['RANK']].value_counts().reset_index()
    rank_counts.columns = ['Rank', 'Count']
    rank_counts = rank_counts.sort_values('Count', ascending=False) # Sort by count

    fig = px.bar(
        rank_counts,
        x='Rank',
        y='Count',
        title='2. Count of Faculty by Academic Rank',
        color='Rank',
        color_discrete_sequence=px.colors.qualitative.D3
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_gender_vs_rank(df):
    """Visualization 3: Grouped Bar Chart of Rank by Gender."""
    if COLUMNS['RANK'] not in df.columns or COLUMNS['GENDER'] not in df.columns: return

    # Count occurrences of Rank segmented by Gender
    df_counts = df.groupby([COLUMNS['RANK'], COLUMNS['GENDER']]).size().reset_index(name='Count')
    df_counts.columns = ['Rank', 'Gender', 'Count']

    fig = px.bar(
        df_counts,
        x='Rank',
        y='Count',
        color='Gender',
        barmode='group',
        title='3. Faculty Rank Distribution, Grouped by Gender',
        color_discrete_sequence=['lightcoral', 'skyblue'] # Custom colors
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_experience_histogram(df):
    """Visualization 4: Histogram of Years of Service/Experience."""
    if COLUMNS['EXPERIENCE'] not in df.columns: return

    # Drop rows where 'Years_of_Service' might be NaN after conversion
    df_clean = df.dropna(subset=[COLUMNS['EXPERIENCE']])

    fig = px.histogram(
        df_clean,
        x=COLUMNS['EXPERIENCE'],
        title='4. Distribution of Years of Service (Experience)',
        nbins=20, # Number of bins for the histogram
        marginal="box", # Adds a box plot on top for summary statistics
        color_discrete_sequence=['mediumseagreen']
    )
    fig.update_layout(xaxis_title="Years of Service")
    st.plotly_chart(fig, use_container_width=True)


def plot_department_distribution(df):
    """Visualization 5: Bar Chart of Faculty Department Counts."""
    if COLUMNS['DEPARTMENT'] not in df.columns: return

    dept_counts = df[COLUMNS['DEPARTMENT']].value_counts().reset_index()
    dept_counts.columns = ['Department', 'Count']
    dept_counts = dept_counts.sort_values('Count', ascending=True) # Sorted for a horizontal bar chart

    fig = px.bar(
        dept_counts,
        x='Count',
        y='Department',
        orientation='h',
        title='5. Count of Faculty by Department',
        color='Count',
        color_continuous_scale=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Main Streamlit App Logic ---

def main():
    st.title("🏛️ Law Faculty Data Analysis Dashboard")
    st.markdown("---")

    # Load data
    law_df = load_data('https://raw.githubusercontent.com/intannajwa20/EC2024/refs/heads/main/law_faculty_data.csv')

    if not law_df.empty:
        # Display Data Head
        st.subheader("📊 Data Preview")
        st.dataframe(law_df.head(5))
        st.markdown("---")

        st.header("📈 Key Faculty Visualizations")

        # Layout the charts in two columns for better dashboard view
        col1, col2 = st.columns(2)

        with col1:
            plot_gender_distribution(law_df)
            plot_experience_histogram(law_df)
        
        with col2:
            plot_rank_distribution(law_df)
            plot_department_distribution(law_df)
        
        # A visualization that needs full width or is complex
        plot_gender_vs_rank(law_df)


if __name__ == "__main__":
    main()
