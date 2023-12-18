import streamlit as st
import anthropic
from vector_store import get_vector_store, get_embed_model

from pathlib import Path
from llama_hub.file.pymu_pdf.base import PyMuPDFReader
from llama_index.node_parser.text import SentenceSplitter
from llama_index.schema import TextNode

uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"))

vector_store = get_vector_store()

embed_model = get_embed_model()

# deal with the pdf file
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":

        #save uploaded_file to local
        try:
            with open('/home/likegiver/Desktop/codes/2023_11/nlp_final/our_work/data/'+ uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except:
            st.write("Error while saving file, maybe because there already exists a file with the same name.")

        loader = PyMuPDFReader()
        documents = loader.load(file_path='/home/likegiver/Desktop/codes/2023_11/nlp_final/our_work/data/'+ uploaded_file.name)
        
        text_parser = SentenceSplitter(
            chunk_size=200,
            # separator=" ",
        )

        text_chunks = []
        # maintain relationship with source doc index, to help inject doc metadata in (3)
        doc_idxs = []
        for doc_idx, doc in enumerate(documents):
            cur_text_chunks = text_parser.split_text(doc.text)
            text_chunks.extend(cur_text_chunks)
            doc_idxs.extend([doc_idx] * len(cur_text_chunks))

        nodes = []
        for idx, text_chunk in enumerate(text_chunks):
            node = TextNode(
                text=text_chunk,
            )
            src_doc = documents[doc_idxs[idx]]
            node.metadata = src_doc.metadata
            nodes.append(node)
            
        for node in nodes:
            node_embedding = embed_model.get_text_embedding(
                node.get_content(metadata_mode="all")
            )
            node.embedding = node_embedding
        
        vector_store.add(nodes)
        st.write("Done!")