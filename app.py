import json
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd

from instructions import load_faiss
from query import query_ollama, search_bites

# Initialisation de Flask et des extensions
app = Flask(__name__)

retriever = load_faiss()
with open("bites_articles_fr_cleaned.json", "r", encoding="utf-8") as file:
    data = json.load(file)
df = pd.json_normalize(data)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Modèle Utilisateur
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie! Connecte-toi maintenant.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Connexion réussie!", "success")
            return redirect(url_for('chat'))
        else:
            flash("Identifiants incorrects", "danger")
    return render_template('login.html')

# Route de déconnexion
@app.route('/logout')
def logout():
    logout_user()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('login'))

# Page du chatbot (accessible uniquement aux utilisateurs connectés)
@app.route('/chat')
@login_required
def chat():
    return render_template('index.html')

@app.route("/query", methods=["POST"])
@login_required  # Ensuring only logged-in users can query the chatbot
def query():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"answer": "Je n'ai pas compris votre question."})
    
    greetings = ["bonjour", "salut", "coucou"]
    if user_message.lower() in greetings:
        response = "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    else:
        search_results = search_bites(user_message, retriever, df)
        if search_results and "❌" not in search_results[0]:
            prompt = "Voici les morsures correspondant à votre question :\n\n"
            for bite in search_results:
                prompt += f"- {bite}\n"
            prompt += "\nPeux-tu donner des recommandations médicales ?"
 
            response = query_ollama(prompt)
        else:
            response = search_results[0]

    return jsonify({"answer": response})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
