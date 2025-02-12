from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import faiss
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama

from model.query import query_model

embedding_model = OllamaEmbeddings(model="llama3.2")
vector_store = FAISS.load_local("/antidote/model/faiss_index", embedding_model)

llm = Ollama(model="llama3.2")

app = Flask(__name__)
CORS(app)

@app.route('/chat')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    pass
# must add generative logic

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    user_query = data.get("question", "")
    response = query_model(user_query)
    return jsonify({"response": response})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Rechercher les documents les plus pertinents
    docs = vector_store.similarity_search(question, k=3)

    # Construire le contexte pour LLaMA
    context = "\n\n".join([doc.page_content for doc in docs])

    # Générer la réponse avec LLaMA
    prompt = f"Réponds à la question en utilisant les informations ci-dessous :\n\n{context}\n\nQuestion : {question}\nRéponse :"
    response = llm.invoke(prompt)

    return jsonify({"question": question, "answer": response})

if __name__ == '__main__':
    app.run(debug=True)