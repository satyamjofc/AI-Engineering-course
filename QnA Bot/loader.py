from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data.pdf")
docs = loader.load()