import pandas as pd
import matplotlib.pyplot as plt

def get_stooq_data(ticker):
    url = f"https://stooq.com/q/d/l/?s={ticker}&i=d"
    df = pd.read_csv(url)
    if df.empty or len(df.columns) < 2:
        return pd.Series()
    
    # Znajdujemy kolumnę z ceną (zazwyczaj 'Close' lub 'Zamkniecie')
    price_col = [c for c in df.columns if c.lower() in ['close', 'zamkniecie']][-1]
    
    # Pierwsza kolumna to zawsze data
    df.index = pd.to_datetime(df.iloc[:, 0])
    return df[price_col]

wibor = get_stooq_data('PLOPLN3M')
bonds = get_stooq_data('10PLY.B')

if not wibor.empty and not bonds.empty:
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
else:
    print("Błąd pobierania danych. Spróbuj uruchomić skrypt ponownie za chwilę.")
