import pandas as pd

# 1. Read RAW CSV
df = pd.read_csv('customer_shopping_behavior.csv')


# 2. Column cleaning
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')

df.rename(
    columns={'purchase_amount_(usd)': 'purchase_amount'},
    inplace=True
)


# 3. Create age group
labels = ['Young Adult', 'Adult', 'Middle_aged', 'Senior']

df['age_group'] = pd.qcut(
    df['age'],
    q=4,
    labels=labels
)


# 4. Create purchase frequency days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = (
    df['frequency_of_purchases'].map(frequency_mapping)
)


# 5. Check duplicate information
print(
    df[['discount_applied', 'promo_code_used']].head(10)
)

print(
    (df['discount_applied'] == df['promo_code_used']).all()
)


# 6. Drop unwanted column
df = df.drop('promo_code_used', axis=1)


# 7. Check final cleaned data
print(df.head())
print(df.columns)


# =====================================
# 8. CONNECT TO SQL SERVER
# =====================================

from sqlalchemy import create_engine
from urllib.parse import quote_plus

server = r'DESKTOP-H81HP38'
database = 'customer_behavior'

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

engine = create_engine(
    'mssql+pyodbc:///?odbc_connect=' +
    quote_plus(connection_string)
)


# 9. LOAD CLEANED DATA
df.to_sql(
    'customer_shopping',
    con=engine,
    if_exists='replace',
    index=False
)

print("Cleaned data loaded successfully!")