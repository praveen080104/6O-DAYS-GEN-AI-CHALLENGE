from langchain_community.document_loaders import ArxivLoader # type: ignore

a = ArxivLoader(query = "1706.03762")

print(a.load())