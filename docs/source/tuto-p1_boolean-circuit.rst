How to build a boolean circuit
==============================

Boolean is another built-in circuit type in the ``circkit`` framework.
We can follow the same steps as when we build an arithmetic circuit to
build a boolean one.

Operations
----------

A boolean circuit supports the following operations:

========= =========================== ===============================
Operation Notation                    Note
========= =========================== ===============================
AND       :math:`\&` or :math:`*`
OR        :math:`\mid`
XOR       :math:`\wedge` or :math:`+`
NOT       :math:`\sim`                unary operation
RND       :math:`\text{C.RND()()}`    :math:`\text{C}` is the circuit
========= =========================== ===============================

Examples
--------

Below is a simple example of building a boolean circuit.

.. code:: ipython3

    from circkit.boolean import BooleanCircuit

    C = BooleanCircuit()
    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a + b
    x1 = a * b
    x2 = a ^ b
    x3 = a & b
    x4 = x0 | x1
    x5 = ~x2 ^ 1
    x6 = C.RND()()
    x7 = x6 ^ x4
    x8 = x5 * 1

    C.add_output(x7)
    C.add_output(x8)

    inp = [1, 0]
    out = C.evaluate(inp)
    print("Circuit output: ")
    print(out)



.. code-block:: none

    Circuit output:
    [1, 1]


In the advanced examples of this documentation, we build the bitslicing
AES based on boolean circuit to demonstrate the usefulness of this
circuit type in real applications.
