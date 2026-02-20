import pandas as pd
import matplotlib.pyplot as plt

def get_stooq_data(ticker):
    url = f"https://stooq.com/q/d/l/?s={ticker}&i=d"
    # Używamy index_col=0, aby uniknąć problemu z nazwą kolumny 'Data'/'Date'
    df = pd.read_csv(url, index_col=0, parse_dates=True)
    return df.iloc[:, 3] # Wybieramy czwartą kolumnę (Cena zamknięcia)

wibor = get_stooq_data('PLOPLN3M')
bonds = get_stooq_data('10PLY.B')

df = pd.DataFrame({'WIBOR': wibor, 'BONDS': bonds}).dropna()
df['Spread'] = df['BONDS'] - df['WIBOR']
df['Inversion'] = df['Spread'] < 0

inversion_groups = (df['Inversion'] != df['Inversion'].shift()).cumsum()
inversion_durations = df[df['Inversion']].groupby(inversion_groups).size()
max_inversion = inversion_durations.max()

print(f"Najdłuższa ciągła inwersja: {max_inversion} dni")
print(f"Aktualny spread: {df['Spread'].iloc[-1]:.2f} p.p.")

plt.figure(figsize=(12, 6))
plt.plot(df['Spread'], label='Spread (10Y Bonds - WIBOR 3M)', color='blue')
plt.axhline(0, color='red', linestyle='--', alpha=0.5)
plt.fill_between(df.index, df['Spread'], 0, where=df['Inversion'], color='red', alpha=0.3)
plt.title('Inwersja Krzywej Dochodowości w Polsce')
plt.savefig('wibor_plot.png')
