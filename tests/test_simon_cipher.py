# Reference: https://github.com/inmcm/Simon_Speck_Ciphers/blob/master/Python/simonspeckciphers/simon/simon.py
# For the sake of simplicity, we modified some functions of the original implementation
import sys
sys.path.append("../")
import pytest
from collections import deque
from circkit.bitwise import BitwiseCircuit


class SimonCipher(object):
    """Simon Block Cipher Object"""

    # Z Arrays (stored bit reversed for easier usage)
    z0 = 0b01100111000011010100100010111110110011100001101010010001011111
    z1 = 0b01011010000110010011111011100010101101000011001001111101110001
    z2 = 0b11001101101001111110001000010100011001001011000000111011110101
    z3 = 0b11110000101100111001010001001000000111101001100011010111011011
    z4 = 0b11110111001001010011000011101000000100011011010110011110001011

    # valid cipher configurations stored:
    # block_size:{key_size:(number_rounds,z sequence)}
    __valid_setups = {32: {64: (32, z0)},
                      48: {72: (36, z0), 96: (36, z1)},
                      64: {96: (42, z2), 128: (44, z3)},
                      96: {96: (52, z2), 144: (54, z3)},
                      128: {128: (68, z2), 192: (69, z3), 256: (72, z4)}}

    def __init__(self, key, key_size=128, block_size=128):
        """
        Initialize an instance of the Simon block cipher.
        :param key: Int representation of the encryption key
        :param key_size: Int representing the encryption key in bits
        :param block_size: Int representing the block size in bits
        :return: None
        """

        # Setup block/word size
        self.possible_setups = self.__valid_setups[block_size]
        self.block_size = block_size
        self.word_size = self.block_size >> 1

        self.rounds, self.zseq = self.possible_setups[key_size]
        self.key_size = key_size

        # Create Properly Sized bit mask for truncating addition and left shift outputs
        self.mod_mask = (2 ** self.word_size) - 1

        # Check key length
        assert len(key) == (self.key_size // self.word_size)
        self.key = key

        # Pre-compute the key schedule
        self.key_schedule()


    def key_schedule(self):
        m = self.key_size // self.word_size
        m1 = m - 1
        self.round_keys = []
        # Create list of subwords from encryption key
        k_init = self.key

        k_reg = deque(k_init)  # Use queue to manage key subwords

        round_constant = self.mod_mask ^ 3  # Round Constant is 0xFFFF..FC

        # Generate all round keys
        for x in range(self.rounds):
            s3 = self.word_size - 3
            rs_3 = ((k_reg[0] << s3) + (k_reg[0] >> 3))

            if m == 4:
                rs_3 = rs_3 ^ k_reg[2]

            s1 = self.word_size - 1
            rs_1 = ((rs_3 << s1) + (rs_3 >> 1))

            c_z = ((self.zseq >> (x % 62)) & 1) ^ round_constant

            new_k = c_z ^ rs_1 ^ rs_3 ^ k_reg[m1]

            self.round_keys.append(k_reg.pop())
            k_reg.appendleft(new_k)
        
        return self.round_keys

    def encrypt(self, l, r):
        x = l
        y = r

        # Run Encryption Steps For Appropriate Number of Rounds
        for k in self.round_keys:
             # Generate all circular shifts
            s1 = self.word_size - 1
            s8 = self.word_size - 8
            s2 = self.word_size - 2
            ls_1_x = ((x >> s1) + (x << 1))
            ls_8_x = ((x >> s8) + (x << 8))
            ls_2_x = ((x >> s2) + (x << 2))

            # XOR Chain
            xor_1 = (ls_1_x & ls_8_x) ^ y
            xor_2 = xor_1 ^ ls_2_x
            y = x
            x = k ^ xor_2

        return x, y   

    def decrypt(self, l, r):    
        x = l
        y = r

        # Run Encryption Steps For Appropriate Number of Rounds
        for k in reversed(self.round_keys): 
             # Generate all circular shifts
            ls_1_x = ((x >> (self.word_size - 1)) + (x << 1))
            ls_8_x = ((x >> (self.word_size - 8)) + (x << 8))
            ls_2_x = ((x >> (self.word_size - 2)) + (x << 2))

            # XOR Chain
            xor_1 = (ls_1_x & ls_8_x) ^ y
            xor_2 = xor_1 ^ ls_2_x
            y = x
            x = k ^ xor_2

        return x, y

@pytest.mark.parametrize(
    "_key_size, _block_size, k_inp, m_inp, c_out",
    [
        (64, 32, [0x1918, 0x1110, 0x0908, 0x0100], [0x6565, 0x6877], [0xc69b, 0xe9bb]),
        (72, 48, [0x121110, 0x0a0908, 0x020100], [0x612067, 0x6e696c], [0xdae5ac, 0x292cac]),
        (96, 48, [0x1a1918, 0x121110, 0x0a0908, 0x020100], [0x726963, 0x20646e], [0x6e06a5, 0xacf156]),
        (96, 64, [0x13121110, 0x0b0a0908, 0x03020100], [0x6f722067, 0x6e696c63], [0x5ca2e27f, 0x111a8fc8]),
        (128, 64, [0x1b1a1918, 0x13121110, 0x0b0a0908, 0x03020100], [0x656b696c, 0x20646e75], [0x44c8fc20, 0xb9dfa07a]),
        (96, 96, [0x0d0c0b0a0908, 0x050403020100], [0x2072616c6c69, 0x702065687420], [0x602807a462b4, 0x69063d8ff082]),
        (144, 96, [0x151413121110, 0x0d0c0b0a0908, 0x050403020100], [0x746168742074, 0x73756420666f], [0xecad1c6c451e, 0x3f59c5db1ae9]),
        (128, 128, [0x0f0e0d0c0b0a0908, 0x0706050403020100], [0x6373656420737265, 0x6c6c657661727420], [0x49681b1e1e54fe3f, 0x65aa832af84e0bbc]),
        (192, 128, [0x1716151413121110, 0x0f0e0d0c0b0a0908, 0x0706050403020100], [0x206572656874206e, 0x6568772065626972], [0xc4ac61effcdc0d4f, 0x6c9c8d6e2597b85b]),
        (256, 128, [0x1f1e1d1c1b1a1918, 0x1716151413121110, 0x0f0e0d0c0b0a0908, 0x0706050403020100], [0x74206e69206d6f6f, 0x6d69732061207369], [0x8d2b5579afc8a3a0, 0x3bf72a87efe7b868])
    ]
)

def test_simoncipher(_key_size, _block_size, k_inp, m_inp, c_out):
    _word_size = _block_size >> 1
    key_word = _key_size // _word_size
    msg_word = _block_size // _word_size
    
    C = BitwiseCircuit(word_size=_word_size)
    key = C.add_inputs(n=key_word, format="k%d")
    msg = C.add_inputs(n=msg_word, format="m%d")
    simon = SimonCipher(key, key_size=_key_size, block_size=_block_size)
    cpt = simon.encrypt(msg[0], msg[1])
    C.add_output(cpt)

    inp = k_inp + m_inp
    out = C.evaluate(inp)

    assert out == c_out
