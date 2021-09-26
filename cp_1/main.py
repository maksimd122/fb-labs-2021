import pandas
import openpyxl
from math import log2

alphabet = [chr(code) for code in range(ord("а"), ord("а") + 32)]
alphabet.remove("ъ")

letter_count = {}
letter_count_2 = {}
bigrams_count = {}
bigrams_count_2 = {}
bigrams_count_3 = {}
bigrams_count_4 = {}

def make_bigram(dict, name):
    pd = pandas.DataFrame(index=alphabet, columns=alphabet)
    for letter in alphabet:
        for second_letter in alphabet:
            if dict.get(letter + second_letter) is not None:
                pd[second_letter][letter] = dict[letter + second_letter]
            else:
                pd[second_letter][letter] = 0
    pd.to_excel(f"{name}.xlsx")


def bigrams_counting(dict, text, step):
    length = len(text)
    for i in range(length):
        if text[i] != ' ':
            if i < length - step:
                if text[i + step] != ' ':
                    bigram = text[i] + text[i + step]
                    if dict.get(bigram) is None:
                        dict[bigram] = 1
                    else:
                        dict[bigram] += 1
    bigram_sums = 0
    for bigram in dict:
        bigram_sums += dict[bigram]
    for bigram in dict:
        dict[bigram] = dict[bigram] / bigram_sums


def enthropy(dict, n):
    summ = 0
    for keys in dict:
        if dict[keys] != 0:
            summ += dict[keys] * log2(dict[keys])
    return 1 / n * -summ


def count_letters(dict, space):
    global text
    for char in text:
        if char not in alphabet:
            if space is True and char == ' ':
                if dict.get(char) is None:
                    dict[char] = 1
                else:
                    dict[char] += 1
            else:
                text = text.replace(char, '')
        else:
            if dict.get(char) is None:
                dict[char] = 1
            else:
                dict[char] += 1
    length = len(text)
    for key in dict:
        dict[key] = dict[key] / length


# TODO считать текст
with open("text2.txt", 'r', encoding='utf8') as data_file:
    text = data_file.read()
    text = text.lower()

# TODO убрать все знаки и посчитать все буквы
count_letters(letter_count, True)

# TODO посчитать все биграмы и биграмы +1
bigrams_counting(bigrams_count, text, 1)
bigrams_counting(bigrams_count_2, text, 2)

# TODO посчитать энтропии
h1 = enthropy(letter_count, 1)
h2 = enthropy(bigrams_count, 2)
h3 = enthropy(bigrams_count_2, 2)
print(f"Entropy with spaces: for letters - {h1}, for bigrams - {h2}, for bigrams with step 2 - {h3}")

# TODO убрать пробелы
count_letters(letter_count_2, False)
bigrams_counting(bigrams_count_3, text, 1)
bigrams_counting(bigrams_count_4, text, 2)

# TODO посчитать энтропии
h11 = enthropy(letter_count_2, 1)
h22 = enthropy(bigrams_count_3, 2)
h33 = enthropy(bigrams_count_4, 2)
print(f"Entropy without spaces: for letters - {h11}, for bigrams - {h22}, for bigrams with step 2 - {h33}")

# TODO сохранить результаты
letters1 = pandas.DataFrame(
    {"Letter": [key for key in letter_count], "Frequency": [letter_count[key] for key in letter_count]})
letters1 = letters1.sort_values(by='Frequency', ascending=False, ignore_index=True)
letters1.to_excel("letters1.xlsx", index=False)

letters2 = pandas.DataFrame(
    {"Letter": [key for key in letter_count_2], "Frequency": [letter_count_2[key] for key in letter_count_2]})
letters2 = letters2.sort_values(by='Frequency', ascending=False, ignore_index=True)
letters2.to_excel("letters2.xlsx", index=False)

make_bigram(bigrams_count, 'bigrams1')
make_bigram(bigrams_count_2, 'bigrams2')
make_bigram(bigrams_count_3, 'bigrams3')
make_bigram(bigrams_count_4, 'bigrams4')
