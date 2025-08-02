import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

print("Downloading BTC-USD data...")
btc = yf.download('BTC-USD', period='1d', interval='5m')

print("Calculating returns and rolling stats...")
btc['returns'] = btc['Close'].pct_change()
mean = btc['returns'].rolling(window=10).mean()
std = btc['returns'].rolling(window=10).std()
btc['zscore'] = (btc['returns'] - mean) / std

print("Detecting anomalies...")
anomalies = btc[btc['zscore'].abs() > 2].copy()

# Format annotation for meaning
def anomaly_meaning(z):
    if np.isnan(z):
        return ""
    elif z > 0:
        return "Price Spike (Up)"
    else:
        return "Price Drop (Down)"

anomalies['Meaning'] = anomalies['zscore'].apply(anomaly_meaning)

# Format time string for table
anomalies['Time'] = anomalies.index.strftime('%b %d, %I:%M %p')
anomaly_table = anomalies[['Time', 'Close', 'zscore', 'Meaning']].copy()
anomaly_table.rename(columns={'Close': 'Close Price', 'zscore': 'Z-Score'}, inplace=True)
anomaly_table['Close Price'] = anomaly_table['Close Price'].round(2)
anomaly_table['Z-Score'] = anomaly_table['Z-Score'].round(2)

plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(16, 12))

# Specify layout: upper part for graph, lower for table
gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

# --- Top: Price Chart with Anomalies ---
ax = fig.add_subplot(gs[0])
ax.plot(btc.index, btc['Close'], label='BTC-USD Close Price', color='#0066CC', linewidth=2.5)
ax.scatter(anomalies.index, anomalies['Close'], color='white', edgecolor='#CC0000',
           s=170, linewidth=2, label='Detected Anomaly', zorder=10)

# Annotate each anomaly with its z-score
for i, row in anomalies.iterrows():
    zscore_value = row['zscore']
    if isinstance(zscore_value, pd.Series):
        zscore_value = zscore_value.iloc[0]
    ax.annotate(f"{zscore_value:.2f}", (i, row['Close']),
                textcoords="offset points", xytext=(0,12), ha='center',
                fontsize=11, color='#CC0000', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.1", alpha=0.2, color='red'))

for anomaly_time in anomalies.index:
    ax.axvline(anomaly_time, color='#CC0000', linestyle='--', alpha=0.3, linewidth=1)

ax.set_title('BTC-USD Close Price with Anomaly Detection', fontsize=20, fontweight='bold', pad=20)
ax.set_xlabel('Time', fontsize=15, fontweight='bold')
ax.set_ylabel('BTC-USD Close Price (USD)', fontsize=15, fontweight='bold')
ax.legend(fontsize=13, frameon=True, shadow=True, loc='upper left')
ax.grid(color='#CCCCCC', linestyle='--', linewidth=1, alpha=0.3)

# Format x-axis
num_days = (btc.index[-1] - btc.index[0]).days + 1
if num_days <= 1:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
else:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %I:%M %p'))
plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=12)
plt.setp(ax.get_yticklabels(), fontsize=12)

# --- Bottom: Table of Anomalies ---
ax_table = fig.add_subplot(gs[1])

# Hide axes for table
ax_table.axis('off')
print("Anomaly Table:\n", anomaly_table)
if not anomaly_table.empty:
    table = ax_table.table(
        cellText=anomaly_table.values,
        colLabels=anomaly_table.columns,
        loc='center',
        cellLoc='center',
        colLoc='center',
        colWidths=[0.22, 0.18, 0.14, 0.28],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1.2, 2)  # Stretch table for readability

    # Style header
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_fontsize(14)
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#0066CC')
        else:
            cell.set_fontsize(13)
            # Make spikes green and drops red in "Meaning"
            if col == 3:
                if "Up" in cell.get_text().get_text():
                    cell.set_facecolor('#d0f0c0')
                elif "Down" in cell.get_text().get_text():
                    cell.set_facecolor('#fcdada')
plt.subplots_adjust(hspace=0.27)
plt.tight_layout()
plt.show()
