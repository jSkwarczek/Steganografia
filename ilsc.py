from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pdfplumber
import io

SHIFT = 0.8
LINE_H = 20

def embed_message_ilsc(cover_text, secret_message, output_pdf_path):
    shift_amount=SHIFT
   
    lines = cover_text.split('\n')
    
    secret_bits = []
    for char in secret_message:
        binary = format(ord(char), '08b')
        secret_bits.extend([int(bit) for bit in binary])
    
    lines_per_page = 35
    pivot_lines_per_page = {0, 4}
    
    total_capacity = 0
    for i in range(len(lines)):
        page_line_idx = i % lines_per_page
        if page_line_idx not in pivot_lines_per_page:
            total_capacity += 1
    
    if len(secret_bits) > total_capacity:
        raise Exception(f"Secret message too long: {len(secret_bits)}>{total_capacity}")
    
    pdfmetrics.registerFont(TTFont('DejaVuSans', './DejaVuSans.ttf'))
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    c.setFont('DejaVuSans', 12)
    width, height = letter
    
    base_y = height - 50
    line_height = LINE_H
    bit_index = 0
    page_line_count = 0
    
    for i, line in enumerate(lines):
        if page_line_count >= lines_per_page:
            c.showPage()
            c.setFont('DejaVuSans', 12)
            base_y = height - 50
            page_line_count = 0
           
        line_position_on_page = page_line_count
        
        if not line.strip():
            y_position = base_y - (page_line_count * line_height)
            c.drawString(50, y_position, line)
            page_line_count += 1
            continue
        
        normalized_line = line.strip()
        
        is_pivot = line_position_on_page in pivot_lines_per_page
        
        if is_pivot:
            y_position = base_y - (page_line_count * line_height)
            c.drawString(50, y_position, normalized_line)
        else:
            if bit_index < len(secret_bits):
                secret_bit = secret_bits[bit_index]                
                base_position = base_y - (page_line_count * line_height)
                
                if secret_bit == 1:
                    y_position = base_position - shift_amount
                else:
                    y_position = base_position + shift_amount
                
                c.drawString(50, y_position, normalized_line)
                bit_index += 1
            else:
                y_position = base_y - (page_line_count * line_height)
                c.drawString(50, y_position, normalized_line)
        
        page_line_count += 1
    
    c.save()
    return True


def extract_message_ilsc(input_pdf_path):
    shift_threshold=SHIFT/2
    extracted_bits = []
    
    with pdfplumber.open(input_pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
            
            if not words:
                continue
            
            lines_dict = {}
            for word in words:
                y_pos = round(word['top'], 0)
                
                found_line = None
                for existing_y in lines_dict.keys():
                    if abs(existing_y - y_pos) <= 3:
                        found_line = existing_y
                        break
                
                if found_line is not None:
                    lines_dict[found_line].append(word)
                else:
                    lines_dict[y_pos] = [word]
            
            sorted_y_positions = sorted(lines_dict.keys())
            lines = []
            
            for y_pos in sorted_y_positions:
                lines.append({'y': y_pos,})
            
            
            if len(lines) < 2:
                continue
            
            pivot_indices = [0, 4]
            
            if len(lines) > 4:
                pivot_y1 = lines[0]['y']
                pivot_y2 = lines[4]['y']
                expected_line_height = (pivot_y2 - pivot_y1) / 4
            else:
                expected_line_height = LINE_H
                pivot_y1 = lines[0]['y']
            
            for line_idx, line in enumerate(lines):
                if line_idx in pivot_indices:
                    continue
                
                if line_idx < 4:
                    expected_y = pivot_y1 + (line_idx * expected_line_height)
                else:
                    if len(lines) > 4:
                        lines_after_pivot = line_idx - 4
                        expected_y = pivot_y2 + (lines_after_pivot * expected_line_height)
                    else:
                        expected_y = pivot_y1 + (line_idx * expected_line_height)
                
                actual_y = line['y']
                shift = actual_y - expected_y
                
                
                if shift < -shift_threshold:
                    secret_bit = 0
                elif shift > shift_threshold:
                    secret_bit = 1
                else:
                    secret_bit = 0
                
                extracted_bits.append(secret_bit)
    
    if len(extracted_bits) == 0:
        raise Exception("Extracted 0 bits!")
            
    if len(extracted_bits) % 8 != 0:
        remainder = len(extracted_bits) % 8
        extracted_bits = extracted_bits[:-remainder]
    
    secret_message = ""
    for i in range(0, len(extracted_bits), 8):
        byte = extracted_bits[i:i+8]
        byte_string = ''.join(str(bit) for bit in byte)
        char_code = int(byte_string, 2)
        
        if char_code == 0:
            break
        
        if 32 <= char_code < 127:
            secret_message += chr(char_code)
        elif char_code >= 128:
            try:
                secret_message += chr(char_code)
            except ValueError:
                pass

    return secret_message


if __name__ == "__main__":
    cover_text = """To jest przykładowy tekst okładkowy.
Może zawierać polskie znaki: ąćęłńóśźż.
Ta linia będzie służyć jako przykład.
Kolejna linia tekstu normalnego.
Piąta linia to drugi pivot.
Szósta linia może być kodowana.
Siódma linia również.
Ósma linia tekstu.
Dziewiąta linia dokumentu.
Dziesiąta linia na koniec.
Jedenasta linia dla pewności.
Dwunasta linia tekstu.
Trzynasta linia okładki.
Czternasta linia dokumentu.
Piętnasta linia treści.
Szesnasta linia przykładu.
Siedemnasta linia tekstu.
Osiemnasta linia danych.
Dziewiętnasta linia okładki.
Dwudziesta i ostatnia linia.
To jest przykładowy tekst okładkowy.
Może zawierać polskie znaki: ąćęłńóśźż.
Ta linia będzie służyć jako przykład.
Kolejna linia tekstu normalnego.
Piąta linia to drugi pivot.
Szósta linia może być kodowana.
Siódma linia również.
Ósma linia tekstu.
Dziewiąta linia dokumentu.
Dziesiąta linia na koniec.
Jedenasta linia dla pewności.
Dwunasta linia tekstu.
Trzynasta linia okładki.
Czternasta linia dokumentu.
Piętnasta linia treści.
Szesnasta linia przykładu.
Siedemnasta linia tekstu.
Osiemnasta linia danych.
Dziewiętnasta linia okładki.
Dwudziesta i ostatnia linia.
To jest przykładowy tekst okładkowy.
Może zawierać polskie znaki: ąćęłńóśźż.
Ta linia będzie służyć jako przykład.
Kolejna linia tekstu normalnego.
Piąta linia to drugi pivot.
Szósta linia może być kodowana.
Siódma linia również.
Ósma linia tekstu.
Dziewiąta linia dokumentu.
Dziesiąta linia na koniec.
Jedenasta linia dla pewności.
Dwunasta linia tekstu.
Trzynasta linia okładki.
Czternasta linia dokumentu.
Piętnasta linia treści.
Szesnasta linia przykładu.
Siedemnasta linia tekstu.
Osiemnasta linia danych.
Dziewiętnasta linia okładki.
Dwudziesta i ostatnia linia."""
    
    secret_message = "Tajne"
    
    embed_message_ilsc(cover_text, secret_message, "stego_output.pdf")
    decoded = extract_message_ilsc("stego_output.pdf")
    print(f"Odkodowana wiadomość: {decoded}")
