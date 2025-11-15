from flask import Flask, request, jsonify
from utils import calculate_cosine_similarity, highlight_matching_text
import joblib
import os

app = Flask(__name__)

model = None
if os.path.exists("plagiarism_model.pkl"):
    model = joblib.load("plagiarism_model.pkl")
    print("Model loaded")
else:
    print("Model not found")

@app.route("/")
def home():
    return jsonify({"message": "Plagiarism Checker API"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/check", methods=["POST"])
def check():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    if 'original' not in request.files or 'submission' not in request.files:
        return jsonify({"error": "Need both files"}), 400
    
    try:
        f1 = request.files['original']
        f2 = request.files['submission']
        
        text1 = f1.read().decode("utf-8")
        text2 = f2.read().decode("utf-8")
        
        if not text1 or not text2:
            return jsonify({"error": "Empty files"}), 400
        
        sim = calculate_cosine_similarity(text1, text2)
        pred = model.predict([[sim]])[0]
        prob = model.predict_proba([[sim]])[0][1]
        hl1, hl2 = highlight_matching_text(text1, text2)
        
        return jsonify({
            "similarity_score": round(float(sim), 4),
            "plagiarized": bool(pred),
            "probability": round(float(prob), 4),
            "highlighted_original": hl1,
            "highlighted_submission": hl2,
            "statistics": {
                "original": {
                    "characters": len(text1),
                    "words": len(text1.split()),
                    "lines": len(text1.splitlines())
                },
                "submission": {
                    "characters": len(text2),
                    "words": len(text2.split()),
                    "lines": len(text2.splitlines())
                }
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

