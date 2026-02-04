#!/usr/bin/env python3
"""
Census Building Permits Explorer
Interactive web app for visualizing building permit data (2000-2024)
across six major U.S. metropolitan areas.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="Census Building Permits Explorer",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Column mapping for unit types
UNIT_TYPE_COLUMNS: Dict[str, str] = {
    'Total Units': 'Total_Units',
    '1-Unit (Single Family)': 'Units',
    '2-Units (Duplex)': 'Units.1',
    '3-4 Units': 'Units.2',
    '5+ Units (Apartments)': 'Units.3'
}

@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and prepare the census permit data."""
    df = pd.read_csv(
        'historical_data/processed/six_metros_2000_2024_combined.csv',
        low_memory=False
    )

    # Convert unit columns to numeric
    for col in ['Units', 'Units.1', 'Units.2', 'Units.3', 'Total_Units']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Ensure Year is integer
    df['Year'] = df['Year'].astype(int)

    # Clean place names (remove extra whitespace)
    df['Name'] = df['Name'].str.strip()

    return df

def plot_multiple_places(df: pd.DataFrame, places: List[str], unit_type: str) -> go.Figure:
    """
    Create a line chart comparing multiple places for a single unit type.

    Args:
        df: The full dataset
        places: List of place names to compare
        unit_type: The type of units to display (key from UNIT_TYPE_COLUMNS)

    Returns:
        Plotly figure object
    """
    column = UNIT_TYPE_COLUMNS[unit_type]

    # Filter data for selected places
    filtered_df = df[df['Name'].isin(places)].copy()

    # Create figure
    fig = px.line(
        filtered_df,
        x='Year',
        y=column,
        color='Name',
        markers=True,
        title=f'{unit_type} Permits by Place (2000-2024)',
        labels={
            column: 'Number of Units',
            'Year': 'Year',
            'Name': 'Place'
        }
    )

    # Customize layout
    fig.update_layout(
        hovermode='x unified',
        xaxis=dict(tickmode='linear', tick0=2000, dtick=2),
        yaxis=dict(title='Number of Units', separatethousands=True),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        height=500
    )

    # Improve hover template
    fig.update_traces(
        hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Units: %{y:,.0f}<extra></extra>'
    )

    return fig

def plot_multiple_unit_types(df: pd.DataFrame, place: str, unit_types: List[str]) -> go.Figure:
    """
    Create a line chart comparing multiple unit types for a single place.

    Args:
        df: The full dataset
        place: Place name to analyze
        unit_types: List of unit types to display (keys from UNIT_TYPE_COLUMNS)

    Returns:
        Plotly figure object
    """
    # Filter data for selected place
    filtered_df = df[df['Name'] == place].copy()

    # Create figure
    fig = go.Figure()

    # Add a line for each unit type
    for unit_type in unit_types:
        column = UNIT_TYPE_COLUMNS[unit_type]
        fig.add_trace(go.Scatter(
            x=filtered_df['Year'],
            y=filtered_df[column],
            mode='lines+markers',
            name=unit_type,
            hovertemplate=f'<b>{unit_type}</b><br>Year: %{{x}}<br>Units: %{{y:,.0f}}<extra></extra>'
        ))

    # Customize layout
    fig.update_layout(
        title=f'Building Permits in {place} by Unit Type (2000-2024)',
        xaxis=dict(
            title='Year',
            tickmode='linear',
            tick0=2000,
            dtick=2
        ),
        yaxis=dict(
            title='Number of Units',
            separatethousands=True
        ),
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        height=500
    )

    return fig

def main():
    """Main application logic."""

    # Header
    st.title("🏗️ Census Building Permits Explorer")
    st.markdown("Explore building permit data (2000-2024) across six major U.S. metropolitan areas")

    # Load data
    with st.spinner("Loading data..."):
        df = load_data()

    # Get sorted list of unique place names
    places = sorted(df['Name'].unique().tolist())

    # Sidebar
    st.sidebar.header("Settings")

    # Mode selection
    mode = st.sidebar.radio(
        "Visualization Mode",
        ["Compare Places", "Compare Unit Types"],
        help="Choose whether to compare multiple places or multiple unit types"
    )

    st.sidebar.markdown("---")

    # Mode 1: Compare Places
    if mode == "Compare Places":
        st.sidebar.subheader("Compare Multiple Places")

        # Unit type selection
        unit_type = st.sidebar.selectbox(
            "Select Unit Type",
            list(UNIT_TYPE_COLUMNS.keys()),
            index=0,  # Default to Total Units
            help="Choose which type of housing units to display"
        )

        # Place selection (up to 5)
        selected_places = st.sidebar.multiselect(
            "Select Places to Compare (max 5)",
            places,
            default=[],
            max_selections=5,
            help="Search and select up to 5 places to compare"
        )

        # Display chart
        if selected_places:
            fig = plot_multiple_places(df, selected_places, unit_type)
            st.plotly_chart(fig, use_container_width=True)

            # Show summary statistics
            with st.expander("📊 Summary Statistics"):
                summary_df = df[df['Name'].isin(selected_places)].groupby('Name')[UNIT_TYPE_COLUMNS[unit_type]].agg([
                    ('Total 2000-2024', 'sum'),
                    ('Average per Year', 'mean'),
                    ('Peak Year Value', 'max'),
                    ('Minimum Year Value', 'min')
                ]).round(0)
                st.dataframe(summary_df, use_container_width=True)
        else:
            st.info("👈 Select one or more places from the sidebar to begin exploring")

            # Show example
            st.markdown("### Example Places You Can Explore:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Major Cities:**")
                st.markdown("- Washington\n- San Francisco\n- Seattle")
            with col2:
                st.markdown("**Suburbs:**")
                st.markdown("- Cambridge\n- Palo Alto\n- Bellevue")
            with col3:
                st.markdown("**Counties:**")
                st.markdown("- Montgomery County Unincorporated Area")

    # Mode 2: Compare Unit Types
    else:
        st.sidebar.subheader("Compare Unit Types")

        # Place selection (single)
        selected_place = st.sidebar.selectbox(
            "Select a Place",
            places,
            index=None,
            help="Search and select a place to analyze"
        )

        # Unit type selection (multiple)
        selected_unit_types = st.sidebar.multiselect(
            "Select Unit Types to Compare",
            list(UNIT_TYPE_COLUMNS.keys()),
            default=['Total Units'],
            help="Choose which unit types to display on the chart"
        )

        # Display chart
        if selected_place and selected_unit_types:
            fig = plot_multiple_unit_types(df, selected_place, selected_unit_types)
            st.plotly_chart(fig, use_container_width=True)

            # Show summary statistics
            with st.expander("📊 Summary Statistics"):
                place_df = df[df['Name'] == selected_place].copy()
                summary_data = {}
                for unit_type in selected_unit_types:
                    col = UNIT_TYPE_COLUMNS[unit_type]
                    summary_data[unit_type] = {
                        'Total 2000-2024': place_df[col].sum(),
                        'Average per Year': place_df[col].mean(),
                        'Peak Year Value': place_df[col].max(),
                        'Minimum Year Value': place_df[col].min()
                    }
                summary_df = pd.DataFrame(summary_data).T.round(0)
                st.dataframe(summary_df, use_container_width=True)
        elif not selected_place:
            st.info("👈 Select a place from the sidebar to begin exploring")
        else:
            st.warning("Please select at least one unit type to display")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    Data from the U.S. Census Bureau Building Permits Survey, covering:
    - **Years**: 2000-2024
    - **Places**: 1,061 municipalities
    - **Metro Areas**: NYC, LA, DC, Boston, SF, Seattle
    """)

    st.sidebar.markdown("[📂 View on GitHub](https://github.com/dylanmatthews/census-permit-data)")
    st.sidebar.markdown("[📊 Download Data](https://github.com/dylanmatthews/census-permit-data/blob/main/historical_data/processed/six_metros_2000_2024_combined.csv)")

if __name__ == "__main__":
    main()
