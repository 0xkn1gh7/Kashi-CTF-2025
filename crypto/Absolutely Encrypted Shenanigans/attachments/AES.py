def xor(b1, b2):
    if len(b1)!=len(b2):
        raise ValueError("Lengths of byte strings are not equal")
    return bytes([b1[i]^b2[i] for i in range(len(b1))])

def bytes2matrix(text):
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    s = b""
    for l in matrix:
        s += bytes(l)
    return s
    
def shift_rows(s):
    s[2][2], s[2][1], s[0][3], s[2][0], s[3][3], s[2][3], s[3][1], s[1][3], s[0][2], s[1][0], s[0][1], s[0][0], s[1][1], s[3][0], s[3][2], s[1][2] = s[2][2], s[3][3], s[0][0], s[1][1], s[2][1], s[1][2], s[3][0], s[2][3], s[0][3], s[0][2], s[3][2], s[0][1], s[3][1], s[1][0], s[2][0], s[1][3]
    return s


xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)
    return a


def mix_columns(s):
    for i in range(4):
        s[i] = mix_single_column(s[i])
    return s


s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

    
def add_round_key(s, k):
    ns = []
    for i in range(4):
        ns.append([])
        for j in range(4):
            ns[i].append(s[i][j]^k[j][i])
    return ns

def sub_bytes(s, sbox=s_box):
    resmatrix = []
    for i in range(4):
        resmatrix.append([])
        for j in range(4):
            hexval=hex(s[i][j])[2:]
            if len(hexval)==1:
                a,b = 0,int(hexval,16)
            else:
                a,b = int(hexval[0],16), int(hexval[1],16)
            resmatrix[i].append(sbox[a*16+b])
            
    return resmatrix


N_ROUNDS = 10


def expand_key(master_key):
    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )
    key_columns = bytes2matrix(master_key)
    iteration_size = len(master_key) // 4
    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        word = list(key_columns[-1])
        if len(key_columns) % iteration_size == 0:
            word.append(word.pop(0))
            word = [s_box[b] for b in word]
            word[0] ^= r_con[i]
            i += 1
        elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
            word = [s_box[b] for b in word]
        word = bytes(i^j for i, j in zip(word, key_columns[-iteration_size]))
        key_columns.append(word)
    return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]


def encrypt_block(key, pt_block):
    round_keys = expand_key(key)
    state = bytes2matrix(pt_block)
    state = add_round_key(state, round_keys[0])
    state = sub_bytes(state)
    state = shift_rows(state)

    for i in range(1,N_ROUNDS):
        state = mix_columns(state)
        state = add_round_key(state, round_keys[i])
        state = sub_bytes(state)
        state = shift_rows(state)
    
    state = add_round_key(state, round_keys[N_ROUNDS])
    ct_block = matrix2bytes(state)

    return ct_block


def encrypt(key, plaintext, mode="ECB", iv=None):
    if len(plaintext)%16 != 0:
        raise ValueError("Invalid Plaintext")
    elif len(key)!=16:
        raise ValueError("Invalid Key")
    ciphertext = b""
    if mode=="ECB":
        for i in range(0, len(plaintext), 16):
            ciphertext += encrypt_block(key, plaintext[i: i+16])
        
    elif mode=="CBC":
        if (iv==None or len(iv)!=16):
            raise ValueError("Invalid IV")
        ciphertext += iv
        for i in range(0, len(plaintext), 16):
            ciphertext += encrypt_block(key, xor(ciphertext[i: i+16], plaintext[i: i+16]))
        
    return ciphertext[16:]


def pad(text, blocksize):
    padding_len = blocksize - (len(text)%blocksize)
    padding = bytes([padding_len])*padding_len
    return text+padding
