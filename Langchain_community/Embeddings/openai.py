from langchain_community.embeddings import OpenAIEmbeddings  # type: ignore
a = OpenAIEmbeddings(open_api_key = "<your - key>")
b = "Hello i am praveen!"
c = a.embed_query(b)
print(c)