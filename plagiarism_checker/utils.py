from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    sim = cosine_similarity(vectors[0:1], vectors[1:2])
    return sim[0][0]

def highlight_matching_text(text1, text2):
    matcher = difflib.SequenceMatcher(None, text1, text2)
    blocks = matcher.get_matching_blocks()

    def add_marks(text, blocks, first=True):
        result = []
        last = 0
        for block in blocks:
            start = block.a if first else block.b
            size = block.size
            if size == 0:
                continue
            result.append(text[last:start])
            result.append(f"<mark>{text[start:start+size]}</mark>")
            last = start + size
        result.append(text[last:])
        return ''.join(result)

    return add_marks(text1, blocks, True), add_marks(text2, blocks, False)
