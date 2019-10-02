# ALBERT

## A Lite BERT reimplmentation

This is A lite Bert reimlpementation which modify from google-research/bert

Three addition:
* Add Lamb optimazation  -- optimization_albert.py
* Add factorization     --modeling_albert (embedding_lookup_factorized)
* Shared Parameter    -- Please refer to modeling_albert.py 

To do:
> Senetence Order Prediction didn't use ! now still the pretrained method is Next Sentence Preduction

[2019/10/01] Now can train!!! you need to first generate bpe vocab.txt (Please refer to subword-nmt) and modify the syntax to collect your subword unit.

## Train from Scratch Tuturial
First your need to download your data {Wikipedia or BookCorpus}, then 
* use subword-nmt [github](https://github.com/rsennrich/subword-nmt) to generate code.bpe, 
* use code.bpe generate vocab.txt then you can train~.

[Finish]:
    On testing can validate that the total parameter will not increasing although increase layer number.
[Finish]:
    can train using below code
[To do]:
    you need to collect data

`python rim_albert_pretraining --input_file {training data}  --bert_config_file config.json --output_dir {your path}`
