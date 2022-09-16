Speck Cipher
============

Implementation of Speck cipher
------------------------------

.. code:: ipython3

    # Reference: https://github.com/inmcm/Simon_Speck_Ciphers/blob/master/Python/simonspeckciphers/speck/speck.py
    # For the sake of simplicity, we modified some functions of the original implementation

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


Then, we can test the above implementation with `some test vectors given
by the authors of Speck <https://eprint.iacr.org/2013/404.pdf>`__

.. code:: ipython3


    k3264 = [0x1918, 0x1110, 0x0908, 0x0100]
    m3264 = [0x6574, 0x694c]
    c3264 = SpeckCipher(k3264, 64, 32)
    t3264 = c3264.encrypt(m3264[0], m3264[1])
    assert t3264 == (0xa868, 0x42f2)

    k128256 = [0x1f1e1d1c1b1a1918, 0x1716151413121110, 0x0f0e0d0c0b0a0908, 0x0706050403020100]
    m128256 = [0x65736f6874206e49, 0x202e72656e6f6f70]
    c128256 = SpeckCipher(k128256, 256, 128)
    t128256 = c128256.encrypt(m128256[0], m128256[1])
    assert t128256 == (0x4109010405c0f53e, 0x4eeeb48d9c188f43)

Build a circuit for Simon cipher
--------------------------------

.. code:: ipython3

    from circkit.bitwise import BitwiseCircuit

    C = BitwiseCircuit(word_size=16)
    key = C.add_inputs(n=4, format="k%d")
    msg = C.add_inputs(n=2, format="m%d")
    simon = SpeckCipher(key, key_size=64, block_size=32)
    cpt = simon.encrypt(msg[0], msg[1])
    C.add_output(cpt)

Then, we can evaluate the circuit to test its correctness.

.. code:: ipython3

    k3264 = [0x1918, 0x1110, 0x0908, 0x0100]
    m3264 = [0x6574, 0x694c]
    inp = k3264 + m3264
    out = C.evaluate(inp)
    print(out)


.. code-block:: none

    [43112, 17138]


Note that we are using bitwise circuit and the truncation
``x & self.mod_mask`` is done automatically in the circuit. Therefore it
is not necessary to have this truncation in the circuit. In the above
Simon cipher, we still put it there because it is needed for the
verification of the Simon implementation before building its circuit.
