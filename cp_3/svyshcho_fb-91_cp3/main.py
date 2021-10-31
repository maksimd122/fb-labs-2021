alphabet = [chr(code) for code in range(ord("а"), ord("а") + 32)]
alphabet.remove('ъ')

most_frequent_bigrams = ['ст', 'но', 'то', 'на', 'ен']

# TODO Считать текст
with open("18.txt", 'r', encoding='utf8') as data_file:
    text_r = data_file.read()


def sort(text_un):
    for character in text_un:
        if character not in alphabet:
            text_un = text_un.replace(character, "")
    return text_un


# TODO ищем 5 самых частых биграм

def walk_through(text):
    dict_bigrams = {}
    length = len(text)
    for i in range(0, length, 1):
        first_letter = text[i]
        if i < length - 1:
            second_letter = text[i + 1]
            bigram = first_letter + second_letter
            if dict_bigrams.get(bigram) is None:
                dict_bigrams[bigram] = 1
            else:
                dict_bigrams[bigram] += 1
    max_bigrams = ["", '', '', '', '']
    max_freq = [0, 0, 0, 0, 0]
    for key in dict_bigrams:
        dict_bigrams[key] = value = dict_bigrams[key] / length
        for i in range(5):
            if dict_bigrams[key] > max_freq[i]:
                max_bigrams[i] = key
                max_freq[i] = value
                break
    return max_bigrams


# TODO Алгоритм Эвклида
def gcd(a, b, u=[1, 0], v=[0, 1]):
    r = a % b
    q = (a - r) / b
    u_next = u[0] - q * u[1]
    v_next = v[0] - q * v[1]
    if r == 0:
        return [b, u[1], v[1]]
    else:
        return gcd(b, r, [u[1], u_next], [v[1], v_next])


# TODO Найти ключ
def count_bigram(bigram):
    length = len(alphabet)
    number = alphabet.index(bigram[0]) * length + alphabet.index(bigram[1])
    return number


def check_key(open_bigrams, cypher_bigrams):
    length = len(alphabet) * len(alphabet)
    all_keys = []
    for j in range(5):
        for o in range(5):
            if o == j:
                pass
            else:
                for i in range(5):
                    for t in range(5):
                        if t == i:
                            pass
                        else:
                            keys = []
                            first_x = count_bigram(open_bigrams[j])
                            second_x = count_bigram(open_bigrams[o])
                            first_y = count_bigram(cypher_bigrams[i])
                            second_y = count_bigram(cypher_bigrams[t])
                            result_y = first_y - second_y
                            result_x = first_x - second_x
                            divider = gcd(result_x, length)[0]
                            if divider == 1:
                                u = gcd(result_x, length)[1]
                                a = (u * result_y) % length
                                b = (first_y - a * first_x) % length
                                keys.append([a, b])
                            elif divider > 1:
                                if result_y % divider == 0:
                                    for y in range(int(divider)):
                                        a1 = result_x / divider
                                        b1 = result_y / divider
                                        n1 = length / divider
                                        x = ((b1 * gcd(a1, n1)[1]) % n1) + y * n1
                                        a = (x * result_y) % length
                                        b = (first_y - a * first_x) % length
                                        keys.append([a, b])
                                else:
                                    pass
                            all_keys.append(keys)
    return all_keys


# TODO Проверить текст
def check_text(text):
    # banned_bigrams = ["оь", "уь", "еь", "аь", "ыь", "эь", "юь", "яь", "иь", "йь", "жы", "шы", "ээ", "йй", "ааа"]
    banned_bigrams = ["оь", "уь", "еь", "аь", "ыь", "эь", "юь", "яь", "иь", "йь"]
    for bigram in banned_bigrams:
        if bigram in text:
            return False
    return True


# TODO Разшифровать текст
def decipher(text, a, b):
    new_text = ""
    length = len(text)
    alph_pow = len(alphabet) * len(alphabet)
    for i in range(0, length, 2):
        first_letter = text[i]
        if i < length - 1:
            second_letter = text[i + 1]
            bigram = first_letter + second_letter
            counting = count_bigram(bigram)
            a_rev = gcd(a, alph_pow)[1]
            x = ((counting - b) * a_rev) % alph_pow
            new_second_letter = x % len(alphabet)
            new_first_letter = (x - new_second_letter) / len(alphabet)
            new_text += alphabet[int(new_first_letter)] + alphabet[int(new_second_letter)]
    return new_text


text_r = sort(text_r)
cypher_bigrams = walk_through(text_r)
all_keys = check_key(most_frequent_bigrams, cypher_bigrams)
for keys in all_keys:
    for key in keys:
        plain_text = decipher(text_r, key[0], key[1])
        if check_text(plain_text):
            print(key)
            print(plain_text)
