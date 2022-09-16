from circkit.boolean import BooleanCircuit
import random
import pytest


#
# For each operation, we try to test all possible cases. 
# For example, XOR:
#   - node ^ node
#   - node ^ constant
#   - constant ^ node
# We also test error cases:
#   - invalid constant
#

def test_xor():
    C = BooleanCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    x0 = a ^ b
    x1 = x0 ^ 1
    x2 = 0 ^ x1
    C.add_output(x2)

    inp = [random.randint(0, 1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a ^ b
        x1 = x0 ^ 1
        x2 = 0 ^ x1
        return [x2]
    assert out == check(*inp)

def test_and():
    C = BooleanCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    x0 = a & b
    x1 = x0 & 1
    x2 = 0 & x1
    C.add_output(x2)

    inp = [random.randint(0, 1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a & b
        x1 = x0 & 1
        x2 = 0 & x1
        return [x2]
    assert out == check(*inp)

def test_or():
    C = BooleanCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    x0 = a | b
    x1 = x0 | 1
    x2 = 0 | x1
    C.add_output(x2)

    inp = [random.randint(0, 1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a | b
        x1 = x0 | 1
        x2 = 0 | x1
        return [x2]
    assert out == check(*inp)

def test_not():
    C = BooleanCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    x0 = ~a
    x1 = ~b
    x2 = x0 ^ x1
    C.add_output(x2)

    inp = [random.randint(0, 1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = ~a
        x1 = ~b
        x2 = x0 ^ x1
        return [x2]
    assert out == check(*inp)

def test_add():
    C = BooleanCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    x0 = a + b
    x1 = x0 + 1
    x2 = 0 + x1
    C.add_output(x2)

    inp = [random.randint(0, 1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a ^ b
        x1 = x0 ^ 1
        x2 = 0 ^ x1
        return [x2]
    assert out == check(*inp)

def test_mul():
    C = BooleanCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    x0 = a * b
    x1 = x0 * 1
    x2 = 1 * x1
    C.add_output(x2)

    inp = [random.randint(0, 1) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a & b
        x1 = x0 & 1
        x2 = 1 & x1
        return [x2]
    assert out == check(*inp)

def test_invalid_const():
    with pytest.raises(ValueError):
        C = BooleanCircuit()
        a = C.add_input("a")
        a ^ 2    
