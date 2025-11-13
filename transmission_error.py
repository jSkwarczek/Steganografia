data = input("Secret message: ")
err_cnt_max = input("Wrong bits: ")
err_cnt = 0

MARKER_1 = '​'  # U+200B Zero Width Space
MARKER_0 = '‌'  # U+200C Zero Width Non-Joiner
    
HOMOGLYPHS = {
    'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с',
    'y': 'у', 'x': 'х', 'i': 'і', 'j': 'ј', 's': 'ѕ',
    'A': 'А', 'E': 'Е', 'O': 'О', 'P': 'Р', 'C': 'С',
    'Y': 'У', 'X': 'Х', 'I': 'І', 'J': 'Ј', 'S': 'Ѕ',
}

REVERSE_HOMOGLYPHS = {v: k for k, v in HOMOGLYPHS.items()}
 
data_with_errors = ""

skip_word = False

for c in data:
    if err_cnt == err_cnt_max:
        break
    
    if skip_word:
        data_with_errors += c
        if c == ' ':
            skip_word = False
        continue

    if c == MARKER_0:
        data_with_errors += MARKER_1
        err_cnt += 1
    elif c == MARKER_1:
        data_with_errors += MARKER_0 
        err_cnt += 1
    # elif c in HOMOGLYPHS.keys():
    #     data_with_errors += HOMOGLYPHS[c]
    #     skip_word = True
    # elif c in REVERSE_HOMOGLYPHS.keys():
    #     data_with_errors += REVERSE_HOMOGLYPHS[c]
    #     skip_word = True
    else:
        data_with_errors += c
        
print(data_with_errors)