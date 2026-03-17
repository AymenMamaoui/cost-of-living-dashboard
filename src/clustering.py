import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


CLUSTER_FEATURES = [
    'meal_cheap_restaurant',
    'meal_for_2_mid_restaurant',
    'apartment_1br_city',
    'utilities_monthly',
    'avg_net_salary',
    'internet_monthly',
    'monthly_pass_transport'
]

CLUSTER_LABELS = {
    0: 'Budget',
    1: 'Mid-Range',
    2: 'Expensive'
}

def get_optimal_k(df: pd.DataFrame, max_k: int = 10) -> list:
    """Compute inertia for elbow method."""
    features = [f for f in CLUSTER_FEATURES if f in df.columns]
    X = df[features].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    inertias = []
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
    return inertias

def apply_kmeans(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    """
    Apply KMeans clustering and add cluster labels to DataFrame.
    Returns enriched DataFrame with 'cluster' and 'cluster_label' columns.
    """
    features = [f for f in CLUSTER_FEATURES if f in df.columns]
    df_model = df[features].copy()

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_model)

    # Fit KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Order clusters by avg_net_salary (low → high)
    cluster_order = (
        df.groupby('cluster')['avg_net_salary']
        .mean()
        .sort_values()
        .index.tolist()
    )
    mapping = {old: new for new, old in enumerate(cluster_order)}
    df['cluster'] = df['cluster'].map(mapping)
    df['cluster_label'] = df['cluster'].map(CLUSTER_LABELS)

    print(f"KMeans applied — {n_clusters} clusters")
    print(df['cluster_label'].value_counts())
    return df

def get_cluster_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return mean values per cluster for key features."""
    features = [f for f in CLUSTER_FEATURES if f in df.columns]
    features += ['cluster_label']
    summary = (
        df[features]
        .groupby('cluster_label')
        .mean()
        .round(2)
    )
    return summary