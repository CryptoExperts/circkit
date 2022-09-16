Simon Cipher
============

Implementation of Simon cipher
------------------------------

.. code:: ipython3

    # Reference: https://github.com/inmcm/Simon_Speck_Ciphers/blob/master/Python/simonspeckciphers/simon/simon.py
    # For the sake of simplicity, we modified some functions of the original implementation
    from collections import deque

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
                rs_3 = ((k_reg[0] << s3) + (k_reg[0] >> 3)) & self.mod_mask

                if m == 4:
                    rs_3 = rs_3 ^ k_reg[2]

                s1 = self.word_size - 1
                rs_1 = ((rs_3 << s1) + (rs_3 >> 1)) & self.mod_mask

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
                ls_1_x = ((x >> s1) + (x << 1)) & self.mod_mask
                ls_8_x = ((x >> s8) + (x << 8)) & self.mod_mask
                ls_2_x = ((x >> s2) + (x << 2)) & self.mod_mask

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
                ls_1_x = ((x >> (self.word_size - 1)) + (x << 1)) & self.mod_mask
                ls_8_x = ((x >> (self.word_size - 8)) + (x << 8)) & self.mod_mask
                ls_2_x = ((x >> (self.word_size - 2)) + (x << 2)) & self.mod_mask

                # XOR Chain
                xor_1 = (ls_1_x & ls_8_x) ^ y
                xor_2 = xor_1 ^ ls_2_x
                y = x
                x = k ^ xor_2

            return x, y


Then, we can test the above implementation with `some test vectors given
by the authors of Simon <https://eprint.iacr.org/2013/404.pdf>`__

.. code:: ipython3

    k3264 = [0x1918, 0x1110, 0x0908, 0x0100]
    l3264, r3264 = 0x6565, 0x6877
    c3264 = SimonCipher(k3264, key_size=64, block_size=32)
    t3264 = c3264.encrypt(l3264, r3264)
    assert t3264 == (0xc69b, 0xe9bb)

    k128256 = [0x1f1e1d1c1b1a1918, 0x1716151413121110, 0x0f0e0d0c0b0a0908, 0x0706050403020100]
    l128256, r128256 = 0x74206e69206d6f6f, 0x6d69732061207369
    c128256 = SimonCipher(k128256, key_size=256, block_size=128)
    t128256 = c128256.encrypt(l128256, r128256)
    assert t128256 == (0x8d2b5579afc8a3a0, 0x3bf72a87efe7b868)

Build a circuit for Simon cipher
--------------------------------

We use a bitwise circuit to construct the Simon cipher.

.. code:: ipython3

    from circkit.bitwise import BitwiseCircuit

    C = BitwiseCircuit()
    key = C.add_inputs(n=4, format="k%d")
    msg = C.add_inputs(n=2, format="m%d")
    simon = SimonCipher(key, key_size=64, block_size=32)
    cpt = simon.encrypt(msg[0], msg[1])
    C.add_output(cpt)


Then, we can evaluate the circuit to test its correctness.

.. code:: ipython3

    k3264 = [0x1918, 0x1110, 0x0908, 0x0100]
    m3264 = [0x6565, 0x6877]
    inp = k3264 + m3264
    out = C.evaluate(inp)
    print(out)


.. code-block:: none

    [50843, 59835]


Note that we are using bitwise circuit and the truncation
``x & self.mod_mask`` is done automatically in the circuit. Therefore it
is not necessary to have this truncation in the circuit. In the above
Simon cipher, we still put it there because it is needed for the
verification of the Simon implementation before building its circuit.
