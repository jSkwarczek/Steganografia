import sys
import argparse
import string

def embed_message_epa(cover_text_file, secret_message):
    if not set(secret_message).issubset(set(string.ascii_letters)):
        raise ValueError(f"Only ASCII characters are allowed! Invalid characters: {set(secret_message) - set(string.ascii_letters)}")

    with open(cover_text_file, 'r', encoding='utf-8') as f:
        cover_text = f.read()

    sm_bits = ''.join(format(ord(char), '08b') for char in secret_message)
    bit_index = 0

    words = cover_text.split()

    stego_content = []
    key = []

    for word in words:
        stego_content.append(word)

        L = 1
        word_len = len(word)

        while L <= word_len:
            s_index = L - 1
            e_index = word_len - L

            s = word[s_index]
            e = word[e_index]

            if s == e:
                L += 1
                continue

            if bit_index < len(sm_bits):
                x = sm_bits[bit_index]
                bit_index += 1

                if x == '1':
                    key.append(e)
                else:
                    key.append(s)
            else:
                break

            L += 1

        if bit_index >= len(sm_bits):
            remaining_words = words[words.index(word) + 1:]
            stego_content.extend(remaining_words)
            break

    return "".join(key)

def extract_message_epa(stego_file, key):
    with open(stego_file, 'r', encoding='utf-8') as f:
        stego_text = f.read()

    words = stego_text.split()

    binary_data = []
    key_index = 0

    for word in words:
        if key_index >= len(key):
            break

        L = 1
        word_len = len(word)

        while L <= word_len:
            if key_index >= len(key):
                break

            s_index = L - 1
            e_index = word_len - L

            s = word[s_index]
            e = word[e_index]

            if s == e:
                L += 1
                continue

            c = key[key_index]
            key_index += 1

            if c == s:
                binary_data.append('0')
            elif c == e:
                binary_data.append('1')
            # może być jeszcze dziwny case gdzie c != s i c != e

            L += 1

    bitstring = ''.join(binary_data)
    if len(bitstring) % 8 != 0:
        bitstring = bitstring[:-(len(bitstring) % 8)]

    secret_message = ''
    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i+8]
        secret_message += chr(int(byte, 2))

    return secret_message

def main():
    parser = argparse.ArgumentParser(
        description='EPA'
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    embed_parser = subparsers.add_parser('embed', help='Embed secret message')
    embed_parser.add_argument(
        'cover_text',
        help='Cover Text'
    )
    embed_parser.add_argument(
        '-s', '--secret',
        help='Secret Message'
    )

    extract_parser = subparsers.add_parser('extract', help='Extract secret message')
    extract_parser.add_argument(
        'stego_file',
        help='Stego Text'
    )
    extract_parser.add_argument(
        '-k', '--key',
        help='Key File'
    )

    args = parser.parse_args()

    try:
        if args.command == 'embed':
            print(embed_message_epa(
                args.cover_text,
                args.secret,
            ))
        elif args.command == 'extract':
            print(extract_message_epa(
                args.stego_file,
                args.key
            ))
    except FileNotFoundError as e:
        print(f"[ERROR]: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e: # prolly not the best practice
        print(f"[ERROR]: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
