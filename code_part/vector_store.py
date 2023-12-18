import psycopg2
from sqlalchemy import make_url
from llama_index.vector_stores import PGVectorStore
from llama_index.embeddings import HuggingFaceEmbedding

db_name = "news_db"
host = "localhost"
password = "123456"
port = "5432"
user = "likegiver"

embed_model = HuggingFaceEmbedding(model_name="/home/likegiver/Desktop/codes/huggingface_models/m3e-base")

vector_store = PGVectorStore.from_params(
    database=db_name,
    host=host,
    password=password,
    port=port,
    user=user,
    table_name="2023_12_18_news",
    embed_dim=768,  # openai embedding dimension
)

def get_vector_store():
    return vector_store

def get_embed_model():
    return embed_model