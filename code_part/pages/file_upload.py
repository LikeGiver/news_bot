import streamlit as st
import anthropic

uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
