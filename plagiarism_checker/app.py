import streamlit as st
import joblib
import os
from utils import calculate_cosine_similarity, highlight_matching_text

st.set_page_config(page_title="Plagiarism Checker", page_icon="📄", layout="wide")

st.title("📄 Plagiarism Checker")
st.write("Upload two text files to check for plagiarism")

model_path = "plagiarism_model.pkl"
if not os.path.exists(model_path):
    st.error("Model not found! Run: python model.py")
    st.stop()

try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Document")
    file1 = st.file_uploader("Upload original", type=["txt"], key="original")
    
with col2:
    st.subheader("Submission Document")
    file2 = st.file_uploader("Upload submission", type=["txt"], key="submission")

if file1 and file2:
    try:
        text1 = file1.read().decode("utf-8")
        text2 = file2.read().decode("utf-8")
        
        st.markdown("---")
        st.subheader("Results")
        
        sim_score = calculate_cosine_similarity(text1, text2)
        
        pred = model.predict([[sim_score]])[0]
        prob = model.predict_proba([[sim_score]])[0][1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Similarity", f"{sim_score:.4f}")
        
        with col2:
            st.metric("Probability", f"{prob:.2%}")
        
        with col3:
            result = "PLAGIARIZED" if pred == 1 else "ORIGINAL"
            st.metric("Result", result)
        
        st.markdown("---")
        
        if pred == 1:
            st.error("This looks plagiarized!")
            st.write(f"Similarity is {sim_score:.2%}")
        else:
            st.success("This looks original")
            st.write(f"Similarity is {sim_score:.2%}")
        
        st.markdown("---")
        st.subheader("Matching Text")
        
        hl1, hl2 = highlight_matching_text(text1, text2)
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("**Original:**")
            st.markdown(
                f"<div style='background-color:#f9f9f9;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:400px;overflow-y:auto'>{hl1}</div>",
                unsafe_allow_html=True
            )
        
        with c2:
            st.markdown("**Submission:**")
            st.markdown(
                f"<div style='background-color:#f0f0f0;padding:15px;border-radius:8px;border:1px solid #ddd;max-height:400px;overflow-y:auto'>{hl2}</div>",
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        st.subheader("Stats")
        
        s1, s2 = st.columns(2)
        
        with s1:
            st.write("**Original:**")
            st.write(f"Characters: {len(text1)}")
            st.write(f"Words: {len(text1.split())}")
            st.write(f"Lines: {len(text1.splitlines())}")
        
        with s2:
            st.write("**Submission:**")
            st.write(f"Characters: {len(text2)}")
            st.write(f"Words: {len(text2.split())}")
            st.write(f"Lines: {len(text2.splitlines())}")
        
    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Upload both files")

with st.sidebar:
    st.header("About")
    st.write("This app checks plagiarism using TF-IDF and cosine similarity")
    st.write("")
    st.write("**How it works:**")
    st.write("1. Upload two files")
    st.write("2. Calculate similarity")
    st.write("3. ML model predicts result")
    st.write("4. Shows matching text")

