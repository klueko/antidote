import os
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from sentence_transformers import SentenceTransformer

FAISS_INDEX_PATH = "C:/antidote/model/bites_faiss_index"
CLEANED_DATA_FILE = "C:/antidote/data_call/bites_articles_fr_cleaned.json"

def create_faiss_db(data=None):
    """Creates a FAISS index from cleaned PubMed articles using HuggingFace embeddings."""

    # Load data if not provided
    if data is None:
        try:
            with open(CLEANED_DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"❌ Error: {CLEANED_DATA_FILE} not found. Run `clean_data.py` first.")
            return

    if not data:
        print("❌ No data available for FAISS indexing.")
        return

    # Load Sentence Transformer model
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # Prepare text and metadata for embedding
    texts = [
        f"{article.get('Title', '')} - {article.get('Abstract', '')}"
        for article in data
    ]
    pubmed_ids = [article.get("PubMed ID", "No ID") for article in data]

    print(f"✅ {len(texts)} articles prêts pour l'indexation FAISS.")

    embeddings = model.encode(texts, convert_to_tensor=False)
    print(f"✅ {len(embeddings)} embeddings générés avec succès.")

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create FAISS documents with metadata
    documents = [
        Document(page_content=text, metadata={"PubMed ID": pubmed_id})
        for text, pubmed_id in zip(texts, pubmed_ids)
    ]

    # Create FAISS index
    vector_store = FAISS.from_documents(documents, embedder)
    vector_store.save_local(FAISS_INDEX_PATH)

    return vector_store

def test_faiss():
    """ Loads FAISS and tests retrieval. """
    if not os.path.exists(FAISS_INDEX_PATH):
        print(f"FAISS index {FAISS_INDEX_PATH} not found.")
        return

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    retriever = FAISS.load_local(FAISS_INDEX_PATH, embedder, allow_dangerous_deserialization=True).as_retriever()

    query = "Quels sont les effets des morsures de serpent?"
    results = retriever.get_relevant_documents(query)

    for i, doc in enumerate(results[:3]):
        print(f"🔹 Résultat {i+1} : {doc.page_content[:300]}...")

if __name__ == "__main__":
    print("🚀 Début de l'indexation FAISS...")
    
    create_faiss_db()  # Création et sauvegarde de l'index FAISS
    test_faiss()

    print("Processus complété")
