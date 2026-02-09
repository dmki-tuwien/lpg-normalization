# A Graph-Native Approach to Normalization

Welcome to the [documentation](https://dmki-tuwien.github.io/lpg-normalization/) and [repository](https://github.com/dmki-tuwien/lpg-normalization)
accompanying the paper "A Graph-Native Approach to Normalization".

Repository structure:
* `docs/`: The documentation of the source code of this repository. Basis for the [documentation](https://dmki-tuwien.github.io/lpg-normalization/).
* `gnfd/`: A Python package that implements the Graph Object Functional Dependencies
* `graphs/`: Contains graphs that are normalized as part of the evaluation
* `out/`: Contains the output of the evaluation as CSV files
* `tests/`: Contains Python pytests for the dependencies and the normalization

## Getting Started

Since this repository contains a submodule for the 
[Northwind](https://github.com/neo4j-graph-examples/northwind) graph dataset, 
the command `git clone https://github.com/dmki-tuwien/lpg-normalization.git --recurse-submodules` needs to be used to clone the repository. 

Please also download all datasets as described in the `graphs/` folder before running the evaluation.

Following the cloning of the repository run the command `docker compose build` to prepare the containers for the evaluation.

The evaluation scenarios are defined the file `setup.yaml`. For available configuration options, please refer to the comments in `setup.yaml`.

The command `docker compose up --abort-on-container-exit` automatically sets up the databases,
runs the evaluation, and 
shuts down the database containers after the evaluation finished.

If you want to run the evaluation and view the HTML documentation, run
`docker compose --profile docs up`

After running the Docker containers,
the output of the evaluation, 
which is the basis for the figures and tables used in the paper, 
can be found in the directory `out/`.
Additionally, 
a Juypter Notebook `evaluation_tables_and_figures.ipynb` is provided for the further analysis of the evaluation results.

## Development
For the generation of the parser of the dependencies, [ANTLR](https://www.antlr.org/) 
is used.
On macOS, ANTLR can be installed using [Homebrew](https://brew.sh/): 
`brew install antlr`.

