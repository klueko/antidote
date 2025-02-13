from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from query import query_ollama, search_bites

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

    if not user_query:
        return jsonify({"error": "No question provided"}), 400

    # Search FAISS for relevant documents
    results = search_bites(user_query)

    # Generate response with Ollama
    prompt = "Voici les instructions médicales:\n\n" + "\n".join(results)
    prompt += "\nPeux-tu faire des recommandations de prise en charge médicale et chirurgicale ?"

    response = query_ollama(prompt)
    return jsonify({"question": user_query, "answer": response})

if __name__ == '__main__':
    app.run(debug=True)