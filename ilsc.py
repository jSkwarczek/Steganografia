from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
import pdfplumber
import os
import math

TTF_PATH = "DejaVuSans.ttf"
FONT_NAME = "DejaVuSans"
FONT_SIZE = 11
LINE_SPACING = 1.3
SHIFT_AMOUNT = 0.1

def embed_message_ilsc(cover_text: str, secret_message: str, output_path):
    pivots = [0]
    if not os.path.exists(TTF_PATH):
        raise FileNotFoundError(f"Font not found")

    pdfmetrics.registerFont(TTFont(FONT_NAME, TTF_PATH))

    lines = cover_text.splitlines()
    if len(lines) == 0:
        raise ValueError("Provide convert text")

    cover_capacity = len(lines)

    secret_bytes = secret_message.encode("utf-8")
    secret_bits = ''.join(f"{byte:08b}" for byte in secret_bytes)
    secret_len = len(secret_bits)

    if secret_len > cover_capacity:
        raise ValueError(f"Embedding Message Failed: needed size: {secret_len}, "
                         f"got: {cover_capacity}")

    while len(secret_bits) < cover_capacity:
        secret_bits += str(random.randint(0, 1))

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    leading = FONT_SIZE * LINE_SPACING

    y = height - 50

    textobj = c.beginText()
    textobj.setFont(FONT_NAME, FONT_SIZE)

    for idx, line in enumerate(lines):
        if idx in pivots:
            margin = 50
            if idx == 4:
                margin = 35
            textobj.setTextOrigin(margin, y)
            textobj.textLine(line)
            y -= leading
            continue
        
        bit = int(secret_bits[idx])

        rise = SHIFT_AMOUNT if bit == 1 else -SHIFT_AMOUNT

        if y < 50:
            c.drawText(textobj)
            c.showPage()
            textobj = c.beginText()
            textobj.setFont(font_name, font_size)

        textobj.setTextOrigin(35, y+rise)
        # textobj.setRise(rise)
        textobj.textLine(line)
        
        # textobj.setRise(0)
        
        y -= leading+rise

    c.drawText(textobj)
    c.save()
    print(f"Stego PDF saved to: {output_path}")

def extract_message_ilsc(pdf_path: str, tolerance: float = 0.05) -> str:
    diffs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            words = page.extract_words()
            
            lines = {}
            for word in words:
                y_pos = word['top']
                if y_pos not in lines:
                    lines[y_pos] = []
                lines[y_pos].append(word)

            sorted_lines = sorted(lines.keys())
            
            for i in range(len(sorted_lines) - 1):
                current_line = sorted_lines[i]
                next_line = sorted_lines[i + 1]
                diff = (next_line - current_line) - (FONT_SIZE * LINE_SPACING)
                diffs.append(diff)

    print(diffs)
    bits = []
    for diff in diffs:
        if diff <= 0:
            bits.append("0")
        else:
            bits.append("1")

    n = len(bits) - (len(bits) % 8)
    bits = bits[:n]

    message = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) == 8:
            val = int("".join(byte), 2)
            try:
                message += bytes([val]).decode("utf-8")
            except UnicodeDecodeError:
                pass

    return message

def get_line_distances(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\n--- Strona {page_num} ---")
            
            words = page.extract_words()
            
            lines = {}
            for word in words:
                y_pos = word['top']
                if y_pos not in lines:
                    lines[y_pos] = []
                lines[y_pos].append(word)
            
            sorted_lines = sorted(lines.keys())
            
            for i in range(len(sorted_lines) - 1):
                current_line = sorted_lines[i]
                next_line = sorted_lines[i + 1]
                distance = next_line - current_line
                
                print(f"Odległość między linią {i+1} a {i+2}: {distance} punktów")

def main():
    cover = """To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    To jest przykładowy tekst przykrywający.
    Każda linia może reprezentować jeden bit ukrytej wiadomości.
    System przesuwa linie nieznacznie w górę lub w dół, by zakodować dane.
    """
    print(cover.count('\n'))
    secret = "hej"
    embed_message_ilsc(cover, secret, "stego_outputt.pdf")
    get_line_distances("stego_outputt.pdf")
    print(extract_message_ilsc("stego_outputt.pdf"))

if __name__ == '__main__':
    main()

