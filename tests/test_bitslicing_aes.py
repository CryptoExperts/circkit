import operator

class Vector(list):
    ZERO = 0
    WIDTH = None

    @classmethod
    def make(cls, lst):
        lst = list(lst)
        if cls.WIDTH is not None:
            assert len(lst) == cls.WIDTH
        return cls(lst)

    def split(self, n=2):
        assert len(self) % n == 0
        w = len(self) // n
        return Vector(self.make(self[i:i+w]) for i in range(0, len(self), w))

    def rol(self, n=1):
        n %= len(self)
        return self.make(self[n:] + self[:n])

    def ror(self, n=1):
        return self.rol(-n)

    def __repr__(self):
        return "<Vector len=%d list=%r>" % (len(self), list(self))

    def flatten(self):
        if isinstance(self[0], Vector):
            return self[0].concat(*self[1:])
        return reduce(operator.add, list(self))

    def map(self, f, with_coord=False):
        if with_coord:
            return self.make(f(i, v) for i, v in enumerate(self))
        else:
            return self.make(f(v) for v in self)

    def __xor__(self, other):
        assert isinstance(other, Vector)
        assert len(self) == len(other)
        return self.make(a ^ b for a, b in zip(self, other))

    def __or__(self, other):
        assert isinstance(other, Vector)
        assert len(self) == len(other)
        return self.make(a | b for a, b in zip(self, other))

    def __and__(self, other):
        assert isinstance(other, Vector)
        assert len(self) == len(other)
        return self.make(a & b for a, b in zip(self, other))

    def set(self, x, val):
        return self.make(v if i != x else val for i, v in enumerate(self))



class Rect(object):
    def __init__(self, vec, h=None, w=None):
        assert h or w
        if h:
            w = len(vec) // h
        elif w:
            h = len(vec) // w
        assert w * h == len(vec)
        self.w, self.h = w, h

        self.lst = []
        for i in range(0, len(vec), w):
            self.lst.append(list(vec[i:i+w]))

    @classmethod
    def from_rect(cls, rect):
        self = object.__new__(cls)
        self.lst = rect
        self.h = len(rect)
        self.w = len(rect[0])
        return self

    def __getitem__(self, pos):
        y, x = pos
        return self.lst[y][x]

    def __setitem__(self, pos, val):
        y, x = pos
        self.lst[y][x] = val

    def row(self, i):
        return Vector(self.lst[i])

    def col(self, i):
        return Vector(self.lst[y][i] for y in range(self.h))

    def set_row(self, y, vec):
        for x in range(self.w):
            self.lst[y][x] = vec[x]
        return self

    def set_col(self, x, vec):
        for y in range(self.h):
            self.lst[y][x] = vec[y]
        return self

    def apply(self, f, with_coord=False):
        for y in range(self.h):
            if with_coord:
                self.lst[y] = [f(y, x, v) for x, v in enumerate(self.lst[y])]
            else:
                self.lst[y] = list(map(f, self.lst[y]))
        return self

    def apply_row(self, x, func):
        return self.set_row(x, func(self.row(x)))

    def apply_col(self, x, func):
        return self.set_col(x, func(self.col(x)))

    def flatten(self):
        lst = []
        for v in self.lst:
            lst += v
        return Vector(lst)

    def zipwith(self, f, other):
        assert isinstance(other, Rect)
        assert self.h == other.h
        assert self.w == other.w
        return Rect(
            [f(a, b) for a, b in zip(self.flatten(), other.flatten())],
            h=self.h, w=self.w
        )

    def transpose(self):
        rect = [[self.lst[y][x] for y in range(self.h)] for x in range(self.w)]
        return Rect.from_rect(rect=rect)

    def __repr__(self):
        return "<Rect %dx%d>" % (self.h, self.w)

# Bitslicing Sbox
def Not(x):
    return 1^x

def GF_SQ_2(A): return A[1], A[0]
def GF_SCLW_2(A): return A[1], A[1] ^ A[0]
def GF_SCLW2_2(A): return A[1] ^ A[0], A[0]

def GF_MULS_2(A, ab, B, cd):
    abcd = (ab & cd)
    p = ((A[1] & B[1])) ^ abcd
    q = ((A[0] & B[0])) ^ abcd
    return q, p

def GF_MULS_SCL_2(A, ab, B, cd):
    t = (A[0] & B[0])
    p = ((ab & cd)) ^ t
    q = ((A[1] & B[1])) ^ t
    return q, p

def XOR_LIST(a, b):
    return [a ^ b for a, b in zip(a, b)]

def NotOr(a, b):
    # return Not(a | b)
    return Not(a) & Not(b)

def GF_INV_4(A):
    a = A[2:4]
    b = A[0:2]
    sa = a[1] ^ a[0]
    sb = b[1] ^ b[0]

    ab = GF_MULS_2(a, sa, b, sb)
    ab2 = GF_SQ_2(XOR_LIST(a, b))
    ab2N = GF_SCLW2_2(ab2)
    d = GF_SQ_2(XOR_LIST(ab, ab2N))

    c = [
        NotOr(sa, sb) ^ (Not(a[0] & b[0])),
        NotOr(a[1], b[1]) ^ (Not(sa & sb)),
    ]

    sd = d[1] ^ d[0]
    p = GF_MULS_2(d, sd, b, sb)
    q = GF_MULS_2(d, sd, a, sa)
    return q + p

def GF_SQ_SCL_4(A):
    a = A[2:4]
    b = A[0:2]
    ab2 = GF_SQ_2(a ^ b)
    b2 = GF_SQ_2(b)
    b2N2 = GF_SCLW_2(b2)
    return b2N2 + ab2

def GF_MULS_4(A, a, Al, Ah, aa, B, b, Bl, Bh, bb):
    ph = GF_MULS_2(A[2:4], Ah, B[2:4], Bh)
    pl = GF_MULS_2(A[0:2], Al, B[0:2], Bl)
    p = GF_MULS_SCL_2(a, aa, b, bb)
    return XOR_LIST(pl, p) + XOR_LIST(ph, p) #(pl ^ p), (ph ^ p)

def GF_INV_8(A):
    a = A[4:8]
    b = A[0:4]
    sa = XOR_LIST(a[2:4], a[0:2])
    sb = XOR_LIST(b[2:4], b[0:2])
    al = a[1] ^ a[0]
    ah = a[3] ^ a[2]
    aa = sa[1] ^ sa[0]
    bl = b[1] ^ b[0]
    bh = b[3] ^ b[2]
    bb = sb[1] ^ sb[0]

    c1 = (ah & bh)
    c2 = (sa[0] & sb[0])
    c3 = (aa & bb)

    c = [
        (NotOr(a[0] , b[0] ) ^ ((al & bl))) ^ ((sa[1] & sb[1])) ^ Not(c2), #0
        (NotOr(al   , bl   ) ^ (Not(a[1] & b[1]))) ^ c2 ^ c3 , #1
        (NotOr(sa[1], sb[1]) ^ (Not(a[2] & b[2]))) ^ c1 ^ c2 , #2
        (NotOr(sa[0], sb[0]) ^ (Not(a[3] & b[3]))) ^ c1 ^ c3 , #3
    ]
    d = GF_INV_4(c)

    sd = XOR_LIST(d[2:4], d[0:2])
    dl = d[1] ^ d[0]
    dh = d[3] ^ d[2]
    dd = sd[1] ^ sd[0]
    p = GF_MULS_4(d, sd, dl, dh, dd, b, sb, bl, bh, bb)
    q = GF_MULS_4(d, sd, dl, dh, dd, a, sa, al, ah, aa)
    return q + p


def MUX21I(A, B, s): #return ((~A & s) ^ (~B & ~s)
    return Not(A if s else B)

def SELECT_NOT_8( A, B, s):
    Q = [None] * 8
    for i in range(8):
        Q[i] = MUX21I(A[i], B[i], s)
    return Q

def Sbox(A, encrypt):
    R1 = A[7] ^ A[5]
    R2 = A[7] ^ Not(A[4])
    R3 = A[6] ^ A[0]
    R4 = A[5] ^ Not(R3)
    R5 = A[4] ^ R4
    R6 = A[3] ^ A[0]
    R7 = A[2] ^ R1
    R8 = A[1] ^ R3
    R9 = A[3] ^ R8

    B = [None] * 8
    B[7] = R7 ^ Not(R8)
    B[6] = R5
    B[5] = A[1] ^ R4
    B[4] = R1 ^ Not(R3)
    B[3] = A[1]^ R2 ^ R6
    B[2] = Not( A[0])
    B[1] = R4
    B[0] = A[2] ^ Not(R9)

    Y = [None] * 8
    Y[7] = R2
    Y[6] = A[4] ^ R8
    Y[5] = A[6] ^ A[4]
    Y[4] = R9
    Y[3] = A[6] ^ Not(R2)
    Y[2] = R7
    Y[1] = A[4] ^ R6
    Y[0] = A[1] ^ R5

    Z = SELECT_NOT_8(B, Y, encrypt)
    C = GF_INV_8(Z)

    T1 = C[7] ^ C[3]
    T2 = C[6] ^ C[4]
    T3 = C[6] ^ C[0]
    T4 = C[5] ^ Not(C[3])
    T5 = C[5] ^ Not(T1)
    T6 = C[5] ^ Not(C[1])
    T7 = C[4] ^ Not(T6)
    T8 = C[2] ^ T4
    T9 = C[1] ^ T2
    T10 = T3 ^ T5

    D = [None] * 8
    D[7] = T4
    D[6] = T1
    D[5] = T3
    D[4] = T5
    D[3] = T2 ^ T5
    D[2] = T3 ^ T8
    D[1] = T7
    D[0] = T9

    X = [None] * 8
    X[7] = C[4] ^ Not(C[1])
    X[6] = C[1] ^ T10
    X[5] = C[2] ^ T10
    X[4] = C[6] ^ Not(C[1])
    X[3] = T8 ^ T9
    X[2] = C[7] ^ Not(T7)
    X[1] = T6
    X[0] = Not(C[2])
    return SELECT_NOT_8(D, X, encrypt)


def bitSbox(A, inverse=False):
    res = Sbox(A[::-1], encrypt=1-inverse)[::-1]
    return res

# Bitslicing ShiftRow and MixColumn
def ShiftRow(row, nr, inverse=False):
    if inverse:
        nr = -nr
    off = nr % 4
    return row[off:] + row[:off]

def MixColumn(col, inverse=False):
    res = [[0] * 8 for _ in range(4)]
    table = MCi_TABLE if inverse else MC_TABLE
    for yi in range(4):
        for yj in range(8):
            y = yi * 8 + yj
            for x in table[y]:
                xi, xj = divmod(x, 8)
                res[yi][yj] ^= col[xi][xj]
    return res

# y -> set of x indices to xor
MC_TABLE = [{1, 8, 9, 16, 24}, {2, 9, 10, 17, 25}, {3, 10, 11, 18, 26}, {0, 4, 8, 11, 12, 19, 27}, {0, 5, 8, 12, 13, 20, 28}, {6, 13, 14, 21, 29}, {0, 7, 8, 14, 15, 22, 30}, {0, 8, 15, 23, 31}, {0, 9, 16, 17, 24}, {1, 10, 17, 18, 25}, {2, 11, 18, 19, 26}, {3, 8, 12, 16, 19, 20, 27}, {4, 8, 13, 16, 20, 21, 28}, {5, 14, 21, 22, 29}, {6, 8, 15, 16, 22, 23, 30}, {7, 8, 16, 23, 31}, {0, 8, 17, 24, 25}, {1, 9, 18, 25, 26}, {2, 10, 19, 26, 27}, {3, 11, 16, 20, 24, 27, 28}, {4, 12, 16, 21, 24, 28, 29}, {5, 13, 22, 29, 30}, {6, 14, 16, 23, 24, 30, 31}, {7, 15, 16, 24, 31}, {0, 1, 8, 16, 25}, {1, 2, 9, 17, 26}, {2, 3, 10, 18, 27}, {0, 3, 4, 11, 19, 24, 28}, {0, 4, 5, 12, 20, 24, 29}, {5, 6, 13, 21, 30}, {0, 6, 7, 14, 22, 24, 31}, {0, 7, 15, 23, 24}]
MCi_TABLE = [{1, 2, 3, 8, 9, 11, 16, 18, 19, 24, 27}, {0, 2, 3, 4, 8, 9, 10, 12, 16, 17, 19, 20, 24, 25, 28}, {1, 3, 4, 5, 8, 9, 10, 11, 13, 17, 18, 20, 21, 24, 25, 26, 29}, {2, 4, 5, 6, 8, 9, 10, 11, 12, 14, 16, 18, 19, 21, 22, 25, 26, 27, 30}, {1, 2, 5, 6, 7, 10, 12, 13, 15, 16, 17, 18, 20, 22, 23, 24, 26, 28, 31}, {1, 6, 7, 8, 9, 13, 14, 17, 21, 23, 24, 25, 29}, {2, 7, 8, 9, 10, 14, 15, 16, 18, 22, 25, 26, 30}, {0, 1, 2, 8, 10, 15, 17, 18, 23, 26, 31}, {0, 3, 9, 10, 11, 16, 17, 19, 24, 26, 27}, {0, 1, 4, 8, 10, 11, 12, 16, 17, 18, 20, 24, 25, 27, 28}, {0, 1, 2, 5, 9, 11, 12, 13, 16, 17, 18, 19, 21, 25, 26, 28, 29}, {1, 2, 3, 6, 10, 12, 13, 14, 16, 17, 18, 19, 20, 22, 24, 26, 27, 29, 30}, {0, 2, 4, 7, 9, 10, 13, 14, 15, 18, 20, 21, 23, 24, 25, 26, 28, 30, 31}, {0, 1, 5, 9, 14, 15, 16, 17, 21, 22, 25, 29, 31}, {1, 2, 6, 10, 15, 16, 17, 18, 22, 23, 24, 26, 30}, {2, 7, 8, 9, 10, 16, 18, 23, 25, 26, 31}, {0, 2, 3, 8, 11, 17, 18, 19, 24, 25, 27}, {0, 1, 3, 4, 8, 9, 12, 16, 18, 19, 20, 24, 25, 26, 28}, {1, 2, 4, 5, 8, 9, 10, 13, 17, 19, 20, 21, 24, 25, 26, 27, 29}, {0, 2, 3, 5, 6, 9, 10, 11, 14, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30}, {0, 1, 2, 4, 6, 7, 8, 10, 12, 15, 17, 18, 21, 22, 23, 26, 28, 29, 31}, {1, 5, 7, 8, 9, 13, 17, 22, 23, 24, 25, 29, 30}, {0, 2, 6, 9, 10, 14, 18, 23, 24, 25, 26, 30, 31}, {1, 2, 7, 10, 15, 16, 17, 18, 24, 26, 31}, {0, 1, 3, 8, 10, 11, 16, 19, 25, 26, 27}, {0, 1, 2, 4, 8, 9, 11, 12, 16, 17, 20, 24, 26, 27, 28}, {0, 1, 2, 3, 5, 9, 10, 12, 13, 16, 17, 18, 21, 25, 27, 28, 29}, {0, 1, 2, 3, 4, 6, 8, 10, 11, 13, 14, 17, 18, 19, 22, 26, 28, 29, 30}, {2, 4, 5, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 23, 25, 26, 29, 30, 31}, {0, 1, 5, 6, 9, 13, 15, 16, 17, 21, 25, 30, 31}, {0, 1, 2, 6, 7, 8, 10, 14, 17, 18, 22, 26, 31}, {0, 2, 7, 9, 10, 15, 18, 23, 24, 25, 26}]


# Bitslicing Key Schedule
Rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
        0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97,
        0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72,
        0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66,
        0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
        0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
        0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
        0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61,
        0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
        0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc,
        0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
        0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
        0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c,
        0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
        0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4,
        0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
        0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08,
        0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
        0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
        0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2,
        0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74,
        0xe8, 0xcb ]

def tobin(x, n):
    return tuple(map(int, bin(x).lstrip("0b").rjust(n, "0")))

def c8(c):
    return Vector(tobin(c, 8))

BitRcon = list(map(c8, Rcon))

def ks_rotate(word):
    return word[1:] + word[:1]

def ks_core(word, iteration):
    word = word.rol(1)
    word = word.map(lambda b: Vector(bitSbox(b)))
    word = word.set(0, word[0] ^ BitRcon[iteration])
    return word

def KS_round(kstate, rno):
    t = ks_core(kstate.col(3), rno+1)
    kstate.apply_col(0, lambda c: c ^ t)
    t = kstate.col(0)
    kstate.apply_col(1, lambda c: c ^ t)
    t = kstate.col(1)
    kstate.apply_col(2, lambda c: c ^ t)
    t = kstate.col(2)
    kstate.apply_col(3, lambda c: c ^ t)
    return kstate

# Bit slicing AES
def BitAES(plaintext, key, rounds=10):
    bx = Vector(plaintext).split(16)
    bk = Vector(key).split(16)

    state = Rect(bx, w=4, h=4).transpose()
    kstate = Rect(bk, w=4, h=4).transpose()

    for rno in range(rounds):
        state = AK(state, kstate)
        state = SB(state)
        state = SR(state)
        if rno < rounds-1:
            state = MC(state)
        kstate = KS(kstate, rno)
    state = AK(state, kstate)

    state = state.transpose()
    kstate = kstate.transpose()
    bits = sum( map(list, state.flatten()), [])
    kbits = sum( map(list, kstate.flatten()), [])
    return bits, kbits

def AK(state, kstate):
    return state.zipwith(lambda a, b: a ^ b, kstate)

def SB(state, inverse=False):
    return state.apply(lambda v: Vector(bitSbox(v, inverse=inverse)))

def SR(state, inverse=False):
    for y in range(4):
        state.apply_row(y, lambda row: ShiftRow(row, y, inverse=inverse))
    return state

def MC(state, inverse=False):
    for x in range(4):
        state.apply_col(x, lambda v: list(map(Vector, MixColumn(v))))
    return state

def KS(kstate, rno):
    return KS_round(kstate, rno)

# Circuit
from circkit.boolean import BooleanCircuit

C = BooleanCircuit()
pt = C.add_inputs(n=128, format="m%d")
k = C.add_inputs(n=128, format="k%d")
ct, k10 = BitAES(pt, k, rounds=10)
C.add_output(ct)

# Test
def str2bin(s):
    return list(map(int, "".join(bin(ord(c))[2:].zfill(8) for c in s)))

def hex2bin(s):
    return list(map(int, "".join(bin(c)[2:].zfill(8) for c in bytes.fromhex(s))))

def bin2hex(s):
    assert len(s) % 8 == 0
    v = int("".join(map(str, s)), 2)
    v = ("%x" %v).zfill(len(s) // 4)
    return v

# Expected ciphertext: 69c4e0d86a7b0430d8cdb78070b4c55a
# See the AES documentation of NIST: https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf
def test_bitslicing_aes():
    MSG = "00112233445566778899aabbccddeeff"
    KEY = "000102030405060708090a0b0c0d0e0f"

    inp = hex2bin(MSG) + hex2bin(KEY)
    out = C.evaluate(inp)
    out = bin2hex(out)
    assert out == "69c4e0d86a7b0430d8cdb78070b4c55a"

