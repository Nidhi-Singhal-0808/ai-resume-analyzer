import streamlit as st
import os
from utils.pdf_parser import extract_text_from_pdf
from utils.analyzer import analyze_resume_with_gemini

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & ATS Scorer")
st.markdown("Analyze your resume against any job description instantly using Google Gemini AI.")

st.markdown("---")

# Input Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste Job Description here...", height=150)

st.markdown("---")

# Analysis Action Button
if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
    # Error Handling & Validation
    if not uploaded_file:
        st.error("⚠️ Please upload a PDF resume before analyzing.")
    elif not job_description.strip():
        st.error("⚠️ Please enter or paste a job description.")
    else:
        with st.spinner("Extracting text and analyzing resume with Gemini AI... Please wait."):
            try:
                # Extract text
                resume_text = extract_text_from_pdf(uploaded_file)
                
                # Analyze with Gemini
                result = analyze_resume_with_gemini(resume_text, job_description)
                
                st.success("✅ Analysis Complete!")
                
                # Dashboard Display
                st.markdown("### 📊 Dashboard Results")
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric(label="Overall Resume Score", value=f"{result.get('overall_score', 0)} / 100")
                with metric_col2:
                    st.metric(label="Estimated ATS Score", value=f"{result.get('ats_score', 0)} / 100")
                
                st.info("💡 *Note: Scores are AI-estimated metrics based on keyword and skill matching, not official ATS software algorithms.*")
                
                # Detailed Breakdown
                tab1, tab2, tab3, tab4 = st.tabs(["Skills & Keywords", "Strengths & Weaknesses", "Missing Areas", "Action Plan"])
                
                with tab1:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("#### ✅ Matching Skills")
                        for skill in result.get("matching_skills", []):
                            st.markdown(f"- {skill}")
                    with col_b:
                        st.markdown("#### 🔍 Missing Keywords")
                        for kw in result.get("missing_keywords", []):
                            st.markdown(f"- {kw}")
                            
                with tab2:
                    col_c, col_d = st.columns(2)
                    with col_c:
                        st.markdown("#### 💪 Strengths")
                        for s in result.get("strengths", []):
                            st.markdown(f"- {s}")
                    with col_d:
                        st.markdown("#### ⚠️ Weaknesses")
                        for w in result.get("weaknesses", []):
                            st.markdown(f"- {w}")
                            
                with tab3:
                    st.markdown("#### ❌ Missing Skills Required by JD")
                    for ms in result.get("missing_skills", []):
                        st.markdown(f"- {ms}")
                        
                with tab4:
                    st.markdown("#### 🚀 Improvement Suggestions")
                    for sug in result.get("improvement_suggestions", []):
                        st.markdown(f"- {sug}")
                        
            except Exception as e:
                st.error(f"❌ An error occurred during processing: {str(e)}")