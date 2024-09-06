import pandas as pd
import numpy as np
import datetime

date_range = pd.date_range(start='2023-01-01', end='2024-02-02')
cryptocurrencies = [
{'name': 'Bitcoin', 'symbol': 'BTC', 'market_cap': 600000000000, 'price': 50000},
{'name': 'Ethereum', 'symbol': 'ETH', 'market_cap': 250000000000, 'price': 4000},
{'name': 'Ripple', 'symbol': 'XRP', 'market_cap': 50000000000, 'price': 1}
]
historical_data = []
for crypto in cryptocurrencies:
    for date in date_range:
        price = np.random.uniform(low=crypto['price'] * 0.8, high=crypto['price'] * 1.2)
        historical_data.append({
        'cryptocurrency': crypto['name'],
        'date': date,
        'price': round(price, 10)
        })
crypto_df = pd.DataFrame(cryptocurrencies)
historical_df = pd.DataFrame(historical_data)
crypto_df.to_csv('./sample_cryptocurrencies.csv', index=False)
historical_df.to_csv('./sample_historical_prices.csv', index=False)
print("Sample data generated and saved to 'sample_cryptocurrencies.csv' and 'sample_historical_prices.csv'.")
