# A Graph-Native Approach to Normalization

Welcome to the online documentation of the paper ["A Graph-Native Approach to Normalization"](https://github.com/dmki-tuwien/lpg-normalization/blob/master/paper/extended_version.pdf).

This documentation provides details on the performed evaluation and provides a documentation for our
[Python](https://www.python.org) implementation of LPG normalization.

## Getting Started

1. To get started with the evaluation and the implementation of LPG normalization, first clone the repository.
Since this repository contains a submodule for the 
[Northwind](https://github.com/neo4j-graph-examples/northwind) graph dataset, 
the command<br> `git clone https://github.com/dmki-tuwien/lpg-normalization.git --recurse-submodules`<br> needs to be used to *clone* the repository. 

2. *Download all datasets* as described in the `graphs/` folder before running the evaluation.

3. *Prepare the containers* for the evaluation by running the command `docker compose build`.

4. *Prepare evaluation scenarios* and you local environment.
<br>
The [evaluation scenarios](evaluation_scenarios.md) are defined the file `setup.yaml`. For available configuration options, please refer to the comments in `setup.yaml`.
<br>
Also adjust the `GRAPHS_PATH` environment variable in the file `.env` to be the *absolute* path to your `graphs` folder.
Relative paths cannot be used due to a limitation of Docker.
<br>In case Docker Desktop is used, please uncomment the 
`TC_HOST` environment variable.


5. The command `docker compose --profile eval up --abort-on-container-exit` automatically sets up the databases,
*runs the evaluation*, and 
shuts down the database containers after the evaluation finished.


After running the Docker containers,
the output of the evaluation, 
which is the basis for the figures and tables used in the paper, 
can be found in the directory `out/`.

## REST API
A REST API service for graph-native normalization can be started using
`docker compose --profile rest up --build`

## Development
For the generation of the parser of the dependencies, [ANTLR](https://www.antlr.org/) 
is used.
On macOS, ANTLR can be installed using [Homebrew](https://brew.sh/): 
`brew install antlr`.

