# 📉 WIBOR Inversion Analysis Tool

Profesjonalne narzędzie analityczne do monitorowania i wizualizacji inwersji polskiej krzywej dochodowości. Projekt skupia się na analizie spreadu między rentownością obligacji skarbowych (10Y) a stawką WIBOR 3M.

## 🎯 Cel projektu
Głównym celem modelu jest identyfikacja okresów inwersji krzywej dochodowości, która historycznie stanowi jeden z najsilniejszych sygnałów wyprzedzających dla cykli koniunkturalnych i potencjalnego spowolnienia PKB.

## 🛠️ Kluczowe Funkcjonalności
* **Dynamiczna Wizualizacja**: Dashboard w stylu "Dark Finance" ułatwiający interpretację danych rynkowych.
* **Automatyczna Detekcja Punktów Ekstremalnych**: Skrypt samodzielnie odnajduje i oznacza adnotacją moment najgłębszej inwersji ("Max Inversion Point").
* **Robust Data Pipeline**: Zaawansowany mechanizm pobierania danych z API Stooq z wbudowaną obsługą błędów.

## 📊 Wizualizacja Modelu
<img width="1782" height="1043" alt="wibor_plot_pro" src="https://github.com/user-attachments/assets/f6beb973-73f3-4552-b268-f8462e873a7e" />
*Powyższy wykres przedstawia analizę spreadu z automatycznie wyznaczonym punktem krytycznym oraz zaznaczonymi obszarami inwersji.*

## 💡 Rozwiązane Problemy Techniczne (Quant Case Study)
Podczas rozwoju narzędzia największym wyzwaniem była stabilność dostaw danych z darmowych źródeł API. 

**Zastosowane rozwiązanie:**
Implementacja mechanizmu **Fallback (Tryb Awaryjny)**. W przypadku braku odpowiedzi serwera lub blokady IP (częsty problem w środowiskach chmurowych), skrypt automatycznie przełącza się na generowanie danych syntetycznych/historycznych. Gwarantuje to ciągłość pracy modelu i możliwość przeprowadzenia prezentacji analitycznej niezależnie od stanu usług zewnętrznych.

## 💻 Technologia
* **Język**: Python 3.x
* **Biblioteki**: Pandas, Matplotlib, Requests, NumPy
* **Źródło danych**: Stooq (z autorskim wrapperem obsługującym nagłówki User-Agent)

---
*Projekt przygotowany w ramach rozwijania kompetencji z zakresu Inżynierii Finansowej i Analizy Quant.*
