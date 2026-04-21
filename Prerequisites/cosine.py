import json
from numpy import dot
from numpy.linalg import norm
import numpy as np

def cos_sim(embd1, embd2):
    similarity = dot(embd1, embd2)/(norm(embd1) * norm(embd2))
    return similarity

with open("king.json", "r") as file:
    data = json.load(file)
    result = data["results"]
    king = result["embeddings"]
    king = king[0]

with open("queen.json", "r") as file:
    data = json.load(file)
    result = data["results"]
    queen = result["embeddings"]
    queen = queen[0]

with open("man.json", "r") as file:
    data = json.load(file)
    result = data["results"]
    man = result["embeddings"]
    man = man[0]
    
with open("women.json", "r") as file:
    data = json.load(file)
    result = data["results"]
    women = result["embeddings"]
    women = women[0]

king_queen = cos_sim(king, queen)
# print(king_queen)
man_women = cos_sim(man, women)
# print(man_women)
king_man = cos_sim(king, man)
queen_women = cos_sim(queen, women)


# result = king_queen - man_women
# result1 = king_man - queen_women
# print(result)
# print(result1)

analogy = np.array(king) - np.array(man) + np.array(women)
score = cos_sim(analogy, queen)
print(score)