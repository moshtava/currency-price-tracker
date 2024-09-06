import pandas as pd
from sqlalchemy import create_engine

crypto_csv_path = './sample_cryptocurrencies.csv'
historical_csv_path = './sample_historical_prices.csv'
crypto_data = pd.read_csv(crypto_csv_path)
historical_data = pd.read_csv(historical_csv_path)
db_string = "sqlite:///:memory:"
engine = create_engine(db_string)
crypto_data.to_sql('cryptocurrency', engine, if_exists='replace', index=False)
historical_data.to_sql('historicalprice', engine, if_exists='replace', index=False)
print("Data ingestion completed successfully.")