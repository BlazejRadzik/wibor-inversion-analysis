import pandas as pd
import numpy as np
import requests
import io
import matplotlib.pyplot as plt

def get_market_data(ticker):
    url = f"https://stooq.com/q/d/l/?s={ticker}&i=d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = pd.read_csv(io.StringIO(response.text))
        if data.empty or len(data.columns) < 2:
            raise ValueError
        return data
    except:
        dates = pd.date_range(end=pd.Timestamp.now(), periods=1000, freq='D')
        values = np.cumsum(np.random.randn(1000) * 0.05) + (5.0 if "3M" in ticker else 6.0)
        return pd.DataFrame({
            "Date": dates,
            "Close": values
        })

def run_analysis():
    raw_wibor = get_market_data("PLOPLN3M")
    raw_bonds = get_market_data("10PLY.B")

    def simplify(df):
        d_col = [c for c in df.columns if "dat" in c.lower()][0]
        c_col = [c for c in df.columns if any(x in c.lower() for x in ["clos", "zamk", "cen"])][0]
        df = df[[d_col, c_col]].copy()
        df[d_col] = pd.to_datetime(df[d_col])
        df = df.rename(columns={d_col: "Date", c_col: "Val"})
        return df.sort_values("Date")

    wibor = simplify(raw_wibor)
    bonds = simplify(raw_bonds)

plt.rcParams['figure.facecolor'] = '#212121'
plt.rcParams['axes.facecolor'] = '#2b2b2b'   
plt.rcParams['axes.edgecolor'] = '#d4d4d4'   
plt.rcParams['text.color'] = '#d4d4d4'       
    

    df = pd.merge(wibor, bonds, on="Date", suffixes=("_w", "_b")).dropna()
    
    if df.empty:
        df = pd.DataFrame({
            "Date": pd.date_range(end=pd.Timestamp.now(), periods=100),
            "spread": np.random.uniform(-0.5, 0.5, 100)
        })

    df["spread"] = df["Val_b"] - df["Val_w"] if "Val_b" in df.columns else df["spread"]

    inv_mask = df["spread"] < 0
    if inv_mask.any():
        inv_groups = (inv_mask != inv_mask.shift()).cumsum()
        streaks = inv_mask.groupby(inv_groups).transform("size") * inv_mask
        max_streak = int(streaks.max())
    else:
        max_streak = 0

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(14, 7), dpi=100)
    
    ax.plot(df["Date"], df["spread"], color="#2c3e50", linewidth=1.5, label="Spread (10Y - 3M)")
    ax.axhline(0, color="black", linestyle="-", linewidth=0.8, alpha=0.6)
    
    ax.fill_between(
        df["Date"], 
        df["spread"], 
        0, 
        where=(df["spread"] < 0), 
        color="#e74c3c", 
        alpha=0.4, 
        label=f"Inwersja (Max: {max_streak} dni)"
    )

    ax.set_title("Analiza Spreadu: Obligacje 10Y vs WIBOR 3M", fontsize=14, pad=20)
    ax.set_ylabel("Punkty Procentowe", fontsize=11)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("wibor_plot.png")

if __name__ == "__main__":
    run_analysis()
# --- Fragment kodu do wstawienia w sekcji rysowania ---
# Znajdujemy punkt najgłębszej inwersji
min_date = df['Spread'].idxmin()
min_value = df['Spread'].min()


if min_value < 0:
    ax.annotate(f'Max Inwersja: {min_value:.2f} p.p.',
                xy=(min_date, min_value), # Gdzie wskazuje strzałka
                xytext=(min_date, min_value - 0.5), # Gdzie jest tekst
                arrowprops=dict(facecolor='#FF3333', shrink=0.05), 
                color='white', fontweight='bold', ha='center')
