# Load model directly
from transformers import AutoModel, AutoTokenizer
# model = AutoModel.from_pretrained("/home/likegiver/Desktop/codes/huggingface_models/ChatGLM3-6b/", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("/home/likegiver/Desktop/codes/huggingface_models/ChatGLM3-6b/", trust_remote_code=True)