# AI Chatbot with FAISS, LangChain, Flask, Ollama, and LLaMA 3.2

## 📌 Description
This project is an intelligent chatbot capable of answering questions about bites using a vector database indexed with **FAISS** and an advanced language model (**LLaMA 3.2**). It is built with **LangChain** for prompt and document management and runs on **Flask** as the backend.

## 🚀 Features
- Indexing and similarity search with **FAISS**
- **LangChain** for structuring queries
- **LLaMA 3.2** model integration via **Ollama**
- **Flask** API interface to interact with the chatbot
- Processes a cleaned data file on bites

---

## 🛠️ Installation

### Prerequisites
Before installing the project, make sure you have installed:
- **Python 3.8+**
- **pip**
- **virtualenv** (I recommended)
- **SQLite** database for users informations

### Installation Steps

1. **Clone the project**
   ```sh
   git clone https://github.com/your-repo/chatbot-faiss-llama.git
   cd chatbot-faiss-llama
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Flask application**
   ```sh
   python app.py
   ```

The API will be available by default at: `http://127.0.0.1:5000/`

---

## 🏗️ Project Structure
```
chatbot-faiss-llama/
│── data_call/            # where we get and manage our data
│── vector/               # Trained models and indexing
│── app.py                # Main Flask script
│── README.md             # Project documentation
```

---

## 🎯 Usage

### Sending a request to the chatbot
Once the Flask server is running, you can interact with the chatbot by sending a **POST** request to the API:

## 🛠️ Technologies Used
- **FAISS**: Indexing and similarity search
- **LangChain**: Orchestrating queries and prompt management
- **Flask**: Backend API
- **Ollama**: Interface to run LLaMA 3.2
- **Python**: Main programming language

