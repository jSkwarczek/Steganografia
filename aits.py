import math
import string

ZWC_TABLE = {
    '00': '\u200C',
    '01': '\u202C',
    '10': '\u202D',
    '11': '\u200E',
}

REVERSE_ZWC_TABLE = {v: k for k, v in ZWC_TABLE.items()}

def embed_message_aits(cover_message, secret_message, symmetric_key):
    if not set(secret_message).issubset(set(string.ascii_letters)):
        raise ValueError(f"Only ASCII characters are allowed! Invalid characters: {set(secret_message) - set(string.ascii_letters)}")
    SM = secret_message
    CM = cover_message
    MS_SK = symmetric_key

    SM_binary = ""
    for i, char in enumerate(SM):
        n = ord(char)

        if n == 0:
            alpha = 1
            beta = 0
        else:
            eta_plus_1 = n + 1

            alpha = 1
            while alpha < 64 and eta_plus_1 % (2 ** alpha) == 0:
                alpha += 1
            alpha -= 1

            k = eta_plus_1 // (2 ** alpha)
            beta = (k - 1) // 2

        alpha_binary = format(alpha, '06b')
        beta_binary = format(beta, '06b')

        SM_binary += alpha_binary + beta_binary

    LSK = len(MS_SK)

    if len(SM_binary) % LSK == 0:
        P = 0
    else:
        P = 1

    NC = math.floor(len(SM_binary) / LSK) + P

    MS_SK_binary = ''.join(format(ord(c), '08b') for c in MS_SK)
    Hash_position_bits = MS_SK_binary * NC

    Hashed_SM_binary = ""
    for i in range(len(SM_binary)):
        bit_sm = SM_binary[i]
        bit_hash = Hash_position_bits[i % len(Hash_position_bits)]
        xor_result = str(int(bit_sm) ^ int(bit_hash))
        Hashed_SM_binary += xor_result

    SK_binary = ''.join(format(ord(c), '08b') for c in symmetric_key)
    HM_SK = ""
    for i in range(0, len(SK_binary), 2):
        if i + 1 < len(SK_binary):
            two_bits = SK_binary[i:i+2]
            HM_SK += ZWC_TABLE[two_bits]

    HM = HM_SK
    for i in range(0, len(Hashed_SM_binary), 2):
        if i + 1 < len(Hashed_SM_binary):
            two_bits = Hashed_SM_binary[i:i+2]
            HM += ZWC_TABLE[two_bits]

    CM_HM = HM + CM

    return CM_HM

def extract_message_aits(carrier_message, symmetric_key):
    CM_HM = carrier_message
    MR_SK = symmetric_key

    Hashed_SM_binary = ""
    for i, char in enumerate(CM_HM):
        if char in REVERSE_ZWC_TABLE:
            bits = REVERSE_ZWC_TABLE[char]

            if char == '\u200C':
                Hashed_SM_binary += "00"
            elif char == '\u202C':
                Hashed_SM_binary += "01"
            elif char == '\u202D':
                Hashed_SM_binary += "10"
            elif char == '\u200E':
                Hashed_SM_binary += "11"

    MR_SK_binary = ''.join(format(ord(c), '08b') for c in MR_SK)

    key_length_in_bits = len(MR_SK_binary)

    if len(Hashed_SM_binary) >= key_length_in_bits:
        Hashed_SM_binary = Hashed_SM_binary[key_length_in_bits:]

    LSK = len(MR_SK_binary)

    if len(Hashed_SM_binary) % LSK == 0:
        P = 0
    else:
        P = 1

    NC = math.floor(len(Hashed_SM_binary) / LSK) + P

    Hash_position_bits = MR_SK_binary * NC

    SM_binary = ""
    for i in range(len(Hashed_SM_binary)):
        bit_hashed = Hashed_SM_binary[i]
        bit_hash = Hash_position_bits[i] if i < len(Hash_position_bits) else '0'
        xor_result = str(int(bit_hashed) ^ int(bit_hash))
        SM_binary += xor_result

    SM = ""
    i = 0
    while len(SM_binary) >= 12 and i + 12 <= len(SM_binary):
        AlfaBeta = SM_binary[i:i+12]

        Alfa = AlfaBeta[0:6]
        Beta = AlfaBeta[6:12]

        alpha = int(Alfa, 2)
        beta = int(Beta, 2)

        eta = (2 ** alpha) * (2 * beta + 1) - 1

        if eta <= 127:
            SM += chr(eta)

        i += 12

    return SM


if __name__ == "__main__":
    cover_msg = "To jest wiadomość okładkowa, która będzie zawierać ukrytą informację."
    secret_msg = "TAJNE"
    key = "KLUCZ"


    carrier = embed_message_aits(cover_msg, secret_msg, key)
    print(carrier)
    for ca in carrier:
        print(ord(ca))

    extracted = extract_message_aits(carrier, key)
    print(f"SM: '{extracted}'")
