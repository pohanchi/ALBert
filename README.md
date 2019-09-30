# ALBERT

## A Lite BERT reimplmentation

This is a lite bert reimlpementation.

Three addition:
* Add Lamb optimazation
* Add factorization
* Shared Parameter    -- Please refer to modeling_albert.py / optimization_albert

Finish:
    On testing can validate that the total parameter will not increasing although increase layer number.

To do:
    Can't train (no data) ( no TPU)