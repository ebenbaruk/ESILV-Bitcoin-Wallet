# ESILV Bitcoin Wallet - BIP39 / BIP32 command line tool


def menu():
    print()
    print("===== ESILV Bitcoin Wallet =====")
    print("1 - Generate wallet")
    print("2 - Import mnemonic")
    print("3 - Show master keys")
    print("4 - Derive child key")
    print("5 - Exit")
    return input("> ").strip()


def main():
    while True:
        choice = menu()
        if choice == "5":
            print("Bye!")
            break
        else:
            print("Not implemented yet")


if __name__ == "__main__":
    main()
