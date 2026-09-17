import secrets

from keys import child_key, master_keys, parse_path, public_key, root_key
from mnemonic import entropy_to_mnemonic, is_valid, mnemonic_to_seed, to_bits

# Meme
LAMBO = r"""
                         W E N   L A M B O  ?

                      _______________________
             ___..--''     |           |     ''--.._
       _.--''              |           |            '-._
     .'_________ __________|___________|___ ___________ '.
    |   .---.   |                          |   .---.    |=
    '--( (o) )--'--------------------------'--( (o) )---'
         '---'                                  '---'

    me in 2021: "bought 0.002 BTC, lambo soon trust me"

 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    me in 2026:
                    __o
                  _ \<_          portfolio: -87%
                 (_)/(_)         lambo: still loading...
"""


def main():
    mnemonic = None

    while True:
        print()
        print("1 - Generate wallet")
        print("2 - Import mnemonic")
        print("3 - Show master keys")
        print("4 - Derive child key")
        print("5 - Exit")
        print("6 - Click on me Nathan")

        choice = input("> ")

        if choice == "1":
            entropy = secrets.token_bytes(16)  # 128 bits

            print("Entropy int   :", int.from_bytes(entropy, "big"))
            print("Entropy bytes :", entropy)
            print("Entropy hex   :", entropy.hex())
            print("Entropy binary:", to_bits(entropy))

            mnemonic = entropy_to_mnemonic(entropy)


            print("Mnemonic:", mnemonic)



        elif choice == "2":
            text = input("Mnemonic: ").strip().lower()

            if is_valid(text):
                mnemonic = text
                print("Valid mnemonic")


            else:

                print("Invalid mnemonic")

        elif choice == "3" or choice == "4":

            if mnemonic is None:

                print("Generate or import a wallet first")
                continue

            seed = mnemonic_to_seed(mnemonic)
            key, chain = master_keys(seed)

            if choice == "3":

                print("Seed          :", seed.hex())
                print("Private key   :", key.hex())
                print("Chain code    :", chain.hex())
                print("Public key    :", public_key(key).hex())
                print("BIP32 root key:", root_key(key, chain))
                continue

            path = input("Path, ex: m/0 or m/44'/0'/0'/0/5: ").strip()
            indexes = parse_path(path)

            if indexes is None:

                print("Invalid path")
                continue

            parts = path.split("/")
            depth = 0

            print("m")

            # one level at a time
            for index in indexes:

                key, chain = child_key(key, chain, index)
                depth = depth + 1
                print("  " * depth + "└─ " + parts[depth])

            print("Depth      :", depth)
            print("Private key:", key.hex())
            print("Chain code :", chain.hex())
            print("Public key :", public_key(key).hex())

        elif choice == "5":

            print("Bye")
            break

        elif choice == "6":
            
            print(LAMBO)
