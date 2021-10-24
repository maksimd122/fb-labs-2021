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

with open("text2.txt", 'r', encoding='utf8') as data_file:
    text = data_file.read()
    text = text.lower()


def sort(text_un):
    text_un = text_un.replace("\n\n", " ")
    text_un = text_un.replace("\n", " ")
    characters = [',', '.', '!', '?', '"', ':', ';', "'", '-', "—", '…', '«', "»", '*', '(', ')', '1', '2', '3', '4',
                  '5', '6', '7', '8', '9', '№', '0', '“', '„', '́', 'c']
    for character in characters:
        text_un = text_un.replace(character, '')
    while text_un.find("  ") != -1:
        text_un = text_un.replace("  ", " ")
    return text_un


text = sort(text)
