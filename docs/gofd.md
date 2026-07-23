# Graph Object Functional Dependencies

To express the dependencies in an LPG relevant for normalization, 
in addition to the expressions used in the [paper](http://arxiv.org/abs/2603.02995),
we defined an ASCII syntax, whose [grammar](#grammar) is shown below.

For the evaluation in the [paper](http://arxiv.org/abs/2603.02995), 
we implemented the GO-FDs in form of a Python package, which can be found [here](source_code_documentation.md#gnfd.GOFD).

## Grammar

For parsing GO-FDs an ANTLR grammar has been written, which is shown below. The Python implementation of GO-FDs ([`GOFD`][gofd.gnfd.GOFD]) is relying on this grammar.

```
--8<-- "gofd/gnfd.g4"
```


