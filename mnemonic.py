import hashlib

# the 2048 words of the BIP39 english list
with open("english.txt") as f:

    WORDS = f.read().split()


def to_binary(number, size):

    bits = bin(number)[2:]

    while len(bits) < size:

        bits = "0" + bits

    return bits


def to_bits(data):

    bits = ""

    for byte in data:

        bits = bits + to_binary(byte, 8)

    return bits


def checksum(entropy):

    digest = hashlib.sha256(entropy).digest()
    return to_bits(digest)[:4]


def entropy_to_mnemonic(entropy):

    bits = to_bits(entropy) + checksum(entropy)

    print("Checksum:", checksum(entropy))

    words = []

    # groups of 11 bits, each one is a word
    for i in range(0, len(bits), 11):

        group = bits[i:i + 11]
        number = int(group, 2)
        word = WORDS[number]

        print(" ", group, "=", number, "->", word)

        words.append(word)

    return " ".join(words)


def is_valid(mnemonic):

    words = mnemonic.split()

    if len(words) != 12:

        return False

    bits = ""

    for word in words:

        if word not in WORDS:
            return False

        bits = bits + to_binary(WORDS.index(word), 11)

    # 12 words = 132 bits = 128 bits of entropy + 4 bits of checksum
    entropy = int(bits[:128], 2).to_bytes(16, "big")

    return checksum(entropy) == bits[128:]


def mnemonic_to_seed(mnemonic):
    
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode(), b"mnemonic", 2048)
