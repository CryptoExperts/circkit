How to build an arithmetic circuit
==================================

In this tutorial, we show you how to build an arithmetic circuit based
on the ``circkit`` framework. In particular, we provide the instructions
on:

1. `How to build a circuit <#how-to-build-a-circuit>`__
2. `How to visualize a circuit <#how-to-visualize-a-circuit>`__
3. `How to transform a circuit to a
   matrix <#how-to-transform-a-circuit-to-a-matrix>`__
4. `How to trace the intermediate
   values <#how-to-trace-the-intermediate-values>`__

1. How to build a circuit
--------------------------

There are 5 steps to build a circuit.

Step 1: Initialize a new arithmetic circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Arithmetic circuit types
^^^^^^^^^^^^^^^^^^^^^^^^

There are 2 types of arithmetic circuit that you can use:

-  ``ArithmeticCircuit``: This supports regular arithmetic operations
   (e.g., :math:`+`, :math:`-`, :math:`*`, :math:`/`, … See step 3 for
   more details)
-  ``OptArithmeticCircuit``: This inherits the ``ArithmeticCircuit``
   type and additionally supports

   -  caching operations and nodes
   -  precomputing annihilator operations, e.g. a*0 = 0
   -  precomputing identity operations, e.g. a*1 = a, a+0 = 0
   -  precomputing constant operations

Here we just provide examples on the ``ArithmeticCircuit`` type. For the
``OptArithmeticCircuit``, it is almost similar.

Base ring
^^^^^^^^^

In case the computation of the circuit takes place in a field, we can
specify the ring when instantiating a new circuit. All constants in the
circuit will then be automatically converted to values in the field. Let
us take :math:`GF(2^8)` as an example.

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")
    print("Circuit information:")
    print(C)


.. code-block:: none

    Circuit information:
    <ArithmeticCircuit 'AToyCircuit' in:0 out:0 nodes:0>


By default, if we do not specify a base ring for the circuit, the
operations of the circuit will take place in decimal numbers.

Step 2: Define the input nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can define the input nodes of the circuit by one of the two following
methods:

-  ``add_input``: this creates an input node. We use this method to
   create the input nodes one by one. Note that the name of a node
   (e.g., ``inp_0``, ``inp_1`` in the example below) is a mandatory
   argument.

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (one by one)
    a = C.add_input("inp_0")
    b = C.add_input("inp_1")
    print("Circuit input nodes:")
    print(C.inputs)


.. code-block:: none

    Circuit input nodes:
    [<ArithmeticCircuit:INPUT[name=inp_0]#0 ()>, <ArithmeticCircuit:INPUT[name=inp_1]#1 ()>]


-  ``add_inputs``: this creates a list of input nodes. Note that the
   names of the nodes are specified by a format, e.g. \ ``inp_%d`` where
   ``%d`` is automatically replaced by a counter in :math:`[0,n)`. You
   can see that the following example creates the same input nodes as
   the previous one.

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    print("Circuit input nodes:")
    print(C.inputs)


.. code-block:: none

    Circuit input nodes:
    [<ArithmeticCircuit:INPUT[name=inp_0]#0 ()>, <ArithmeticCircuit:INPUT[name=inp_1]#1 ()>]


Step 3: Perform the computation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic operations
^^^^^^^^^^^^^^^^

Below are the built-in operations in ``ArithmeticCircuit`` and
``OptArithmeticCircuit``. The operators of a operation can be nodes or
constants.

============== ============ ================================
Operation      Notation     Note
============== ============ ================================
Addition       :math:`+`
Subtraction    :math:`-`
Multiplication :math:`*`
Division       :math:`/`
Exponentiation :math:`**`   only support constant exponent
Inversion      :math:`\sim` only for base ring elements
Negation       :math:`-`    unary operation for decimal only
============== ============ ================================

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    a, b = inp_nodes

    # Step 3: Perform the computations
    x0 = a + b
    x1 = x0 - 5
    x2 = x1 * x0
    x3 = x2 / 3
    x4 = x3 ** 4
    x5 = ~x4
    print("Circuit information:")
    print(C)


.. code-block:: none

    Circuit information:
    <ArithmeticCircuit 'AToyCircuit' in:2 out:0 nodes:10>


Other operations
^^^^^^^^^^^^^^^^

-  Random (``RND``): In a circuit, we can create a random node which
   contains a random value. See the following example:

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    a = C.add_input("a")
    b = C.add_input("b")

    # Step 3: Perform the computations
    # x is a node holding a random value
    x = C.RND()()
    z = a + b + x

-  Lookup table (``LUT``): Given a node :math:`x` and a table :math:`T`
   of constants, this operation return a new node of value :math:`T[x]`.

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    a = C.add_input("a")
    b = C.add_input("b")

    # Step 3: Perform the computations
    T = (11, 22, 33, 44, 55)
    T = tuple([K.fetch_int(v) for v in T])
    x = C.LUT(T)(a)
    y = C.LUT(T)(b)
    # Or we can write
    # x = a.lookup_in(T)
    # y = b.lookup_in(T)

Step 4: Define the output nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``add_output`` is the only method used to define output nodes. However,
it can be used in two different ways:

-  define the output nodes one by one as the following example

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    a, b = inp_nodes

    # Step 3: Perform the computations
    x0 = a + b
    x1 = x0 - 5
    x2 = x1 * x0
    x3 = x2 / 3
    x4 = x3 ** 4
    x5 = ~x4

    # Step 4: Define the output nodes (one by one)
    C.add_output(x4)
    C.add_output(x5)
    print("Circuit output nodes:")
    print(C.outputs)


.. code-block:: none

    Circuit output nodes:
    [<ArithmeticCircuit:EXP[power=4]#8 (7)>, <ArithmeticCircuit:INV#9 (8)>]


-  define a list of output nodes as the following example.

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    a, b = inp_nodes

    # Step 3: Perform the computations
    x0 = a + b
    x1 = x0 - 5
    x2 = x1 * x0
    x3 = x2 / 3
    x4 = x3 ** 4
    x5 = ~x4

    # Step 4: Define the output nodes (one by one)
    C.add_output([x4, x5])
    print("Circuit output:")
    print(C.outputs)


.. code-block:: none

    Circuit output:
    [<ArithmeticCircuit:EXP[power=4]#8 (7)>, <ArithmeticCircuit:INV#9 (8)>]


Step 5: Evaluate the circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``evaluate(input: list, convert_input: bool, convert_output: bool)`` is
the method used to evaluate a circuit. It returns a list of output
values corresponding to the output nodes. This method has 3 arguments:

-  ``input``: this is a list of input whose length equals to the number
   of input nodes.
-  ``convert_input``: this indicates that the input elements should be
   converted from decimal numbers to base ring elements or not
-  ``convert_output``: this indicates that the output elements should be
   converted from base ring elements to decimal numbers or not.

By default, ``convert_input = True`` and ``convert_output = True``

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    a, b = inp_nodes

    # Step 3: Perform the computations
    x0 = a + b
    x1 = x0 - 5
    x2 = x1 * x0
    x3 = x2 / 3
    x4 = x3 ** 4
    x5 = ~x4

    # Step 4: Define the output nodes (one by one)
    C.add_output([x4, x5])

    # Step 5: Evaluate the circuit
    inp = [7, 9]
    out = C.evaluate(inp, convert_input=True, convert_output=False)
    print("Circuit output:")
    print(out)


.. code-block:: none

    Circuit output:
    [z8^7 + z8^6 + z8^2 + z8 + 1, z8^7 + z8^4 + z8^3 + z8^2 + z8]


2. How to visualize a circuit
------------------------------

We use `graphviz <https://graphviz.readthedocs.io/en/stable/>`__ to
visualize a circuit. Once we have a circuit, we can visualize it by
calling the method ``C.digraph().view()``

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    a, b = inp_nodes

    # Step 3: Perform the computations
    x0 = a + b
    x1 = x0 - 5 + a
    x2 = x1 * x0
    x3 = x2 / 3
    x4 = x3 ** 4
    x5 = ~x4

    # Step 4: Define the output nodes (one by one)
    C.add_output([x4, x5])

    # Visualize the circuit (Run the code to see)
    C.digraph().view()

.. image:: ../circuit-visualization.png
    :width: 400
    :align: center


3. How to transform a circuit to a matrix
------------------------------------------

An arithmetic circuit can be transformed to an affine
:math:`y = Ax + b`, where :math:`x` is the input and :math:`y` is the
output of the circuit. It is a linear mapping when :math:`b = 0`.

To be able to transform to an affine mapping, the operations of the
circuit must be in the following set:

============== ========= ======= =====================
Operation      Notation  2 nodes a node and a constant
============== ========= ======= =====================
Addition       :math:`+` Yes     Yes
Subtraction    :math:`-` Yes     Yes
Multiplication :math:`*` No      Yes
============== ========= ======= =====================

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF, matrix, vector
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    a, b = inp_nodes

    # Step 3: Perform the computation
    x0 = a + b
    x1 = x0 * 19
    x2 = x1 + x0
    x3 = x2 * 3
    x4 = x3 - x2
    x5 = x1 + 2

    # Step 4: Define the output nodes (one by one)
    C.add_output([x4, x5])

    # Transform to a matrix
    A, b = C.to_matrix()
    print(f"A = {A}")
    print(f"b = {b}")


.. code-block:: none

    A = [[z8^5 + z8^2, z8^5 + z8^2], [z8^4 + z8 + 1, z8^4 + z8 + 1]]
    b = [0, z8]


Let us verify that the result of the computation :math:`y = Ax+b` is the
same as the output of the circuit’s evaluation.

.. code:: ipython3

    # Verify
    A = matrix(A)
    b = vector(b)

    inp = [15, 20]
    out = C.evaluate(inp, convert_input=True, convert_output=False)

    x = vector([K.fetch_int(v) for v in inp])
    y = A*x + b

    print("Circuit output:")
    print(out)
    print("Verification")
    print(y)
    print(f"circuit output = verification? {list(y) == out}")


.. code-block:: none

    Circuit output:
    [z8^5 + z8^3 + z8 + 1, z8^7 + z8]
    Verification
    (z8^5 + z8^3 + z8 + 1, z8^7 + z8)
    circuit output = verification? True


4. How to trace the intermediate values
----------------------------------------

Given an input, we can trace the values of each node in a circuit when
evaluating the circuit. To do so, we use the function
``trace(input: list, convert_input: bool, convert_values: bool, as_list: bool)``

-  ``input``: list of values fedding the input nodes
-  ``convert_input`` (``True`` by default): convert the input values
   from decimal to values on base ring
-  ``convert_values`` (``True`` by default): convert the intermediate
   values from base ring to decimal
-  ``as_list`` (``False`` by default): it returns a list of values when
   ``as_list=True``. Otherwise, it displays the details of nodes and
   their corresponding values

.. code:: ipython3

    from circkit.arithmetic import ArithmeticCircuit
    from sage.all import GF, matrix, vector
    K = GF(2**8)

    # Step 1: Initialize a new arithmetic circuit
    C = ArithmeticCircuit(base_ring=K, name="AToyCircuit")

    # Step 2: Define the input nodes (by a list)
    inp_nodes = C.add_inputs(n=2, format="inp_%d")
    a, b = inp_nodes

    # Step 3: Perform the computation
    x0 = a + b
    x1 = x0 * 19
    x2 = x1 + x0
    x3 = x2 * 3
    x4 = x3 - x2
    x5 = x1 + 2

    # Step 4: Define the output nodes (one by one)
    C.add_output([x4, x5])

    # Trace the intermediate values
    inp = [15, 20]
    T = C.trace(inp, convert_input=True, convert_values=True, as_list=False)
    print("Trace information:")
    print(T)

    # Display the graph (Run the code to see)
    C.digraph().view()


.. code-block:: none

    Trace information:
    {<ArithmeticCircuit:INPUT[name=inp_0]#0 ()>: 15, <ArithmeticCircuit:INPUT[name=inp_1]#1 ()>: 20, <ArithmeticCircuit:ADD#2 (0,1)>: 27, <ArithmeticCircuit:CONST[value=z8^4 + z8 + 1]#3 ()>: 19, <ArithmeticCircuit:MUL#4 (2,3)>: 128, <ArithmeticCircuit:ADD#5 (4,2)>: 155, <ArithmeticCircuit:CONST[value=z8 + 1]#6 ()>: 3, <ArithmeticCircuit:MUL#7 (5,6)>: 176, <ArithmeticCircuit:SUB#8 (7,5)>: 43, <ArithmeticCircuit:CONST[value=z8]#9 ()>: 2, <ArithmeticCircuit:ADD#10 (4,9)>: 130}



As we can see in the output, every node in the circuit is shown along
with its value. We can see in the graph for a better illustration. Now,
let’s set ``as_list=True`` to see the output:

.. code:: ipython3

    T = C.trace(inp, convert_input=True, convert_values=True, as_list=True)
    print("Trace values:")
    print(T)


.. code-block:: none

    Trace values:
    [15, 20, 27, 19, 128, 155, 3, 176, 43, 2, 130]

