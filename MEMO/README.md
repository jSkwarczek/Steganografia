# 📦 GALILEO-CBOC VITERBI STEGANOGRAPHY

> Algorytm ukrywania tajnych wiadomości w zwykłym tekście z wykorzystaniem kodowania konwolucyjnego i modulacji CBOC.

## 🚀 Quick Start (30 sekund)

```python
from test3 import GalileoSteganography

stego = GalileoSteganography()

# Ukryj wiadomość w tekście nośnym
stego_text = stego.hide_message(
    secret="prezes",
    carrier_text="Lorem ipsum dolor sit amet consectetur adipiscing elit " * 10
)

# Wydobądź wiadomość
recovered = stego.extract_message(stego_text)
# recovered = "prezes" ✅
```

## 📚 Dokumentacja

Wybierz dokument w zależności od Twojej roli:

| Rola | Dokument | Czas | Zawartość |
|------|----------|------|-----------|
| 🚀 **Zaraz zaczynam** | [`QUICK_REFERENCE.txt`](./QUICK_REFERENCE.txt) | 10 min | Copy-paste, API, tips |
| 👨‍💻 **Programista** | [`ALGORYTM_MEMO.md`](./ALGORYTM_MEMO.md) | 40 min | Pełna dokumentacja |
| 🔬 **Architekt/Researcher** | [`TECHNICZNY_PRZEGLĄD.txt`](./TECHNICZNY_PRZEGLĄD.txt) | 20 min | Deep dive, złożoność |
| 👨‍💼 **Menadżer** | [`EXECUTIVE_SUMMARY.txt`](./EXECUTIVE_SUMMARY.txt) | 15 min | Business, ROI, roadmap |
| 🗺️ **Navigation** | [`INDEX.md`](./INDEX.md) | 5 min | Guide do całej dokumentacji |

**Nie wiesz od czego zacząć?** → Czytaj [`INDEX.md`](./INDEX.md) (5 minut)

## 🎯 Co to robi?

System ukrywa tajną wiadomość w publicznym tekście za pomocą trzech technik:

1. **Kodowanie konwolucyjne** (171, 133)
   - Zwiększa redundancję bitów 2x
   - Umożliwia korekcję błędów

2. **Modulacja CBOC**
   - Homoglify: zamiana liter na cyrylicę (bit1)
   - Zero-width znaki: niewidzialne markery (bit2)
   - 2 bity na słowo tekstu nośnego

3. **Dekodowanie Viterbi**
   - Odtwarzanie oryginalnego tekstu
   - Poprawa błędów transmisji (~3-4 błędy)

**Rezultat:** Wiadomość "prezes" ukryta w publicznym artykule, niezauważalna dla oka.

## ⚡ Wymagania

```
Python 3.6+
Bez dodatkowych zależności (numpy jest importowany ale nieużywany)
```

## 📊 Parametry

| Parametr | Wartość | Opis |
|----------|---------|------|
| Generator 1 | 0o171 | Kod konwolucyjny |
| Generator 2 | 0o133 | Kod konwolucyjny |
| Constraint length | K=7 | Długość rejestru |
| Liczba stanów | 64 | 2^(K-1) |
| Rate | 1/2 | 1 bit → 2 bity |
| Bity/słowo | 2 | Homoglyf + ZW marker |

## 💾 Wymogi dla tekstu nośnego

```
Dla wiadomości N znaków potrzeba minimum:
  Words ≥ N × 8 + 6

Przykłady:
  "prezes" (6 znaków) → 54 słowa minimum
  "test" (4 znaki) → 38 słów minimum
  "A" (1 znak) → 14 słów minimum
```

## ⚠️ Ograniczenia (v1.0)

- ✓ Obsługiwane: ASCII (7-bitowe znaki)
- ✗ Brak: UTF-8 support (v1.1)
- ✗ Brak: szyfrowania (opcjonalne AES w v1.2)
- ⚠️ Zero-width znaki mogą być usunięte przez edytory
- ⚠️ Homoglify mogą być zauważone przy bliższej inspekcji

## 🧪 Testy

```bash
# Uruchom kod (zawiera wbudowany test)
python test3.py

# Oczekiwany wynik:
# ✅ SUKCES! Wiadomość poprawnie ukryta i odzyskana!
```

## 📈 Performance

| Operacja | Czas |
|----------|------|
| hide_message("prezes") | ~6ms |
| extract_message() | ~12ms |
| **Total round-trip** | **~18ms** |

## 🔧 API

### Główna klasa

```python
stego = GalileoSteganography(debug=False)
```

### Publiczne metody

```python
# Ukrywanie wiadomości
stego_text = stego.hide_message(
    secret_message: str,
    carrier_text: str
) -> str

# Wydobywanie wiadomości
message = stego.extract_message(
    stego_text: str
) -> str
```

### Utility metody

```python
bits = stego._text_to_bits(text: str) -> List[int]
text = stego._bits_to_text(bits: List[int]) -> str
```

## 🛠️ Komponenty

### ConvolutionalEncoder
- Koduje bity kodem (171, 133)
- Rate 1/2 (1 bit → 2 bity)
- K=7 (6-bitowy rejestr + 1 wejście)

### ViterbiDecoder
- Dekoduje z poprawą błędów
- 64 stany, metrika Hamminga
- Potrafi naprawić ~3-4 błędy bitów

### CBOCModulator
- Ukrywa bity w tekście
- Homoglify (łacina ↔ cyrylica)
- Zero-width znaki (U+200B, U+200C)

## 📝 Struktura projektu

```
/home/tux/test/
├── test3.py                     ← Kod źródłowy
├── README.md                    ← Ty jesteś tutaj
├── INDEX.md                     ← Mapa dokumentacji
├── QUICK_REFERENCE.txt          ← Dla developerów
├── ALGORYTM_MEMO.md            ← Pełna dokumentacja
├── TECHNICZNY_PRZEGLĄD.txt      ← Deep dive
└── EXECUTIVE_SUMMARY.txt        ← Dla biznesu
```

## 🚀 Roadmap

- **v1.0** (bieżąca) - Prototyp funkcjonalny
- **v1.1** - UTF-8, compression, CRC
- **v1.2** - AES encryption, Turbo codes
- **v2.0** - Multi-format (images, audio), Cloud API

## 🤝 Contribution

1. Czytaj [`ALGORYTM_MEMO.md`](./ALGORYTM_MEMO.md) aby zrozumieć kod
2. Sprawdź [`QUICK_REFERENCE.txt`](./QUICK_REFERENCE.txt) dla API
3. Dodaj testy do Twojego PR
4. Kontaktuj tech lead'a przed zmianami w core

## 📞 Wsparcie

- **Techniczne:** Sprawdzić `QUICK_REFERENCE.txt`
- **Architektura:** Przeczytać `ALGORYTM_MEMO.md`
- **Biznes:** Sprawdzić `EXECUTIVE_SUMMARY.txt`
- **Navigation:** Czytać `INDEX.md`

## 📄 Licencja

Do określenia

---

**Wersja:** 1.0  
**Status:** DRAFT → REVIEW  
**Data:** Listopad 2025

Zacznij od [`QUICK_REFERENCE.txt`](./QUICK_REFERENCE.txt) 🚀
