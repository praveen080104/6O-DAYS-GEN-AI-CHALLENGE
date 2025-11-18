from langchain_community.document_loaders import PyPDFLoader # type: ignore

a = PyPDFLoader('50 Prompt Report.pdf')

print(a.load())