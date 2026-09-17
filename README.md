# ESILV Bitcoin Wallet

A simple command line Bitcoin wallet written in Python.

## Context

I made this project for the **Blockchain Programming** course at **ESILV** (engineering school, A4). It's the second practical workshop (TD2) of the course, about wallet management.

The goal of the workshop is to understand how a Bitcoin HD wallet works by writing the logic yourself:

- **BIP39**: generate a random seed, turn it into a list of words (mnemonic), and import an existing mnemonic
- **BIP32**: get the master private key, chain code and public key from the seed, then derive child keys at any index `N` and depth `M`

The workshop rule is that Bitcoin or HD wallet libraries can't be used. Only basic math and hash functions (SHA256, HMAC, PBKDF2) are allowed, plus a library to get a public key from a private key.

## Installation

You need **Python 3** and **git**.

1. Clone the repository:

```bash
git clone https://github.com/ebenbaruk/ESILV-Bitcoin-Wallet.git
cd ESILV-Bitcoin-Wallet
```

2. (Optional) Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
```

3. Install the only dependency (`ecdsa`):

```bash
pip install -r requirements.txt
```

## Run

Run the program **from the project folder** (it needs to read `english.txt`):

```bash
python3 main.py
```

The menu appears:

```
1 - Generate wallet
2 - Import mnemonic
3 - Show master keys
4 - Derive child key
5 - Exit
>
```

Type the number of an option and press **Enter**. The menu comes back after each action.

## How to use the CLI

### 1 - Generate wallet

Creates a new random wallet. Nothing to type.

The program shows:

- the entropy (128 random bits) as an **integer**, **bytes**, **hex** and **binary**
- the **checksum** (4 bits)
- each **11-bit group**, its number (0 to 2047) and the matching word
- the final **mnemonic** (12 words)

The generated wallet becomes the current wallet, so you can use options 3 and 4 right after.

### 2 - Import mnemonic

Loads an existing wallet. Paste or type a 12-word mnemonic, with a space between each word:

```
Mnemonic: album arctic segment alcohol sight humble lend habit only stone useful reopen
Valid mnemonic
```

The program checks that there are 12 words, that every word is in the BIP39 list and that the checksum is correct. If something is wrong it prints `Invalid mnemonic` and keeps the previous wallet.

### 3 - Show master keys

Needs a wallet (option 1 or 2 first). Shows:

- **Seed**: 64 bytes computed from the mnemonic
- **Private key**: master private key
- **Chain code**: master chain code
- **Public key**: master public key (compressed)
- **BIP32 root key**: the master key in `xprv` format, to compare with Ian Coleman

### 4 - Derive child key

Needs a wallet. Type a **derivation path** that starts with `m`:

| What you want | Path to type |
| --- | --- |
| a child key | `m/0` |
| child key at index `N` (ex: N = 7) | `m/7` |
| child key at index `N` and depth `M` (ex: N = 5, M = 3) | `m/0/0/5` |
| hardened keys (with `'`) | `m/44'/0'/0'/0/5` |

The program derives the keys one level at a time, shows the path as a small tree, then prints the **depth**, the **private key**, the **chain code** and the **public key** of the last key.

If the path is not valid (doesn't start with `m`, contains letters, ...) it prints `Invalid path`.

### 5 - Exit

Closes the program.

There is also a little easter egg hidden in the code, have fun finding it.

## BIP39

BIP39 turns a random number into words that are easy to write down.

1. Generate 128 random bits (entropy) with `secrets`.
2. Checksum = first 4 bits of `SHA256(entropy)`.
3. Entropy + checksum = 132 bits → 12 groups of 11 bits.
4. Each group is a number between 0 and 2047 → a word in `english.txt`.
5. To import a mnemonic, we turn the words back into bits and check the checksum.
6. Seed = `PBKDF2-HMAC-SHA512(mnemonic, "mnemonic", 2048 rounds)`.

## BIP32

BIP32 creates a tree of keys from the seed.

- `I = HMAC-SHA512("Bitcoin seed", seed)`
- master private key = left 32 bytes, master chain code = right 32 bytes
- master public key = private key × G on secp256k1

Child key at index `i`:

- normal: `I = HMAC-SHA512(chain code, public key + i)`
- hardened (`i'`): `I = HMAC-SHA512(chain code, 0x00 + private key + (i + 2^31))`
- child private key = `(left of I + parent private key) mod n`, child chain code = right of I

In the path `m/44'/0'/0'/0/5`, the depth `M` is the number of levels (5) and the index `N` is the last number (5).

## Implementation choices

- The code is split in a few files: `mnemonic.py` (BIP39), `keys.py` (BIP32), `cli.py` (the menu) and `main.py` to run it.
- No Bitcoin library (forbidden by the workshop): checksum, words, HMAC, child keys and root key are written by hand with `hashlib`, `hmac` and `secrets`.
- `ecdsa` is only used to compute the public key from the private key (allowed).
- `english.txt` is the official BIP39 English wordlist (2048 words).
- Only 12-word mnemonics (128 bits) and no BIP39 passphrase, to keep things simple.

## Verify with Ian Coleman

1. Open https://iancoleman.io/bip39/ and paste the mnemonic in **BIP39 Mnemonic**.
2. Compare **BIP39 Seed** and **BIP32 Root Key** with option 3.
3. For a child key like `m/0/5`: go to the **BIP32** tab, set the derivation path to `m/0`, and compare the public key of row `m/0/5` with option 4.
4. For a hardened path like `m/44'/0'/0'/0/3`: go to the **BIP44** tab and compare the public key of row `m/44'/0'/0'/0/3`.

⚠️ This is a school project, don't use it for real bitcoins.
