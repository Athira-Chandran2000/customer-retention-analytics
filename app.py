# app.py
import streamlit as st
import plotly.express as px
import numpy as np
from src.data_processing import load_and_preprocess_data

# Set page configuration
st.set_page_config(page_title="Customer Retention Analytics", layout="wide")

# 1. Data Ingestion & Preprocessing (Cached for performance)
@st.cache_data
def get_data():
    # Load data using our new module
    return load_and_preprocess_data('data/European_Bank.csv')

df = get_data()

if df is None:
    st.error("Failed to load dataset. Please ensure 'dataset.csv' is in the 'data/' folder.")
    st.stop()

# 2. Sidebar: User Capabilities (Filters)
st.sidebar.header("Dashboard Filters")

active_filter = st.sidebar.radio("Activity Status", options=["All", "Active", "Inactive"])
product_slider = st.sidebar.slider("Number of Products", min_value=1, max_value=4, value=(1, 4))
min_balance = st.sidebar.number_input("Minimum Balance", min_value=0.0, max_value=float(df['Balance'].max()), value=0.0)

# Apply filters
filtered_df = df.copy()
if active_filter == "Active":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 1]
elif active_filter == "Inactive":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 0]

filtered_df = filtered_df[(filtered_df['NumOfProducts'] >= product_slider[0]) & 
                          (filtered_df['NumOfProducts'] <= product_slider[1])]
filtered_df = filtered_df[filtered_df['Balance'] >= min_balance]

# 3. Main Dashboard Layout
st.title("🏦 Customer Engagement & Retention Dashboard")
st.markdown("Analyze churn risks based on behavioral engagement, product utilization, and financial commitment.")

# Top Row: Retention Strength Scoring Panels (KPIs)
st.subheader("Key Performance Indicators (Filtered Data)")
col1, col2, col3, col4 = st.columns(4)

overall_churn = filtered_df['Exited'].mean() * 100
premium_risk_mask = (filtered_df['Balance'] > df['Balance'].median()) & (filtered_df['IsActiveMember'] == 0)
premium_risk = filtered_df[premium_risk_mask]['Exited'].mean() * 100

col1.metric("Total Customers Selected", f"{len(filtered_df):,}")
col2.metric("Overall Churn Rate", f"{overall_churn:.2f}%")
if not np.isnan(premium_risk):
    col3.metric("Premium Diseng. Churn", f"{premium_risk:.2f}%")
else:
    col3.metric("Premium Diseng. Churn", "N/A")
col4.metric("Avg Relationship Score", f"{filtered_df['RelationshipStrength'].mean():.2f} / 4.0")

st.markdown("---")

# Middle Row: Core Modules (Charts)
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Engagement vs Churn Overview")
    engagement_churn = filtered_df.groupby('EngagementProfile')['Exited'].mean().reset_index()
    fig1 = px.bar(engagement_churn, x='EngagementProfile', y='Exited', 
                  title="Churn Rate by Engagement Profile",
                  labels={'Exited': 'Churn Rate', 'EngagementProfile': 'Profile'},
                  color='EngagementProfile')
    fig1.layout.yaxis.tickformat = ',.1%'
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Product Utilization Impact")
    prod_churn = filtered_df.groupby('NumOfProducts')['Exited'].mean().reset_index()
    fig2 = px.line(prod_churn, x='NumOfProducts', y='Exited', markers=True,
                   title="Churn Rate vs Number of Products Used",
                   labels={'Exited': 'Churn Rate', 'NumOfProducts': 'Products'})
    fig2.layout.yaxis.tickformat = ',.1%'
    fig2.update_xaxes(dtick=1)
    st.plotly_chart(fig2, use_container_width=True)

# Bottom Row: High-Value Disengaged Detector & Relationship Strength
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("High-Value Disengaged Detector")
    inactive_df = filtered_df[filtered_df['IsActiveMember'] == 0]
    if not inactive_df.empty:
        fig3 = px.scatter(inactive_df, x='EstimatedSalary', y='Balance', color=inactive_df['Exited'].astype(str),
                          title="Inactive Customers: Balance vs Salary (Color = Churn)",
                          labels={'Exited': 'Churned (1=Yes)', 'EstimatedSalary': 'Estimated Salary'},
                          opacity=0.6)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No inactive customers match the current filter criteria.")

with col_d:
    st.subheader("Retention Strength Index")
    rsi_churn = filtered_df.groupby('RelationshipStrength')['Exited'].mean().reset_index()
    fig4 = px.bar(rsi_churn, x='RelationshipStrength', y='Exited',
                  title="Churn Rate by Relationship Strength (0-4)",
                  labels={'Exited': 'Churn Rate', 'RelationshipStrength': 'Strength Score'},
                  color='RelationshipStrength', color_continuous_scale='blues')
    fig4.layout.yaxis.tickformat = ',.1%'
    st.plotly_chart(fig4, use_container_width=True)