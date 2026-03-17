import streamlit as st
import plotly.express as px
import pandas as pd

def show(df: pd.DataFrame):
    st.title("🌐 World Cost of Living Overview")
    st.markdown("Explore the cost of living across **500+ cities** worldwide.")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏙️ Total Cities", f"{len(df):,}")
    col2.metric("🌍 Countries", f"{df['country'].nunique()}")
    col3.metric("💰 Avg Salary (Global)", f"${df['avg_net_salary'].median():,.0f}")
    col4.metric("🍽️ Avg Cheap Meal", f"${df['meal_cheap_restaurant'].median():,.1f}")

    st.markdown("---")

    # World Map
    st.subheader("🗺️ Average Cost by Country")

    country_data = (
        df.groupby('country')['avg_cost']
        .median()
        .reset_index()
        .rename(columns={'avg_cost': 'Average Cost (USD)'})
    )

    fig_map = px.choropleth(
        country_data,
        locations='country',
        locationmode='country names',
        color='Average Cost (USD)',
        color_continuous_scale='RdYlGn_r',
        title='Average Cost of Living by Country',
        hover_name='country'
    )
    fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # Top 10 Most & Least Expensive
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🔴 Top 10 Most Expensive")
        top10_exp = (
            df.groupby('country')['avg_cost']
            .median()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig_exp = px.bar(
            top10_exp, x='avg_cost', y='country',
            orientation='h', color='avg_cost',
            color_continuous_scale='Reds',
            labels={'avg_cost': 'Avg Cost (USD)', 'country': ''},
        )
        fig_exp.update_layout(showlegend=False, coloraxis_showscale=False, height=400)
        fig_exp.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_exp, use_container_width=True)

    with col_right:
        st.subheader("💚 Top 10 Cheapest")
        top10_cheap = (
            df.groupby('country')['avg_cost']
            .median()
            .sort_values(ascending=True)
            .head(10)
            .reset_index()
        )
        fig_cheap = px.bar(
            top10_cheap, x='avg_cost', y='country',
            orientation='h', color='avg_cost',
            color_continuous_scale='Greens_r',
            labels={'avg_cost': 'Avg Cost (USD)', 'country': ''},
        )
        fig_cheap.update_layout(showlegend=False, coloraxis_showscale=False, height=400)
        fig_cheap.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_cheap, use_container_width=True)

    st.markdown("---")

    # Salary vs Rent Scatter
    st.subheader("💡 Salary vs Rent — Affordability View")
    fig_scatter = px.scatter(
        df, x='avg_net_salary', y='apartment_1br_city',
        color='cluster_label',
        hover_data=['city', 'country'],
        color_discrete_map={
            '💚 Budget': '#2ecc71',
            '🟡 Mid-Range': '#f39c12',
            '🔴 Expensive': '#e74c3c'
        },
        labels={
            'avg_net_salary': 'Avg Net Salary (USD)',
            'apartment_1br_city': 'Rent 1BR City Center (USD)',
            'cluster_label': 'Cluster'
        },
        title='Salary vs Rent by City'
    )
    fig_scatter.update_layout(height=450)
    st.plotly_chart(fig_scatter, use_container_width=True)