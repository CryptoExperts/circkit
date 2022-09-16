from circkit.arithmetic import ArithmeticCircuit
import random
import pytest


def test_add():
    C = ArithmeticCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    
    x0 = a + b
    x1 = x0 + 100
    x2 = x1 + 11.2
    x3 = x2 + (-12.6)
    x4 = 222 + x3
    
    C.add_output(x4)
    inp = [random.randint(-10000, 10000) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a + b
        x1 = x0 + 100
        x2 = x1 + 11.2
        x3 = x2 + (-12.6)
        x4 = 222 + x3
        return [x4]

    assert out == check(*inp)

def test_sub():
    C = ArithmeticCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    
    x0 = a - b
    x1 = x0 - 100
    x2 = x1 - 11.2
    x3 = x2 - (-12.6)
    x4 = 222 - x3

    C.add_output(x4)
    inp = [random.randint(-10000, 10000) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a - b
        x1 = x0 - 100
        x2 = x1 - 11.2
        x3 = x2 - (-12.6)
        x4 = 222 - x3
        return [x4]

    assert out == check(*inp)

def test_mul():
    C = ArithmeticCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    
    x0 = a * b
    x1 = x0 * 100
    x2 = x1 * 11.2
    x3 = x2 * (-12.6)
    x4 = 222 * x3

    C.add_output(x4)
    inp = [random.randint(-10000, 10000) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a * b
        x1 = x0 * 100
        x2 = x1 * 11.2
        x3 = x2 * (-12.6)
        x4 = 222 * x3
        return [x4]

    assert out == check(*inp)

def test_div():
    C = ArithmeticCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    
    x0 = a / b
    x1 = 100 / a
    x2 = x0 / 100
    x3 = x1 / 11.2
    x4 = x2 / (-12.6) * x3

    C.add_output(x4)
    inp = [random.randint(1, 10000) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a / b
        x1 = 100 / a
        x2 = x0 / 100
        x3 = x1 / 11.2
        x4 = x2 / (-12.6) * x3
        return [x4]

    assert out == check(*inp)

def test_neg():
    C = ArithmeticCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    
    x0 = -a
    x1 = -b
    x2 = x0 * x1

    C.add_output(x2)
    inp = [random.randint(1, 10000) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = -a
        x1 = -b
        x2 = x0 * x1
        return [x2]

    assert out == check(*inp)

def test_exp():
    C = ArithmeticCircuit()
    a = C.add_input("a")
    b = C.add_input("b")
    
    x0 = a ** (-5)
    x1 = b ** 8
    x2 = x0 * x1

    C.add_output(x2)
    inp = [random.randint(1, 10000) for _ in range(2)]
    out = C.evaluate(inp)

    def check(a, b):
        x0 = a ** (-5)
        x1 = b ** 8
        x2 = x0 * x1
        return [x2]

    assert out == check(*inp)

def test_exp_invalid_power():
    with pytest.raises(TypeError):
        C = ArithmeticCircuit()
        a = C.add_input("a")
        b = C.add_input("b")
        x0 = a ** b

def test_quick_example():
    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit()

    # Step 2: Define the input nodes
    a = C.add_input("a")
    b = C.add_input("b")

    # Step 3: Perform the computation
    x = a + b + 5
    y = 2 * a - 3

    # Step 4: Define the output nodes
    C.add_output(x)
    C.add_output(y)

    # Step 5: Evaluate the circuit
    inp = [random.randint(-2**16, 2**16-1) for _ in range(2)]
    out = C.evaluate(inp)
    
    def check(a, b):
        x = a + b + 5
        y = 2 * a - 3
        return [x, y]

    assert out == check(*inp)
