import pandas as pd
from utils import calculate_cosine_similarity

data = [
    ("This is the original sentence.", "This is the original sentence.", 1),
    ("The sky is blue and beautiful.", "The sky is blue.", 1),
    ("Machine learning is fun.", "I like pizza.", 0),
    ("Python is a great language.", "I use Java for backend.", 0),
    ("Artificial intelligence is transforming technology.", "AI is changing tech.", 1),
    ("Climate change is a global challenge.", "Weather patterns are shifting worldwide.", 1),
    ("The cat sat on the mat.", "Dogs are loyal pets.", 0),
    ("Data science requires statistical knowledge.", "Statistics is important for data analysis.", 1),
    ("The sun rises in the east.", "The sun rises in the east every morning.", 1),
    ("Coffee is a popular beverage.", "Tea is consumed worldwide.", 0),
    ("Programming requires logical thinking.", "Coding needs problem-solving skills.", 1),
    ("The ocean is vast and deep.", "Mountains are tall and majestic.", 0),
]

rows = []
for orig, sub, label in data:
    sim = calculate_cosine_similarity(orig, sub)
    rows.append([orig, sub, sim, label])

df = pd.DataFrame(rows, columns=["Original", "Submission", "Similarity", "Label"])
df.to_csv("plagiarism_dataset.csv", index=False)

print(f"Created dataset with {len(df)} samples")

