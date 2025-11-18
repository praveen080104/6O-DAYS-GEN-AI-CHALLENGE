from langchain_community.embeddings import HuggingFaceEmbeddings  # type: ignore
from langchain_community.vectorstores import FAISS  # type: ignore
a = HuggingFaceEmbeddings(model_name= "all-MiniLM-L6-V2")
b = "Hello i am praveen!"
c = FAISS.from_texts(b,a)
#print(c)

r = c.as_retriever()  # type: ignore

d = "hi?"

ans = r.invoke(d)
print(ans)

print([i.page_content for i in ans])
