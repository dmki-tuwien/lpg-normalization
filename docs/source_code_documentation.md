This page documents the source code of the graph-native LPG normalization.


The [GitHub repository](https://github.com/dmki-tuwien/lpg-normalization) is structured as follows:

 * `docs/`: The documentation of the source code of this repository. Basis for the [documentation](https://dmki-tuwien.github.io/lpg-normalization/).
 * `gofd/`: A Python package that implements the Graph Object Functional Dependencies 
 * `graphs/`: Contains graphs that are normalized as part of the evaluation
 * `out/`: Contains the output of the evaluation as CSV files
 * `tests/`: Contains Python pytests for the dependencies and the normalization

Additionally, three Jupyter Notebooks are provided:

 * `structural_metrics_tables_and_figures.ipynb` is provided for the further analysis of the evaluation results of the structural metrics.
 * `query_experiment.ipynb` is provided for the analysis of the query experiment.
 * `normalization-skavantzos-link.ipynb` 
   computes same metrics as our evaluation scenarios normalized using the method described in [^1]

In the following, the [Python source code is documented](#python-documentation).


## Python Documentation

### `normalize.py`

::: normalize

### GOFD Package

::: gofd



[^1]: Philipp Skavantzos and Sebastian Link. 2025. Third and Boyce-Codd normal
form for property graphs. VLDB J. 34, 2 (2025), 23.

