import json
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
import os

from instructions import load_faiss
from query import query_ollama, search_bites

app = Flask(__name__)

retriever = load_faiss()
if os.path.exists("bites_articles_fr_cleaned.json"):
    with open("bites_articles_fr_cleaned.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    df = pd.json_normalize(data)
else:
    df = None

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Cet email est déjà utilisé. Veuillez en choisir un autre.")
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie! Connecte-toi maintenant.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            return redirect(url_for('login'))
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('chat'))
        else:
            flash("Identifiants incorrects")
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('login'))

@app.route('/chat')
# Accessible uniquement aux utilisateurs connectés)
@login_required
def chat():
    return render_template('index.html')

@app.route("/query", methods=["POST"])
@login_required
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
            prompt = "Voici les recommandations médicales correspondant à votre question :\n\n"
            for bite in search_results:
                prompt += f"- {bite}\n"
            prompt += "\nPeux-tu donner des recommandations médicales comme si je m'étais fait mordre ?"
 
            response = query_ollama(prompt)
        else:
            response = search_results[0]

    return jsonify({"answer": response})

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = db.session.get(User, current_user.id)
    if user:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash("Votre compte a été supprimé avec succès.")
        return redirect(url_for('register'))
    else:
        flash("Erreur lors de la suppression du compte.")
        return redirect(url_for('chat'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
