Repository structure:
* `docs/`: The documentation of the source code of this repository. Basis for the [documentation](https://dmki-tuwien.github.io/lpg-normalization/).
* `gnfd/`: A Python package that implements the Graph Object Functional Dependencies
* `graphs/`: Contains graphs that are normalized as part of the evaluation
* `out/`: Contains the output of the evaluation as CSV files
* `tests/`: Contains Python pytests for the dependencies and the normalization


This repository provides the source code and Docker containers with the implementation of graph-native normalization for
labeled property graphs.



Additionally, two Jupyter Notebooks are provided:
* `evaluation_tables_and_figures.ipynb` is provided for the further analysis of the evaluation results.
* `normalization-skavantzos-link.ipynb` computes same metrics as our evaluation scenarios normalized using the method described in <https://doi.org/10.1007/s00778-025-00902-2>.


