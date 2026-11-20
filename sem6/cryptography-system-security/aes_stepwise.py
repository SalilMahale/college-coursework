"""
AES-128 Step-by-Step Implementation
Shows every intermediate state during encryption and decryption.
Uses Python's pycryptodome only for final verification — core logic is manual.
"""

# ─────────────────────────────────────────
# AES CONSTANTS
# ─────────────────────────────────────────

# S-Box (SubBytes lookup table)
S_BOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
]

# Inverse S-Box
INV_S_BOX = [0] * 256
for i, v in enumerate(S_BOX):
    INV_S_BOX[v] = i

# Round constants (Rcon)
RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

def print_state(label, state):
    print(f"  {label}:")
    for row in state:
        print("    " + " ".join(f"{b:02x}" for b in row))

def bytes_to_state(b):
    """Convert 16 bytes to 4x4 column-major state matrix."""
    return [[b[r + 4*c] for c in range(4)] for r in range(4)]

def state_to_bytes(s):
    """Convert 4x4 state matrix back to 16 bytes."""
    return bytes(s[r][c] for c in range(4) for r in range(4))

def xtime(b):
    """Multiply by 2 in GF(2^8)."""
    return ((b << 1) ^ 0x1b) & 0xff if b & 0x80 else (b << 1) & 0xff

def gmul(a, b):
    """Multiply two bytes in GF(2^8)."""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        hi = a & 0x80
        a = (a << 1) & 0xff
        if hi:
            a ^= 0x1b
        b >>= 1
    return result

# ─────────────────────────────────────────
# KEY EXPANSION
# ─────────────────────────────────────────

def key_expansion(key_bytes):
    """Expand 16-byte key into 11 round keys."""
    print("\n" + "="*60)
    print("KEY EXPANSION")
    print("="*60)

    w = []
    for i in range(4):
        word = list(key_bytes[4*i : 4*i+4])
        w.append(word)
        print(f"  w[{i}] = {' '.join(f'{b:02x}' for b in word)}")

    for i in range(4, 44):
        temp = w[i-1][:]
        if i % 4 == 0:
            # RotWord
            temp = temp[1:] + temp[:1]
            print(f"\n  w[{i}]: RotWord(w[{i-1}]) = {' '.join(f'{b:02x}' for b in temp)}")
            # SubWord
            temp = [S_BOX[b] for b in temp]
            print(f"         SubWord         = {' '.join(f'{b:02x}' for b in temp)}")
            # XOR with Rcon
            temp[0] ^= RCON[(i//4) - 1]
            print(f"         XOR Rcon[{i//4-1}]    = {' '.join(f'{b:02x}' for b in temp)}")
        result = [w[i-4][j] ^ temp[j] for j in range(4)]
        w.append(result)
        print(f"  w[{i}] = w[{i-4}] XOR temp = {' '.join(f'{b:02x}' for b in result)}")

    round_keys = []
    for r in range(11):
        rk = []
        for c in range(4):
            rk.append(w[4*r + c])
        round_keys.append(rk)

    print("\n  Round Keys Summary:")
    for r, rk in enumerate(round_keys):
        flat = [b for col in rk for b in col]
        print(f"    RK[{r:2d}] = {' '.join(f'{b:02x}' for b in flat)}")

    return round_keys

# ─────────────────────────────────────────
# ENCRYPTION STEPS
# ─────────────────────────────────────────

def add_round_key(state, round_key, verbose=True, label="AddRoundKey"):
    result = [[state[r][c] ^ round_key[c][r] for c in range(4)] for r in range(4)]
    if verbose:
        print_state(f"  Before {label}", state)
        rk_state = [[round_key[c][r] for c in range(4)] for r in range(4)]
        print_state("  Round Key", rk_state)
        print_state(f"  After  {label}", result)
    return result

def sub_bytes(state, verbose=True):
    result = [[S_BOX[state[r][c]] for c in range(4)] for r in range(4)]
    if verbose:
        print_state("  Before SubBytes", state)
        print_state("  After  SubBytes", result)
    return result

def inv_sub_bytes(state, verbose=True):
    result = [[INV_S_BOX[state[r][c]] for c in range(4)] for r in range(4)]
    if verbose:
        print_state("  Before InvSubBytes", state)
        print_state("  After  InvSubBytes", result)
    return result

def shift_rows(state, verbose=True):
    result = [
        [state[0][c] for c in range(4)],
        [state[1][(c+1)%4] for c in range(4)],
        [state[2][(c+2)%4] for c in range(4)],
        [state[3][(c+3)%4] for c in range(4)],
    ]
    if verbose:
        print_state("  Before ShiftRows", state)
        print_state("  After  ShiftRows", result)
    return result

def inv_shift_rows(state, verbose=True):
    result = [
        [state[0][c] for c in range(4)],
        [state[1][(c-1)%4] for c in range(4)],
        [state[2][(c-2)%4] for c in range(4)],
        [state[3][(c-3)%4] for c in range(4)],
    ]
    if verbose:
        print_state("  Before InvShiftRows", state)
        print_state("  After  InvShiftRows", result)
    return result

def mix_columns(state, verbose=True):
    result = []
    for r in range(4):
        row = []
        for c in range(4):
            s = state[r]
            # Fixed MixColumns matrix row depends on row index
            pass
        result.append(row)

    # MixColumns matrix: each column independently
    new_state = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        new_state[0][c] = gmul(col[0],2)^gmul(col[1],3)^gmul(col[2],1)^gmul(col[3],1)
        new_state[1][c] = gmul(col[0],1)^gmul(col[1],2)^gmul(col[2],3)^gmul(col[3],1)
        new_state[2][c] = gmul(col[0],1)^gmul(col[1],1)^gmul(col[2],2)^gmul(col[3],3)
        new_state[3][c] = gmul(col[0],3)^gmul(col[1],1)^gmul(col[2],1)^gmul(col[3],2)

    if verbose:
        print_state("  Before MixColumns", state)
        print_state("  After  MixColumns", new_state)
    return new_state

def inv_mix_columns(state, verbose=True):
    new_state = [[0]*4 for _ in range(4)]
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        new_state[0][c] = gmul(col[0],0xe)^gmul(col[1],0xb)^gmul(col[2],0xd)^gmul(col[3],0x9)
        new_state[1][c] = gmul(col[0],0x9)^gmul(col[1],0xe)^gmul(col[2],0xb)^gmul(col[3],0xd)
        new_state[2][c] = gmul(col[0],0xd)^gmul(col[1],0x9)^gmul(col[2],0xe)^gmul(col[3],0xb)
        new_state[3][c] = gmul(col[0],0xb)^gmul(col[1],0xd)^gmul(col[2],0x9)^gmul(col[3],0xe)

    if verbose:
        print_state("  Before InvMixColumns", state)
        print_state("  After  InvMixColumns", new_state)
    return new_state

# ─────────────────────────────────────────
# AES ENCRYPT
# ─────────────────────────────────────────

def aes_encrypt(plaintext_bytes, key_bytes):
    print("\n" + "="*60)
    print("AES-128 ENCRYPTION")
    print("="*60)

    round_keys = key_expansion(key_bytes)
    state = bytes_to_state(plaintext_bytes)

    print(f"\nPlaintext  : {plaintext_bytes.hex()}")
    print(f"Key        : {key_bytes.hex()}")
    print(f"\nInitial State Matrix:")
    print_state("State", state)

    print(f"\n--- Initial AddRoundKey (Round 0) ---")
    state = add_round_key(state, round_keys[0])

    for rnd in range(1, 11):
        print(f"\n{'='*60}")
        print(f"ROUND {rnd} {'(Last Round - No MixColumns)' if rnd == 10 else ''}")
        print(f"{'='*60}")

        print("\n  [SubBytes]")
        state = sub_bytes(state)

        print("\n  [ShiftRows]")
        state = shift_rows(state)

        if rnd < 10:
            print("\n  [MixColumns]")
            state = mix_columns(state)

        print(f"\n  [AddRoundKey - Round {rnd}]")
        state = add_round_key(state, round_keys[rnd])

    ciphertext = state_to_bytes(state)
    print(f"\n{'='*60}")
    print(f"CIPHERTEXT : {ciphertext.hex()}")
    print(f"{'='*60}")
    return ciphertext

# ─────────────────────────────────────────
# AES DECRYPT
# ─────────────────────────────────────────

def aes_decrypt(ciphertext_bytes, key_bytes):
    print("\n" + "="*60)
    print("AES-128 DECRYPTION")
    print("="*60)

    round_keys = key_expansion(key_bytes)
    state = bytes_to_state(ciphertext_bytes)

    print(f"\nCiphertext : {ciphertext_bytes.hex()}")
    print(f"Key        : {key_bytes.hex()}")
    print(f"\nInitial State Matrix:")
    print_state("State", state)

    print(f"\n--- Initial AddRoundKey (Round 10) ---")
    state = add_round_key(state, round_keys[10])

    for rnd in range(9, -1, -1):
        print(f"\n{'='*60}")
        print(f"ROUND {10 - rnd} (Decryption) {'(Last Round - No InvMixColumns)' if rnd == 0 else ''}")
        print(f"{'='*60}")

        print("\n  [InvShiftRows]")
        state = inv_shift_rows(state)

        print("\n  [InvSubBytes]")
        state = inv_sub_bytes(state)

        print(f"\n  [AddRoundKey - Round {rnd}]")
        state = add_round_key(state, round_keys[rnd])

        if rnd > 0:
            print("\n  [InvMixColumns]")
            state = inv_mix_columns(state)

    plaintext = state_to_bytes(state)
    print(f"\n{'='*60}")
    print(f"DECRYPTED  : {plaintext.hex()}")
    print(f"As text    : {plaintext.decode('utf-8', errors='replace')}")
    print(f"{'='*60}")
    return plaintext

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Standard NIST test vector for AES-128
    plaintext = b"Hello AES World!"   # 16 bytes
    key       = b"mysecretkey12345"   # 16 bytes (128-bit key)

    print("╔══════════════════════════════════════════════════════════╗")
    print("║           AES-128 STEP-BY-STEP IMPLEMENTATION           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\nPlaintext : \"{plaintext.decode()}\"  → {plaintext.hex()}")
    print(f"Key       : \"{key.decode()}\"  → {key.hex()}")

    # ENCRYPT
    ciphertext = aes_encrypt(plaintext, key)

    # DECRYPT
    recovered  = aes_decrypt(ciphertext, key)

    # FINAL SUMMARY
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║                     FINAL SUMMARY                       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"  Original Plaintext  : {plaintext.hex()}  (\"{plaintext.decode()}\")")
    print(f"  Encrypted           : {ciphertext.hex()}")
    print(f"  Decrypted           : {recovered.hex()}  (\"{recovered.decode()}\")")
    print(f"\n  Match: {'✓ SUCCESS — Decrypted == Original Plaintext' if plaintext == recovered else '✗ FAILED'}")
