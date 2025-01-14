import streamlit as st
import pandas as pd
import plotly.express as px


data_path = os.path.join(os.path.dirname(__file__), "data", "ai_regulations.csv")


# Load the data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/ai_regulations.csv")
    except FileNotFoundError:
        st.error("The data file is missing. Please upload 'data/ai_regulations.csv'.")
        return pd.DataFrame()

# Load the data
data = load_data()

if data.empty:
    st.stop()  # Stop execution if no data is loaded

# Dashboard Title
st.title("AI Regulation Comparative Dashboard 🌍")
st.write("""
    Welcome to the AI Regulation Dashboard! This tool helps you compare AI-related regulations across different countries/regions.
    You can examine key elements like enforcement levels, penalties, compliance steps, and more.
""")
# Step 1: Multi-select countries/regions for comparison
countries = st.multiselect(
    "Select Countries or Regions for Comparison:",
    options=data['Country/Region'].unique(),
    default=data['Country/Region'].unique()[:2]  # Default: first two countries
)

# Filter data based on selection
filtered_data = data[data['Country/Region'].isin(countries)]

# Step 2: Display Summary Statistics as a Table with Vertical Compliance Steps
st.subheader("Summary of Selected Data")
st.write("""
    Below is a detailed summary of the selected countries' AI regulations. You can compare the regulation name, enforcement level, penalty severity, and compliance steps.
""")

# Filter and display relevant columns in the table
summary_columns = ['Country/Region', 'Regulation Name', 'Enforcement Level', 'Penalties', 'Compliance Steps']
summary_data = filtered_data[summary_columns].dropna()

# Display the summary table
st.dataframe(summary_data.sort_values(by='Country/Region'))

# Now list compliance steps vertically (using Expander)
st.subheader("Compliance Steps Breakdown")
for country in filtered_data['Country/Region'].unique():
    # Filter compliance steps for the country
    country_compliance = filtered_data[filtered_data['Country/Region'] == country]['Compliance Steps']
    
    if not country_compliance.empty:
        # We assume the compliance steps are in the first row for this country (adjust as necessary)
        steps = country_compliance.iloc[0]
        
        with st.expander(f"**{country}** Compliance Steps"):
            # List the compliance steps vertically (assuming each entry is a string, split by commas if needed)
            compliance_steps = steps.split(',')  # Adjust if the steps are stored as strings
            for step in compliance_steps:
                st.write(f"- {step.strip()}")

###List regs per country 
# Step 3: List all Regulations for the Selected Countries

st.subheader("List of Regulations for Selected Countries")
st.write("""
    Below is a list of all regulations for the selected countries. Each country’s regulations are grouped together.
""")

# Group data by Country/Region and combine the Regulation Names into a single string per country
regulations_grouped = filtered_data.groupby('Country/Region')['Regulation Name'].apply(lambda x: ', '.join(x)).reset_index()

# Display the regulations table with countries and their regulations listed together
st.dataframe(regulations_grouped.sort_values(by='Country/Region'))

###Heatmap 

import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data (replace this with your actual data)
data = {
    'Country/Region': ['United States', 'Germany', 'India', 'France', 'Brazil', 'European Union'],
    'Enforcement Level': [3, 2, 4, 3, 1, 2],
    # other columns...
}

# Convert to DataFrame
filtered_data = pd.DataFrame(data)

# Map country names to ISO 3166-1 alpha-3 codes
country_iso_map = {
    'United States': 'USA', 'Germany': 'DEU', 'India': 'IND', 'France': 'FRA', 'Brazil': 'BRA',
    'European Union': 'EU',  # Add the EU code here
}

# Add a new column with ISO codes for countries
filtered_data['ISO_Code'] = filtered_data['Country/Region'].map(country_iso_map)

# Filter out rows with no ISO Code mapping
filtered_data = filtered_data.dropna(subset=['ISO_Code'])

# Step 1: Let the user select countries/regions dynamically
selected_countries = st.multiselect(
    "Select Countries for Enforcement Level Visualization",
    options=filtered_data['Country/Region'].unique(),
    default=['United States', 'Germany', 'India', 'European Union']  # Example default countries (including EU)
)

# Filter the data based on the selected countries
filtered_data = filtered_data[filtered_data['Country/Region'].isin(selected_countries)]

# Ensure 'Enforcement Level' is a numeric value (necessary for choropleth)
filtered_data['Enforcement Level'] = pd.to_numeric(filtered_data['Enforcement Level'], errors='coerce')

# Step 2: Create the choropleth map for selected regions
fig_choropleth = px.choropleth(
    filtered_data,
    locations='ISO_Code',
    color='Enforcement Level',
    hover_name='Country/Region',
    color_continuous_scale='Viridis',  # You can choose another color scale
    title="Enforcement Level Map for Selected Countries",
    labels={'Enforcement Level': 'Enforcement Severity'},
    projection='natural earth'
)

# Step 3: Display the choropleth map
st.plotly_chart(fig_choropleth, use_container_width=True)

# penalties section 


# Assuming you have a function `load_data()` that loads your data
filtered_data = load_data()  # Replace with your actual function to load the data

# Penalties Comparison Section
st.subheader("Penalties for Selected AI Regulations")

# Check if the 'Penalties' column exists in the data
if 'Penalties' in filtered_data.columns:
    # Display the data as a simple table with Country/Region and Penalties
    penalties_comparison = filtered_data[['Country/Region', 'Penalties']]

    # Show the table of penalties data without removing or changing anything
    st.write("Penalties data table:")
    st.dataframe(penalties_comparison)  # Display the data as a table

else:
    st.error("The 'Penalties' column is missing from the dataset.")

## Enforcement Bodies 

import streamlit as st

# Assuming you have a function `load_data()` that loads your data
filtered_data = load_data()  # Replace with your actual function to load the data

# Add the Enforcement Body information manually or pull from your data
# You can add a dictionary or another column with enforcement body information
enforcement_bodies = {
    'EU': 'European Commission',
    'US': 'Federal Trade Commission',
    'UK': 'UK Government',
    # Add more mappings for other countries/regions
}

# Adding the Enforcement Body column based on the 'Country/Region'
filtered_data['Enforcement Body'] = filtered_data['Country/Region'].map(enforcement_bodies)

# Enforcement Bodies Section
st.subheader("Enforcement Bodies for AI Regulations")

# Display each country and its enforcement body as a card
for _, row in filtered_data.iterrows():
    with st.expander(f"{row['Country/Region']}"):
        st.write(f"**Regulation**: {row['Regulation Name']}")
        st.write(f"**Enforcement Body**: {row['Enforcement Body']}")

### Links to law 

import pandas as pd
import streamlit as st

# Sample Data (Make sure this is properly formatted)
timeline_data = {
    'Country/Region': ['EU', 'US', 'UK'],
    'Regulation Name': ['EU AI Act', 'US Algorithmic Accountability Act', 'UK AI Strategy'],
    'Start Year': [2021, 2022, 2021],
    'End Year': [2024, 2024, 2025],
    'Enforcement Body': ['European Commission', 'Federal Trade Commission', 'UK Government'],
    'Law Link': [
        'https://ec.europa.eu/digital-strategy/our-policies/artificial-intelligence_en', 
        'https://www.congress.gov/bill/117th-congress/house-bill/6580/text',
        'https://www.gov.uk/government/publications/uk-ai-strategy-leading-the-future-of-uk-innovation'
    ]
}

# Convert to DataFrame
timeline_df = pd.DataFrame(timeline_data)

# Ensure the 'Start Year' and 'End Year' columns are numeric
timeline_df['Start Year'] = pd.to_numeric(timeline_df['Start Year'], errors='coerce')
timeline_df['End Year'] = pd.to_numeric(timeline_df['End Year'], errors='coerce')

# 1. **Display Links to Laws**
st.header("Direct Links to Regulations")

# Create a table with clickable links
for idx, row in timeline_df.iterrows():
    st.subheader(f"**{row['Regulation Name']}**")
    st.write(f"**Country/Region**: {row['Country/Region']}")
    st.write(f"**Start Year**: {row['Start Year']}")
    st.write(f"**End Year**: {row['End Year']}")
    st.write(f"**Enforcement Body**: {row['Enforcement Body']}")
    st.write(f"**Link to Law**: [Click Here]({row['Law Link']})")
    st.write("---")  # Add a separator between each regulation
