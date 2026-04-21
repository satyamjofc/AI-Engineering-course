import numpy as np
import hashlib
from numpy.linalg import norm

# to create fake embeddings, while storing seed so that if same word came, it will give exact previous embedding
def fake_embeddings(word, dim=50):
    seed = int(hashlib.md5(word.encode()).hexdigest(), 16) % (10**8)
    rng = np.random.default_rng(seed)
    return rng.random(dim)

# fake list
word_list = ["king", "queen", "man", "woman", "apple", "banana", "car", "bike", "dog", "cat", "bat", "mat", "phone", "plane", "mountain", "hills"]
embeddings = {word: fake_embeddings(word) for word in word_list}

# print(embeddings)

k = 3
# taking user input
input = input("Give the word to search for: ")
input_embedding = fake_embeddings(input)

# cosine_similarity
def cosine_sim(embd, embd2):
    similarity = np.dot(embd, embd2) / (norm(embd) * norm(embd2))
    return similarity

rank = []
# searching for similar words
def search(input_embedding, embeddings = embeddings):
    for key, value in embeddings.items():
        how_similar = cosine_sim(input_embedding, value)
        rank.append((key, how_similar))
    rank.sort(key=lambda x:x[1], reverse=True)
    return rank[:k]

print(search(input_embedding))