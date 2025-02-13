from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


# Initialisation de Flask et des extensions
app = Flask(__name__)
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
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            # flash("Tous les champs doivent être remplis.", "danger")
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            # flash("Connexion réussie!", "success")
            return redirect(url_for('chat'))
        else:
            flash("Email ou mot de passe incorrect.", "danger")

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

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)

    if user:
        print(f"🗑️ Suppression du compte : {user.username}")  # Debug
        logout_user()  # Déconnecter avant suppression
        db.session.delete(user)  # Supprimer l'utilisateur de la base
        db.session.commit()
        flash("Votre compte a été supprimé avec succès.", "success")
    else:
        print("❌ Erreur : utilisateur non trouvé")  # Debug
        flash("Erreur : impossible de supprimer le compte.", "danger")

    return redirect(url_for('login'))  # Rediriger vers la page de connexion après suppression

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


