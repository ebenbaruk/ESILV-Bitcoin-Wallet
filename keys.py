import hashlib
import hmac

from ecdsa import SECP256k1, SigningKey  # pyright: ignore[reportMissingImports]

# order of the secp256k1 curve
N = SECP256k1.order

# indexes >= 2^31 are hardened
HARDENED = 2 ** 31


def master_keys(seed):

    i = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return i[:32], i[32:]


def public_key(private_key):

    # ecdsa is only used here
    key = SigningKey.from_string(private_key, curve=SECP256k1)
    point = key.get_verifying_key().to_string()

    x = point[:32]
    y = point[32:]

    # compressed key: 02 if y is even, 03 if y is odd
    if y[-1] % 2 == 0:

        return b"\x02" + x

    else:

        return b"\x03" + x


def child_key(private_key, chain_code, index):

    if index >= HARDENED:

        data = b"\x00" + private_key + index.to_bytes(4, "big")

    else:

        data = public_key(private_key) + index.to_bytes(4, "big")

    i = hmac.new(chain_code, data, hashlib.sha512).digest()

    child = (int.from_bytes(i[:32], "big") + int.from_bytes(private_key, "big")) % N

    return child.to_bytes(32, "big"), i[32:]


def root_key(private_key, chain_code):

    # xprv, same as "BIP32 Root Key" on Ian Coleman
    # depth, fingerprint and index are all 0 for the master key
    data = bytes.fromhex("0488ade4") + b"\x00" * 9 + chain_code + b"\x00" + private_key

    check = hashlib.sha256(hashlib.sha256(data).digest()).digest()
    data = data + check[:4]

    # base58
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    number = int.from_bytes(data, "big")
    text = ""

    while number > 0:

        text = alphabet[number % 58] + text
        number = number // 58

    return text


def parse_path(path):
    # "m/44'/0/5" -> [44 + HARDENED, 0, 5]
    parts = path.split("/")

    if parts[0] != "m":

        return None

    indexes = []

    for part in parts[1:]:

        number = part.replace("'", "")

        if not number.isdigit() or int(number) >= HARDENED:

            return None

        index = int(number)

        if part.endswith("'"):
            
            index = index + HARDENED

        indexes.append(index)

    return indexes
