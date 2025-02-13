import os
import json
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

from vector.indexing import create_faiss_db

DATA_FILE = os.path.join(os.path.dirname(__file__), "bites_articles_fr_cleaned.json")
FAISS_INDEX_PATH = os.path.abspath("C:/antidote/model/bites_faiss_index")

def load_data_as_dataframe():
    """Loads the cleaned dataset into a Pandas DataFrame."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.json_normalize(data)

def load_preprocessed_data():
    """Loads cleaned data as a JSON list."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_faiss():
    """Loads the FAISS index."""
    if not os.path.exists(FAISS_INDEX_PATH):
        print("❌ FAISS index not found. Creating a new one...")
        data = load_preprocessed_data()
        create_faiss_db(data)
    
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(FAISS_INDEX_PATH, embedder, allow_dangerous_deserialization=True)
    
    return vector_store.as_retriever()

def detect_animal_type(query):
    """Identifies the animal mentioned in the user’s query."""
    animal_keywords = {
        "chien": ["chien", "canidé", "rage", "morsure de chien"],
        "chat": ["chat", "félin", "griffure", "morsure de chat"],
        "serpent": ["serpent", "vipère", "cobra", "venin", "morsure de serpent"],
        "chauve-souris": ["chauve-souris", "rage", "morsure de chauve-souris"],
        "araignée": ["araignée", "veuve noire", "recluse brune", "morsure d'araignée"],
        "scorpion": ["scorpion", "venin", "morsure de scorpion"],
        "tique": ["tique", "lyme", "morsure de tique"],
        "insecte": ["moustique", "abeille", "guêpe", "fourmi", "piqûre d'insecte"]
    }

    for animal, keywords in animal_keywords.items():
        if any(keyword in query.lower() for keyword in keywords):
            return animal
    return None
