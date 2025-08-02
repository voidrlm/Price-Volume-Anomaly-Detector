import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

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

# Set up plotting
plt.figure(figsize=(14, 7))
plt.plot(btc.index, btc['Close'], label='BTC-USD Close Price', color='blue')
plt.scatter(anomalies.index, anomalies['Close'], color='red', label='Anomaly', zorder=5)

plt.xlabel('Time')
plt.ylabel('BTC-USD Close Price (USD)')
plt.title('BTC-USD Close Price with Anomaly Detection')
plt.legend()
plt.tight_layout()

# Format x-axis: time only for 1 day, date+time for >1 day
num_days = (btc.index[-1] - btc.index[0]).days + 1
if num_days <= 1:
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
else:
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %I:%M %p'))

plt.xticks(rotation=45)
plt.show()
