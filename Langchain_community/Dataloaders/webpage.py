from langchain_community.document_loaders import WebBaseLoader # type: ignore

a = WebBaseLoader(web_path="https://www.geeksforgeeks.org/machine-learning/machine-learning/")

print(a.load())