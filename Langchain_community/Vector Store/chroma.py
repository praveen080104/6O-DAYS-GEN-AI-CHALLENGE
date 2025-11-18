from langchain_community.embeddings import HuggingFaceEmbeddings # type: ignore
from langchain_community.vectorstores import Chroma # type: ignore

emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

texts = ["Hello I am Praveen!"]

vector_store = Chroma.from_texts(texts, emb, persist_directory="new_chroma_db")

print(vector_store)

vector_store.persist()     # save to disk
