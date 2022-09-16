How to define a new circuit type
================================

In this tutorial, we show you how to define a new circuit type,
i.e. define operations of your preference in a circuit, based on the
``circkit`` framework. In particular, we provide the guidance on:

1. `Defining a new circuit type <#defining-a-new-circuit-type>`__
2. `Syntactic sugar <#syntactic-sugar>`__
3. `Some examples <#some-examples>`__

.. note::

    Note that this tutorial shows you how to define a new circuit type. In practice it is better to use the built-in `ArithmeticCircuit` or `OptArithmeticCircuit` as in the tutorial of building an arithmetic circuit. If necessary, you could inherit those circuits and then define your own operations.

1. Defining a new circuit type
-------------------------------

Defining syntax
~~~~~~~~~~~~~~~~

To define a new circuit type, we follow the steps:

1. Inherit the ``Circuit`` class
2. Inherit the ``Circuit.Operations`` class inside the new circuit type
3. Define the operations of the new circuit type as classes nested
   inside the ``Operations`` class. Depending on the numbers of input
   nodes and output nodes, each operation should inherit one of the
   following types of ``Operation``:

+-----------------------------------+-----------------------------------+
| Class                             | Usage                             |
+===================================+===================================+
| ``Operation.Unary``               | Operation with 1 input node       |
+-----------------------------------+-----------------------------------+
| ``Operation.Binary``              | Operation with 2 input nodes      |
+-----------------------------------+-----------------------------------+
| ``Operation.Ternary``             | Operation with 3 input nodes      |
+-----------------------------------+-----------------------------------+
| ``Operation.Variadic``            | Operation with variable number of |
|                                   | input nodes                       |
+-----------------------------------+-----------------------------------+
| ``Operation.MultiNullary``        | Operation with no inputs and      |
|                                   | variable number of output nodes   |
+-----------------------------------+-----------------------------------+
| ``Operation.MultiUnary``          | Operation with 1 input and        |
|                                   | variable number of output nodes   |
+-----------------------------------+-----------------------------------+
| ``Operation.MultiBinary``         | Operation with 2 inputs and       |
|                                   | variable number of output nodes   |
+-----------------------------------+-----------------------------------+
| ``Operation.MultiTernary``        | Operation with 3 inputs and       |
|                                   | variable number of output nodes   |
+-----------------------------------+-----------------------------------+
| ``Operation.MultiVariadic``       | Operation with variable number of |
|                                   | input nodes and variable number   |
|                                   | of output nodes                   |
+-----------------------------------+-----------------------------------+

Let’s define addition operation as an example:

.. code:: ipython3

    from circkit import Circuit, Operation

    class NewCircuitType(Circuit):
        class Operations(Circuit.Operations):
            class ADD(Operation.Binary):
                pass

Now, we can construct a circuit with the addition defined above. Recall
that we still can use the following useful functions (as shown in the
tutorial of building an arithmetic circuit) to build a circuit:

-  ``add_input(name)``: add an input node
-  ``add_inputs(n, format)``: add ``n`` input nodes
-  ``add_output(node)``: mark ``node`` as an output node
-  ``add_output(nodelist)``: mark ``nodelist`` as a list of output nodes
-  ``digraph().view()``: draw and view the graph of the circuit

.. code:: ipython3

    circuit = NewCircuitType(name="A test circuit")

    x = circuit.add_input("x")
    y = circuit.add_input("y")
    z = circuit.ADD()(x, y)
    circuit.add_output(z)

    # circuit.digraph().view()
    print("Circuit's input nodes:")
    print(circuit.inputs)
    print("Circuit's output nodes:")
    print(circuit.outputs)


.. code-block:: none

    Circuit's input nodes:
    [<NewCircuitType:INPUT[name=x]#0 ()>, <NewCircuitType:INPUT[name=y]#1 ()>]
    Circuit's output nodes:
    [<NewCircuitType:ADD#2 (0,1)>]


Defining evaluation
--------------------

So far, the circuit is just about the syntax since we define the
computational graph but no computational rules. This is fine, since
typical applications are not all about computing the circuit. However,
evaluating the circuit can be useful for testing purposes. To achieve
this, we simply need to define the evaluation function for our
operation.

.. code:: ipython3

    from circkit import Circuit, Operation

    class NewCircuitType(Circuit):
        class Operations(Circuit.Operations):
            class ADD(Operation.Binary):
                def eval(self, a, b):
                    return a + b

Now we can evaluate the circuit.

.. code:: ipython3

    circuit = NewCircuitType(name="A test circuit")

    x = circuit.add_input("x")
    y = circuit.add_input("y")
    z = circuit.ADD()(x, y)
    circuit.add_output(z)

    inp = [10, 20]
    out = circuit.evaluate(inp)
    print("Circuit's output:")
    print(out)


.. code-block:: none

    Circuit's output:
    [30]


Defining operations with parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defining an operation parameter is done through annotations, with
possible assignment to mark a default value. It is then stored as an
attribute of the operation instance, accessible e.g. for evaluation.
Let’s define ``EXP`` operation with the ``power`` parameter as an
example.

.. code:: ipython3

    from circkit import Circuit, Operation, Param

    class NewCircuitType(Circuit):
        class Operations(Circuit.Operations):
            class ADD(Operation.Binary):
                def eval(self, a, b):
                    return a + b

            class EXP(Operation.Unary):
                power : Param.Int(min_value=0) = 2
                def eval(self, a):
                    return a**self.power

In the example above, ``power`` takes 2 as the default value. Let’s
build a circuit to test it:

.. code:: ipython3

    circuit = NewCircuitType(name="test circuit")

    x = circuit.add_input("x")
    xsquare = circuit.EXP()(x)
    xcube = circuit.EXP(3)(x)
    circuit.add_output([xsquare, xcube])

    inp = [5]
    out = circuit.evaluate([5])
    print("Circuit's output:")
    print(out)


.. code-block:: none

    Circuit's output:
    [25, 125]


Here, we used `Param.Int <source/param.rst#circkit.param.IntParam>`__ to
constraint the parameter type and value. The following table contains
the parameter constraints supported by ``circkit``:

=================== ==========================================
Class               Usage
=================== ==========================================
``Param.Const``     constants
``Param.Int``       integers
``Param.Bool``      booleans
``Param.Str``       strings
``Param.Tuple``     tuples
``Param.InputName`` name of an input, can be string or integer
=================== ==========================================

If we provide an incompatible value, it will cause an error. For
example:

.. code:: ipython3

    xquartic = circuit.EXP("four")(x)


::


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-7-72e779c46385> in <module>
    ----> 1 xquartic = circuit.EXP("four")(x)


    ~/Work/wbc/circkit/.venv/lib/python3.9/site-packages/circkit/operation.py in __call__(cls, *values, **kvalues)
        158         # create the Operation instance anyway
        159         # (not avoiding it to unify parsing of parameters)
    --> 160         op_new = super().__call__(*values, **kvalues)
        161         if cls._circuit is not None and cls._circuit.CACHE_OPERATIONS:
        162             # if a similar operation is in cache,


    ~/Work/wbc/circkit/.venv/lib/python3.9/site-packages/circkit/operation.py in __init__(self, *values, **kvalues)
        276             # - param checks only single value, is independent
        277             # - to check groups, add methods to the op class
    --> 278             setattr(self, name, param.create(self, value=kvalues[name]))
        279
        280     def __call__(self, *incoming, **kwargs):


    ~/Work/wbc/circkit/.venv/lib/python3.9/site-packages/circkit/param.py in create(self, operation, value)
         58
         59     def create(self, operation, value: int):
    ---> 60         value = int(value)
         61         if self.min_value is not None and self.min_value > value:
         62             raise Param.InvalidValue(


    ValueError: invalid literal for int() with base 10: 'four'


2. Syntactic sugar
-------------------

It is a bit clumsy to write ``ADD``, ``EXP`` when building circuits,
when these are basic arithmetic operations. We can define syntax sugar
naturally by subclassing the
`Node <source/node.rst#circkit.node.Node>`__ class.

.. code:: ipython3

    class NewCircuitType(Circuit):
        class Operations(Circuit.Operations):
            class ADD(Operation.Binary):
                def eval(self, a, b):
                    return a + b

            class EXP(Operation.Unary):
                power : Param.Int(min_value=0) = 2
                def eval(self, a):
                    return a**self.power

        class Node(Circuit.Node):
            def __add__(self, other):
                return self.circuit.ADD()(self, other)

            def __pow__(self, power):
                return self.circuit.EXP(power)(self)

Life gets much easier now:

.. code:: ipython3

    circuit = NewCircuitType()
    x = circuit.add_input("x")
    y = circuit.add_input("y")
    z = (x + y)**2 + x**5
    circuit.add_output(z)

    inp = [10, 1]
    out = circuit.evaluate(inp)
    print("Circuit's output:")
    print(out)


.. code-block:: none

    Circuit's output:
    [100121]


3. Some examples
-----------------

In this section, we demonstrate examples of defining circuit types with
some interesting operations (rather than basic addition, substraction,
multiplication, …). This aims to show that we can define a new circuit
type with *our own operations*.

Example 1
~~~~~~~~~

We define a new circuit type with 2 operations:

-  MADD: given a list :math:`(x_1, x_2, \ldots, x_n)`, it returns the
   sum :math:`x_1 + x_2 + \ldots + x_n`
-  MMUL: given a list :math:`(x_1, x_2, \ldots, x_n)`, it returns the
   product :math:`x_1 \times x_2 \times \ldots \times x_n`

.. code:: ipython3

    # Define a new circuit type
    class NewCircuitType(Circuit):
        class Operations(Circuit.Operations):
            class MADD(Operation.Variadic):
                def eval(self, *operands):
                    return sum(operands)

            class MMUL(Operation.Variadic):
                def eval(self, *operands):
                    r = 1
                    for x in operands:
                        r *= x
                    return r

    # Create a new circuit instance
    circuit = NewCircuitType(name="test circuit")
    x = circuit.add_inputs(5, "x%d")
    y = circuit.MADD()(*x)
    z = circuit.MMUL()(*x)
    circuit.add_output(y)
    circuit.add_output(z)

    # Evaluate the circuit
    inp = [x+1 for x in range(5)]
    out = circuit.evaluate(inp)
    print("Circuit's output:")
    print(out)


.. code-block:: none

    Circuit's output:
    [15, 120]


Example 2
~~~~~~~~~

We define a new circuit type with 2 operations:

-  MADDC: given a constant :math:`c` and a list
   :math:`(x_1, x_2, \ldots, x_n)`, it returns a list
   :math:`(c+x_1, c+x_2, \ldots, c+x_n)`
-  MMULC: given a constant :math:`c` and a list
   :math:`(x_1, x_2, \ldots, x_n)`, it returns a list
   :math:`(cx_1, cx_2, \ldots, cx_n)`

.. code:: ipython3

    # Define a new circuit type
    class NewCircuitType(Circuit):
        class Operations(Circuit.Operations):
            class MADDC(Operation.Variadic):
                def eval(self, c, *operands):
                    return [c + x for x in operands]

            class MMULC(Operation.Variadic):
                def eval(self, c, *operands):
                    return [c * x for x in operands]

    # Create a new circuit instance
    circuit = NewCircuitType(name="test circuit")
    c = 10
    x = circuit.add_inputs(5, "x%d")
    y = circuit.MADDC()(c, *x)
    z = circuit.MMULC()(c, *x)
    circuit.add_output(y)
    circuit.add_output(z)

    # Evaluate the circuit
    inp = [x+1 for x in range(5)]
    out = circuit.evaluate(inp)
    print("Circuit's output:")
    print(out)


.. code-block:: none

    Circuit's output:
    [[11, 12, 13, 14, 15], [10, 20, 30, 40, 50]]

