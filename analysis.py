import pandas as pd
import matplotlib.pyplot as plt
import requests
import io

def get_stooq_data(ticker):
    url = f"https://stooq.com/q/d/l/?s={ticker}&i=d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        df = pd.read_csv(io.StringIO(response.text))
        
        # Sprawdzamy, czy dane są poprawne
        if df.empty or len(df.columns) < 5:
            return pd.Series()
            
        # Automatycznie wykrywamy kolumnę daty i ceny
        df.index = pd.to_datetime(df.iloc[:, 0])
        return df.iloc[:, 4] # Zazwyczaj 5-ta kolumna to 'Zamkniecie'
    except:
        return pd.Series()

print("Pobieranie danych o WIBOR 3M i obligacjach 10Y...")
wibor = get_stooq_data('PLOPLN3M')
bonds = get_stooq_data('10PLY.B')

if not wibor.empty and not bonds.empty:
    df = pd.DataFrame({'WIBOR': wibor, 'BONDS': bonds}).dropna()
    df['Spread'] = df['BONDS'] - df['WIBOR']
    df['Inversion'] = df['Spread'] < 0

    inversion_groups = (df['Inversion'] != df['Inversion'].shift()).cumsum()
    inversion_durations = df[df['Inversion']].groupby(inversion_groups).size()
    max_inversion = inversion_durations.max()

    print(f"\n--- Analiza Statystyczna ---")
    print(f"Najdłuższa ciągła inwersja: {max_inversion} dni")
    print(f"Aktualny spread: {df['Spread'].iloc[-1]:.2f} p.p.")

    plt.figure(figsize=(12, 6))
    plt.plot(df['Spread'], label='Spread (10Y Bonds - WIBOR 3M)', color='blue')
    plt.axhline(0, color='red', linestyle='--', alpha=0.5)
    plt.fill_between(df.index, df['Spread'], 0, where=df['Inversion'], color='red', alpha=0.3)
    plt.title('Inwersja Krzywej Dochodowości w Polsce')
    plt.savefig('wibor_plot.png')
    print("\n[SUKCES] Wykres zapisany jako wibor_plot.png")
else:
    print("\n[BŁĄD] Serwer Stooq nie odpowiedział. Odczekaj 30 sekund i spróbuj ponownie.")
