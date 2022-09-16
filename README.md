# circkit 

``circkit`` is a small framework for defining, constructing and manipulating computational circuits. It aims to be very generic. ``circkit`` supports both low-level circuits such as bit-based operations, word-based operations, arithmetic circuits over a ring and high-level circuits made up by gates which are customized non-primitive functions.

## Installation

For arithmetic circuits working on finite fields, it needs to install Sagemath. For circuits working on decimal numbers, integers, boolean and bitwise, it is not necessary to install Sagemath.

### Circuits with Sagemath
1. Install [Sagemath](https://www.sagemath.org).

2. Install ``circkit`` in Sagemath:

- via ``PyPI``:
```
sage -pip install circkit
```

- or via ``setup.py``
```
sage -pip install .
```

3. Run your script with Sagemath:

```
sage -python script.py
```

Or you can open a notebook with Sagemath and build your circuit with the ``circkit`` framework:
```
sage -n
```

### Circuits without Sagemath

1. Install ``circuit``:

- via ``PyPI``:
```
pip3 install circkit
```

- or via ``setup.py``
```
pip3 install .
```

2. Run your python script, for example:

```
python3 script.py
```

### Using a virtual environment
We can use a virtual enviroment to run *both circuits with and without Sagemath*.

1. Create a virtual environment of Sagemath:
```
sage -python -m venv --system-site-packages .venv
```

Then, go to the virtual enviroment:
```
source .venv/bin/activate
```

2. Install ``circkit`` in the virtual environment.

- via ``PyPI``:
```
pip install circkit
```

- or via ``setup.py``
```
pip install .
```

3. Run your script on the virtual enviroment, for example:
```
python script.py
```

Or you can open a python notebook in this virtual enviroment and build your circuit. Again, both circuits working with and without Sagemath can be run on this virtual environment.

## Tests
You can run the tests in the ``tests`` folder:
```
pytest tests
```

NOTE: you should run the tests in the virtual environment (see [installation](#using-a-virtual-environment)) because the tests consists of both circuits with Sagemath and circuits without Sagemath. Otherwise, it will fail on the tests requiring Sagemath.

You can run a specific test, for example:
```
pytest tests/test_simon_cipher.py
```

## Documentation

See [circkit.readthedocs.io](circkit.readthedocs.io) for the documentations. You can also open the file [docs/_build/html/index.html](docs/_build/html/index.html) file on your browser.

### Tutorials

Some jupyter notebooks are provided to help you play with the ``circkit`` framework:

- [How to build an arithmetic circuit](docs/tuto-p1_builtin-circuit.ipynb)
- [How to build a bitwise circuit](docs/tuto-p1_bitwise-circuit.ipynb)
- [How to build a boolean circuit](docs/tuto-p1_boolean-circuit.ipynb)
- [How to define a new circuit type](docs/tuto-p2_new-circuit-type.ipynb)
- [How to define a transformer and example on ISW transformer](docs/tuto-p3_ISWtransformer.ipynb)

### Advanced examples

Some advance examples are also provided. These examples highlight the applications of the ``circkit`` framework in cryptography.

- [Bit-slicing AES](docs/tuto-p4_bitsliceAES.ipynb)
- [Simon cipher](docs/tuto-p4_simon.ipynb)
- [Speck cipher](docs/tuto-p4_speck.ipynb)
- [Minimalist quadratic masking scheme](docs/tuto-p4_BUquadratic-masking.ipynb)

## Authors

CryptoExperts Team
