import json

from llm_sdk import Small_LLM_Model

model = Small_LLM_Model()
path = model.get_path_to_vocab_file()
print("vocab file:", path)
with open(path, encoding="utf-8") as file:
    vocab = json.load(file)
print("entries:", len(vocab), "max id:", max(vocab.values()))

inverse = {token_id: token for token, token_id in vocab.items()}
ids = model.encode("What is the sum of 2 and 3?")[0].tolist()
print("ids:", ids)
print("tokens:", [inverse.get(i) for i in ids])

logits = model.get_logits_from_input_ids(ids)
print("logits length:", len(logits))

for text in ["{", '{"', '"name"', " 42", "42", "3.14", "\n", "é", "中"]:
    pieces = model.encode(text)[0].tolist()
    print(repr(text), pieces, [inverse.get(i) for i in pieces])