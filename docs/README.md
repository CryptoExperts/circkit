# `circkit` documentation

This documentation is created on [Read the Docs](https://docs.readthedocs.io/en/stable/tutorial/) by importing [Sphinx](https://www.sphinx-doc.org/en/master/tutorial/index.html).

## Requirements

In addition to some python packages listed in the ``../requirements.txt`` file, it requires to install [pandoc](https://pandoc.org) and [jupyter](https://jupyter.org/install). Please follow the instruction in their homepage to install them.

- ``pandoc`` is used for file conversion during the compilation of ``Sphinx``. 

- ``jupyter`` is used to convert python notebooks to reStructuredText files ([nbsphinx](https://nbsphinx.readthedocs.io/en/0.8.9/) can be an alternative. It can be used to import notebooks directly into the html file without conversion. But it does not work here and no idea why). 

## Usage

See ``makefile`` for more details. Briefly, the following commands are useful:

- Convert python notebooks to reStructuredText files:
    ```
    make notebook
    ```

- Compile and generate HTML docs:
    ```
    make html
    ```

- Open the file ``_build/html/index.html`` on your browser.