import math
import re
from typing import List, Tuple

COLOR_MAPPING = {
    'Red': 0,
    'Green': 0,
    'Blue': 0,
    'Aqua': 0,
    'Pink': 0,
    'Black': 1,
    'Dark Yellow': 1,
    'Indigo': 1,
    'Dark red': 1,
    'Lavender': 1
}

COLOR_TO_HTML = {
    'Red': '#FF0000',
    'Green': '#00FF00',
    'Blue': '#0000FF',
    'Aqua': '#00FFFF',
    'Pink': '#FFC0CB',
    'Black': '#000000',
    'Dark Yellow': '#CCCC00',
    'Indigo': '#4B0082',
    'Dark red': '#8B0000',
    'Lavender': '#E6E6FA'
}

EMAIL_EXTENSIONS = {
    0: 'gmail.com',
    1: 'hotmail.com',
    2: 'yahoo.com',
    3: 'rediffmail.com',
    4: 'btinternet.com',
    5: 'aol.com',
    6: 'msn.com',
    7: 'verizon.net'
}

EXTENSION_TO_CODE = {ext: code for code, ext in EMAIL_EXTENSIONS.items()}

def lzw_compress(data: str) -> List[int]:
    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}
    
    result = []
    current = ""
    
    for char in data:
        combined = current + char
        if combined in dictionary:
            current = combined
        else:
            result.append(dictionary[current])
            dictionary[combined] = dictionary_size
            dictionary_size += 1
            current = char
    
    if current:
        result.append(dictionary[current])
    
    return result


def lzw_decompress(compressed: List[int]) -> str:
    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}
    
    result = []
    current = chr(compressed[0])
    result.append(current)
    
    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dictionary_size:
            entry = current + current[0]
        else:
            raise ValueError(f"Bad compressed code: {code}")
        
        result.append(entry)
        dictionary[dictionary_size] = current + entry[0]
        dictionary_size += 1
        current = entry
    
    return ''.join(result)

def index_to_letter(index: int) -> str:
    return chr(ord('a') + index)


def letter_to_index(letter: str) -> int:
    return ord(letter.lower()) - ord('a')


def codes_to_bitstream(codes: List[int]) -> List[int]:
    if not codes:
        return []
    
    max_code = max(codes)
    bit_width = max(9, math.ceil(math.log2(max_code + 1)))
    
    bit_stream = []
    for code in codes:
        binary = format(code, f'0{bit_width}b')
        bit_stream.extend([int(b) for b in binary])
    
    return bit_stream


def bitstream_to_codes(bits: List[int], bit_width: int = 9) -> List[int]:
    codes = []
    
    for i in range(0, len(bits), bit_width):
        if i + bit_width <= len(bits):
            binary = ''.join(str(b) for b in bits[i:i+bit_width])
            codes.append(int(binary, 2))
    
    return codes


def get_color_for_bit(bit_value: int, rotation: int) -> str:
    valid_colors = [c for c, v in COLOR_MAPPING.items() if v == bit_value]
    color = valid_colors[rotation % len(valid_colors)]
    return color


def color_text(cover_text: str, bits: List[int]) -> Tuple[str, List[Tuple[str, int]]]:
    color_info = []
    rotation = 0
    
    bit_idx = 0
    for char in cover_text:
        if char == ' ':
            continue
        
        if bit_idx < len(bits):
            bit_value = bits[bit_idx]
            color = get_color_for_bit(bit_value, rotation)
            color_info.append((color, bit_value))
            rotation += 1
            bit_idx += 1
    
    return color_info


def color_info_to_html(cover_text: str, color_info: List[Tuple[str, int]]) -> str:
    html_parts = []
    color_idx = 0
    
    for char in cover_text:
        if char == ' ':
            html_parts.append(' ')
        else:
            if color_idx < len(color_info):
                color_name, _ = color_info[color_idx]
                color_code = COLOR_TO_HTML[color_name]
                html_parts.append(f'<span style="color:{color_code}">{char}</span>')
                color_idx += 1
            else:
                html_parts.append(char)
    
    return ''.join(html_parts)

def html_to_color_info(html_text: str) -> List[Tuple[str, int]]:
    HTML_TO_COLOR = {v: k for k, v in COLOR_TO_HTML.items()}
    
    plain_text = []
    color_info = []
    
    pattern = r'<span style="color:(#[0-9A-Fa-f]{6})">(.)</span>'
    
    pos = 0
    for match in re.finditer(pattern, html_text):
        color_code = match.group(1).upper()
                
        if color_code in HTML_TO_COLOR:
            color_name = HTML_TO_COLOR[color_code]
            bit_value = COLOR_MAPPING[color_name]
            color_info.append((color_name, bit_value))
        
        pos = match.end()
    
    return color_info


def bits_to_emails(bits: List[int]) -> List[str]:
    bits = bits.copy()
    while len(bits) % 12 != 0:
        bits.append(0)
    
    email_addresses = []
    
    for i in range(0, len(bits), 12):
        group = bits[i:i+12]
        
        g1_bits = group[:9]
        g2_bits = group[9:]
        
        g1 = int(''.join(str(b) for b in g1_bits), 2)
        g2 = int(''.join(str(b) for b in g2_bits), 2)
        
        x = g1 // 26
        y = g1 % 26
        z = g2
        
        letter1 = index_to_letter(x)
        letter2 = index_to_letter(y)
        extension = EMAIL_EXTENSIONS.get(z, EMAIL_EXTENSIONS[0])
        
        email = f"{letter1}{letter2}@{extension}"
        email_addresses.append(email)
    
    return email_addresses


def emails_to_bits(email_addresses: List[str]) -> List[int]:
    bits = []
    
    for email in email_addresses:
        parts = email.split('@')
        if len(parts) != 2:
            continue
        
        local_part = parts[0]
        extension = parts[1]
        
        if len(local_part) >= 2:
            letter1 = local_part[0]
            letter2 = local_part[1]
            
            x = letter_to_index(letter1)
            y = letter_to_index(letter2)
            
            g1 = x * 26 + y
            g1_binary = format(g1, '09b')
            
            z = EXTENSION_TO_CODE.get(extension, 0)
            g2_binary = format(z, '03b')
            
            bits.extend([int(b) for b in g1_binary])
            bits.extend([int(b) for b in g2_binary])
    
    return bits

def embed_message_emails(secret_message: str, cover_text: str) -> Tuple[str, List[str]]:
    lzw_codes = lzw_compress(secret_message)
    
    bit_stream = codes_to_bitstream(lzw_codes)
    
    num_chars = sum(1 for c in cover_text if c != ' ')
    
    cover_bits = bit_stream[:num_chars]
    residual_bits = bit_stream[num_chars:]
    
    color_info = color_text(cover_text, cover_bits)
    
    html_colored_text = color_info_to_html(cover_text, color_info)
    
    email_addresses = bits_to_emails(residual_bits)
    
    return html_colored_text, email_addresses


def extract_message_emails(colored_text: str, email_addresses: List[str]) -> str:
    color_info = html_to_color_info(colored_text)
    cover_bits = [bit for _, bit in color_info]
    
    email_bits = emails_to_bits(email_addresses)
    
    all_bits = cover_bits + email_bits
    
    lzw_codes = bitstream_to_codes(all_bits)
    secret_message = lzw_decompress(lzw_codes)
    
    return secret_message

if __name__ == "__main__":
    secret_message = "prezes"
    cover_text = "Only boats catch connotes of the islands sober wines only ships wrap the slips on the cleats of twining lines only flags flap in tags with color that assigns only passage on vessels"
    
    html_colored_text, emails = embed_message_emails(secret_message, cover_text)

    print(html_colored_text)
        
    extracted_message = extract_message_emails(html_colored_text, emails)
    print(f"Extracted message: {extracted_message}")
