from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def extract_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            page_text = page_text.replace("-\n", "")
            page_text = page_text.replace("\n", " ")
            text += page_text + " "
    return text.strip()

def chunk_text(text, pdf_path):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", ".", " ", ""]
    )
    split_texts = splitter.split_text(text)
    docs = [
        Document(
            page_content=chunk,
            metadata={"source": pdf_path, "chunk_id": i, "type": "pdf"}
        )
        for i , chunk in enumerate(split_texts)
    ]
    return docs


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def crate_vectorstore(docs):
    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_name="rag_docs"
        )
    
    def ingest_in_batches(docs, batch_size=32):
        for i in range(0, len(docs), batch_size):
            batch = docs[i:i+batch_size]
            db.add_documents(batch)
        db.persist()
        return db