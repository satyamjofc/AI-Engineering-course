docs = [
    "Football is a popular sport played worldwide",
    "Cricket is widely played in India",
    "Basketball involves dribbling and shooting",

    "Stock markets fluctuate based on economic conditions",
    "Investing in mutual funds can be beneficial",
    "Inflation affects purchasing power",

    "Artificial Intelligence is transforming industries",
    "Machine learning models learn from data",
    "Neural networks are used in deep learning",

    "Cooking requires ingredients and proper technique",
    "Baking involves precise measurements",
    "Recipes guide food preparation"
]

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(docs)

print(embeddings.shape)


import umap
reducer = umap.UMAP(n_neighbors=5, min_dist=0.3, random_state=42)
reduced = reducer.fit_transform(embeddings)

import matplotlib.pyplot as plt

x = reduced[:, 0]
y = reduced[:, 1]

plt.figure(figsize=(8,6))
plt.scatter(x, y)

for i, txt in enumerate(docs):
    plt.annotate(i, (x[i], y[i]))

plt.title("Document Clusters Visualization")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()