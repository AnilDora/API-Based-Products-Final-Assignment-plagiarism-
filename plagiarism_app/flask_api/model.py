import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from utils import calculate_cosine_similarity

data = [
    ("The quick brown fox jumps over the lazy dog.", "The quick brown fox jumps over the lazy dog.", 1),
    ("Data science is interesting.", "I love studying data science.", 1),
    ("Python is cool.", "Java is another language.", 0),
    ("Weather is nice today.", "Apples are tasty.", 0),
    ("Machine learning is transforming industries.", "ML is revolutionizing businesses.", 1),
    ("The Earth revolves around the Sun.", "Our planet orbits the Sun.", 1),
    ("Pizza is delicious.", "I enjoy reading books.", 0),
    ("Artificial intelligence requires computational power.", "AI needs processing capacity.", 1),
    ("Summer is hot and sunny.", "Winter brings cold weather.", 0),
    ("Neural networks are powerful.", "Deep learning models are effective.", 1),
]

rows = []
for orig, sub, label in data:
    sim = calculate_cosine_similarity(orig, sub)
    rows.append([sim, label])

df = pd.DataFrame(rows, columns=["similarity", "label"])
X = df[["similarity"]]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

print(f"Accuracy: {model.score(X_test, y_test):.2%}")

joblib.dump(model, "plagiarism_model.pkl")
print("Done")

