import re
import requests
import json
from instructions import detect_animal_type, load_faiss

# Load FAISS retriever
retriever = load_faiss()

def search_bites(query):
    """Search FAISS for relevant bite information."""
    if not retriever:
        return ["FAISS index not available."]

    print(f"🔍 Searching FAISS for: {query}")

    try:
        docs = retriever.get_relevant_documents(query)
    except Exception as e:
        print(f"FAISS search error: {e}")
        return ["FAISS search failed."]

    results = [doc.page_content for doc in docs]
    if not results:
        return ["No information found for this type of bite."]

    detected_animal = detect_animal_type(query)
    if detected_animal:
        filtered_results = [res for res in results if detected_animal in res.lower()]
        if filtered_results:
            return filtered_results

    return results


def query_ollama(prompt, model="llama3.2"):
    """Sends a request to Ollama (LLaMA 3.2) for a response."""
    print(f"Querying Ollama: {prompt[:100]}...")

    payload = {"model": model, "prompt": prompt}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload, headers=headers, stream=True)
        if response.status_code != 200:
            return f"Ollama error: {response.status_code}"

        final_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    final_response += json_data.get("response", "")
                except json.JSONDecodeError:
                    continue

        return final_response if final_response else "Aucune réponse obtenue."
    
    except requests.exceptions.RequestException as e:
        return f"Connection error to Ollama: {e}"
