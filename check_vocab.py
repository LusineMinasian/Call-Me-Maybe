from llm_sdk import Small_LLM_Model
from src.vocabulary import load_vocabulary

model = Small_LLM_Model()
vocab = load_vocabulary(model.get_path_to_vocab_file())
print("tokens in vocabulary:", len(vocab.texts))

no_text = [i for i, text in enumerate(vocab.texts) if text is None]
print("ids without own text:", len(no_text), no_text[:10])
for token_id in no_text[:3]:
    print("  decode gives:", repr(model.decode([token_id])))

different = []
for token_id, ours in enumerate(vocab.texts):
    if ours is not None and model.decode([token_id]) != ours:
        different.append(token_id)
print("texts that differ from decode:", len(different))
for token_id in different[:10]:
    print(token_id, repr(vocab.texts[token_id]), repr(model.decode([token_id])))