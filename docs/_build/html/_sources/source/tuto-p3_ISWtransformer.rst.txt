How to define a transformer
===========================

By defining a transformer, we can transform a circuit into another
circuit (possibly of a new circuit type). In this tutorial, we show you:

-  ISW transformer: given a circuit, we transform it into a new circuit
   working on shares (ISW circuit, see
   `ISW03 <https://people.eecs.berkeley.edu/~daw/papers/privcirc-crypto03.pdf>`__).
   This is the built-in transformer which you can import and use
   directly from the :mod:`circkit` framework.
-  How to define your own transformer: we show you the steps of defining
   the ISW transformer. You will see how to define a new transformer
   from those steps.

ISW Transformer
---------------

Let us take a boolean circuit as an example. We transform this circuit
into a new boolean circuit working on shares.

.. code:: ipython3

    from circkit.transformers.isw import IswOnArithmetic
    from circkit.boolean import BooleanCircuit

    C = BooleanCircuit()
    x = C.add_input("x")
    y = C.add_input("y")

    z = x * y + 1
    t = z + x + 1
    C.add_output(t)

    # ISW transformer
    transformer = IswOnArithmetic(order=2)
    iswC = transformer.transform(C)

    # see the graph and verify the ISW circuit
    iswC.digraph().view()

    # Evaluate on original circuit
    inp = [1, 0]
    out = C.evaluate(inp)
    print(f"Original circuit output: {out}")

    # Evaluate on ISW circuit
    # 1 = 1 + 0 + 0 and 0 = 1 + 1 + 0
    inp_shares = [1, 0, 0, 1, 1, 0]
    n_tests = 5
    for i in range(n_tests):
        out_shares = iswC.evaluate(inp_shares)
        ret = 0
        for s in out_shares:
            ret ^= s
        print(f"Output shares: {out_shares} --> {ret}")


.. code-block:: none

    Original circuit output: [1]
    Output shares: [1, 1, 1] --> 1
    Output shares: [1, 1, 1] --> 1
    Output shares: [0, 1, 0] --> 1
    Output shares: [0, 0, 1] --> 1
    Output shares: [1, 0, 0] --> 1


How to define your transformer
------------------------------

In this section, we show how to define the ISW transformer from which we
can see the steps of defining a new transformer.

Given a *source circuit*, our goal is to transform it into a *target
circuit*. The high-level idea is to visit all nodes in the source
circuit and process each node in the way we want to define the
transformer. The framework already provides the skeleton of the
transformation in the ``CircuitTransformation`` class. We just need to
inherit this class and then define the ``visit_<OP>`` functions where
``<OP>`` are the operations (or node types) defined in the circuit type.

In a boolean circuit, there are 4 node types. Therefore, we define 4
functions:

-  ``visit_INPUT``: for each input node in the source circuit, we create
   its nodes of shares in the target circuit.
-  ``visit_ADD`` (XOR): a XOR node in the source circuit represents by
   some XOR nodes on the shares of the operands in the target circuit.
-  ``visit_MUL`` (AND): to transform an AND node in the source circuit,
   we have to generate some randomnesses and create some XOR and AND
   nodes on those randomnesses and the shares.
-  ``visit_CONST``: a constant is represented by some shares in the
   target circuit.

The following code is the implementation of the ISW transformer:

.. code:: ipython3

    from circkit.transformers.core import CircuitTransformer
    from circkit.array import Array


    class IswOnArithmetic(CircuitTransformer):
        def __init__(self, order: int):
            """
            Arguments
            ---------
            :order: ISW masking order (number of shares = order + 1)
            """
            super().__init__()
            self.order = order
            self.n_shares = order + 1

        def visit_INPUT(self, node):
            shares = []
            for i in range(self.n_shares):
                new_name = f"{node.operation.name}_share{i}"
                x = self.target_circuit.add_input(new_name)
                shares.append(x)
            shares = Array(shares)

            return shares

        def visit_ADD(self, node, x, y):
            return x + y
        visit_XOR = visit_ADD

        def visit_MUL(self, node, x, y):
            r = [[0] * self.n_shares for _ in range(self.n_shares)]
            for i in range(self.n_shares):
                for j in range(i+1, self.n_shares):
                    r[i][j] = self.target_circuit.RND()()
                    r[j][i] = r[i][j] + x[i]*y[j] + x[j]*y[i]

            z = x * y
            for i in range(self.n_shares):
                for j in range(self.n_shares):
                    if i != j:
                        z[i] = z[i] - r[i][j]
            return z
        visit_AND = visit_MUL

        def visit_CONST(self, node):
            shares = Array(self.target_circuit.RND()() for i in range(self.order))

            c = self.target_circuit.add_const(node.operation.value)
            for i in range(self.order):
                c = c + shares[i]

            shares.append(c)
            return shares
