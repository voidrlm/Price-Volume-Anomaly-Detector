import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

# Set up improved style
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(15, 8))

# Line plot for price
ax.plot(btc.index, btc['Close'], label='BTC-USD Close Price', color='#0066CC', linewidth=2.5)

# Highlight anomalies with large, outlined red circles
ax.scatter(
    anomalies.index,
    anomalies['Close'],
    color='white',
    edgecolor='#CC0000',
    s=150,
    linewidth=2,
    label='Detected Anomaly',
    zorder=10
)

# Add vertical dashed lines for anomalies
for anomaly_time in anomalies.index:
    ax.axvline(anomaly_time, color='#CC0000', linestyle='--', alpha=0.3, linewidth=1)

# Enhance titles and labels
ax.set_title('BTC-USD Close Price with Anomaly Detection', fontsize=19, fontweight='bold', pad=20)
ax.set_xlabel('Time', fontsize=15, fontweight='bold')
ax.set_ylabel('BTC-USD Close Price (USD)', fontsize=15, fontweight='bold')

# Set legend
ax.legend(fontsize=13, frameon=True, shadow=True, loc='upper left')

# Format x-axis: only time if 1 day, date+time otherwise
num_days = (btc.index[-1] - btc.index[0]).days + 1
if num_days <= 1:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
else:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %I:%M %p'))

plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# Make grid lines more subtle
ax.grid(color='#CCCCCC', linestyle='--', linewidth=1, alpha=0.3)

# Tight layout for neatness
plt.tight_layout()
plt.show()
