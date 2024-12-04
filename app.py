import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configure Streamlit page settings
st.set_page_config(
    page_title="Capability Dashboard- EMB",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Custom CSS for styling with professional green theme
st.markdown("""
    <style>
    /* Main container styling */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom right, #ffffff, #f8faf9) !important;
        padding-top: 0 !important;
    }
    
    /* Block default streamlit padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #e8f6ed, #f8faf9) !important;
        border-right: 1px solid #e0e0e0;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div {
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: #000000 !important;
        padding: 0 !important;
    }
    
    /* Style for all sidebar elements */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMultiSelect {
        background-color: #ffffff !important;
        border-radius: 4px !important;
        margin: 0 !important;
        padding: 0 10px !important;
        color: #000000 !important;
    }
    
    /* Style for multiselect dropdown */
    .stMultiSelect > div {
        background-color: #ffffff !important;
        border-radius: 4px !important;
        box-shadow: none !important;
        color: #000000 !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* Style for selected items in multiselect */
    .stMultiSelect [data-testid="stMultiSelectOption"] {
        background-color: #e8f6ed !important;
        color: #000000 !important;
        border-radius: 3px !important;
        margin: 2px !important;
        padding: 2px 8px !important;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    .main {
        padding: 0 1rem !important;
        background: linear-gradient(135deg, #ffffff, #f8faf9);
    }
    
    /* Main title with underline */
    .main-title {
        font-size: 44px;
        font-weight: 800;
        text-align: center;
        color: #2a7144;
        padding: 20px 0;
        margin: 0 0 15px 0;
        background: linear-gradient(120deg, #e8f6ed, #ffffff, #e8f6ed);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        letter-spacing: 0.5px;
        position: relative;
        width: 100%;
    }
    
    .main-title::after {
        content: "";
        display: block;
        width: 200px;
        height: 4px;
        background: linear-gradient(to right, transparent, #46bd72, transparent);
        margin: 15px auto 0;
        border-radius: 2px;
    }

    /* Description box styling */
    .description-box {
        background: #ffffff;
        border: 1px solid #e8f6ed;
        border-radius: 12px;
        padding: 20px 30px;
        margin: 0 0 25px 0;
        width: 100%;
        text-align: center;
        color: #2a7144;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .description-box p {
        margin: 0;
        padding: 0;
    }

    /* Section header with underline */
    .section-header {
        font-size: 34px;
        font-weight: 700;
        text-align: center;
        color: #3da661;
        margin: 20px 0;
        padding: 15px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
        position: relative;
    }
    
    .section-header::after {
        content: "";
        display: block;
        width: 150px;
        height: 3px;
        background: linear-gradient(to right, transparent, #46bd72, transparent);
        margin: 10px auto 0;
        border-radius: 2px;
    }
    
    .stMetric {
        background: linear-gradient(145deg, #ffffff, #f8faf9) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        text-align: center !important;
        border: 1px solid #e8f6ed !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: bold !important;
        color: #46bd72 !important;
        text-align: center !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #2a7144 !important;
        text-align: center !important;
        margin-top: 8px !important;
    }
    
    div[data-testid="stMetricDelta"] {
        text-align: center !important;
        color: #3da661 !important;
        font-weight: 500 !important;
    }
    
    .metric-container {
        text-align: center;
        padding: 15px;
        background: linear-gradient(145deg, #ffffff, #f8faf9);
        border-radius: 12px;
        margin: 10px;
    }
    
    .metric-tooltip {
        font-size: 13px;
        color: #3da661;
        text-align: center;
        margin-top: 8px;
        font-style: italic;
    }
    
    .stDataFrame {
        margin-top: 20px;
        background-color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    
    .stMarkdown {
        margin-bottom: 0 !important;
        color: #2a7144 !important;
    }
    
    .sidebar-title {
        font-size: 24px;
        font-weight: 700;
        text-align: center;
        color: #000000 !important;
        margin: 15px 10px !important;
        padding: 10px !important;
        background: linear-gradient(120deg, rgba(255,255,255,0.9), rgba(232,246,237,0.9));
        border-radius: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        letter-spacing: 0.5px;
    }
    
    /* Style table header and cells */
    div[data-testid="stDataFrame"] th {
        background: #46bd72 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 15px !important;
        border-bottom: 2px solid #2a7144 !important;
        text-transform: uppercase !important;
        font-size: 14px !important;
        letter-spacing: 0.5px !important;
    }
    
    div[data-testid="stDataFrame"] td {
        background-color: #ffffff !important;
        color: #2a7144 !important;
        padding: 12px !important;
        border-bottom: 1px solid #e8f6ed !important;
        font-size: 14px !important;
    }
    
    /* Make specified columns bold */
    div[data-testid="stDataFrame"] td:nth-child(3),  /* Vendor Name */
    div[data-testid="stDataFrame"] td:nth-child(8),  /* Meta Tag */
    div[data-testid="stDataFrame"] td:nth-child(9),  /* Industry */
    div[data-testid="stDataFrame"] td:nth-child(10), /* Sub Industry */
    div[data-testid="stDataFrame"] td:nth-child(11), /* Services */
    div[data-testid="stDataFrame"] td:nth-child(12)  /* Delivery Class */ {
        font-weight: 600 !important;
        color: #46bd72 !important;
    }
    
    /* Style scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #e8f6ed;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #46bd72, #3da661);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #3da661, #2a7144);
    }
    
    /* Style filter labels in sidebar with aligned padding */
    [data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 600 !important;
        margin: 10px 10px 2px 10px !important;
        padding: 0 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px !important;
        display: flex !important;
        align-items: center !important;
        line-height: 1.2 !important;
    }
    
    /* Style help text in sidebar */
    [data-testid="stSidebar"] .stMarkdown small {
        color: #000000 !important;
        opacity: 0.7;
        padding: 0 10px !important;
        display: block !important;
        margin: 0 0 5px 0 !important;
        font-size: 12px !important;
    }
    
    /* Hover effects for interactive elements */
    .stMultiSelect:hover,
    .stSelectbox:hover {
        transform: translateY(-1px);
        transition: all 0.2s ease;
    }
    
    /* Style for table row hover */
    div[data-testid="stDataFrame"] tr:hover td {
        background-color: #f8faf9 !important;
        transition: background-color 0.2s ease;
    }

    /* Sidebar sections spacing */
    [data-testid="stSidebar"] section {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Sidebar expanderHeader */
    [data-testid="stSidebar"] [data-testid="stExpanderHeader"] {
        padding: 0 10px !important;
        margin: 0 !important;
    }

    /* Filter divider */
    .filter-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(0,0,0,0.1), transparent);
        margin: 20px 10px !important;
        padding: 0 !important;
    }

    /* Sidebar collapse control styling */
    [data-testid="collapsedControl"] {
        display: flex;
        justify-content: center;
        align-items: center;
        color: #2a7144 !important;
        background-color: #ffffff !important;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1;
        border: 2px solid #e8f6ed;
    }

    [data-testid="collapsedControl"]::before {
        content: "☰";
        font-size: 20px;
    }

    [data-testid="collapsedControl"] svg {
        display: none;
    }

    [data-testid="collapsedControl"]:hover {
        background-color: #e8f6ed !important;
        color: #46bd72 !important;
        border-color: #46bd72;
        cursor: pointer;
    }

    /* Credits footer styling */
    .credits-footer {
        margin-top: 30px;
        padding: 20px;
        background: linear-gradient(120deg, #e8f6ed, #ffffff, #e8f6ed);
        border-radius: 8px;
        text-align: center;
        color: #2a7144;
        font-size: 14px;
        line-height: 1.6;
    }

    .credits-line {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        margin-bottom: 10px;
    }

    .credits-line span {
        white-space: nowrap;
    }

    .copyright-line {
        margin-top: 10px;
        font-size: 12px;
        color: #46bd72;
    }
    </style>
""", unsafe_allow_html=True)

# Function to load data from Google Sheets
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data():
    try:
        # Use the direct URL to fetch data using pandas
        sheet_id = "15evbdXOccqxdkorKMQ0m-I3eeSQbns5aI-FLMUH2nFo"
        gid = "1772325516"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        # Drop any completely empty rows
        df = df.dropna(how='all')
        # Reset index after dropping rows
        df = df.reset_index(drop=True)
        
        # Keep only required columns in specific order
        columns_to_keep = [
            'Product Code',
            'Classification',
            'Vendor Name',
            'Past Work',
            'Frontend',
            'Backend',
            'Database',
            'Meta Tag',
            'Industry',
            'Sub Industry',
            'Services',
            'Delivery Class'
        ]
        
        # Keep only columns that exist in the dataframe
        existing_columns = [col for col in columns_to_keep if col in df.columns]
        df = df[existing_columns]
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Function to get filtered options based on selection
def get_filtered_options(df, industry_selection=None):
    if industry_selection:
        if 'None' in industry_selection:
            industry_filter = [i for i in industry_selection if i != 'None']
            filtered_df = df[df['Industry'].isin(industry_filter) | df['Industry'].isna()]
        else:
            filtered_df = df[df['Industry'].isin(industry_selection)]
    else:
        filtered_df = df
    
    vendors = sorted([x for x in filtered_df['Vendor Name'].dropna().unique() if pd.notna(x)])
    sub_industries = sorted([x for x in filtered_df['Sub Industry'].dropna().unique() if pd.notna(x)])
    services = sorted([x for x in filtered_df['Services'].dropna().unique() if pd.notna(x)])
    delivery_classes = sorted([x for x in filtered_df['Delivery Class'].dropna().unique() if pd.notna(x)])
    frontends = sorted([x for x in filtered_df['Frontend'].dropna().unique() if pd.notna(x)])
    backends = sorted([x for x in filtered_df['Backend'].dropna().unique() if pd.notna(x)])
    
    return vendors, sub_industries, services, delivery_classes, frontends, backends

# Function to count past works
def count_past_works(df):
    return df['Past Work'].notna().sum()

# Main application
def main():
    st.markdown("""
        <div class="main-title">
            Capability Dashboard- EMB
        </div>
        <div class="description-box">
            <p>Welcome to the EMB Capability Dashboard - your comprehensive tool for exploring and analyzing our technological capabilities across various industries. This dashboard provides real-time insights into our past work, industry expertise, and technological proficiencies. Use the filters on the left to navigate through different segments and discover our extensive portfolio of capabilities.</p>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()

    if df is not None:
        # Sidebar filters
        st.sidebar.markdown("""
            <div class="sidebar-title">
                Filters
            </div>
        """, unsafe_allow_html=True)
        
        # Get unique industries and handle None values
        industries = [x for x in df['Industry'].unique() if pd.notna(x)]
        industries = sorted(industries)
        # Add None option at the beginning
        industries = ['None'] + industries
        
        # Create industry filter
        selected_industry = st.sidebar.multiselect(
            "Industry",
            options=industries,
            help="Select one or more industries"
        )
        
        # Get filtered options based on industry selection
        vendors, sub_industries, services, delivery_classes, frontends, backends = get_filtered_options(df, selected_industry)
        
        # Create dependent filters
        selected_sub_industry = st.sidebar.multiselect(
            "Sub Industry",
            options=sub_industries,
            help="Select one or more sub-industries (filtered based on selected Industry)"
        )
        
        selected_service = st.sidebar.multiselect(
            "Services",
            options=services,
            help="Select one or more services (filtered based on selected Industry)"
        )
        
        selected_delivery_class = st.sidebar.multiselect(
            "Delivery Class",
            options=delivery_classes,
            help="Select one or more delivery classes"
        )
        
        selected_frontend = st.sidebar.multiselect(
            "Frontend",
            options=frontends,
            help="Select one or more frontend technologies"
        )
        
        selected_backend = st.sidebar.multiselect(
            "Backend",
            options=backends,
            help="Select one or more backend technologies"
        )

        # Add divider before vendor filter
        st.sidebar.markdown("""<div class="filter-divider"></div>""", unsafe_allow_html=True)
        
        # Create vendor filter at the end
        selected_vendor = st.sidebar.multiselect(
            "Vendor Name",
            options=vendors,
            help="Select one or more vendors"
        )
        
        # Apply filters
        filtered_df = df.copy()
        
        # Handle industry filter including None
        if selected_industry:
            if 'None' in selected_industry:
                industry_filter = [i for i in selected_industry if i != 'None']
                if industry_filter:
                    filtered_df = filtered_df[filtered_df['Industry'].isin(industry_filter) | filtered_df['Industry'].isna()]
                else:
                    filtered_df = filtered_df[filtered_df['Industry'].isna()]
            else:
                filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industry)]
        
        # Apply vendor filter
        if selected_vendor:
            filtered_df = filtered_df[filtered_df['Vendor Name'].isin(selected_vendor)]
            
        if selected_sub_industry:
            filtered_df = filtered_df[filtered_df['Sub Industry'].isin(selected_sub_industry)]
        if selected_service:
            filtered_df = filtered_df[filtered_df['Services'].isin(selected_service)]
        if selected_delivery_class:
            filtered_df = filtered_df[filtered_df['Delivery Class'].isin(selected_delivery_class)]
        if selected_frontend:
            filtered_df = filtered_df[filtered_df['Frontend'].isin(selected_frontend)]
        if selected_backend:
            filtered_df = filtered_df[filtered_df['Backend'].isin(selected_backend)]
        
        # Display summary statistics at the top
        st.markdown("""
            <div class="section-header">
                Dashboard Overview
            </div>
        """, unsafe_allow_html=True)
        
        # Create metrics container with centered alignment
        metrics_container = st.container()
        with metrics_container:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                total_capabilities = count_past_works(filtered_df)
                total_change = count_past_works(filtered_df) - count_past_works(df) if len(filtered_df) != len(df) else 0
                st.metric(
                    "Total Past Work Capabilities",
                    value=total_capabilities,
                    delta=f"{total_change}" if total_change != 0 else None,
                    delta_color="normal",
                    help="Total count of past work entries"
                )
                st.markdown(f'<div class="metric-tooltip">Count of non-empty Past Work entries</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                unique_industries = len([i for i in filtered_df['Industry'].unique() if pd.notna(i)])
                st.metric(
                    "Number of Industry Segments",
                    value=unique_industries,
                    delta=None,
                    help="Count of unique industry segments"
                )
                st.markdown(f'<div class="metric-tooltip">Unique values from Industry column</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                unique_sub_industries = len([i for i in filtered_df['Sub Industry'].unique() if pd.notna(i)])
                st.metric(
                    "Number of Sub-Industries",
                    value=unique_sub_industries,
                    delta=None,
                    help="Count of unique sub-industries"
                )
                st.markdown(f'<div class="metric-tooltip">Unique values from Sub Industry column</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                unique_services = len([i for i in filtered_df['Services'].unique() if pd.notna(i)])
                st.metric(
                    "Number of Services",
                    value=unique_services,
                    delta=None,
                    help="Count of unique services"
                )
                st.markdown(f'<div class="metric-tooltip">Unique values from Services column</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Add spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display data feed
        st.markdown("""
            <div class="section-header">
                Capability Data Feed
            </div>
        """, unsafe_allow_html=True)
        
        # Display the dataframe
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=500,
            hide_index=True
        )
        
        # Add credits footer
        st.markdown("""
            <div class="credits-footer">
                <div class="credits-line">
                    <span><strong>Data Analyst:</strong> Ashutosh</span>
                    <span><strong>Developed By:</strong> Ashutosh</span>
                </div>
                <div class="copyright-line">
                    © 2023 EMB Capability Dashboard. All rights reserved.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Add timestamp
        st.markdown(f"""
            <div style='text-align: right; color: #46bd72; padding: 20px;'>
                Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("""
            Failed to load data. Please check the Google Sheets URL and permissions.
            Make sure the sheet is accessible and properly formatted.
        """)

if __name__ == "__main__":
    main()
