# Galileo-CBOC Viterbi Steganographic Algorithm
## Szczegółowe wyjaśnienie działania

**Data:** Listopad 2025  
**Temat:** Dokumentacja algorytmu ukrywania wiadomości z wykorzystaniem kodowania konwolucyjnego i modulacji CBOC  
**Odbiorcy:** Zespół deweloperski

---

## 1. Przegląd ogólny

Algorytm implementuje **trzystopniowy system steganograficzny**:

1. **Kodowanie konwolucyjne (Convolutional Encoding)** — tajną wiadomość kodujemy kodem (171, 133) rate 1/2, tym samym zwiększając odporność na błędy transmisji.
2. **Modulacja CBOC (Composite Binary Offset Carrier)** — zakodowane bity ukrywamy w tekście nośnym (carrier text) przy użyciu homoglifów i niewidzialnych znaków Unicode.
3. **Dekodowanie Viterbi (Viterbi Decoding)** — odbiorca dekoduje wiadomość używając algorytmu Viterbi, który znajduje najprawdopodobniejszą sekwencję bitów.

**Cel:** Bezpiecznie przesłać tajną wiadomość poprzez zwykły tekst w taki sposób, że nieobserwiści nie mogą stwierdzić, że wiadomość w ogóle istnieje.

---

## 2. Składniki systemu

### 2.1 ConvolutionalEncoder

**Co robi?**  
Koduje bity tajnej wiadomości kodem konwolucyjnym o parametrach:
- Generator 1: G1 = 0o171 (binarnie: 1111001)
- Generator 2: G2 = 0o133 (binarnie: 1011011)
- Constraint length: K = 7 (długość rejestru przesuwającego)
- Rate kodu: 1/2 (1 bit wejściowy → 2 bity wyjściowe)

**Parametry Viterbi:**
```
G1 = 0o171 = 0111 1001 (binarnie)
G2 = 0o133 = 0101 1011 (binarnie)
K  = 7 (state register length = K-1 = 6 bitów)
```

**Algorytm enkodowania:**

```
1. Zainicjuj stan = 0 (pusty rejestr)
2. Dla każdego bitu wejściowego:
   a) Utwórz rejestr: [input_bit, bit_stanu[0], ..., bit_stanu[K-2]]
   b) Dla G1: policz output1 = XOR(rejestr[i] AND G1[i] dla wszystkich i)
   c) Dla G2: policz output2 = XOR(rejestr[i] AND G2[i] dla wszystkich i)
   d) Dodaj [output1, output2] do wyniku
   e) Aktualizuj stan: przesunięcie rejestru o 1 pozycję w prawo
3. Flush rejestr: dodaj K-1 zer na wejściu, generując K-1 par bitów (razem K-1)
```

**Przykład:**
```
Wejście: [1, 0, 1] (3 bity)
Enkoder wygeneruje: (3 + 6) * 2 = 18 bitów
Struktura: [bit1_wej1, bit2_wej1, bit1_wej2, bit2_wej2, bit1_wej3, bit2_wej3, 
            flush_bit1, flush_bit2, ..., flush_bit12]
```

**Właściwości:**
- Zwiększa redundancję bitów (2x więcej danych)
- Umożliwia korygowanie błędów transmisji (decoder Viterbi potrafi naprawić aż ~K/2 ≈ 3 błędy w kumulacyjnym otoczeniu)
- Standardowy kod używany w systemach satelitarnych Galileo

---

### 2.2 ViterbiDecoder

**Co robi?**  
Rekonstruuje oryginalną sekwencję bitów wejściowych z nieidelanej (potencjalnie zaszumionej) sekwencji bitów wyjściowych enkodera. Używa algorytmu dynamicznego programowania.

**Parametry:**
- Liczba stanów: `num_states = 2^(K-1) = 2^6 = 64`
- Metryka: Odległość Hamminga (liczba bitów różnych między odebranym a oczekiwanym symbolem)
- Inicjalizacja: Zaczynamy w stanie 0 z metryką 0, pozostałe stany mają metryką ∞

**Algorytm Viterbi (forward pass):**

```
1. Konwertuj bity na symbole (pary): [(b0,b1), (b2,b3), ...]
2. Zainicjuj metryki dla wszystkich 64 stanów (tylko stan 0 ma metrykę 0)
3. Dla każdego symbolu t:
   a) Dla każdego możliwego stanu źródłowego (z skończoną metryką):
      i)   Dla input_bit ∈ {0, 1}:
           - Oblicz następny stan (funkcja przejścia)
           - Oblicz oczekiwane bity wyjściowe dla tego przejścia
           - Policz odległość Hamminga: ile bitów się różni
           - nowa_metryka = stara_metryka + distancja
      ii)  Jeśli nowa_metryka < obecna_metryka[następny_stan]:
           - Zaktualizuj metrykę
           - Zapisz nową najlepszą ścieżkę (poprzednia_ścieżka + [input_bit])
   b) Zamień current_metrics na next_metrics
4. Po ostatnim symbolu: wybierz stan z najmniejszą metryką
5. Traceback: zwróć ścieżkę tego stanu
6. Usuń ostatnie K-1 bitów (flush bits dodane przez enkoder)
```

**Złożoność:**
- Czas: O(T × num_states × 2) = O(T × 128) gdzie T = liczba symboli
- Pamięć: O(T × num_states × średnia_długość_ścieżki) — przechowuje całe ścieżki w historii

**Przykład:**
```
Otrzymane bity: [1,0, 0,1, 1,1, ...]  (symbole: (1,0), (0,1), (1,1), ...)
Dekoder przechodzi przez wszystkie 64 możliwe ścieżki
Wybiera ścieżkę o najmniejszej sumie odległości Hamminga
Zwraca: [1, 1, 0, ...] (oryginalny ciąg bitów bez flush)
```

---

### 2.3 CBOCModulator

**Co robi?**  
Ukrywa zakodowane bity w zwykłym tekście nośnym (carrier text). Każde słowo zawiera 2 bity tajnej informacji.

**Metody ukrywania bitów:**

#### Bit 1 — Homoglify (look-alike znaki)
- Jeśli bit = 1: zamień pierwszą pasującą literę na jej cyryliczny odpowiednik
- Jeśli bit = 0: pozostaw literę bez zmian

Mapa homoglifów:
```
Łacińskie → Cyrylica:
a → а, e → е, o → о, p → р, c → с, y → у, x → х, i → і
A → А, E → Е, O → О, P → Р, C → С, Y → У, X → Х, I → І
(i inne...)
```

**Przykład:**
```
Słowo: "python"
Bit1 = 1, Bit2 = 0
→ Zamień 'p' na 'р' (cyrylica): "рython"
→ Wstaw U+200C (marker dla bit2=0) po 'р': "р‌ython"
Wynik: "р‌ython"  (marker niewidoczny)
```

#### Bit 2 — Zero-width markery
- Wstaw niewidoczny marker zaraz po pierwszym znaku słowa
  - U+200B (Zero Width Space): bit = 1
  - U+200C (Zero Width Non-Joiner): bit = 0

Te znaki są **całkowicie niewidoczne** dla ludzkiego oka, ale komputery mogą je odczytać.

**Modulacja — cały proces:**

```
Input:  bits = [1,0,1,1,0,...], carrier_text = "Ala ma kota i psa..."
Output: stego_text z ukrytymi bitami

Krok 1: Podziel carrier na słowa: ["Ala", "ma", "kota", "i", "psa", ...]
Krok 2: Policz potrzebne słowa = ceil(len(bits)/2)
Krok 3: Dla każdego słowa:
  - Pobierz 2 bity (bit1, bit2)
  - Jeśli bit1=1 i w słowie jest pasująca litera: zamień na cyrylicę
  - Wstaw marker (U+200B lub U+200C) po pierwszym znaku
  - Dodaj zmodyfikowane słowo do wyniku
Krok 4: Połącz słowa spacjami
```

**Demodulacja — odwrotny proces:**

```
Input:  stego_text = "р‌ython ma..."
Output: recovered_bits

Dla każdego słowa:
  - bit1 = 1 jeśli w słowie jest cyrylica (ord 0x0400-0x04FF)
           0 w innym przypadku
  - bit2 = 1 jeśli w słowie jest U+200B
         = 0 jeśli w słowie jest U+200C
         = 0 jeśli nie ma żadnego markera
```

**Problemy i ograniczenia:**
- Edytory mogą usunąć zero-width znaki (normalizacja Unicode)
- Jeśli w słowie brak pasujących liter do cyrylicy a chcemy bit1=1, to bit się **utraci** (brak ostrzeżenia)
- Widoczna zmiana znaków może zwrócić uwagę (homoglify są bardzo podobne, ale mogą być rozpoznane)

---

## 3. Przepływ działania: UKRYWANIE WIADOMOŚCI (hide_message)

**Wejście:**
- `secret_message` — tajny tekst do ukrycia, np. "prezes"
- `carrier_text` — publiczny tekst nośny, np. długi artykuł

**Wyjście:**
- `stego_text` — tekst nośny z ukrytą wiadomością

**Kroków po kroku:**

### Krok 1: Konwersja tekstu na bity

```
secret_message = "prezes"

Dla każdego znaku: zamień na kod ASCII, następnie na 8 bitów (MSB first)
'p' = 112 = 01110000
'r' = 114 = 01110010
'e' = 101 = 01100101
'z' = 122 = 01111010
'e' = 101 = 01100101
's' = 115 = 01110011

message_bits = [0,1,1,1,0,0,0,0, 0,1,1,1,0,0,1,0, 0,1,1,0,0,1,0,1, 
                0,1,1,1,1,0,1,0, 0,1,1,0,0,1,0,1, 0,1,1,1,0,0,1,1]
Razem: 6 znaków × 8 bitów = 48 bitów
```

### Krok 2: Kodowanie konwolucyjne

```
encoder.encode(message_bits)

Input:  48 bitów
Output: (48 + 6) * 2 = 108 bitów  [bo K=7, flush dodaje 6 bitów]
```

**Co się dzieje wewnątrz:**
- Każdy z 48 bitów → 2 bity wyjściowe (rate 1/2)
- Plus 6 bitów flush → 2 bity wyjściowe każdy
- Razem: 54 pary = 108 bitów

Te 108 bitów są teraz **redundantne** — zawierają informacje pozwalające na poprawę błędów.

### Krok 3: Modulacja CBOC

```
modulator.modulate(encoded_bits, carrier_text)

encoded_bits = 108 bitów
Potrzeba słów = ceil(108 / 2) = 54 słowa

Jeśli carrier_text ma mniej niż 54 słowa → ERROR!
Jeśli ma ≥54 → OK, modulujemy
```

**Proces dla każdego słowa:**

```
Dla slowa_1 (pierwsza para bitów):
  bit1 = encoded_bits[0] = 0
  bit2 = encoded_bits[1] = 1
  
  Mamy słowo "System" z carrier_text
  - bit1 = 0 → nie zamieniaj litery
  - bit2 = 1 → wstaw U+200B po pierwszym znaku
  
  Wynik: "S​ystem"  (między S a y jest niewidoczny U+200B)

Dla slowa_2 (druga para):
  bit1 = encoded_bits[2] = 1
  bit2 = encoded_bits[3] = 1
  
  Mamy słowo "nawigacji"
  - bit1 = 1 → zamień pierwszą pasującą (np. 'a' → 'а')
  - bit2 = 1 → wstaw U+200B
  
  Wynik: "н‌авигacji"  (н to cyrylica, U+200B po niej)
```

### Krok 4: Wynik

```
stego_text = "S​ystem н‌awigacji..." 
             (ze wszystkimi ukrytymi markerami)
```

Do oka człowieka tekst wygląda prawie identycznie z oryginałem. Można go wysłać jako zwykłą wiadomość.

---

## 4. Przepływ działania: WYDOBYWANIE WIADOMOŚCI (extract_message)

**Wejście:**
- `stego_text` — tekst z ukrytą wiadomością

**Wyjście:**
- `secret_message` — odzyskana tajna wiadomość

**Kroki po kroku:**

### Krok 1: Demodulacja CBOC

```
received_bits = modulator.demodulate(stego_text)

Dla każdego słowa w stego_text:
  - Szukaj cyrylicy → bit1
  - Szukaj markerów U+200B/U+200C → bit2
  
Wynik: lista bitów (być może z błędami, bo formatowanie mogło zniszczyć markery)
```

**Przykład:**

```
Słowo: "S​ystem"
  - Brak cyrylicy → bit1 = 0
  - Jest U+200B → bit2 = 1
  → Odebrano: [0, 1]

Słowo: "н‌awigacji"
  - Jest cyrylica 'н' → bit1 = 1
  - Jest U+200B → bit2 = 1
  → Odebrano: [1, 1]
```

### Krok 2: Dekodowanie Viterbi

```
decoder.decode(received_bits)

Input:  received_bits (potencjalnie z błędami)
Output: decoded_bits (oryginalne bity, sprzed enkodera)

Wewnątrz:
  - Forward pass Viterbi: znajduje najlepszą ścieżkę
  - Traceback: usuwa K-1 flush bitów
  
Wynik: decoded_bits (~48 bitów, jeśli transmisja była bezpieczna)
```

### Krok 3: Konwersja bitów na tekst

```
_bits_to_text(decoded_bits)

Podziel bity na grupy po 8:
  [0,1,1,1,0,0,0,0] → 112 → 'p'
  [0,1,1,1,0,0,1,0] → 114 → 'r'
  [0,1,1,0,0,1,0,1] → 101 → 'e'
  [0,1,1,1,1,0,1,0] → 122 → 'z'
  [0,1,1,0,0,1,0,1] → 101 → 'e'
  [0,1,1,1,0,0,1,1] → 115 → 's'

Wynik: "prezes"
```

Filtr: zwraca tylko znaki drukowalne ASCII (32-126). Inne ignoruje.

### Krok 4: Wynik

```
recovered_message = "prezes"
```

Porównanie z oryginałem:
```
secret_message   = "prezes"
recovered_message = "prezes"
→ SUKCES! ✅
```

---

## 5. Dane i struktury — wizualizacja

### Transformacja danych przez system

```
┌─────────────────────────────────────────────────────────────────┐
│ SENDER (Wysyłający)                                             │
├─────────────────────────────────────────────────────────────────┤

1. Wiadomość → Bity
   "prezes" 
   ↓ (8 bitów/znak)
   48 bitów
   
2. Bity → Kodowanie konwolucyjne
   48 bitów (rate 1/2)
   ↓ (+ flush K-1=6 bitów)
   108 bitów (zakodowanych)
   
3. Bity → Modulacja CBOC
   108 bitów (2 bity/słowo)
   ↓
   54 słowa (z homogliphami/markerami)
   
4. Słowa + carrier_text
   ↓
   stego_text (publicznie wysłany!)

┌─────────────────────────────────────────────────────────────────┐
│ RECEIVER (Odbierający)                                          │
├─────────────────────────────────────────────────────────────────┤

1. stego_text → Demodulacja CBOC
   54 słowa (czyta homoglify + markery)
   ↓
   108 bitów (możliwe z błędami!)
   
2. Bity (błędne?) → Dekodowanie Viterbi
   108 bitów
   ↓ (Viterbi wybiera najlepszą ścieżkę)
   48 bitów (odtworzone, z korekcją błędów!)
   
3. Bity → Tekst
   48 bitów (8 bitów/znak)
   ↓
   "prezes"
   
4. Wynik
   Wiadomość odzyskana! ✅
```

---

## 6. Złożoność obliczeniowa i wymagania

| Parametr | Wartość | Opis |
|----------|---------|------|
| Constraint length (K) | 7 | Długość rejestru przesuwającego |
| Liczba stanów | 2^(K-1) = 64 | Możliwe stany enkodera |
| Rate kodu | 1/2 | 1 bit → 2 bity (redundancja) |
| Homoglify | 20 znaków | Mapa łacinka → cyrylica |
| Zero-width znaki | 2 markery | U+200B i U+200C |

### Wymogi dla wiadomości

```
Wiadomość o długości N znaków wymaga:

- Bitów oryginalnych:     N × 8
- Bitów po kodowaniu:     (N × 8 + 6) × 2 ≈ N × 16
- Słów w carrier_text:    (N × 16) / 2 = N × 8

Reguła: carrier powinien mieć co najmniej ~8 słów na każdy znak wiadomości
```

**Przykład:** "prezes" (6 znaków) → potrzeba ~48 słów

---

## 7. Potencjalne problemy i ograniczenia

### 7.1 Problemy techniczne

| Problem | Przyczyna | Skutek |
|---------|-----------|--------|
| **Usuwanie ZW znaków** | Edytor lub kanał komunikacyjny normalizuje Unicode | Bit2 zostaje utracony |
| **Brak homoglifu w słowie** | Słowo zawiera tylko cyfry/znaki nieuderzalne | Bit1 nie może być ustawiony na 1 |
| **Hałas transmisji** | Edytowanie tekstu po wysłaniu | Błędy bitów, ale Viterbi potrafi je naprawić (~3-4 błędy) |
| **Widoczne homoglify** | Cyrylica wygląda bardzo podobnie do łaciny | Może być zauważone przy bliższej inspekcji |

### 7.2 Ograniczenia algorytmu

1. **Brak autentykacji** — niemożliwe stwierdzenie, czy wiadomość pochodzi z pewnego źródła
2. **Brak szyfrowania** — wiadomość ukryta, ale nie zaszyfrowana (jeśli ktoś odkryje metodę, przeczyta tekst)
3. **Zależność od carrier** — wymaga odpowiednio długiego tekstu nośnego
4. **Wrażliwość na preprocessing** — Zero-width znaki mogą być usuwane

### 7.3 Założenia implementacji

```
✓ Wiadomość jest ASCII (7-bitowa)
✓ Carrier zawiera wystarczająco słów
✓ Carrier zawiera wystarczająco liter do ukrycia
✓ Kanał transmisji nie usuwa U+200B/U+200C
✓ Kanał transmisji nie zmienia kodowania Unicode
```

---

## 8. Przykładowa sesja end-to-end

```python
# Sender (Wysyłający)
secret = "prezes"
carrier = "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."

stego = GalileoSteganography()
stego_text = stego.hide_message(secret, carrier)
# → stego_text wysłany publicznie

# Receiver (Odbierający)
recovered = stego.extract_message(stego_text)
# → recovered = "prezes" ✅
```

**Logi z wykonania:**

```
🔒 UKRYWANIE WIADOMOŚCI
[1/4] Konwersja wiadomości...
      'prezes' → 48 bitów
[2/4] Kodowanie konwolucyjne...
      48 → 108 bitów (rate 1/2)
[3/4] Modulacja CBOC...
      Potrzeba 54 słów, dostępne: 120
[4/4] Gotowe!

🔓 EKSTRAHOWANIE WIADOMOŚCI
[1/4] Demodulacja CBOC...
      Odebrano 108 bitów
[2/4] Dekodowanie Viterbi...
      Zdekodowano 48 bitów
[3/4] Konwersja do tekstu...
      Wiadomość: 'prezes'
[4/4] Gotowe!

✅ SUKCES! Wiadomość poprawnie ukryta i odzyskana!
```

---

## 9. Optymalizacje i rozszerzenia (do przyszłych wersji)

### Krótkoterminowe
1. **Validacja przy modulacji** — zwracaj błąd jeśli bit1=1 ale brak pasujących liter
2. **Compression** — skompresuj wiadomość przed enkodowaniem (zmniejszy rozmiar carrier)
3. **CRC/checksum** — dodaj sumę kontrolną na końcu wiadomości dla weryfikacji poprawności

### Długoterminowe
1. **Iterleaving** — pomieszaj bity, aby rozciągnąć efekt błędów transmisji
2. **Turbo codes** — bardziej zaawansowany kod, lepszą korekcję błędów
3. **Optymalizacja Viterbi** — backpointer zamiast pełnych ścieżek → mniej pamięci
4. **Szyfrowanie** — dodaj AES lub podobne przed kodowaniem

---

## 10. Streszczenie dla programistów

| Etap | Klasa | Wejście | Wyjście | Czym jest |
|------|-------|---------|---------|-----------|
| 1 | ConvolutionalEncoder | bity | bity ×2 + flush | Koder (171,133) rate 1/2 |
| 2 | CBOCModulator | bity | tekst | Steganografia (homoglify + ZW) |
| 3 | CBOCModulator | tekst | bity | Desteganografia |
| 4 | ViterbiDecoder | bity | bity | Dekoder z korekcją błędów |

**API:**

```python
# Sender
stego = GalileoSteganography()
stego_text = stego.hide_message("tajne_hasło", "tekst nośny...")

# Receiver
message = stego.extract_message(stego_text)
```

---

**Koniec dokumentacji**

Dla pytań technicznych proszę zapoznać się z komentarzami w kodzie źródłowym (`test3.py`).
