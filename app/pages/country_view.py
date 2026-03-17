import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

EXPENSE_CATEGORIES = {
    '🍽️ Food & Restaurants': [
        'meal_cheap_restaurant', 'meal_for_2_mid_restaurant',
        'mcmeal', 'milk_1l', 'bread_500g', 'rice_1kg',
        'eggs_12', 'chicken_1kg', 'beef_1kg'
    ],
    '🏠 Housing': [
        'apartment_1br_city', 'apartment_1br_outside',
        'apartment_3br_city', 'apartment_3br_outside'
    ],
    '🚗 Transport': [
        'monthly_pass_transport', 'taxi_start',
        'taxi_1km', 'gasoline_1l'
    ],
    '💡 Utilities': [
        'utilities_monthly', 'internet_monthly',
        'mobile_plan_monthly'
    ],
    '🎭 Leisure': [
        'cinema_ticket', 'fitness_club_monthly',
        'tennis_court_hr'
    ]
}

def show(df: pd.DataFrame):
    st.title("🏙️ Country & City Explorer")
    st.markdown("Deep dive into cost of living for any country or city.")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        countries = sorted(df['country'].unique())
        selected_country = st.selectbox("🌍 Select Country", countries, index=countries.index('France') if 'France' in countries else 0)

    with col2:
        cities = sorted(df[df['country'] == selected_country]['city'].unique())
        selected_city = st.selectbox("🏙️ Select City", cities)

    city_data = df[(df['city'] == selected_city) & (df['country'] == selected_country)].iloc[0]

    st.markdown("---")

    # City KPIs
    st.subheader(f"📊 {selected_city}, {selected_country}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Avg Net Salary", f"${city_data['avg_net_salary']:,.0f}")
    col2.metric("🏠 Rent 1BR (City)", f"${city_data['apartment_1br_city']:,.0f}")
    col3.metric("🍽️ Cheap Meal", f"${city_data['meal_cheap_restaurant']:,.1f}")
    col4.metric("💡 Affordability Index", f"{city_data['affordability_index']:,.2f}")

    st.markdown("---")

    #  Expense Breakdown
    st.subheader("💸 Expense Breakdown by Category")
    selected_category = st.selectbox("Select Category", list(EXPENSE_CATEGORIES.keys()))

    cols_in_cat = [c for c in EXPENSE_CATEGORIES[selected_category] if c in df.columns]
    values = city_data[cols_in_cat]

    fig_bar = px.bar(
        x=cols_in_cat, y=values,
        labels={'x': 'Expense', 'y': 'Cost (USD)'},
        color=values,
        color_continuous_scale='Blues',
        title=f"{selected_category} costs in {selected_city}"
    )
    fig_bar.update_layout(coloraxis_showscale=False, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # City vs Country Average
    st.subheader(f"📈 {selected_city} vs {selected_country} Average")

    compare_cols = [
        'meal_cheap_restaurant', 'apartment_1br_city',
        'utilities_monthly', 'internet_monthly',
        'avg_net_salary', 'monthly_pass_transport'
    ]
    compare_cols = [c for c in compare_cols if c in df.columns]
    country_avg = df[df['country'] == selected_country][compare_cols].mean()

    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        name=selected_city, x=compare_cols, y=city_data[compare_cols],
        marker_color='#3498db'
    ))
    fig_compare.add_trace(go.Bar(
        name=f"{selected_country} avg", x=compare_cols, y=country_avg,
        marker_color='#95a5a6'
    ))
    fig_compare.update_layout(
        barmode='group', height=400,
        title=f"{selected_city} vs {selected_country} Average",
        yaxis_title='Cost (USD)'
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown("---")

    # All Cities in Country
    st.subheader(f"🏙️ All Cities in {selected_country}")
    country_cities = df[df['country'] == selected_country][
        ['city', 'avg_net_salary', 'apartment_1br_city',
         'meal_cheap_restaurant', 'affordability_index', 'cluster_label']
    ].sort_values('affordability_index', ascending=False).reset_index(drop=True)


    country_cities_display = country_cities.rename(columns={
        'city': 'City',
        'avg_net_salary': 'Avg Salary ($)',
        'apartment_1br_city': 'Rent 1BR ($)',
        'meal_cheap_restaurant': 'Cheap Meal ($)',
        'affordability_index': 'Affordability Index',
        'cluster_label': 'Cluster'
    })
    st.dataframe(country_cities_display, use_container_width=True)