# PG-Norm: Native Property Graph Normal Forms

Welcome to the documentation and [repository](https://github.com/dmki-tuwien/lpg-normalization)
accompanying the paper "PG-Norm: Native Property Graph Normal Forms".

Repository structure:
* `assets/`: Contains files required by the normalization tool or during its development. This does not include source code.
* `docs/`: The documentation of the source code of this repository
* `graphs/`: Contains graphs to be normalized
* `out/`: Contains the output of the evaluation
* 
* `spgds.g4`: Contains the ANTLRv4 Grammar of the dependencies

## Getting Started

Since this repository contains submodules for the 
GQL grammar and the 
[Northwind](https://github.com/neo4j-graph-examples/northwind) graph dataset, 
the command `git clone https://github.com/dmki-tuwien/lpg-normalization.git --recurse-submodules` needs to be used. 

Following the cloning of the repository run the command `docker compose build` to prepare the containers for the evaluation.

The command `docker compose up --abort-on-container-exit` runs the evaluation and automatically shuts down the database containers after the evaluation finished.

If you want to run the evaluation and view the HTML documentation, run
`docker compose --profile docs up`

After running the Docker containers, the output of the evaluation, which is identical to the figures and tables used in the paper, 
can be found in teh directory `out/`

## Development
For the generation of the parser of the dependencies, [ANTLR](https://www.antlr.org/) 
is used.
On macOS ANTLR can be installed using [Homebrew](https://brew.sh/): 
`brew install antlr`.

## Troubleshooting

If the resulting plot misses metrics and only shows 0s, there most probably may ha