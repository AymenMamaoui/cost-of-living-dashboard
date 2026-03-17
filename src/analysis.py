import pandas as pd

def compute_affordability_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute Affordability Index per city.
    Score = avg_net_salary / total_monthly_cost
    Higher score = more affordable
    """
    cost_cols = [
        'meal_cheap_restaurant', 'apartment_1br_city',
        'utilities_monthly', 'internet_monthly',
        'monthly_pass_transport'
    ]
    available_cols = [c for c in cost_cols if c in df.columns]
    df['total_monthly_cost'] = df[available_cols].sum(axis=1)
    df['affordability_index'] = (
        df['avg_net_salary'] / df['total_monthly_cost']
    ).round(2)
    print("Affordability Index computed")
    return df

def compute_avg_cost_per_country(df: pd.DataFrame) -> pd.DataFrame:
    """Compute average cost score per country."""
    cost_cols = [
        'meal_cheap_restaurant', 'meal_for_2_mid_restaurant',
        'apartment_1br_city', 'utilities_monthly',
        'internet_monthly', 'gasoline_1l'
    ]
    available_cols = [c for c in cost_cols if c in df.columns]
    df['avg_cost'] = df[available_cols].mean(axis=1)
    return df

def get_top_countries(df: pd.DataFrame, n: int = 10, most_expensive: bool = True) -> pd.DataFrame:
    """Return top N most or least expensive countries."""
    country_cost = (
        df.groupby('country')['avg_cost']
        .median()
        .sort_values(ascending=not most_expensive)
        .head(n)
        .reset_index()
    )
    return country_cost

def get_city_summary(df: pd.DataFrame, city: str, country: str) -> pd.Series:
    """Return cost summary for a specific city."""
    result = df[(df['city'] == city) & (df['country'] == country)]
    if result.empty:
        raise ValueError(f"City '{city}' in '{country}' not found.")
    return result.iloc[0]