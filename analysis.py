import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime

# Data
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime.now()

# Dane z Stooq
# PLOPLN3M -> WIBOR 3M, 10PLY.B -> Rentowność obligacji 10-letnich
print("Pobieranie danych o polskim rynku długu...")
wibor = web.DataReader('PLOPLN3M', 'stooq', start, end)['Close']
bonds = web.DataReader('10PLY.B', 'stooq', start, end)['Close']

# Obliczenie spreadu
# Inwersja występuje, gdy spread < 0
spread = bonds - wibor

# Wykres
plt.figure(figsize=(12, 6))
plt.plot(spread, label='Spread (Obligacje 10Y - WIBOR 3M)', color='blue')
plt.axhline(0, color='red', linestyle='--', label='Poziom Inwersji')

# Zaznaczanie obszarów inwersji na czerwono
plt.fill_between(spread.index, spread, 0, where=(spread < 0), color='red', alpha=0.3)

plt.title('Analiza Inwersji Krzywej Dochodowości w Polsce')
plt.xlabel('Rok')
plt.ylabel('Różnica (p.p.)')
plt.legend()
plt.grid(True)

# Zapisanie wykresu
plt.savefig('wibor_inversion.png')
print("Wykres został zapisany jako wibor_inversion.png")
plt.show()
