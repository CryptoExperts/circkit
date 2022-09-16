from circkit.arithmetic import ArithmeticCircuit
from sage.all import GF
import random
K = GF(2**8)


def test_toycircuit():
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    a, b = inp_nodes

    x0 = a + b
    x1 = x0 - 5
    x2 = x1 * x0
    x3 = x2 / 3
    x4 = x3 ** 4
    x5 = ~x4

    C.add_output([x4, x5])

    inp = [random.randint(0, 255), random.randint(0, 255)]
    out = C.evaluate(inp)

    def stdresults(a, b):
        a = K.fetch_int(a)
        b = K.fetch_int(b)

        c5 = K.fetch_int(5)
        c3 = K.fetch_int(3)

        x0 = a + b
        x1 = x0 - c5
        x2 = x1 * x0
        x3 = x2 / c3
        x4 = x3 ** 4
        x5 = ~x4
        return [x4.integer_representation(), x5.integer_representation()]
    assert out == stdresults(*inp)
