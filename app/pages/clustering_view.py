import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.clustering import get_cluster_summary, CLUSTER_FEATURES

COLOR_MAP = {
    'Budget': '#2ecc71',
    'Mid-Range': '#f39c12',
    'Expensive': '#e74c3c'
}

def show(df: pd.DataFrame):
    st.title("🤖 KMeans Clustering Analysis")
    st.markdown("Cities grouped into **3 cost profiles** using KMeans clustering.")
    st.markdown("---")

    # Cluster Distribution + Summary
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📊 Cluster Distribution")
        cluster_counts = (
            df['cluster_label']
            .value_counts()
            .reset_index()
        )
        cluster_counts.columns = ['Cluster', 'Count']

        fig_pie = px.pie(
            cluster_counts,
            values='Count',
            names='Cluster',
            color='Cluster',
            color_discrete_map=COLOR_MAP
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("📈 Cluster Summary")
        summary = get_cluster_summary(df)
        summary_display = summary.rename(columns={
            'meal_cheap_restaurant': 'Cheap Meal ($)',
            'meal_for_2_mid_restaurant': 'Meal for 2 ($)',
            'apartment_1br_city': 'Rent 1BR ($)',
            'utilities_monthly': 'Utilities ($)',
            'avg_net_salary': 'Avg Salary ($)',
            'internet_monthly': 'Internet ($)',
            'monthly_pass_transport': 'Transport ($)'
        })
        st.dataframe(
            summary_display.style.format("${:.2f}"),
            use_container_width=True
        )

    st.markdown("---")

    # World Map by Cluster
    st.subheader("🗺️ Clusters by Country")

    country_cluster_label = (
        df.groupby('country')['cluster_label']
        .agg(lambda x: x.value_counts().index[0])
        .reset_index()
    )

    fig_map = px.choropleth(
        country_cluster_label,
        locations='country',
        locationmode='country names',
        color='cluster_label',
        color_discrete_map=COLOR_MAP,
        title='Cost Profile by Country',
        hover_name='country'
    )
    fig_map.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # Scatter Salary vs Rent
    st.subheader("💡 Salary vs Rent by Cluster")

    fig_scatter = px.scatter(
        df,
        x='avg_net_salary',
        y='apartment_1br_city',
        color='cluster_label',
        color_discrete_map=COLOR_MAP,
        hover_data=['city', 'country'],
        labels={
            'avg_net_salary': 'Avg Net Salary (USD)',
            'apartment_1br_city': 'Rent 1BR (USD)',
            'cluster_label': 'Cluster'
        },
        title='Salary vs Rent by City'
    )
    fig_scatter.update_layout(height=450)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # Explore Cities by Cluster
    st.subheader("🔍 Explore Cities by Cluster")

    # Utilise les vraies valeurs du DataFrame
    cluster_options = sorted(df['cluster_label'].unique().tolist())
    selected_cluster = st.selectbox("Select Cluster", cluster_options)

    filtered = (
        df[df['cluster_label'] == selected_cluster][[
            'city', 'country', 'avg_net_salary',
            'apartment_1br_city', 'meal_cheap_restaurant',
            'utilities_monthly', 'affordability_index'
        ]]
        .sort_values('affordability_index', ascending=False)
        .reset_index(drop=True)
    )

    filtered_display = filtered.rename(columns={
        'city': 'City',
        'country': 'Country',
        'avg_net_salary': 'Avg Salary ($)',
        'apartment_1br_city': 'Rent 1BR ($)',
        'meal_cheap_restaurant': 'Cheap Meal ($)',
        'utilities_monthly': 'Utilities ($)',
        'affordability_index': 'Affordability Index'
    })

    st.markdown(f"**{len(filtered_display)}** cities in **{selected_cluster}** cluster")
    st.dataframe(filtered_display, use_container_width=True, hide_index=True)

    # Bar Chart — Top 10 Most Affordable in Cluster
    st.subheader(f"🏆 Top 10 Most Affordable Cities — {selected_cluster}")
    top10 = filtered_display.head(10)

    fig_top = px.bar(
        top10,
        x='Affordability Index',
        y='City',
        orientation='h',
        color='Affordability Index',
        color_continuous_scale='Greens',
        hover_data=['Country', 'Avg Salary ($)', 'Rent 1BR ($)'],
        title=f"Top 10 Most Affordable — {selected_cluster}"
    )
    fig_top.update_layout(
        coloraxis_showscale=False,
        height=400
    )
    fig_top.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_top, use_container_width=True)