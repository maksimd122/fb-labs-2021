import pandas
import openpyxl
from math import log2

alphabet = [chr(code) for code in range(ord("а"), ord("а") + 32)]
alphabet.append('ё')
alphabet.append(' ')

letter_count = {}
letter_count_2 = {}
bigrams_count = {}
bigrams_count_2 = {}
bigrams_count_3 = {}
bigrams_count_4 = {}


def sort():
    global text
    text = text.replace("\n\n", " ")
    text = text.replace("\n", " ")
    characters = [',', '.', '!', '?', '"', ':', ';', "'", '-', "—", '…', '«', "»", '*', '(', ')', '1', '2', '3', '4',
                  '5', '6', '7', '8', '9', '№', '0', '“', '„', '́', 'c']
    for character in characters:
        text = text.replace(character, '')
    while text.find("  ") != -1:
        text = text.replace("  ", " ")


def walk_through(dict_letters, dict_one_step, dict_two_step, text):
    length = len(text)
    for i in range(0, length, 1):
        first_letter = text[i]
        if dict_letters.get(first_letter) is None:
            dict_letters[first_letter] = 1
        else:
            dict_letters[first_letter] += 1
        if i < length - 1:
            second_letter = text[i + 1]
            bigram = first_letter + second_letter
            if dict_one_step.get(bigram) is None:
                dict_one_step[bigram] = 1
            else:
                dict_one_step[bigram] += 1
            if i % 2 == 0:
                if dict_two_step.get(bigram) is None:
                    dict_two_step[bigram] = 1
                else:
                    dict_two_step[bigram] += 1
    for key in dict_letters:
        dict_letters[key] = dict_letters[key] / length
    for key in dict_one_step:
        dict_one_step[key] = dict_one_step[key] / length
    for key in dict_two_step:
        dict_two_step[key] = dict_two_step[key] / length * 2


def make_bigram(dict, name):
    pd = pandas.DataFrame(index=alphabet, columns=alphabet)
    for letter in alphabet:
        for second_letter in alphabet:
            if dict.get(letter + second_letter) is not None:
                pd[second_letter][letter] = dict[letter + second_letter]
            else:
                pd[second_letter][letter] = 0
    pd.to_excel(f"{name}.xlsx")


def enthropy(dict, n):
    summ = 0
    for keys in dict:
        if dict[keys] != 0:
            summ += dict[keys] * log2(dict[keys])
    return 1 / n * -summ


# TODO считать текст
with open("text2.txt", 'r', encoding='utf8') as data_file:
    text = data_file.read()
    text = text.lower()

sort()

walk_through(letter_count, bigrams_count, bigrams_count_2, text)

letters1 = pandas.DataFrame(
    {"Letter": [key for key in letter_count], "Frequency": [letter_count[key] for key in letter_count]})
letters1 = letters1.sort_values(by='Frequency', ascending=False, ignore_index=True)
letters1.to_excel("letters1.xlsx", index=False)

make_bigram(bigrams_count, 'bigrams1')
make_bigram(bigrams_count_2, 'bigrams2')

text = text.replace(' ', '')
# TODO посчитать энтропии
h1 = enthropy(letter_count, 1)
h2 = enthropy(bigrams_count, 2)
h3 = enthropy(bigrams_count_2, 2)
print(f"Entropy with spaces: for letters - {h1}, for bigrams - {h2}, for bigrams with step 2 - {h3}")

alphabet.remove(' ')

walk_through(letter_count_2, bigrams_count_3, bigrams_count_4, text)

letters2 = pandas.DataFrame(
    {"Letter": [key for key in letter_count_2], "Frequency": [letter_count_2[key] for key in letter_count_2]})
letters2 = letters2.sort_values(by='Frequency', ascending=False, ignore_index=True)
letters2.to_excel("letters2.xlsx", index=False)

make_bigram(bigrams_count_3, 'bigrams3')
make_bigram(bigrams_count_4, 'bigrams4')

# TODO посчитать энтропии
h11 = enthropy(letter_count_2, 1)
h22 = enthropy(bigrams_count_3, 2)
h33 = enthropy(bigrams_count_4, 2)
print(f"Entropy without spaces: for letters - {h11}, for bigrams - {h22}, for bigrams with step 2 - {h33}")
