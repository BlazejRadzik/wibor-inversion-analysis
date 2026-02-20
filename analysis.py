import pandas as pd
import matplotlib.pyplot as plt
import requests
import io
import numpy as np
import matplotlib.dates as mdates

plt.rcParams['figure.facecolor'] = '#212121'
plt.rcParams['axes.facecolor'] = '#2b2b2b'
plt.rcParams['axes.edgecolor'] = '#d4d4d4'
plt.rcParams['axes.labelcolor'] = '#d4d4d4'
plt.rcParams['xtick.color'] = '#d4d4d4'
plt.rcParams['ytick.color'] = '#d4d4d4'
plt.rcParams['text.color'] = '#d4d4d4'
plt.rcParams['grid.color'] = '#444444'

def get_data(ticker):
    url = f"https://stooq.com/q/d/l/?s={ticker}&i=d"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200 and len(r.text) > 100:
            df = pd.read_csv(io.StringIO(r.text), index_col=0, parse_dates=True)
            return df.iloc[:, -1]
    except Exception:
        pass
    return pd.Series()

wibor = get_data('PLOPLN3M')
bonds = get_data('10PLY.B')
data_source = "Stooq Data (Live)"

if wibor.empty or bonds.empty:
    data_source = "Synthetic Demo Data"
    dates = pd.date_range(end=pd.Timestamp.now(), periods=1000, freq='D')
    spread_values = np.cumsum(np.random.normal(0, 0.06, 1000)) + 1.0
    spread_values[400:700] = spread_values[400:700] - 3.0 
    df = pd.DataFrame({'Spread': spread_values}, index=dates)
else:
    df = pd.DataFrame({'WIBOR': wibor, 'BONDS': bonds}).dropna()
    df['Spread'] = df['BONDS'] - df['WIBOR']

df['Inversion'] = df['Spread'] < 0

fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(df.index, df['Spread'], label='Spread (10Y - 3M)', color='#00BFFF', linewidth=2)
ax.axhline(0, color='#FF3333', linestyle='--', linewidth=1.5, alpha=0.8)
ax.fill_between(df.index, df['Spread'], 0, where=df['Inversion'], 
                color='#FF0000', alpha=0.4, label='Inversion Area')

min_date = df['Spread'].idxmin()
min_value = df['Spread'].min()

if min_value < 0:
    ax.annotate(f'Max Inversion: {min_value:.2f} p.p.',
                xy=(min_date, min_value),
                xytext=(min_date, min_value - 0.8),
                arrowprops=dict(facecolor='#FF3333', shrink=0.05, width=2, headwidth=8),
                color='white', fontweight='bold', ha='center',
                bbox=dict(boxstyle="round,pad=0.3", fc="#FF3333", ec="none", alpha=0.3))

ax.set_title('Yield Curve Inversion Analysis (Poland)', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Spread (Percentage Points)', fontsize=12)
ax.grid(True, linestyle=':', linewidth=0.7)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
fig.autofmt_xdate()

legend = ax.legend(loc='upper right', facecolor='#333333', edgecolor='#555555')
plt.setp(legend.get_texts(), color='#d4d4d4')

plt.figtext(0.95, 0.02, f'Source: {data_source} | Quant Portfolio Analytics', 
            ha='right', fontsize=9, color='#888888')

plt.tight_layout()
plt.savefig('wibor_plot_pro.png', dpi=150, bbox_inches='tight')
