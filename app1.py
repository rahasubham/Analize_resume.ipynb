import streamlit as st
import openai
import PyPDF2
import docx
import os

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key_here"
openai.api_key = OPENAI_API_KEY

# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Function to analyze resume and give feedback
def get_resume_feedback(resume_text):
    prompt = f"""
    Analyze the following resume and provide feedback on how to improve it.
    Identify missing skills, suggest better wording, and recommend additional experiences or projects.

    Resume Content:
    {resume_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("AI Resume Analyzer and Guidance")
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    # Extract resume text
    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format.")
        resume_text = ""

    if resume_text:
        # Get AI-based feedback
        feedback = get_resume_feedback(resume_text)

        # Display results
        st.subheader("Extracted Resume Content")
        st.text(resume_text[:1000])  # Show only first 1000 characters for readability

        st.subheader("AI Resume Feedback")
        st.write(feedback)