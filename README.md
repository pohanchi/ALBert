# ALBERT

## A Lite BERT reimplmentation

This is a lite bert reimlpementation.

Three addition:
* Add Lamb optimazation
* Add factorization
* Shared Parameter    -- Please refer to modeling_albert.py / optimization_albert.py

[2019/10/01] now can train!!! you need to first generate bpe vocab.txt (Please refer to subword-nmt) and modify the syntax to collect your subword unit

Finish:
    On testing can validate that the total parameter will not increasing although increase layer number.

To do:
    can train but the data you need to collect!!
