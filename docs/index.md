# Omówienie zastosowanych algorytmów steganograficznych

## Character Pair Text Steganography based on the Enhanced Paragraph Approach

### Design
[Source](https://ieeexplore.ieee.org/document/8507117)

#### Embed

```mermaid
flowchart TD

A0([Start]) --> A1[Wczytaj ukrytą wiadomość SM i tekst nośny CT]
A1 --> A2[Konwertuj SM na ciąg bitów]
A2 --> A3[Pobierz kolejne słowo z CT i zapisz je do stego-tekstu]
A3 --> A4[Ustaw L = 1<br/>s = pierwszy znak<br/>e = ostatni znak]
A4 --> A5[s == e?]

A5 -- Tak --> A6[Zwiększ L o 1]
A6 --> A7[Czy są kolejne znaki<br/>dla poziomu L?]
A7 -- Tak --> A8[Ustal s = następny znak od przodu<br/>e = następny znak od tyłu]
A8 --> A5

A7 -- Nie --> A3

A5 -- Nie --> A9[Pobierz kolejny bit x]
A9 --> A10[Bit x == 1?]
A10 -- Tak --> A11[Zapisz e do Stego-Key SK]
A10 -- Nie --> A12[Zapisz s do Stego-Key SK]

A11 --> A13[Zwiększ L o 1]
A12 --> A13

A13 --> A14[Czy są kolejne znaki<br/>dla poziomu L?]
A14 -- Tak --> A15[Ustal s = następny znak od przodu<br/>e = następny znak od tyłu]
A15 --> A5

A14 -- Nie --> A16[Czy są kolejne słowa CT?]
A16 -- Tak --> A3
A16 -- Nie --> A17([Koniec])
```

#### Extract

```mermaid
flowchart TD

B0([Start]) --> B1[Wczytaj Stego-Key SK i Stego-Tekst ST]
B1 --> B2[Pobierz kolejne słowo z ST]
B2 --> B3[Ustaw L = 1<br/>s = pierwszy znak<br/>e = ostatni znak]
B3 --> B4[s == e?]

B4 -- Tak --> B5[Zwiększ L o 1]
B5 --> B6[Czy są kolejne znaki<br/>dla poziomu L?]
B6 -- Tak --> B7[Ustal s = następny znak od przodu<br/>e = następny znak od tyłu]
B7 --> B4

B6 -- Nie --> B16

B4 -- Nie --> B8[Pobierz kolejny znak c z SK]
B8 --> B9[c == s?]

B9 -- Tak --> B10[Zapisz bit 0 do pliku binarnego]
B9 -- Nie --> B11[c == e?]
B11 -- Tak --> B12[Zapisz bit 1 do pliku binarnego]
B11 -- Nie --> B12b[Znak spoza pary — błąd lub pomiń]

B10 --> B13[Zwiększ L o 1]
B12 --> B13
B12b --> B13

B13 --> B14[Czy są kolejne znaki<br/>dla poziomu L?]
B14 -- Tak --> B15[Ustal s = następny znak od przodu<br/>e = następny znak od tyłu]
B15 --> B4

B14 -- Nie --> B16[Czy w SK są jeszcze znaki?]
B16 -- Tak --> B2
B16 -- Nie --> B17[Konwertuj binarny strumień<br/>na tekst jawny]
B17 --> B18([Koniec])
```

### Help
Ograniczenia:

- wsparcie tylko dla ASCII

#### Embed
W polu _Stego File_ należy wpisać Cover Text lub wczytać go z pliku przy użyciu _Load stego file_.
W polu _Secret Message_ należy wpisać wiadomość, która ma zostać ukryta.
Po kliknięciu w przycisk _Embed_, w polu _Key_ pojawi się klucz, za pomocą którego można później odczytać ukrytą wiadomość.

#### Extract
W polu _Stego File_ należy wpisać Cover Text lub wczytać go z pliku przy użyciu _Load stego file_.
W polu _Key_ należy wpisać klucz otrzymany podczas operacji _Embed_.
Po kliknięciu w przycisk _Extract_, w polu _Extracted Secret Message_ pojawi się pierwotnie ukryta wiadomość.

## Unicode For Hiding Information in a Text Document

### Design
[Source](https://ieeexplore.ieee.org/document/9368819)

#### Embed

```mermaid
flowchart TD

A([Start]) --> B[Wczytaj pusty dokument .docx]
B --> C[Pobierz tekst tajny A–Z]
C --> D[Wstaw znacznik początku: kombinacja ZW-ZW-ZW kod 26]
D --> E[Sprawdź pojemność kontenera: liczba spacji >= 3 * długość wiadomości]
E -->|OK| F[Iteruj po literach tajnego tekstu]
E -->|Brak pojemności| Z[Zakończ z błędem]

F --> G[Odczytaj literę]
G --> H[Znajdź jej kod trójkowy THIN=0, HAIR=1, ZW=2 wg tabeli]
H --> I[Zamień 3 kolejne spacje na odpowiednie spacje Unicode]
I --> J[Czy to ostatnia litera?]
J -->|Nie| F
J -->|Tak| K[Wstaw znacznik końca: ZW-ZW-ZW]
K --> L[Zapisz dokument]
L --> M([Koniec])
```

#### Extract

```mermaid
flowchart TD

A([Start]) --> B[Wczytaj dokument .docx]
B --> C[Przeszukaj spacje między słowami]
C --> D[Czy znaleziono znacznik start: ZW-ZW-ZW]
D -->|Nie| C
D -->|Tak| E[Przechodź po kolejnych trójkach spacji]

E --> F[Odczytaj 3 spacje]
F --> G[Konwersja do wartości 0/1/2]
G --> H[Sprawdź czy to kod '26']
H -->|Tak| K([Koniec: zwróć odczytany tekst])
H -->|Nie| I[Zamień kod trójkowy na literę A–Z]
I --> J[Dodaj literę do wyniku]
J --> E
```

### Help
Ograniczenia:

- liczba spacji musi być równa (ILOŚĆ ZNAKÓW TAJNEJ WIADOMOŚCI + 2)
- wsparcie tylko dla znaków ASCII

#### Embed
W polu _Stego File_ należy wpisać Cover Text.
W polu _Secret Message_ należy wpisać wiadomość, która ma zostać ukryta.
Po kliknięciu w przycisk _Embed_, pojawi się okno wyboru ścieżki do zapisania pliku .docx.
Utworzony plik zawiera Cover Text z ukrytą wiadomością.

#### Extract
Najpierw należy wczytać Cover Text z pliku, przy użyciu przycisku _Load stego file_.
Po kliknięciu w przycisk _Extract_, w polu _Extracted Secret Message_ pojawi się pierwotnie ukryta wiadomość.


## Text Steganography on Sundanese Script using Improved Line Shift Coding

### Design
[Source](https://ieeexplore.ieee.org/document/8628471)

#### Embed

```mermaid
flowchart TD

A([Start]) --> B[Wczytaj cover text]
B --> D[Pobierz tajny tekst]
D --> E[Konwersja ASCII na bity]

E --> F[Policz możliwe linie do przesunięcia]
F --> G[Czy liczba linii < liczba bitów?]
G -->|Nie| Z[Odrzuć: brak pojemności]
G -->|Tak| H[Liczba bitów == liczba linii?]

H --> |Nie| I[Dodaj losowe bity]
H --> |Tak| V[Iteruj po liniach]

I --> V

V --> VV[Linia to Pivot]

VV --> |Tak| V
VV --> |Nie| J[Iteruj po bitach]

J --> K[Odczytaj bit]
K --> L[Bit == 1]
K --> M[Bit == 0]
L --> N[Przesuń linię w górę]
M --> O[Przesuń linię w dół]
N --> R[Czy ostatni bit?]
O --> R[Czy ostatni bit?]
R -->|Nie| V
R -->|Tak| S[Normalizacja]
S --> T[Zapisz jako PDF]
T --> U([Koniec])
```

#### Extract

```mermaid
flowchart TD

A([Start]) --> C[Wczytaj plik PDF]
C --> B[Iteruj po liniach]
B --> D[Linia to Pivot?]
D --> |Tak| B
D --> |Nie| F[Porównaj linię z Pivot'em]
F --> G[Linia jest wyżej niż powinna]
F --> V[Linia jest niżej niż powinna]
G --> VV[Bit = 1]
V --> VVV[Bit = 0]
VV --> H[Dodaj bit do bufferu]
VVV --> H[Dodaj bit do bufferu]
H --> I[Czy zebrano wymaganą liczbę bitów?]
I -->|Nie| B
I -->|Tak| J[Konwersja bitów na ASCII]
J --> K[Odtworzenie tajnej wiadomości]
K --> L([Koniec])
```

### Help
Ograniczenia:

- wspracie tylko dla ASCII
- liczba linii Cover Textu musi być równa liczbie bitów tajnej wiadomości

#### Embed
W polu _Stego File_ należy wpisać Cover Text.
W polu _Secret Message_ należy wpisać wiadomość, która ma zostać ukryta.
Po kliknięciu w przycisk _Embed_, pojawi się okno wyboru ścieżki do zapisania pliku .pdf.
Utworzony plik zawiera Cover Text z ukrytą wiadomością.

#### Extract
Najpierw należy wczytać Cover Text z pliku, przy użyciu przycisku _Load stego file_.
Po kliknięciu w przycisk _Extract_, w polu _Extracted Secret Message_ pojawi się pierwotnie ukryta wiadomość.

## A high capacity text steganography scheme based on LZW compression and color coding

### Design
[Source](https://www.sciencedirect.com/science/article/pii/S2215098616301331)

#### Embed

```mermaid
flowchart TB
  V([Start]) --> A[Pobierz tajny komunikat S]
  A --> B[Kompresuj S algorytmem LZW na kody]
  B --> C[Konwersja kodów LZW do strumienia bitów]
  C --> D[Pobierz tekst przykrywający i policz liczbę znaków nie-spacji]
  D --> E[Wyodrębnij z bitstreamu dokładnie tyle bitów, ile znaków ma T na C_t]
  E --> F[Wspólna Tabela Kodowania Kolorami: mapowanie kolor na bit]
  F --> G[Kolorowanie liter w T zgodnie z bitami C_t]
  G --> H[Pozostałe bity podziel na grupy 12-bitowe]
  H --> I["Dla każdej grupy 12bit: podziel na G_1 (9 bitów) i G_2 (3 bity)"]
  I --> J["Oblicz: x = floor(G_1/26), y = G_1 mod 26, z = G_2 (dziesiętnie)"]
  J --> K[Skonwertuj x,y na litery przy użyciu kwadratu łacińskiego i wybierz odpowiednie ID e-mail z klucza K1 oraz utwórz K2]
  K --> L[Z mapowania domen wybierz rozszerzenie e-mail na podstawie z]
  L --> M["Zbuduj nośnik stego: pokolorowany tekst T + listę adresów e-mail (K2)"]
  M --> N[Wyślij stego-wiadomość poprzez system przekazywania e-mail]
  N --> VV([Koniec])
```

#### Extract

```mermaid
flowchart TB
  V([Start]) --> A["Odbierz stego-wiadomość (pokolorowany tekst T + adresy e-mail K2)"]
  A --> B[Z kolorów liter odczytaj bity C_1 zgodnie z Tabelą Kodowania Kolorami]
  B --> C[Iteruj po adresach email]
  C --> VV[Pobierz dwie litery z adresu]
  VV --> VVV[Odzyskaj x i y używając kwadratu łacińskiego]
  VVV --> VVVV[Z rozszerzenia domeny odzyskaj z]
  VVVV --> D["Odtwórz G_1 = (x*26 + y) jako 9 bitów oraz G_2 = z jako 3 bity"]
  D --> VVVVV[To ostatni adres email?]
  VVVVV --> |Nie| C
  VVVVV --> |Tak| E[Połącz wszystkie G_1+G_2 tworząc strumień G]
  E --> F[Połącz C_1 z G]
  F --> G[Dekompresuj LZW]
  G --> H[Wyświetl ukrytą wiadomość]
  H --> I([Koniec])
```

### Help
Ograniczenia:

- wsparcie tylko dla ASCII

Algorytm pozwala ukryć nieskończenie długą wiadomość, ponieważ nawet gdy Cover Text jest za krótki, to wiadomość jest ukrywana w adresach mailowych w CC.

#### Embed
W polu _Stego File_ należy wpisać Cover Text.
W polu _Secret Message_ należy wpisać wiadomość, która ma zostać ukryta.
Po kliknięciu w przycisk _Embed_, pojawi się okno wyboru ścieżki do zapisania plików.
Jeden plik to HTML zawierający Cover Text z ukrytą wiadomością, drugi plik to JSON z listą adresów email, które należy dodać w CC.

#### Extract
Najpierw należy wczytać Cover Text z pliku HTML, przy użyciu przycisku _Load stego file_.
Po kliknięciu w przycisk _Extract_, w polu _Extracted Secret Message_ pojawi się pierwotnie ukryta wiadomość,
a w polu _Email addresses in CC_ pojawią się adresy, które w realnym scenariuszu znajdowałyby się w CC maila.

## An Innovative Text Steganography Technique for Hidden Transmission of Text Message via Social Media

### Design
[Source](https://ieeexplore.ieee.org/document/8440030)

#### Embed

```mermaid
flowchart TB

  V([Start]) --> A["Pobierz tajną wiadomość SM"]
  A --> B["Czy SM jest pusta?"]
  B -->|Tak| B1["Przerwij: brak danych do ukrycia"]
  B -->|Nie| C["Oblicz ASCII η dla każdej litery"]

  C --> D["Zastosuj funkcję Gödela – pary ⟨α,β⟩"]
  D --> E["Konwersja α i β do 6-bit — 12-bit na literę"]
  E --> F["Połącz wszystko — SM_binary"]

  F --> G["Pobierz klucz czasowy MS_SK"]
  G --> H["Czy format czasu poprawny?"]
  H -->|Nie| H1["Przerwij: błąd formatu klucza"]
  H -->|Tak| I["Zamień MS_SK na 8-bit — SK_binary"]

  I --> J["Powiel SK_binary aż pokryje SM_binary — Hash_position_bits"]

  J --> K["Czy długości pasują?"]
  K -->|Nie| K1["Dodaj brakujące bity przez powtórzenia"]
  K -->|Tak| L["XOR + odwracanie — Hashed_SM_binary"]

  L --> M["Zamień każdy 2-bit na odpowiedni ZWC"]
  M --> N["Wygeneruj HM_SK (też w ZWC)"]

  N --> O["Czy rozmiar HM + CM mieści się w limicie aplikacji?"]
  O -->|Nie| O1["Przerwij: limit wiadomości przekroczony"]
  O -->|Tak| P["Połącz HM_SK + HM i umieść przed CM"]

  P --> Q["Zwróć CMHM (gotową wiadomość)"]
  Q --> R(["Koniec"])
```

#### Extarct

```mermaid
flowchart TB
  V([Start]) --> A[Odbierz CMHM]
  A --> B[Czy widoczne są ZWC?]
  B -->|Nie| B1[Przerwij: brak ukrytej treści]
  B -->|Tak| C["Odczytaj ZWC (2-bitowe sekwencje)"]

  C --> D["Wyodrębnij pierwsze 8 bitów (MS_SK)"]
  D --> E[Oblicz własny klucz MR_SK z czasu odbioru]

  E --> F[Czy MS_SK = MR_SK?]
  F -->|Nie| F1[Odrzuć wiadomość: nieprawidłowy klucz]
  F -->|Tak| G[Usuń SK z początku Hashed_SM_binary]

  G --> H[Wygeneruj Hash_position_bits z MR_SK]
  H --> I["Odwróć hash (XOR + odwracanie) otrzymując SM_binary"]

  I --> J[Czy SM_binary długości % 12 = 0?]
  J -->|Nie| J1[Przerwij: strumień uszkodzony]
  J -->|Tak| K[Podziel SM_binary na bloki 12 bitów]

  K --> L[Każdy blok → 6 bitów α + 6 bitów β]
  L --> M["Oblicz η = 2^α(2β+1) − 1"]

  M --> N[Czy η w zakresie ASCII?]
  N -->|Nie| N1[Przerwij: błąd dekodowania]
  N -->|Tak| O[Konwertuj η na znak ASCII]

  O --> P[Łącz znaki kolejno]
  P --> Q[Zwróć odzyskaną wiadomość SM]
  Q --> R([Koniec])
```

### Help
Ograniczenia:

- wsparcie tylko dla ASCII

#### Embed
W polu _Stego File_ należy wpisać Cover Text lub wczytać go z pliku przy użyciu _Load stego file_.
W polu _Secret Message_ należy wpisać wiadomość, która ma zostać ukryta.
W polu _Key_ należy podać klucz symetryczny do szyfrowania.
Po kliknięciu w przycisk _Embed_, pojawi się okno wyboru ścieżki do zapisania pliku .txt.

#### Extract
W polu _Stego File_ należy wczytać Cover Text z pliku przy użyciu _Load stego file_.
W polu _Key_ należy wpisać klucz symetryczny użyty do zaszyfrowania wiadomości.
Po kliknięciu w przycisk _Extract_, w polu _Extracted Secret Message_ pojawi się pierwotnie ukryta wiadomość.

## Custom algorithm

### Design
[Inspiration](https://www.gsc-europa.eu/sites/default/files/sites/all/files/Galileo_OS_SIS_ICD_v2.1.pdf)

#### Embed

```mermaid
flowchart TD
    A([Start]) --> B["Wejście: secret_message, carrier_text"]
    B --> C["Konwersja wiadomości na bity"]
    C --> D["Tekst ASCII 8 bitów/znak"]
    D --> E["Lista bitów wiadomości"]
    E --> F[Czy mamy bity?]
    F -->|Nie| G["Błąd: pusta wiadomość"]
    F -->|Tak| H["Kodowanie splotowe K=7, G1=0o171, G2=0o133"]
    H --> I["Dla każdego bitu wiadomości"]
    I --> J["Oblicz 2 bity wyjścia poly_output G1, poly_output G2"]
    J --> K["Przesunięcie registru stanu"]
    K --> L["Dodaj tail bity K-1=6 zer"]
    L --> M["Lista bitów zakodowanych 2x dłuższa"]
    M --> N[Czy tekst nośny wystarczający?]
    N -->|Nie| O["Błąd: tekst za krótki"]

    N -->|Tak| P["Rozbij tekst na słowa"]
    P --> Q["Dla każdych 2 bitów zakodowanych"]
    Q --> R["bit1, bit2 (lub 0 na końcu)"]
    R --> S["Ukryj w słowie: bit1=homoglif, bit2=marker"]
    S --> T["Jeśli bit1=1: zamień literę na homoglif"]
    T --> U[Czy homoglif znaleziony?]
    U -->|Nie| V["Spróbuj inną literę"]
    V --> U
    U -->|Tak| W["Wstaw marker: bit2=1=MARKER_1, bit2=0=MARKER_0"]
    W --> X["Tekst steganograficzny ze wszystkimi ukrytymi danymi"]
    X --> Y["Zwróć tekst steganograficzny"]
    Y --> Z([Koniec])
```

#### Extract

```mermaid
flowchart TD
    A([Start]) --> B["Wejście: stego_text (tekst z ukrytą wiadomością)"]
    B --> C["Rozbij na słowa split(' ')"]
    C --> D["Lista słów steganograficznych"]
    D --> E["Dla każdego słowa"]
    E --> F["Ekstrahuj bit1: szukaj homoglifu lub cyrylicy"]
    F --> G[Czy znaleziono homoglif?]
    G -->|Tak| H["bit1 = 1"]
    G -->|Nie| I["bit1 = 0"]
    H --> J["Ekstrahuj bit2: szukaj markera"]
    I --> J
    J --> K[Czy MARKER_1 obecny?]
    K -->|Tak| L["bit2 = 1"]
    K -->|Nie| M[Czy MARKER_0 obecny?]
    M -->|Tak| N["bit2 = 0"]
    M -->|Nie| O["bit2 = 0 domyślnie"]
    L --> P["Dodaj bit1, bit2 do listy"]
    N --> P
    O --> P
    P --> Q[Wszystkie słowa przetworzono?]
    Q -->|Nie| E
    Q -->|Tak| R["Dekodowanie Viterbiego"]
    R --> S["Inicjalizuj metryki: state[0]=0, rest=∞"]
    S --> T["Dla każdej pary bitów"]
    T --> U["Dla każdego stanu: oblicz następny stan i metrikę"]
    U --> V[Wszystkie symbole przetworzono?]
    V -->|Nie| T
    V -->|Tak| W["Znajdź best state z minimalną metryką"]
    W --> X["Odczytaj ścieżkę bitów"]
    X --> Y["Usuń tail bity K-1=6"]
    Y --> Z["Konwersja bitów na tekst ASCII"]
    Z --> AA["Filtruj znaki drukowane 32-126"]
    AA --> AB["Zwróć tekst tajny"]
    AB --> AC([Koniec])
```

### Help

Ograniczenia:

- wsparcie tylko dla ASCII

#### Embed
W polu _Stego File_ należy wpisać Cover Text lub wczytać go z pliku przy użyciu _Load stego file_.
W polu _Secret Message_ należy wpisać wiadomość, która ma zostać ukryta.
Po kliknięciu w przycisk _Embed_, pojawi się okno wyboru ścieżki do zapisania pliku .txt.

#### Extract
W polu _Stego File_ należy wczytać Cover Text z pliku przy użyciu _Load stego file_.
Po kliknięciu w przycisk _Extract_, w polu _Extracted Secret Message_ pojawi się pierwotnie ukryta wiadomość.
