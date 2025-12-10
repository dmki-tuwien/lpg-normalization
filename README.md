# Global Property Graph Normalization


Repository structure:
* `/assets`: Contains files required by the normalization tool or during its development. This does not include source code.
* `/graphs`: Contains graphs to be normalized
* `/out`: Contains the output of the evaluation
* `spgds.g4`: Contains the ANTLRv4 Grammar of the dependencies

## Development
For the generation of the parser of the dependencies, ANTLR was used.
ANTLR can be installed on macOS using Brew: `brew install antlr`.

