#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Galileo-CBOC Viterbi Steganographic Algorithm
Ukrywanie tekstu w tekście z wykorzystaniem technik dekodowania sygnału Galileo
"""

import numpy as np
from typing import List, Tuple, Dict


class ConvolutionalEncoder:
    """Koder konwolucyjny (171, 133) jak w Galileo I/NAV"""
    
    def __init__(self):
        self.G1 = 0o171  # 1111001 binary
        self.G2 = 0o133  # 1011011 binary
        self.K = 7       # Constraint length
        
    def _polynomial_output(self, state: int, input_bit: int, poly: int) -> int:
        """Oblicza bit wyjściowy dla danego wielomianu"""
        # Stan + nowy bit tworzą rejestr
        register = input_bit
        for i in range(self.K - 1):
            register = (register << 1) | ((state >> i) & 1)
        
        # XOR wszystkich bitów wskazanych przez wielomian
        output = 0
        temp = register & poly
        while temp:
            output ^= (temp & 1)
            temp >>= 1
        
        return output
    
    def encode(self, bits: List[int]) -> List[int]:
        """Koduje sekwencję bitów"""
        state = 0
        encoded = []
        
        for bit in bits:
            # Oblicz oba bity wyjściowe
            out1 = self._polynomial_output(state, bit, self.G1)
            out2 = self._polynomial_output(state, bit, self.G2)
            encoded.extend([out1, out2])
            
            # Aktualizuj stan (przesunięcie rejestru)
            state = ((bit << (self.K - 2)) | (state >> 1))
        
        # Flush register - dodaj K-1 zer
        for _ in range(self.K - 1):
            out1 = self._polynomial_output(state, 0, self.G1)
            out2 = self._polynomial_output(state, 0, self.G2)
            encoded.extend([out1, out2])
            state = (state >> 1)
        
        return encoded


class ViterbiDecoder:
    """Dekoder Viterbi dla kodu (171, 133)"""
    
    def __init__(self):
        self.G1 = 0o171
        self.G2 = 0o133
        self.K = 7
        self.num_states = 2 ** (self.K - 1)  # 64 stany
        self.encoder = ConvolutionalEncoder()
    
    def _get_output_for_transition(self, from_state: int, input_bit: int) -> Tuple[int, int]:
        """Oblicza para bitów wyjściowych dla przejścia"""
        out1 = self.encoder._polynomial_output(from_state, input_bit, self.G1)
        out2 = self.encoder._polynomial_output(from_state, input_bit, self.G2)
        return (out1, out2)
    
    def _next_state(self, state: int, input_bit: int) -> int:
        """Oblicza następny stan"""
        return ((input_bit << (self.K - 2)) | (state >> 1))
    
    def decode(self, received_bits: List[int]) -> List[int]:
        """Dekoduje sekwencję używając algorytmu Viterbi"""
        # Upewnij się że parzysta liczba bitów
        if len(received_bits) % 2 != 0:
            received_bits = received_bits[:-1]
        
        if len(received_bits) == 0:
            return []
        
        # Konwertuj na symbole (pary bitów)
        symbols = [(received_bits[i], received_bits[i+1]) 
                   for i in range(0, len(received_bits), 2)]
        
        # Inicjalizacja metryk
        current_metrics = [float('inf')] * self.num_states
        current_metrics[0] = 0  # Zaczynamy od stanu 0
        
        # Przechowuj całą historię dla traceback
        paths = [[[] for _ in range(self.num_states)] for _ in range(len(symbols) + 1)]
        metrics_history = [[float('inf')] * self.num_states for _ in range(len(symbols) + 1)]
        metrics_history[0][0] = 0
        
        # Forward pass
        for t, symbol in enumerate(symbols):
            next_metrics = [float('inf')] * self.num_states
            next_paths = [[] for _ in range(self.num_states)]
            
            for state in range(self.num_states):
                if current_metrics[state] == float('inf'):
                    continue
                
                # Próbuj oba możliwe bity wejściowe
                for input_bit in [0, 1]:
                    # Oblicz następny stan i oczekiwane wyjście
                    next_state = self._next_state(state, input_bit)
                    expected = self._get_output_for_transition(state, input_bit)
                    
                    # Metryka Hamminga
                    distance = (symbol[0] != expected[0]) + (symbol[1] != expected[1])
                    new_metric = current_metrics[state] + distance
                    
                    # Update jeśli lepsza ścieżka
                    if new_metric < next_metrics[next_state]:
                        next_metrics[next_state] = new_metric
                        next_paths[next_state] = paths[t][state] + [input_bit]
            
            current_metrics = next_metrics
            paths[t + 1] = next_paths
            metrics_history[t + 1] = next_metrics
        
        # Traceback - znajdź najlepszą końcową ścieżkę
        best_metric = float('inf')
        best_path = []
        
        for state in range(self.num_states):
            if current_metrics[state] < best_metric:
                best_metric = current_metrics[state]
                best_path = paths[len(symbols)][state]
        
        # Usuń flush bits (ostatnie K-1)
        if len(best_path) >= self.K - 1:
            best_path = best_path[:-(self.K - 1)]
        
        return best_path


class CBOCModulator:
    """Modulator CBOC - ukrywanie bitów w tekście"""
    
    # Markery dla bitów
    MARKER_1 = '​'  # U+200B Zero Width Space
    MARKER_0 = '‌'  # U+200C Zero Width Non-Joiner
    
    # Homoglyfy
    HOMOGLYPHS = {
        'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с',
        'y': 'у', 'x': 'х', 'i': 'і', 'j': 'ј', 's': 'ѕ',
        'A': 'А', 'E': 'Е', 'O': 'О', 'P': 'Р', 'C': 'С',
        'Y': 'У', 'X': 'Х', 'I': 'І', 'J': 'Ј', 'S': 'Ѕ',
    }
    
    REVERSE_HOMOGLYPHS = {v: k for k, v in HOMOGLYPHS.items()}
    
    def __init__(self):
        pass
    
    def modulate(self, bits: List[int], carrier_text: str) -> str:
        """Moduluje bity do tekstu - 2 bity na słowo"""
        words = carrier_text.split()
        needed_words = (len(bits) + 1) // 2
        
        if len(words) < needed_words:
            raise ValueError(f"Za mało słów! Potrzeba {needed_words}, mamy {len(words)}")
        
        result = []
        bit_idx = 0
        
        for word in words:
            if bit_idx >= len(bits):
                result.append(word)
                continue
            
            # Pobierz 2 bity
            bit1 = bits[bit_idx] if bit_idx < len(bits) else 0
            bit2 = bits[bit_idx + 1] if bit_idx + 1 < len(bits) else 0
            bit_idx += 2
            
            # Ukryj w słowie
            modulated = self._hide_bits_in_word(word, bit1, bit2)
            result.append(modulated)
        
        return ' '.join(result)
    
    def _hide_bits_in_word(self, word: str, bit1: int, bit2: int) -> str:
        """Ukrywa 2 bity w słowie"""
        if len(word) == 0:
            return word
        
        chars = list(word)
        
        # Bit 1: Homoglyf w pierwszej pasującej literze
        if bit1 == 1:
            for i, char in enumerate(chars):
                if char in self.HOMOGLYPHS:
                    chars[i] = self.HOMOGLYPHS[char]
                    break
        
        # Bit 2: Zero-width marker po pierwszej literze
        marker = self.MARKER_1 if bit2 == 1 else self.MARKER_0
        chars.insert(1, marker)
        
        return ''.join(chars)
    
    def demodulate(self, stego_text: str) -> List[int]:
        """Ekstrahuje bity z tekstu"""
        words = stego_text.split()
        bits = []
        
        for word in words:
            bit1, bit2 = self._extract_bits_from_word(word)
            bits.extend([bit1, bit2])
        
        return bits
    
    def _extract_bits_from_word(self, word: str) -> Tuple[int, int]:
        """Ekstrahuje 2 bity ze słowa"""
        if len(word) == 0:
            return (0, 0)
        
        # Bit 1: Szukaj homoglyfu (cyrylicy)
        bit1 = 0
        for char in word:
            if char in self.REVERSE_HOMOGLYPHS or (0x0400 <= ord(char) <= 0x04FF):
                bit1 = 1
                break
        # Bit 2: Szukaj zero-width markera
        bit2 = 0
        if self.MARKER_1 in word:
            bit2 = 1
        elif self.MARKER_0 in word:
            bit2 = 0
        
        return (bit1, bit2)


class GalileoSteganography:
    """Główna klasa steganografii Galileo-CBOC-Viterbi"""
    
    def __init__(self, debug: bool = False):
        self.encoder = ConvolutionalEncoder()
        self.decoder = ViterbiDecoder()
        self.modulator = CBOCModulator()
        self.debug = debug
    
    def _text_to_bits(self, text: str) -> List[int]:
        """Konwertuje tekst na bity"""
        bits = []
        for char in text:
            byte_val = ord(char)
            for i in range(8):
                bits.append((byte_val >> (7 - i)) & 1)
        return bits
    
    def _bits_to_text(self, bits: List[int]) -> str:
        """Konwertuje bity na tekst"""
        # Uzupełnij do wielokrotności 8
        while len(bits) % 8 != 0:
            bits.append(0)
        
        chars = []
        for i in range(0, len(bits), 8):
            byte_val = 0
            for j in range(8):
                if i + j < len(bits):
                    byte_val = (byte_val << 1) | bits[i + j]
            
            # Pomiń null bytes i nieprawidłowe znaki
            if 32 <= byte_val <= 126:  # Printable ASCII
                chars.append(chr(byte_val))
        
        return ''.join(chars)
    
    def hide_message(self, secret_message: str, carrier_text: str) -> str:
        """Ukrywa wiadomość w tekście"""
        print(f"[1/4] Konwersja wiadomości...")
        message_bits = self._text_to_bits(secret_message)
        print(f"      '{secret_message}' → {len(message_bits)} bitów")
        
        if self.debug:
            print(f"      Bity: {message_bits[:32]}...")
        
        print(f"[2/4] Kodowanie konwolucyjne...")
        encoded_bits = self.encoder.encode(message_bits)
        print(f"      {len(message_bits)} → {len(encoded_bits)} bitów (rate 1/2)")
        
        if self.debug:
            print(f"      Zakodowane: {encoded_bits[:32]}...")
        
        print(f"[3/4] Modulacja CBOC...")
        words_needed = (len(encoded_bits) + 1) // 2
        words_available = len(carrier_text.split())
        print(f"      Potrzeba {words_needed} słów, dostępne: {words_available}")
        
        if words_needed > words_available:
            raise ValueError(f"Za krótki tekst nośny! Potrzeba ≥{words_needed} słów")
        
        modulated_text = self.modulator.modulate(encoded_bits, carrier_text)
        print(f"[4/4] Gotowe!")
        
        return modulated_text
    
    def extract_message(self, stego_text: str) -> str:
        """Ekstrahuje wiadomość z tekstu"""
        print(f"[1/4] Demodulacja CBOC...")
        received_bits = self.modulator.demodulate(stego_text)
        print(f"      Odebrano {len(received_bits)} bitów")
        
        if self.debug:
            print(f"      Odebrane bity: {received_bits[:32]}...")
        
        print(f"[2/4] Dekodowanie Viterbi...")
        decoded_bits = self.decoder.decode(received_bits)
        print(f"      Zdekodowano {len(decoded_bits)} bitów")
        
        if self.debug:
            print(f"      Zdekodowane bity: {decoded_bits[:32]}...")
        
        print(f"[3/4] Konwersja do tekstu...")
        message = self._bits_to_text(decoded_bits)
        print(f"      Wiadomość: '{message}'")
        
        print(f"[4/4] Gotowe!")
        return message


def main():
    print("=" * 70)
    print("Galileo-CBOC Viterbi Steganographic Algorithm")
    print("=" * 70)
    print()
    
    # Włącz debug
    stego = GalileoSteganography(debug=False)
    
    # Tajna wiadomość
    secret = "prezes"
    print(f"📝 Tajna wiadomość: '{secret}'")
    print()
    
    # Tekst nośny - DŁUŻSZY
    carrier = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut massa erat, vulputate accumsan risus ut, lacinia dignissim dolor. Fusce nisl tellus, lacinia et urna et, dignissim aliquet turpis. Nullam vitae lacinia ante. Proin mollis tortor nec posuere euismod. Nulla facilisi. Duis gravida massa nec accumsan dictum. Duis in urna non justo mattis ultrices. Sed blandit at erat quis congue. Maecenas.
    """.replace('\n', ' ').strip()
    
    print(f"📄 Tekst nośny: {len(carrier.split())} słów")
    print()
    
    # Test enkodowania/dekodowania
    print("\n🔬 TEST PODSTAWOWY (bez steganografii)")
    print("-" * 70)
    test_bits = stego._text_to_bits("T")
    print(f"Oryginalne bity: {test_bits}")
    encoded = stego.encoder.encode(test_bits)
    print(f"Po kodowaniu: {encoded[:20]}... (długość: {len(encoded)})")
    decoded = stego.decoder.decode(encoded)
    print(f"Po dekodowaniu: {decoded}")
    recovered = stego._bits_to_text(decoded)
    print(f"Odzyskany tekst: '{recovered}'")
    print()
    
    # UKRYWANIE
    print("\n🔒 UKRYWANIE WIADOMOŚCI")
    print("-" * 70)
    try:
        stego_text = stego.hide_message(secret, carrier)
        print()

        ctr = 0
        for i, char in enumerate(stego_text):
            vl = ord(char)
            if vl == 1072:
                stego_text = stego_text[:i] + 'a' + stego_text[i+1:]
                ctr += 1
            if vl == 1077:
                stego_text = stego_text[:i] + 'e' + stego_text[i+1:]
                ctr += 1

            if ctr == 4:
                break

        print(ctr)
        print(f"Stego tekst: {stego_text}")

        # EKSTRAHOWANIE
        print("\n🔓 EKSTRAHOWANIE WIADOMOŚCI")
        print("-" * 70)
        recovered = stego.extract_message(stego_text)
        print()
        
        # Weryfikacja
        print("=" * 70)
        if recovered.strip() == secret:
            print("✅ SUKCES! Wiadomość poprawnie ukryta i odzyskana!")
        else:
            print(f"⚠️  Błąd w transmisji:")
            print(f"   Oryginał:  '{secret}'")
            print(f"   Odzyskana: '{recovered}'")
            print(f"   Długość: {len(secret)} → {len(recovered)}")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
