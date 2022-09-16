# Reference: https://github.com/inmcm/Simon_Speck_Ciphers/blob/master/Python/simonspeckciphers/speck/speck.py
# For the sake of simplicity, we modified some functions of the original implementation
import pytest
from circkit.bitwise import BitwiseCircuit


class SpeckCipher(object):
    """Speck Block Cipher Object"""
    # valid cipher configurations stored:
    # block_size:{key_size:number_rounds}
    __valid_setups = {32: {64: 22},
                      48: {72: 22, 96: 23},
                      64: {96: 26, 128: 27},
                      96: {96: 28, 144: 29},
                      128: {128: 32, 192: 33, 256: 34}}

    def __init__(self, key, key_size=128, block_size=128):

        # Setup block/word size
        self.possible_setups = self.__valid_setups[block_size]
        self.block_size = block_size
        self.word_size = self.block_size >> 1

        # Setup Number of Rounds and Key Size
        self.rounds = self.possible_setups[key_size]
        self.key_size = key_size

        # Create Properly Sized bit mask for truncating addition and left shift outputs
        self.mod_mask = (2 ** self.word_size) - 1

        # Mod mask for modular subtraction
        self.mod_mask_sub = (2 ** self.word_size)

        # Setup Circular Shift Parameters
        if self.block_size == 32:
            self.beta_shift = 2
            self.alpha_shift = 7
        else:
            self.beta_shift = 3
            self.alpha_shift = 8

        assert len(key) == (self.key_size // self.word_size)
        self.key = key

        # Pre-compile key schedule
        self.key_schedule()

    def key_schedule(self):
        self.round_keys = [self.key[-1]]
        l_schedule = [self.key[i] for i in reversed(range(self.key_size // self.word_size - 1))]

        for x in range(self.rounds - 1):
            new_l_k = self.encrypt_round(l_schedule[x], self.round_keys[x], x)
            l_schedule.append(new_l_k[0])
            self.round_keys.append(new_l_k[1])
        
        return self.round_keys

    def encrypt_round(self, x, y, k):
        """Complete One Round of Feistel Operation"""
        rs_x = ((x << (self.word_size - self.alpha_shift)) + (x >> self.alpha_shift)) & self.mod_mask

        add_sxy = (rs_x + y) & self.mod_mask

        new_x = k ^ add_sxy

        ls_y = ((y >> (self.word_size - self.beta_shift)) + (y << self.beta_shift)) & self.mod_mask

        new_y = new_x ^ ls_y

        return new_x, new_y

    def decrypt_round(self, x, y, k):
        """Complete One Round of Inverse Feistel Operation"""

        xor_xy = x ^ y

        new_y = ((xor_xy << (self.word_size - self.beta_shift)) + (xor_xy >> self.beta_shift)) & self.mod_mask

        xor_xk = x ^ k

        msub = ((xor_xk - new_y) + self.mod_mask_sub) % self.mod_mask_sub

        new_x = ((msub >> (self.word_size - self.alpha_shift)) + (msub << self.alpha_shift)) & self.mod_mask

        return new_x, new_y

    def encrypt(self, x, y):    
        # Run Encryption Steps For Appropriate Number of Rounds
        for k in self.round_keys:
            x, y = self.encrypt_round(x, y, k)
            
        return x, y   

    def decrypt(self, x, y):    
        # Run Encryption Steps For Appropriate Number of Rounds
        for k in reversed(self.round_keys): 
            x, y = self.decrypt_round(x, y, k)

        return x, y


@pytest.mark.parametrize(
    "_key_size, _block_size, k_inp, m_inp, c_out",
    [
        (64, 32, [0x1918, 0x1110, 0x0908, 0x0100], [0x6574, 0x694c], [0xa868, 0x42f2]),
        (72, 48, [0x121110, 0x0a0908, 0x020100], [0x20796c, 0x6c6172], [0xc049a5, 0x385adc]),
        (96, 48, [0x1a1918, 0x121110, 0x0a0908, 0x020100], [0x6d2073, 0x696874], [0x735e10, 0xb6445d]),
        (96, 64, [0x13121110, 0x0b0a0908, 0x03020100], [0x74614620, 0x736e6165], [0x9f7952ec, 0x4175946c]),
        (128, 64, [0x1b1a1918, 0x13121110, 0x0b0a0908, 0x03020100], [0x3b726574, 0x7475432d], [0x8c6fa548, 0x454e028b]),
        (96, 96, [0x0d0c0b0a0908, 0x050403020100], [0x65776f68202c, 0x656761737520], [0x9e4d09ab7178, 0x62bdde8f79aa]),
        (144, 96, [0x151413121110, 0x0d0c0b0a0908, 0x050403020100], [0x656d6974206e, 0x69202c726576], [0x2bf31072228a, 0x7ae440252ee6]),
        (128, 128, [0x0f0e0d0c0b0a0908, 0x0706050403020100], [0x6c61766975716520, 0x7469206564616d20], [0xa65d985179783265, 0x7860fedf5c570d18]),
        (192, 128, [0x1716151413121110, 0x0f0e0d0c0b0a0908, 0x0706050403020100], [0x7261482066656968, 0x43206f7420746e65], [0x1be4cf3a13135566, 0xf9bc185de03c1886]),
        (256, 128, [0x1f1e1d1c1b1a1918, 0x1716151413121110, 0x0f0e0d0c0b0a0908, 0x0706050403020100], [0x65736f6874206e49, 0x202e72656e6f6f70], [0x4109010405c0f53e, 0x4eeeb48d9c188f43])
    ]
)
def test_speckcipher(_key_size, _block_size, k_inp, m_inp, c_out):
    _word_size = _block_size >> 1
    key_word = _key_size // _word_size
    msg_word = _block_size // _word_size    
    
    C = BitwiseCircuit(word_size=_word_size)
    key = C.add_inputs(n=key_word, format="k%d")
    msg = C.add_inputs(n=msg_word, format="m%d")
    simon = SpeckCipher(key, key_size=_key_size, block_size=_block_size)
    cpt = simon.encrypt(msg[0], msg[1])
    C.add_output(cpt)

    inp = k_inp + m_inp
    out = C.evaluate(inp)
    assert out == c_out