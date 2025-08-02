import yfinance as yf
print("Downloading BTC-USD data...")
btc = yf.download('BTC-USD', period='1d', interval='5m')
print("Calculating returns...")
btc['returns'] = btc['Close'].pct_change()
print("Calculating rolling mean and std...")
mean = btc['returns'].rolling(window=10).mean()
std = btc['returns'].rolling(window=10).std()
print("Calculating z-scores...")
btc['zscore'] = (btc['returns'] - mean) / std
print("Detecting anomalies...")
anomalies = btc[btc['zscore'].abs() > 2]
anomalies.index = anomalies.index.to_series().dt.strftime('%b %d, %I:%M %p')
print("Anomalies found:")
print(anomalies[['Close', 'zscore']])
