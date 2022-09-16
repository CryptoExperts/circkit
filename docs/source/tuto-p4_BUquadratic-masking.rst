Minimalist quadratic masking transformer
========================================

This is an example for the transformer of minimalist quadratic masking
scheme which was proposed in
`BU18 <https://eprint.iacr.org/2018/049.pdf>`__

Define the transformer
----------------------

.. code:: ipython3

    from circkit.transformers.core import CircuitTransformer
    from circkit.boolean import BooleanCircuit
    from circkit.array import Array

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



Test on a boolean circuit
-------------------------

.. code:: ipython3

    from circkit.boolean import BooleanCircuit

    C = BooleanCircuit()
    x = C.add_input("x")
    y = C.add_input("y")

    z = x * y + 1
    t = z + x + 1
    C.add_output(t)

    # ISW transformer
    transformer = BUQuadraticMasking()
    newC = transformer.transform(C)

    # see the graph and verify the ISW circuit
    # iswC.digraph().view()

    # # Evaluate on original circuit
    inp = [1, 0]
    out = C.evaluate(inp)
    print(f"Original circuit output: {out}")

    # Evaluate on BU quadratic masking circuit
    # 1 = 1 * 0 + 1 and 0 = 1 * 1 + 1
    inp_shares = [1, 0, 1, 1, 1, 1]
    n_tests = 10
    for i in range(n_tests):
        out_shares = newC.evaluate(inp_shares)
        a, b, c = out_shares
        ret = a*b + c
        print(f"Output shares: {out_shares} --> {ret}")


.. code-block:: none

    Original circuit output: [1]
    Output shares: [0, 0, 1] --> 1
    Output shares: [1, 1, 0] --> 1
    Output shares: [1, 0, 1] --> 1
    Output shares: [1, 1, 0] --> 1
    Output shares: [0, 1, 1] --> 1
    Output shares: [0, 0, 1] --> 1
    Output shares: [1, 0, 1] --> 1
    Output shares: [1, 1, 0] --> 1
    Output shares: [0, 0, 1] --> 1
    Output shares: [0, 0, 1] --> 1

