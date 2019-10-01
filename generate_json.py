import json 

config = {}
config["batch_size"] = 24 
config["seq_length"] = 512
config["is_training"] = True
config["use_input_mask"] = True
config["use_token_type_ids"] = True
config["vocab_size"] = 103
config["hidden_size"] = 768
config["num_hidden_layers"] = 12
config["num_attention_heads"] = 12
config["intermediate_size"] =3072
config["hidden_act"] = "gelu"
config["hidden_dropout_prob"] = 0.1
config["attention_probs_dropout_prob"] =0.1
config["max_position_embeddings"] = 512
config["type_vocab_size"] = 2
config["intializer_range"] = 0.02
config["scope"] = None

json.dump(config,open("./config.json","w"))