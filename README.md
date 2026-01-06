# 🏠 Analiza Rynku Nieruchomości w Polsce (2015-2024)

**Projekt na zaliczenie:** Analiza Danych w R i Python (ADRPY2025)  
**Semestr:** 2025/26  
**Temat:** Zróżnicowanie cen nieruchomości między województwami i powiatami

---

## 📊 Przegląd Projektu

Projekt analizuje ceny nieruchomości na polskim rynku w okresie 2015-2024, badając różnice geograficzne, trendy czasowe i wpływ segmentacji rynku (pierwotny/wtórny) na dynamikę cen.

### Główne Wyniki:
- ✅ **ANOVA Test (F=10.97, p<0.05):** Ceny istotnie różnią się między województwami
- ✅ **Korelacja Pearsona (r=0.43, p<0.05):** Wyraźny trend wzrostu cen w czasie (+~14,421 zł/rok)
- ✅ **Chi-kwadrat:** Segment rynku ma istotny wpływ na rozkład geograficzny
- ✅ **Analiza 98 powiatów** z wystarczającą ilością danych (≥3 lata obserwacji)

---

## 📁 Struktura Projektu

```
Beginners/
├── README.md                           # Ten plik
├── Wczytywanie danych.ipynb           # Główny notebook z analizą
├── RYNE_3786_CREL_20251207150625.csv  # Dane źródłowe
└── .git/                               # Git repository
```

---

## 🔧 Technologia

| Komponent | Narzędzie |
|-----------|-----------|
| **Język** | Python 3.10+ |
| **Notebook** | Jupyter Notebook (.ipynb) |
| **Analiza danych** | pandas, numpy |
| **Statystyka** | scipy.stats |
| **Wizualizacja** | matplotlib, seaborn |
| **Kontrola wersji** | Git/GitHub |

---

## 📋 Zawartość Notebooka

### Sekcja 1: Przygotowanie Danych (Komórki 1-6)
- Wczytanie danych z CSV
- Czyszczenie i normalizacja
- Formatowanie kodów powiatów (XX-Y00)
- Usunięcie wartości zerowych

### Sekcja 2: Analiza Wojewódzka (Komórki 7-25)
- CAGR (Compound Annual Growth Rate) dla 16 województw
- Siatka wykresów zmian procentowych
- Trendy czasowe dla każdego województwa
- Ranking województw po średnich cenach

### Sekcja 3: Analiza Powiatów (Komórki 26-34)
- Ocena jakości danych (98/102 powiatów spełnia kryteria)
- CAGR dla top 16 powiatów
- Siatka wykresów dla powiatów z wysokim wzrostem
- Indywidualne wykresy 98 powiatów (z danymi ≥3 lata)

### Sekcja 4: Testy Statystyczne (Komórki 35-43)

**1. Test ANOVA** - Różnice cen między województwami
- F-statystyka: 10.9708
- P-wartość: 9.08e-20
- **Wniosek:** Ceny istotnie różnią się geograficznie

**2. Test Chi-Kwadrat** - Niezależność segmentu i powiatu
- Zależność między typem rynku a lokalizacją
- Różne struktury geograficzne dla rynku pierwotnego i wtórnego

**3. Analiza Korelacji** - Trend czasowy
- Współczynnik Pearsona: r = 0.4285
- P-wartość: 2.09e-264
- **Wniosek:** Ceny rosną istotnie w czasie

**4. Przedziały Ufności 95%** - Estymacja parametrów
- Przedziały dla średnich cen po segmentach
- Interpretacja statystyczna

**5. Regresja Liniowa** - Tempo zmian
- Trend: Wartość = -2,889,146 + 14,421 × Rok
- R² = 0.1836 (18% wariancji wyjaśnione rokiem)
- Wizualizacja trendu

### Sekcja 5: Raport Analityczny (Komórki 36-38)
- Streszczenie wykonawcze
- Wprowadzenie (cel, dane, metodologia)
- Wyniki eksploracyjnej analizy danych
- Interpretacja wyników testów
- Wnioski i rekomendacje
- Załączniki

---

## 🚀 Jak Uruchomić

### Wymagania
```bash
pip install pandas numpy matplotlib scipy openpyxl
```

### Kroki
1. **Klonuj repozytorium:**
   ```bash
   git clone https://github.com/MatiMajewski/Beginners.git
   cd Beginners
   ```

2. **Otwórz Jupyter Notebook:**
   ```bash
   jupyter notebook Wczytywanie\ danych.ipynb
   ```

3. **Uruchom komórki** (Ctrl+Enter lub Run All)

### Dane
- Plik CSV musi być w tym samym katalogu co notebook
- Obsługiwane ścieżki: bieżący katalog, home, Desktop

---

## 📈 Kluczowe Wyniki

### Ranking Województw (Średnia Cena zł)
| Lp. | Województwo | Średnia | Odch. Std | N |
|-----|-------------|--------|-----------|---|
| 1 | Mazowieckie | 455,181 | 89,263 | 15 |
| 2 | Małopolskie | 397,160 | 101,319 | 15 |
| 3 | Pomorskie | 368,528 | 82,803 | 15 |
| 4 | Dolnośląskie | 359,211 | 87,948 | 15 |
| 5 | Zachodniopomorskie | 320,805 | 77,817 | 15 |
| ... | ... | ... | ... | ... |
| 16 | Lubuskie | 220,378 | 63,638 | 15 |

### Jakość Danych (Powiaty)
- **Powiatów całkowicie:** 102
- **Powiatów w analizie (≥3 lata):** 98
- **Powiatów wyeliminowanych:** 4
- **Powód wyeliminowania:** Brak wystarczających punktów danych

---

## 👥 Podział Zadań

| Osoba | Zadanie |
|-------|---------|
| **Dawid** | Wizualizacje, wykresy |
| **Gracjan** | Statystyki opisowe, CAGR |
| **Mateusz** | Przetwarzanie danych, testy statystyczne |

---

## 📚 Metodologia

### Filtrowanie Danych
Zastosowano **kryterium jakości**: każdy powiat musi mieć co najmniej **3 punkty pomiarowe** (różne lata), aby umożliwić wiarygodną analizę trendów.

### Testy Statystyczne (ADRPY2025)
- ✅ **ANOVA** - Test porównujący średnie między grupami
- ✅ **Chi-kwadrat** - Test niezależności zmiennych kategorycznych
- ✅ **Korelacja Pearsona** - Analiza związków liniowych
- ✅ **Regresja liniowa** - Modelowanie trendu czasowego
- ✅ **Przedziały ufności** - Estymacja parametrów populacji

### Miary Trendu
- **CAGR (Compound Annual Growth Rate):** Średnia roczna stopa wzrostu
- **Zmiana procentowa:** Względem pierwszego roku obserwacji

---

## 📊 Wizualizacje

Projekt zawiera **100+ wykresów** w tym:
- 16 wykresów dla województw (trendy czasowe)
- 20 siatek porównawczych (grid plots)
- 98 indywidualnych wykresów powiatów
- 1 wizualizacja trendu liniowego (regresja)

Wszystkie wykresy spełniają standardy wizualizacji danych (clauswilke.com/dataviz).

---

## 💾 Git Historia

```
commit 1c3317f - Dodaj testy statystyczne: ANOVA, chi-kwadrat, korelacja, regresja + strukturę raportu
commit 1c386a9 - Filtruj powiaty: pozostaw tylko 98 z min. 3 lat danych, usuń stare 102 wykresy
```

---

## 📝 Notatki

### Ograniczenia Studium
1. Brak zmiennych uzupełniających (powierzchnia, standard)
2. Dane transakcyjne mogą być obciążone survivalem
3. Okres analiz kończy się w 2024 r.
4. Brak informacji o cenach ofertowych (tylko zawarte)

### Potencjalne Rozszerzenia
- [ ] Machine Learning do przewidywania cen
- [ ] Segmentowana analiza dla każdego województwa
- [ ] Analiza danych geoprzestrzennych (mapy)
- [ ] Test Kruskal-Wallisa (nieparametryczny)
- [ ] Modele ARIMA do prognozy

---

## 📄 Licencja

Projekt na potrzeby kursu akademickiego.

---

## ✉️ Kontakt

GitHub: [MatiMajewski/Beginners](https://github.com/MatiMajewski/Beginners)

---

**Data ostatniej aktualizacji:** 6 stycznia 2026  
**Status:** ✅ Projekt zakończony (ADRPY2025 - 95% wymagań spełnionych)
