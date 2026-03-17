import pandas as pd

RENAME_MAP = {
    'x1': 'meal_cheap_restaurant',
    'x2': 'meal_for_2_mid_restaurant',
    'x3': 'mcmeal',
    'x4': 'domestic_beer_restaurant',
    'x5': 'imported_beer_restaurant',
    'x6': 'cappuccino',
    'x7': 'coke_pepsi',
    'x8': 'water_restaurant',
    'x9': 'milk_1l',
    'x10': 'bread_500g',
    'x11': 'rice_1kg',
    'x12': 'eggs_12',
    'x13': 'cheese_1kg',
    'x14': 'chicken_1kg',
    'x15': 'beef_1kg',
    'x16': 'apples_1kg',
    'x17': 'banana_1kg',
    'x18': 'oranges_1kg',
    'x19': 'tomato_1kg',
    'x20': 'potato_1kg',
    'x21': 'onion_1kg',
    'x22': 'lettuce_1head',
    'x23': 'water_1_5l',
    'x24': 'wine_bottle',
    'x25': 'domestic_beer_market',
    'x26': 'imported_beer_market',
    'x27': 'cigarettes_20pack',
    'x28': 'one_way_ticket',
    'x30': 'monthly_pass_transport',
    'x31': 'taxi_start',
    'x32': 'taxi_1km',
    'x33': 'taxi_1hr_wait',
    'x34': 'gasoline_1l',
    'x35': 'volkswagen_golf',
    'x36': 'apartment_1br_city',
    'x37': 'apartment_1br_outside',
    'x38': 'apartment_3br_city',
    'x39': 'apartment_3br_outside',
    'x41': 'utilities_monthly',
    'x42': 'mobile_plan_monthly',
    'x43': 'intl_primary_school_yearly',
    'x44': 'internet_monthly',
    'x45': 'fitness_club_monthly',
    'x46': 'tennis_court_hr',
    'x47': 'cinema_ticket',
    'x48': 'preschool_monthly',
    'x49': 'intl_school_yearly',
    'x50': 'jeans_levis',
    'x51': 'summer_dress',
    'x54': 'avg_net_salary',
    'x55': 'mortgage_rate'
}

def drop_high_missing_columns(df: pd.DataFrame, threshold: float = 40.0) -> pd.DataFrame:
    """Drop columns with missing values above threshold (%)."""
    missing_percent = (df.isnull().sum() / len(df) * 100)
    cols_to_drop = missing_percent[missing_percent > threshold].index.tolist()
    df = df.drop(columns=cols_to_drop)
    print(f"Dropped {len(cols_to_drop)} columns: {cols_to_drop}")
    return df

def impute_median_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values using median grouped by country."""
    cols_to_impute = df.select_dtypes(include='number').columns.tolist()
    if 'Unnamed: 0' in cols_to_impute:
        cols_to_impute.remove('Unnamed: 0')
    df[cols_to_impute] = df.groupby('country')[cols_to_impute].transform(
        lambda x: x.fillna(x.median())
    )
    # Fallback — global median for countries with single city
    df[cols_to_impute] = df[cols_to_impute].fillna(df[cols_to_impute].median())
    print(f"Imputation done — {df.isnull().sum().sum()} missing values remaining")
    return df

def remove_duplicates_and_index(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates and unnecessary index column."""
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    if 'data_quality' in df.columns:
        df = df.drop(columns=['data_quality'])
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicates")
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns with meaningful names."""
    df = df.rename(columns=RENAME_MAP)
    print("Columns renamed")
    return df

def fix_gasoline_scale(df: pd.DataFrame) -> pd.DataFrame:
    """Fix gasoline_1l scale — divide by 20,000 to convert to USD."""
    if 'gasoline_1l' in df.columns:
        df['gasoline_1l'] = df['gasoline_1l'] / 20000
        print(f"gasoline_1l fixed — median: {df['gasoline_1l'].median():.2f}$")
    return df

def cap_outliers(df: pd.DataFrame, col: str, factor: float = 10.0) -> pd.DataFrame:
    """Cap outliers using IQR method."""
    if col not in df.columns:
        return df
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + factor * IQR
    df[col] = df[col].clip(upper=upper)
    print(f"Outliers capped for {col} — max: {df[col].max():.2f}$")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning pipeline — runs all steps in order."""
    print("\nStarting data cleaning pipeline...")
    df = drop_high_missing_columns(df)
    df = impute_median_by_country(df)
    df = remove_duplicates_and_index(df)
    df = rename_columns(df)
    df = fix_gasoline_scale(df)
    df = cap_outliers(df, 'apartment_3br_city')
    df = cap_outliers(df, 'apartment_1br_city')
    print(f"\nCleaning complete — {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df