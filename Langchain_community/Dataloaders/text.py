from langchain_community.document_loaders import TextLoader # type: ignore

a = TextLoader('1.txt')

print(a.load())
