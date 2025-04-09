from datasets import load_dataset, load_from_disk
from collections import Counter
import re
import os

DATA_PATH = "data/bookcorpus_subset"

def getBookCorpus():
    if os.path.exists(DATA_PATH):
        print("Loading dataset from local cache...")
        return load_from_disk(DATA_PATH)
    else:
        print("Downloading BookCorpus dataset (subset)...")
        dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train[:5%]") 
        print("Saving dataset locally for future use...")
        os.makedirs("data", exist_ok=True)
        dataset.save_to_disk(DATA_PATH)
        return dataset

def buildVocabulary(dataset, vocab_size=10000):
    word_counter = Counter()
    for sample in dataset:
        # Lowercase and tokenize using regex (keep words & punctuation)
        words = re.findall(r"\b\w+\b|[^\w\s]", sample['text'].lower())
        word_counter.update(words)

    # Most common words
    most_common = word_counter.most_common(vocab_size - 2)  # Reserve 2 for <unk> and <pad>
    vocab = {"<unk>": 0, "<pad>": 1}
    vocab.update({word: idx + 2 for idx, (word, _) in enumerate(most_common)})
    return vocab

def tokenize(text, vocab):
    words = re.findall(r"\b\w+\b|[^\w\s]", text.lower())
    token_ids = [vocab.get(word, vocab["<unk>"]) for word in words]
    return words, token_ids

# --------------------------
# Main execution
# --------------------------
if __name__ == "__main__":
    
    dataset = getBookCorpus()

    vocab = buildVocabulary(dataset, vocab_size=5000)

    sample_text = "The cat sat on the mat"
    tokens, token_ids = tokenize(sample_text, vocab)

    print("\n Sample Input:", sample_text)
    print("🔹 Tokens:", tokens)
    print("🔹 Token IDs:", token_ids)
