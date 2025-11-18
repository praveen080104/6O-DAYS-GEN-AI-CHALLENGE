from langchain_text_splitters import RecursiveCharacterTextSplitter # type: ignore
from langchain_community.document_loaders import PyPDFLoader # type: ignore
a= PyPDFLoader('50 Prompt Report.pdf')
d=a.load()
c = " ".join([i.page_content for i in d])
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
texts = text_splitter.split_text(c)
print(texts)
