import random
import pytest
from circkit.bitwise import BitwiseCircuit


#
# For each operation, we try to test all possible cases. 
# For example, XOR:
#   - node ^ node
#   - node ^ constant
#   - constant ^ node
# We also test error cases:
#   - invalid constant
#

def test_add():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a + b
    x1 = x0 + 3
    x2 = 5 + x1
    x3 = x2 + 9.3 # 9.3 is rounded to 9
    x4 = x3 + 300
    
    C.add_output(x4)

    inp = [random.randint(0, 2**16-1) for _ in range(2)]
    out = C.evaluate(inp)
    
    def check(a, b):
        mask = 2**8 - 1
        a = a & mask
        b = b & mask

        x0 = (a + b) & mask
        x1 = (x0 + 3) & mask
        x2 = (5 + x1) & mask
        x3 = (x2 + 9) & mask
        x4 = (x3 + (300 & mask)) & mask
        return [x4]

    assert out == check(*inp)

def test_sub():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a - b
    x1 = x0 - 3
    x2 = x1 - 300
    x3 = x2 - 9.3
    x4 = 5 - x3

    C.add_output(x4)

    inp = [random.randint(0, 2**16-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        mask = 2**8 - 1
        a = a & mask
        b = b & mask

        x0 = (a - b) & mask
        x1 = (x0 - 3) & mask
        x2 = (x1 - (300 & mask)) & mask
        x3 = (x2 - 9) & mask
        x4 = (5 - x3) & mask
        return [x4]

    assert out == check(*inp)

def test_mul():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a * b
    x1 = x0 * 3
    x2 = x1 * 300
    x3 = x2 * 9.3
    x4 = 5 * x3

    C.add_output(x4)

    inp = [random.randint(0, 2**16-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        mask = 2**8 - 1
        a = a & mask
        b = b & mask

        x0 = (a * b) & mask
        x1 = (x0 * 3) & mask
        x2 = (x1 * (300 & mask)) & mask
        x3 = (x2 * 9) & mask
        x4 = (5 * x3) & mask
        return [x4]

    assert out == check(*inp)

def test_div():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a / b
    x1 = x0 / 3
    x2 = x1 / 300
    x3 = x2 / 9.3
    x4 = 255 / b

    C.add_output([x3, x4])

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        mask = 2**8 - 1
        x0 = int(a / b)
        x1 = int(x0 / 3)
        x2 = int(x1 / (300 & mask))
        x3 = int(x2 / 9)
        x4 = int(255 / b)
        return [x3, x4]

    assert out == check(*inp)

def test_and():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a & b
    x1 = x0 & 3
    x2 = x1 & 300
    x3 = x2 & 9.3
    x4 = 5 & x3

    C.add_output(x4)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        mask = 2**8 - 1

        x0 = int(a & b)
        x1 = int(x0 & 3)
        x2 = int(x1 & (300 & mask))
        x3 = int(x2 & 9)
        x4 = int(5 & x3)
        return [x4]

    assert out == check(*inp)

def test_or():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a | b
    x1 = x0 | 3
    x2 = x1 | 300
    x3 = x2 | 9.3
    x4 = 5 | x3

    C.add_output(x4)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        mask = 2**8 - 1

        x0 = int(a | b)
        x1 = int(x0 | 3)
        x2 = int(x1 | (300 & mask))
        x3 = int(x2 | 9)
        x4 = int(5 | x3)
        return [x4]

    assert out == check(*inp)

def test_xor():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a ^ b
    x1 = x0 ^ 3
    x2 = x1 ^ 300
    x3 = x2 ^ 9.3
    x4 = 5 ^ x3

    C.add_output(x4)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        mask = 2**8 - 1

        x0 = int(a ^ b)
        x1 = int(x0 ^ 3)
        x2 = int(x1 ^ (300 & mask))
        x3 = int(x2 ^ 9)
        x4 = int(5 ^ x3)
        return [x4]

    assert out == check(*inp)

def test_not():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a ^ ~b
    x1 = ~x0

    C.add_output(x1)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a ^ ~b
        x1 = ~x0
        return [x1]

    assert out == check(*inp)

def test_shiftleft():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a << 1
    x1 = b << 5
    x2 = x0 << 256 # 256 will not be masked
    x3 = x2 ^ x1

    C.add_output(x3)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        mask = 2**8 - 1
        x0 = (a << 1) & mask
        x1 = (b << 5) & mask
        x2 = (x0 << (256)) & mask
        x3 = x2 ^ x1
        return [x3]

    assert out == check(*inp)

def test_shiftleft_non_constant():
    with pytest.raises(TypeError):
        C = BitwiseCircuit(word_size=8)

        a = C.add_input("a")
        b = C.add_input("b")

        x0 = a << b

def test_shiftright():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a >> 1
    x1 = b >> 5
    x2 = x0 >> 100
    x3 = x2 ^ x1

    C.add_output(x3)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = (a >> 1)
        x1 = (b >> 5)
        x2 = (x0 >> 100)
        x3 = x2 ^ x1
        return [x3]

    assert out == check(*inp)

def test_shiftright_non_constant():
    with pytest.raises(TypeError):
        C = BitwiseCircuit(word_size=8)

        a = C.add_input("a")
        b = C.add_input("b")

        x0 = a >> b

def test_shiftleft_non_constant():
    with pytest.raises(TypeError):
        C = BitwiseCircuit(word_size=8)

        a = C.add_input("a")
        b = C.add_input("b")

        x0 = a << b

def test_rol():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a.rol(1)
    x1 = b.rol(5)
    x2 = x0.rol(100)
    x3 = x2 ^ x1

    C.add_output(x3)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        def rol(x, v):
            word_size = 8
            v = v % word_size
            r = (x << v) | (x >> (word_size - v))
            return r

        mask = 2**8 - 1
        x0 = rol(a, 1) & mask
        x1 = rol(b, 5) & mask
        x2 = rol(x0, 100) & mask
        x3 = x2 ^ x1
        return [x3]

    assert out == check(*inp)

def test_rol_non_constant():
    with pytest.raises(TypeError):
        C = BitwiseCircuit(word_size=8)

        a = C.add_input("a")
        b = C.add_input("b")

        x0 = a.rol(b)

def test_ror():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a.ror(1)
    x1 = b.ror(5)
    x2 = x0.ror(100)
    x3 = x2 ^ x1

    C.add_output(x3)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        def ror(x, v):
            word_size = 8
            v = v % word_size
            r = (x >> v) | (x << (word_size - v))
            return r

        mask = 2**8 - 1
        x0 = ror(a, 1) & mask
        x1 = ror(b, 5) & mask
        x2 = ror(x0, 100) & mask
        x3 = x2 ^ x1
        return [x3]

    assert out == check(*inp)

def test_ror_non_constant():
    with pytest.raises(TypeError):
        C = BitwiseCircuit(word_size=8)

        a = C.add_input("a")
        b = C.add_input("b")

        x0 = a.ror(b)

def test_mod():
    C = BitwiseCircuit(word_size=8)

    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a % b
    x1 = x0 % 3
    x2 = x1 % 300
    x3 = x2 % 9.3

    C.add_output(x3)

    inp = [random.randint(1, 2**8-1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        mask = 2**8 - 1

        x0 = int(a % b)
        x1 = int(x0 % 3)
        x2 = int(x1 % (300 & mask))
        x3 = int(x2 % 9)
        return [x3]

    assert out == check(*inp)