# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

notebook:
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p1_builtin-circuit.ipynb
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p1_bitwise-circuit.ipynb
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p1_boolean-circuit.ipynb
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p2_new-circuit-type.ipynb
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p3_ISWtransformer.ipynb
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p4_bitsliceAES.ipynb
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p4_simon.ipynb
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p4_speck.ipynb
	jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags skip --to rst tuto-p4_BUquadratic-masking.ipynb
	mv tuto-p1_builtin-circuit.rst source/
	mv tuto-p1_bitwise-circuit.rst source/
	mv tuto-p1_boolean-circuit.rst source/
	mv tuto-p2_new-circuit-type.rst source/
	mv tuto-p3_ISWtransformer.rst source/
	mv tuto-p4_bitsliceAES.rst source/
	mv tuto-p4_simon.rst source/
	mv tuto-p4_speck.rst source/
	mv tuto-p4_BUquadratic-masking.rst source/

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
