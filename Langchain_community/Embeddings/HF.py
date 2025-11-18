from langchain_community.embeddings import HuggingFaceEmbeddings  # type: ignore
a = HuggingFaceEmbeddings(model_name= "all-MiniLM-L6-V2")
b = "Hello i am praveen!"
c = a.embed_query(b)
print(c[:5])