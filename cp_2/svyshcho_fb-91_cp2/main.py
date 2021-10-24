import pandas

alphabet = [chr(code) for code in range(ord("а"), ord("а") + 32)]
common_letters = ['о', "е", "а", "и"]

keys = ["ад", "дом", "река", "ангел", "боеголовка", "дармоедство", "голосистость", "аллергический", "заинтересовать",
        "гидрометеоролог", "лесозаготовитель", "радиооборудование", "благотворительница",
        "интервенционистский", "женоненавистничество"]

ciphertexts = {}

with open("text.txt", 'r', encoding='utf8') as data_file:
    text = data_file.read()
    text = text.lower()


def sort(text_un):
    for character in text_un:
        if character not in alphabet:
            text_un = text_un.replace(character, "")
    return text_un


def cipher(plaintext: str, key: str):
    global alphabet
    ciphertext = ""
    for (index, char) in enumerate(plaintext):
        orig_ind = alphabet.index(char)
        key_ind = alphabet.index(key[index % len(key)])
        new_ind = (orig_ind + key_ind) % 32
        ciphertext += alphabet[new_ind]
    return ciphertext


def decipher(ciphertext: str, key: str):
    plaintext = ""
    for (index, char) in enumerate(ciphertext):
        new_ind = alphabet.index(char)
        key_ind = alphabet.index(key[index % len(key)])
        orig_ind = (new_ind - key_ind) % 32
        plaintext += alphabet[orig_ind]
    return plaintext


def corr_ind(data: str):
    letters_count = {}
    length = len(data)
    for char in data:
        if letters_count.get(char) is None:
            letters_count[char] = 1
        else:
            letters_count[char] += 1
    summ = 0
    for letter in letters_count:
        summ += letters_count[letter] * (letters_count[letter] - 1)
    ind = summ / (length * (length - 1))
    return ind


def blocking(whole_text: str, period: int):
    blocks = ["" for i in range(period)]
    for (index, char) in enumerate(whole_text):
        blocks[index % period] += char
    return blocks


def get_key(block: str):
    letters_count = {}
    for char in block:
        if letters_count.get(char) is None:
            letters_count[char] = 1
        else:
            letters_count[char] += 1
    max_val = ["", 0]
    for key in letters_count:
        if letters_count[key] > max_val[1]:
            max_val[1] = letters_count[key]
            max_val[0] = key
    key_letter1 = (alphabet.index(max_val[0]) - alphabet.index(common_letters[0])) % 32
    key_letter2 = (alphabet.index(max_val[0]) - alphabet.index(common_letters[1])) % 32
    key_letter3 = (alphabet.index(max_val[0]) - alphabet.index(common_letters[2])) % 32
    key_letter4 = (alphabet.index(max_val[0]) - alphabet.index(common_letters[3])) % 32
    return [alphabet[key_letter1], alphabet[key_letter2], alphabet[key_letter3], alphabet[key_letter4]]


# /////////////////////////////////////////////////////////////////////////////////////////

# text = sort(text)
# plain_ind = corr_ind(text)
# indexes = {"Відкритий текст": plain_ind}
# for key in keys:
#     ciphertexts[key] = cipher(text, key)
#     blocks = blocking(ciphertexts[key], len(key))
#     summ = 0
#     for block in blocks:
#         summ += corr_ind(block)
#     summ = summ / len(key)
#     indexes[len(key)] = summ
# results = pandas.DataFrame(
#     {"Довжина ключа": [key for key in indexes], "Індекс": [indexes[key] for key in indexes]})
# results.to_excel("index.xlsx", index=False)

# /////////////////////////////////////////////////////////////////////////////////////////
with open("ciphertext.txt", 'r', encoding='utf8') as data_file:
    ciphertext = data_file.read()

keys_lengths = []
dec_indexes = {}

for i in range(2, 31):
    key = ['', '', '', '']
    blocks = blocking(ciphertext, i)
    summ = 0
    for block in blocks:
        summ += corr_ind(block)
        letters = get_key(block)
        for j in range(4):
            key[j] += letters[j]
    summ = summ / i
    print(f"Keys for {i} - {key}")
    # dec_indexes[i] = summ
    # results = pandas.DataFrame(
    #     {"Довжина ключа": [key for key in dec_indexes], "Індекс": [dec_indexes[key] for key in dec_indexes]})
    # results.to_excel("dec_index.xlsx", index=False)
#
print(decipher(ciphertext, "человеквфутляре"))
