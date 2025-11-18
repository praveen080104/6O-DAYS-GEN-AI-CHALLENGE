from langchain_xai import XAIEmbeddings # type: ignore

emb = XAIEmbeddings(
    model="grok-2-embed",
    api_key="YOUR_XAI_API_KEY"
)

result = emb.embed_query("Hello I am Praveen!")
print(result[:5])
