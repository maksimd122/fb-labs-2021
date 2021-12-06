from random import randint


# Додаткові функції
def kpi_re(a, b):
    def euclid(a, b):
        if not b:
            return 1, 0, a
        y, x, d = euclid(b, a % b)
        return x, y - (a // b) * x, d

    x, _, _ = euclid(a, b)
    return x


def gcd(a, b, u=[1, 0], v=[0, 1]):
    r = a % b
    q = (a - r) / b
    u_next = u[0] - q * u[1]
    v_next = v[0] - q * v[1]
    if r == 0:
        return [b, u[1], v[1]]
    else:
        return gcd(b, r, [u[1], u_next], [v[1], v_next])


def gorner(e, n, x):
    bin_e = bin(e)
    y = 1
    for i in range(len(bin_e) - 2):
        y = (y ** 2) % n
        if int(bin_e[i + 2]) == 1:
            y = (x * y) % n
    return y


#####################


def rand_number():
    number = randint(2 ** 255, 2 ** 258)
    while number % 2 == 0:
        number = randint(2 ** 255, 2 ** 258)
    return number


def miller_test(p):
    m = 100
    counter = 0
    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    while counter < m:
        x = randint(2, p - 1)
        if gcd(x, p)[0] > 1:
            return False
        elif gorner(d, p, x) == 1 or gorner(d, p, x) == p - 1:
            counter += 1
            continue
        else:
            quit = False
            for r in range(1, s):
                x_r = gorner(d * (2 ** r), p, x)
                if x_r == p - 1:
                    counter += 1
                    quit = True
                    break
                elif x_r == 1:
                    return False
            if quit:
                continue
            return False
    return True


def GenerateKeyPair():
    first_key = rand_number()
    while not miller_test(first_key):
        first_key = rand_number()
    second_key = rand_number()
    while not miller_test(second_key):
        second_key = rand_number()
    n = first_key * second_key
    oyler_func = (first_key - 1) * (second_key - 1)
    e = randint(2, oyler_func - 1)
    while gcd(e, oyler_func)[0] != 1:
        e = randint(2, oyler_func - 1)
    d = kpi_re(e, oyler_func) % oyler_func
    return (d, first_key, second_key), (n, e)


def Encrypt(plain_text, open_key):
    n = open_key[0]
    e = open_key[1]
    ciphertext = gorner(e, n, plain_text)
    return ciphertext


def Decrypt(ciphertext, open_key, private_key):
    n = open_key[0]
    d = private_key[0]
    plain_text = gorner(d, n, ciphertext)
    return plain_text


def Sign(plain_text, private_key, open_key):
    sign = gorner(private_key[0], open_key[0], plain_text)
    return sign


def Verify(plain_text, sign, open_key):
    new_text = gorner(open_key[1], open_key[0], sign)
    if new_text == plain_text:
        return True
    else:
        return False


def ReceiveKey(ciphertext, cipher_sign, private_key, open_key_first, open_key_second):
    plain_text = Decrypt(ciphertext, open_key_first, private_key)
    sign = Decrypt(cipher_sign, open_key_first, private_key)
    verified = Verify(plain_text, sign, open_key_second)
    print("Message was received")
    return plain_text, verified


def SendKey(plain_text, private_key, open_key_first, open_key_second):
    ciphertext = Encrypt(plain_text, open_key_first)
    sign = Sign(plain_text, private_key, open_key_second)
    cipher_sign = Encrypt(sign, open_key_first)
    print("Message was generated")
    return ciphertext, cipher_sign


second_pair = GenerateKeyPair()
print("Second pair was generated")
first_pair = GenerateKeyPair()
while first_pair[0][1] * first_pair[0][2] > second_pair[0][1] * second_pair[0][2]:
    first_pair = GenerateKeyPair()
print("First pair was generated")

plain_text = randint(1, 2 ** 255)
print("\n", plain_text)

k, s = SendKey(plain_text, first_pair[0], second_pair[1], first_pair[1])
mess, ver = ReceiveKey(k, s, second_pair[0], second_pair[1], first_pair[1])
if ver:
    print(mess, "Verified from A to B")

k, s = SendKey(plain_text, second_pair[0], first_pair[1], second_pair[1])
mess, ver = ReceiveKey(k, s, first_pair[0], first_pair[1], second_pair[1])
if ver:
    print(mess, "Verified from B to A")
# print(first_pair[1])
# n = 31112285075822532646729297530475648802686015336023437238550519326095914087104717002934043460402427959576991463143012659235950011608951046128966210431217121571
# e = 65537
# print(SendKey(plain_text, first_pair[0], (n, e), first_pair[1]))
