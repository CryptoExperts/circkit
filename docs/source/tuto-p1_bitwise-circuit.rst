How to build a bitwise circuit
==============================

Bitwise is another built-in circuit type in the ``circkit`` framework.
We can follow the same steps as when we build an arithmetic circuit to
build a bitwise one.

Operations
----------

A bitwise circuit supports the following operations:

========= ===================== ========================================
Operation Notation              Note
========= ===================== ========================================
AND       :math:`\&`
OR        :math:`\|`
XOR       :math:`\wedge`
NOT       :math:`\sim`          unary operation
SHL       :math:`\ll`           shift left (constant postions)
SHR       :math:`\gg`           shift right (constant postions)
ROL       ``node.rol(n)``       circular shift left (constant postions)
ROR       ``node.ror(n)``       circular shift right (constant postions)
ADD       :math:`+`             addition
SUB       :math:`-`             subtraction
MUL       :math:`*`             multiplication
DIV       :math:`/`             division
MOD       :math:`\%`            modulo
NEG       :math:`-`             negation, unary operation
LUT       ``node.lookup_in(-)`` lookup table, value of node is index
RND       ``C.RND()()``         :math:`\text{C}` is the circuit
========= ===================== ========================================

Examples
--------

To build a bitwise circuit, we have to specify :math:`\text{word_size}`
which is the bit size of a word (value of a node). We denote
:math:`\text{mask} = 2^\text{word_size} - 1`. Every word in the circuit
is automatically ensured not to exceed :math:`\text{word_size}` bits by
AND-ing with the mask. Below is a simple example.

.. code:: ipython3

    from circkit.bitwise import BitwiseCircuit

    C = BitwiseCircuit(word_size=8)
    a = C.add_input("a")
    b = C.add_input("b")

    x0 = a + b
    x1 = a - b + 2
    x2 = a * b - 3
    x3 = a / b * 5
    x4 = a % 3 + b

    x5 = x0 << 2
    x6 = x1 >> 4
    x7 = x2.rol(5)
    x8 = x3.ror(6)
    x9 = ~x4

    x10 = x5 ^ x6
    x11 = x7 | x8
    x12 = x9 & x10
    x13 = -x11

    C.add_output(x12)
    C.add_output(x13)

    inp = [100, 200]
    out = C.evaluate(inp)
    print("Circuit output:")
    print(out)


.. code-block:: none

    Circuit output:
    [48, 93]


In the advanced examples of this documentation, we build the Simon
cipher and Speck cipher based on bitwise circuits to demonstrate the
usefulness of this circuit type in applications

.. code:: ipython3

    from circkit.bitwise import BitwiseCircuit

    C = BitwiseCircuit(word_size=8)
    a = C.add_input("a")

    x0 = a + 257
    x1 = a + 1

    x2 = a / 3

    C.add_output([x0, x1, x2])

    inp = [1]
    out = C.evaluate(inp)
    print("Circuit output:")
    print(out)


.. code-block:: none

    Circuit output:
    [2, 2, 0]


In the above example, :math:`257` is represented by :math:`1` in a 8-bit
word, thus :math:`x_0 = x_1`. The division only takes the round number,
thus :math:`x_2 = 1/3 = 0`.
