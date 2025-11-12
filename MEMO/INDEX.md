# 📚 GALILEO-CBOC VITERBI STEGANOGRAPHY
## Kompleksowa dokumentacja algorytmu — INDEX

**Data:** Listopad 2025  
**Status:** DRAFT → REVIEW  
**Przygotował:** Zespół Deweloperski

---

## 🎯 Jak czytać tę dokumentację?

Dokumentacja została podzielona na **5 głównych dokumentów**, z których każdy jest przeznaczony dla **innej grupy odbiorców**.

Przeczytaj odpowiedni dokument w zależności od Twojej roli:

### 👨‍💼 **Jeśli jesteś: Menadżer / Stakeholder / Podejmujący decyzje**
→ **CZYTAJ: `EXECUTIVE_SUMMARY.txt`** (15 min)

Zawiera:
- Szybkie streszczenie o co chodzi
- Analiza ryzyka i korzyści
- Budżet i ROI
- Rekomendacje dla kierownictwa

---

### 👨‍💻 **Jeśli jesteś: Programista / Deweloper implementujący**
→ **CZYTAJ: `QUICK_REFERENCE.txt`** (10 min) → `ALGORYTM_MEMO.md` (20 min)

Zawiera:
- Quick start (copy-paste kodu)
- API i interfejsy
- Typowe błędy i rozwiązania
- Snippety do integracji

---

### 🔬 **Jeśli jesteś: Specjalista DS / Researcher / Architekt**
→ **CZYTAJ: `ALGORYTM_MEMO.md`** (30 min) → `TECHNICZNY_PRZEGLĄD.txt` (20 min)

Zawiera:
- Krok-po-kroku wyjaśnienie każdego komponentu
- Wizualizacje danych i przepływów
- Złożoność obliczeniowa
- Analiza edge-case'ów

---

### 🧪 **Jeśli jesteś: QA Engineer / Tester**
→ **CZYTAJ: `QUICK_REFERENCE.txt`** (szczególnie sekcja TESTY) → `TECHNICZNY_PRZEGLĄD.txt`

Zawiera:
- Template testów jednostkowych
- Przypadki testowe
- Potencjalne problemy do testowania
- Performance metrics

---

### 📖 **Jeśli chcesz pełne wyjaśnienie (dla dokumentacji)**
→ **CZYTAJ: `ALGORYTM_MEMO.md`** w całości (40 min)

Zawiera:
- Kompletny opis architektury
- Szczegółowy opis każdej klasy
- Pełne przepływy danych
- Założenia i ograniczenia

---

## 📄 Spis dokumentów

| Plik | Rozmiar | Dla kogo | Czas czytania | Typ |
|------|---------|---------|--------------|-----|
| **INDEX.md** | 3KB | WSZYSCY | 5 min | Navigation |
| **QUICK_REFERENCE.txt** | 12KB | Devs + QA | 10 min | Cheat Sheet |
| **ALGORYTM_MEMO.md** | 25KB | Architekci + Devs | 40 min | Full Documentation |
| **TECHNICZNY_PRZEGLĄD.txt** | 18KB | QA + Researchers | 20 min | Technical Deep Dive |
| **EXECUTIVE_SUMMARY.txt** | 15KB | Menadżerowie | 15 min | Business + Strategy |

---

## 🚀 Quick Start (90 sekund)

Jeśli jesteś programistą i chcesz szybko uruchomić:

```python
from test3 import GalileoSteganography

# Stwórz instancję
stego = GalileoSteganography()

# UKRYWANIE
secret_msg = "prezes"
carrier_text = "Lorem ipsum dolor sit amet consectetur adipiscing elit " * 10
stego_text = stego.hide_message(secret_msg, carrier_text)

# WYDOBYWANIE
recovered = stego.extract_message(stego_text)

assert recovered.strip() == secret_msg  # ✅ Success!
```

**Wymagania:** Python 3.6+, żadnych innych zależności (numpy jest importowany ale nie używany)

---

## 🎓 Koncepty kluczowe (1 minuta)

Algorytm robi 3 rzeczy:

1. **Kodowanie konwolucyjne** (171, 133)
   - Zamienia N bitów → 2N bitów (redundancja)
   - Pozwala na poprawę błędów transmisji
   - Parametry: K=7, 64 stany

2. **Modulacja CBOC** (Composite Binary Offset Carrier)
   - Ukrywa 2 bity na słowo:
     - Bit 1: homoglify (łacina → cyrylica)
     - Bit 2: zero-width znaki (U+200B / U+200C)
   - Tekst wyglądał prawie identycznie dla oka

3. **Dekodowanie Viterbi**
   - Odtwarza oryginalny tekst z potencjalnie błędnych bitów
   - Metoda: dynamic programming na 64 stanach
   - Potrafi naprawić ~3-4 błędy bitów

**Rezultat:** Tajna wiadomość w publicznym tekście, niezauważalna.

---

## 🔍 Struktura katalogów

```
/home/tux/test/
├── test3.py                      # Kod źródłowy algorytmu
├── INDEX.md                      # TY JESTEŚ TUTAJ
├── QUICK_REFERENCE.txt           # Dla developerów (quick lookup)
├── ALGORYTM_MEMO.md             # Pełna dokumentacja
├── TECHNICZNY_PRZEGLĄD.txt       # Głębokie wyjaśnienie
├── EXECUTIVE_SUMMARY.txt         # Dla menadżerów
├── test.py                       # (ignoruj - test files)
├── test2.py                      # (ignoruj - test files)
└── .venv/                        # Python venv (ignoruj)
```

---

## 📊 Szybka diagnoza problemu

**Nie wiem od czego zacząć:**
→ Przeczytaj **QUICK_REFERENCE.txt** (sekcja "Quick Start")

**Muszę zintegrować z naszym systemem:**
→ Przeczytaj **QUICK_REFERENCE.txt** (sekcja "Integracja")

**Chcę zrozumieć jak to działa wewnątrz:**
→ Przeczytaj **ALGORYTM_MEMO.md** (sekcja "Przepływ hide_message")

**Mam błąd lub problem z performacją:**
→ Przeczytaj **QUICK_REFERENCE.txt** (sekcja "Common Pitfalls")

**Muszę testować to systematycznie:**
→ Przeczytaj **QUICK_REFERENCE.txt** (sekcja "Testy jednostkowe")

**Musimy zdecydować czy wdrażać:**
→ Przeczytaj **EXECUTIVE_SUMMARY.txt** (całość)

---

## ⚠️ Ważne uwagi zanim zaczniesz

### 1. **Wymogi dla carrier_text**

Carrier musi mieć wystarczająco słów:

```
Dla wiadomości N znaków potrzeba: (N × 8 + 6) słów

Przykład:
  "prezes" (6 znaków) → 54 słowa
  "hello" (5 znaków) → 46 słów
  "A" (1 znak) → 14 słów
```

Jeśli carrier ma za mało: `ValueError`

### 2. **Zero-width znaki mogą być usunięte**

Edytory lub kanały komunikacyjne mogą usunąć U+200B/U+200C:
- Powodem: normalizacja Unicode
- Skutek: bit2 zostaje utracony
- Rozwiązanie: Viterbi potrafi naprawić do 4 błędy

### 3. **Homoglify mogą być zauważone**

Cyrylica wygląda bardzo podobnie do łaciny, ale nie identycznie:
- 'а' (cyrylica) vs 'a' (łacina) - bardzo podobne
- 'с' (cyrylica) vs 'c' (łacina) - bardzo podobne
- Przy bliższej inspekcji może zostać zauważone

### 4. **Obsługiwane tylko ASCII (7-bit)**

Unicode znaki (>127) są obcinane w `_bits_to_text()`:
- Rozwiązanie: dodaj UTF-8 support (v1.1)

---

## 🛠️ Troubleshooting

| Problem | Rozwiązanie |
|---------|------------|
| `ValueError: Za mało słów!` | Zwiększ carrier_text (dodaj słowa) |
| `recovered != secret` | Viterbi nie zdołał naprawić błędów (>4 błędy bitów) |
| Mnóstwo błędów składni | Sprawdzić czy Python 3.6+ |
| Import error `numpy` | Zainstaluj: `pip install numpy` (jest ignorowany) |
| Homoglify widoczne | Normalne - cyrylica wygląda bardzo podobnie |
| Zero-width znaki znikają | Editor usunął je - Viterbi próbuje naprawić |

---

## 📞 Kontakty

- **Pytania techniczne (kod):** Sprawdź `QUICK_REFERENCE.txt`
- **Pytania biznesowe (wdrażanie):** Przeczytaj `EXECUTIVE_SUMMARY.txt`
- **Pytania o algorytm (teoria):** Przeczytaj `ALGORYTM_MEMO.md`

---

## 🎯 Recommended Reading Order

Jeśli masz 1 godzinę na zapoznanie się całą dokumentacją:

1. **5 min** - Ten plik (INDEX.md) - JESTEŚ TUTAJ
2. **15 min** - `EXECUTIVE_SUMMARY.txt` - Co to jest i po co
3. **10 min** - `QUICK_REFERENCE.txt` - Jak to używać
4. **20 min** - `ALGORYTM_MEMO.md` (sekcje 1-4) - Jak to działa
5. **10 min** - `TECHNICZNY_PRZEGLĄD.txt` - Szczegóły techniczne

**Total: ~60 minut → masz kompletne zrozumienie!**

---

## 📈 Wersjonowanie

| Wersja | Data | Status | Uwagi |
|--------|------|--------|-------|
| 1.0 | Listopad 2025 | **DRAFT** | Prototyp funkcjonalny |
| 1.1 | Planowana | Zaplanowana | UTF-8, compression, CRC |
| 2.0 | Mid 2026 | Koncepcja | Multi-format, Cloud API |

Bieżąca wersja: **1.0 (DRAFT)**

---

## ✅ Checklist dla nowego członka zespołu

Zanim zaczniesz pracować nad tym projektem:

- [ ] Przeczytałem `QUICK_REFERENCE.txt` (sekcja Quick Start)
- [ ] Uruchomiłem kod - `hide_message()` i `extract_message()` działają
- [ ] Zrozumiałem wymóg: carrier musi mieć ≥ 8N+6 słów
- [ ] Sprawdziłem `ALGORYTM_MEMO.md` (sekcje 2-4) dla zrozumienia architektury
- [ ] Przygotowuję pull request z testami + kodem
- [ ] Kontaktowałem się z tech leadem przed zmianami w core

---

## 🔗 Linki do sekcji dokumentów

### W QUICK_REFERENCE.txt
- [Quick Start](#) - Copy-paste code
- [Cheat Sheet — Parametry](#) - Stałe i zmienne
- [Rozmiary Danych](#) - Ile skoków potrzebujesz
- [Typowe Problemy](#) - Common pitfalls
- [Testy Jednostkowe](#) - Template testów

### W ALGORYTM_MEMO.md
- [Przegląd Ogólny](#) - CO to jest
- [Składniki Systemu](#) - Każda klasa
- [Przepływ Ukrywania](#) - Hide message krok po kroku
- [Przepływ Wydobywania](#) - Extract message krok po kroku
- [Problemy i Ograniczenia](#) - Co się może źle pójść

### W TECHNICZNY_PRZEGLĄD.txt
- [Schemat Blokowy](#) - Wizualizacja
- [Algorytm Viterbi](#) - Pseudo-kod
- [Złożoność](#) - Performance analysis
- [Lista Kontrolna](#) - Co implementować

### W EXECUTIVE_SUMMARY.txt
- [Szybkie Fakty](#) - TL;DR
- [Analiza Ryzyka](#) - Co może pójść nie tak
- [Roadmap](#) - Przyszłe wersje
- [Budżet](#) - Koszty implementacji

---

## 🎓 Learning Path

### Dla pragmatyka (chcę zaraz używać)
```
QUICK_REFERENCE.txt → kod → testuj
(30 minut)
```

### Dla inżyniera (muszę zrozumieć)
```
ALGORYTM_MEMO.md (całość) → testuj → kod
(60 minut)
```

### Dla architekta (designing system)
```
EXECUTIVE_SUMMARY.txt → ALGORYTM_MEMO.md → TECHNICZNY_PRZEGLĄD.txt
(90 minut)
```

### Dla kierownika (decyzje biznesowe)
```
EXECUTIVE_SUMMARY.txt → budżet/timeline
(30 minut)
```

---

## 📝 Notacja używana w dokumentach

Symbole i konwencje:

```
✓  = Zrealizowane / OK / wspierane
✗  = Nie zrealizowane / Problem / nie wspierane
⚠️  = Uwaga / ograniczenie
🎯 = Cel / rekomendacja
📈 = Wzrost / poprawa
🔓 = Bezpieczeństwo / ryzyko
```

Kod w sekcjach:

```python
# Python snippety - copy-paste ready
def example():
    return "code"
```

ASCII art:

```
┌─────────────┐
│   Komponenty│
└─────────────┘
```

Tabele:

| Kolumna 1 | Kolumna 2 |
|-----------|----------|
| Wartość   | Opis     |

---

## 🚀 Next Steps dla zespołu

**Dla Tech Lead:**
1. [ ] Przeczytać ALGORYTM_MEMO.md (całość)
2. [ ] Code review test3.py
3. [ ] Zatwierdzić plan v1.1 (UTF-8, compression)
4. [ ] Setup CI/CD pipeline

**Dla Programistów:**
1. [ ] Przeczytać QUICK_REFERENCE.txt
2. [ ] Klonować repo i uruchomić `test3.py`
3. [ ] Napisać własny test (`test_my_case()`)
4. [ ] Zaproponować улучшения

**Dla QA:**
1. [ ] Przeczytać TECHNICZNY_PRZEGLĄD.txt (sekcja testy)
2. [ ] Przygotować test plan
3. [ ] Uruchomić test case'y
4. [ ] Zgłosić bugów (jeśli jakieś)

**Dla PM:**
1. [ ] Przeczytać EXECUTIVE_SUMMARY.txt (całość)
2. [ ] Przygotować komunikat dla stakeholderów
3. [ ] Setup meeting z klientami
4. [ ] Plan dla roadmap'u

---

## 📚 Referencje i dalsze czytanie

### Teoretyczne
- Viterbi, A. J. "Error bounds for convolutional codes" (1967)
- Berlekamp, E. "Algebraic Coding Theory" (1968)
- Galileo ICD (Interface Control Document)

### Praktyczne
- Wikipedia: Convolutional codes
- Wikipedia: Viterbi algorithm
- Wikipedia: Steganography

### Narzędzia
- Python 3.6+
- Git
- pytest (do testów)

---

## 💾 Jak używać tę dokumentację w zespole

### Przechowywanie
- Wszystkie pliki w repozytorium `/docs/` lub root
- Wersjonuj wraz z kodem (git)
- Update dokumentacji = część każdego PR

### Udostępnianie
- GitHub: Pull Requests wołają na `QUICK_REFERENCE.txt`
- Wiki: Link do `ALGORYTM_MEMO.md` dla architektu
- Slack: Share `EXECUTIVE_SUMMARY.txt` dla stakeholderów

### Aktualizacja
- Gdy zmienisz kod → update dokumentacji
- Gdy dodasz feature → update sekcji Roadmap
- Gdy znajdziesz bug → update sekcji "Common Pitfalls"

---

## 🎉 Koniec!

Jesteś gotów do pracy z algorytmem Galileo-CBOC Viterbi Steganography! 

**Pytania?** Sprawdź appropriate dokument w tabelce wyżej.

**Gotów zacząć?** → QUICK_REFERENCE.txt

**Chcesz głębokie zrozumienie?** → ALGORYTM_MEMO.md

Powodzenia! 🚀

---

**Dokument:** INDEX.md  
**Wersja:** 1.0  
**Data:** Listopad 2025  
**Status:** DRAFT → REVIEW  
**Autor:** Zespół Deweloperski  

*Last updated: 2025-11-12*
