from circkit.transformers.core import CircuitTransformer
from circkit.boolean import BooleanCircuit
from circkit.array import Array
import random


class BUQuadraticMasking(CircuitTransformer):
    # circuit type of the target circuit
    TARGET_CIRCUIT = BooleanCircuit

    def __init__(self):
        """
        Arguments
        ---------
        :order: ISW masking order
        """
        super().__init__()
        # fixed number of shares
        self.n_shares = 3

    def refresh(self, shares, randshares):
        a, b, c = shares
        ra, rb, rc = randshares

        ma = ra * (b + rc)
        mb = rb * (a + rc)
        rc = ma + mb + (ra + rc)*(rb + rc) + rc

        a1 = a + ra
        b1 = b + rb
        c1 = c + rc
        new_shares = Array([a1, b1, c1])
        return new_shares

    def visit_INPUT(self, node):
        shares = []
        for i in range(self.n_shares):
            new_name = f"{node.operation.name}_share{i}"
            x = self.target_circuit.add_input(new_name)
            shares.append(x)
        shares = Array(shares)

        return shares

    def visit_XOR(self, node, shares_1, shares_2):
        ra = self.target_circuit.RND()()
        rb = self.target_circuit.RND()()
        rc = self.target_circuit.RND()()
        randshares_1 = Array([ra, rb, rc])

        rd = self.target_circuit.RND()()
        re = self.target_circuit.RND()()
        rf = self.target_circuit.RND()()
        randshares_2 = Array([rd, re, rf])

        a, b, c = self.refresh(shares_1, randshares_1)
        d, e, f = self.refresh(shares_2, randshares_2)

        x = a + d
        y = b + e
        z = c + f + a*e + b*d

        return Array([x, y, z])

    def visit_AND(self, node, shares_1, shares_2):
        ra = self.target_circuit.RND()()
        rb = self.target_circuit.RND()()
        rc = self.target_circuit.RND()()
        randshares_1 = Array([ra, rb, rc])

        rd = self.target_circuit.RND()()
        re = self.target_circuit.RND()()
        rf = self.target_circuit.RND()()
        randshares_2 = Array([rd, re, rf])

        a, b, c = self.refresh(shares_1, randshares_1)
        d, e, f = self.refresh(shares_2, randshares_2)

        ma = b*f + rc * e
        md = c*e + rf * b

        x = a*e + rf
        y = b*d + rc
        z = a*ma + d*md + rc*rf + c*f

        return Array([x, y, z])

    def visit_CONST(self, node):
        ra = self.target_circuit.RND()()
        rb = self.target_circuit.RND()()

        x = self.target_circuit.add_const(node.operation.value)
        rx = ra*rb + x

        shares = Array([ra, rb, rx])
        return shares


def test_quadratic_masking():
    C = BooleanCircuit()
    x = C.add_input("x")
    y = C.add_input("y")

    z = x * y + 1
    t = z + x + 1
    C.add_output(t)

    # ISW transformer
    transformer = BUQuadraticMasking()
    newC = transformer.transform(C)

    # Evaluate on original circuit
    inp = [random.randint(0, 1) for _ in range(2)]
    out = C.evaluate(inp)

    # Evaluate on BU quadratic masking circuit
    x_shares = [random.randint(0, 1) for _ in range(2)]
    x_shares.append(x_shares[0] & x_shares[1] ^ inp[0])
    y_shares = [random.randint(0, 1) for _ in range(2)]
    y_shares.append(y_shares[0] & y_shares[1] ^ inp[1])
    inp_shares = x_shares + y_shares
    out_shares = newC.evaluate(inp_shares)
    a, b, c = out_shares
    ret = a&b ^ c
    assert ret == out[0]
