import streamlit as st
import requests

st.set_page_config(page_title="Plagiarism Checker", layout="wide")

st.title("Plagiarism Checker")
st.write("Upload two files")

API_URL = "http://localhost:5000/check"

try:
    res = requests.get("http://localhost:5000/health", timeout=1)
    if res.status_code == 200:
        st.success("API connected")
except:
    st.error("API not running")

st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Original")
    file1 = st.file_uploader("Upload original", type=["txt"], key="f1")

with c2:
    st.subheader("Submission")
    file2 = st.file_uploader("Upload submission", type=["txt"], key="f2")

if file1 and file2:
    if st.button("Check"):
        try:
            res = requests.post(API_URL, files={
                "original": ("orig.txt", file1.getvalue()),
                "submission": ("sub.txt", file2.getvalue())
            })
            
            if res.status_code == 200:
                data = res.json()
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns(3)
                
                sim = data['similarity_score'] * 100
                prob = data['probability'] * 100
                result = "PLAGIARIZED" if data["plagiarized"] else "ORIGINAL"
                
                col1.metric("Similarity", f"{sim:.1f}%")
                col2.metric("Probability", f"{prob:.1f}%")
                col3.metric("Result", result)
                
                st.markdown("---")
                
                if data["plagiarized"]:
                    st.error("Plagiarism detected")
                else:
                    st.success("Looks original")
                
                st.markdown("---")
                
                c1, c2 = st.columns(2)
                
                with c1:
                    st.write("**Original:**")
                    st.markdown(data['highlighted_original'], unsafe_allow_html=True)
                
                with c2:
                    st.write("**Submission:**")
                    st.markdown(data['highlighted_submission'], unsafe_allow_html=True)
                
                if "statistics" in data:
                    st.markdown("---")
                    s1, s2 = st.columns(2)
                    
                    stats1 = data['statistics']['original']
                    stats2 = data['statistics']['submission']
                    
                    s1.write(f"Chars: {stats1['characters']}, Words: {stats1['words']}")
                    s2.write(f"Chars: {stats2['characters']}, Words: {stats2['words']}")
            else:
                st.error("Error")
                
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Upload both files")
