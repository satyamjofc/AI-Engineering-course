from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader import docs

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 250,
    add_start_index = True
)

all_splits = text_splitter.split_documents(docs)
# print({len(all_splits)})