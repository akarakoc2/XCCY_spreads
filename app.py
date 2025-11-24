"""
Streamlit Web App for OAS Curve Analysis
User-friendly interface for portfolio managers

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.visualization import InteractiveOASPlotter
from src.engine import NelsonSiegelSvensson, CurveFitter

# Page configuration
st.set_page_config(
    page_title="OAS Curve Analyzer",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 OAS Spread Curve Analyzer")
st.markdown("""
Upload your bond data to analyze OAS spreads with Nelson-Siegel-Svensson curve fitting.
Hover over points to see bond details.
""")

# Sidebar for parameters
st.sidebar.header("⚙️ Settings")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Excel File",
    type=['xlsx', 'xls'],
    help="Excel file should contain: bond_name, bid_years_to_wkout, oas"
)

# Issuer name (extracted from filename or manual input)
issuer_name = st.sidebar.text_input(
    "Issuer/Curve Name",
    value="",
    help="Name of the issuer or curve (auto-filled from filename)"
)

# Duration filter range
st.sidebar.subheader("Duration Filter (years)")
duration_range = st.sidebar.slider(
    "Duration Range",
    min_value=0.0,
    max_value=30.0,
    value=(1.0, 30.0),
    step=0.5,
    help="Filter bonds within this duration range"
)

# OAS filter range
st.sidebar.subheader("OAS Filter (bps)")
oas_range = st.sidebar.slider(
    "OAS Range",
    min_value=0,
    max_value=500,
    value=(0, 300),
    step=10,
    help="Filter bonds within this OAS range"
)

show_statistics = st.sidebar.checkbox("Show Fit Statistics", value=True)

# Main content
if uploaded_file is not None:
    try:
        # Extract issuer name from filename if not provided
        if not issuer_name:
            issuer_name = uploaded_file.name.replace('.xlsx', '').replace('.xls', '').replace('_', ' ')
        
        # Load data
        df = pd.read_excel(uploaded_file)
        
        # Display data summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Bonds", len(df))
        
        # Clean data
        df['bid_years_to_wkout'] = pd.to_numeric(df['bid_years_to_wkout'], errors='coerce')
        df['oas'] = pd.to_numeric(df['oas'], errors='coerce')
        df_clean = df.dropna(subset=['bid_years_to_wkout', 'oas'])
        
        # Apply filters with ranges
        df_filtered = df_clean[
            (df_clean['bid_years_to_wkout'] >= duration_range[0]) &
            (df_clean['bid_years_to_wkout'] <= duration_range[1]) &
            (df_clean['oas'] >= oas_range[0]) &
            (df_clean['oas'] <= oas_range[1])
        ]
        
        with col2:
            st.metric("After Filters", len(df_filtered))
        with col3:
            st.metric("Filtered Out", len(df) - len(df_filtered))
        
        if len(df_filtered) < 3:
            st.error("⚠️ Not enough data points after filtering. Adjust filter parameters.")
        else:
            # Create tabs
            tab1, tab2, tab3 = st.tabs(["📈 Interactive Chart", "📊 Data Table", "📋 Statistics"])
            
            with tab1:
                # Create interactive plot
                plotter = InteractiveOASPlotter()
                
                # Sort data
                df_sorted = df_filtered.sort_values('bid_years_to_wkout')
                durations = df_sorted['bid_years_to_wkout'].values
                oas_values = df_sorted['oas'].values
                
                # Create figure
                fig = go.Figure()
                
                # Add scatter with hover
                hover_text = [
                    f"<b>{row['bond_name']}</b><br>" +
                    f"Duration: {row['bid_years_to_wkout']:.2f} years<br>" +
                    f"OAS: {row['oas']:.2f} bps"
                    for _, row in df_sorted.iterrows()
                ]
                
                fig.add_trace(go.Scatter(
                    x=durations,
                    y=oas_values,
                    mode='markers',
                    name='Market Data',
                    marker=dict(size=10, color="#06243a", line=dict(color='black', width=1)),
                    hovertext=hover_text,
                    hoverinfo='text'
                ))
                
                # Fit NSS curve
                try:
                    nss = NelsonSiegelSvensson()
                    fitter = CurveFitter()
                    
                    params, params_dict = nss.fit(durations, oas_values)
                    
                    x_smooth = np.linspace(durations.min(), durations.max(), 500)
                    y_fit = nss.predict(x_smooth, params)
                    
                    fig.add_trace(go.Scatter(
                        x=x_smooth,
                        y=y_fit,
                        mode='lines',
                        name='NSS Fit',
                        line=dict(color="#4ad627", width=3)
                    ))
                    
                    # Calculate metrics
                    y_fit_actual = nss.predict(durations, params)
                    fit_metrics = fitter.calculate_goodness_of_fit(oas_values, y_fit_actual)
                    
                except Exception as e:
                    st.warning(f"Could not fit NSS curve: {e}")
                    params_dict = None
                    fit_metrics = None
                
                # Update layout
                fig.update_layout(
                    title=f"{issuer_name} - OAS Spread Curve with NSS Fit",
                    xaxis_title="Duration (Years)",
                    yaxis_title="OAS (bps)",
                    hovermode='closest',
                    height=600,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, width='stretch')
                
                # Show statistics below chart
                if show_statistics and params_dict and fit_metrics:
                    st.subheader("📊 Curve Fit Statistics")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**NSS Parameters:**")
                        st.write(f"- β₀ (Level): {params_dict['beta0_level']:.2f}")
                        st.write(f"- β₁ (Slope): {params_dict['beta1_slope']:.2f}")
                        st.write(f"- β₂ (Curvature): {params_dict['beta2_curvature']:.2f}")
                        st.write(f"- β₃ (2nd Curvature): {params_dict['beta3_second_curvature']:.2f}")
                        st.write(f"- τ₁: {params_dict['tau1']:.2f}")
                        st.write(f"- τ₂: {params_dict['tau2']:.2f}")
                    
                    with col2:
                        st.markdown("**Goodness of Fit:**")
                        st.metric("R² Score", f"{fit_metrics['r_squared']:.4f}")
                        st.metric("RMSE", f"{fit_metrics['rmse']:.2f} bps")
                        st.metric("MAE", f"{fit_metrics['mae']:.2f} bps")
            
            with tab2:
                # Show data table
                st.subheader("Filtered Bond Data")
                st.dataframe(
                    df_filtered[['bond_name', 'bid_years_to_wkout', 'oas']].sort_values('bid_years_to_wkout'),
                    width='stretch',
                    height=400
                )
                
                # Download button
                csv = df_filtered.to_csv(index=False)
                st.download_button(
                    label="📥 Download Filtered Data (CSV)",
                    data=csv,
                    file_name="filtered_bonds.csv",
                    mime="text/csv"
                )
            
            with tab3:
                # Summary statistics
                st.subheader("Summary Statistics")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Duration Statistics:**")
                    st.write(df_filtered['bid_years_to_wkout'].describe())
                
                with col2:
                    st.markdown("**OAS Statistics:**")
                    st.write(df_filtered['oas'].describe())
    
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        st.info("Make sure your Excel file has columns: bond_name, bid_years_to_wkout, oas")

else:
    # Instructions when no file uploaded
    st.info("👈 Upload an Excel file from the sidebar to begin analysis")
    
    st.markdown("""
    ### 📋 Required Data Format
    
    Your Excel file should contain these columns:
    - **bond_name**: Name or identifier of the bond
    - **bid_years_to_wkout**: Duration in years
    - **oas**: Option-Adjusted Spread in basis points
    
    ### ✨ Features
    - 📊 Interactive charts with hover details
    - 🔍 Adjustable filters for duration and OAS
    - 📈 Nelson-Siegel-Svensson curve fitting
    - 📉 Goodness-of-fit statistics
    - 💾 Download filtered data
    """)
    
    # Show example
    with st.expander("📖 See Example Data"):
        example_df = pd.DataFrame({
            'bond_name': ['Bond A', 'Bond B', 'Bond C'],
            'bid_years_to_wkout': [2.5, 5.0, 10.0],
            'oas': [45.2, 52.3, 48.7]
        })
        st.dataframe(example_df)
