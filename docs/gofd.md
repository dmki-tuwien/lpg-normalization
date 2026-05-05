# Graph Object Functional Dependencies

To express the dependencies in an LPG relevant for normalization, we defined 

## Grammar

For parsing GO-FDs an ANTLR grammar has been written, which is shown below. The Python implementation of GO-FDs (:class:`gnfd.GNFD`) is relying on this grammar.

```
--8<-- "gnfd/gnfd.g4"
```