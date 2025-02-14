import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
import pytest
from app import app, db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SERVER_NAME'] = 'localhost'
    app.config['APPLICATION_ROOT'] = '/'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def authenticated_client(client):
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
        user = User(username='testuser', email='test@example.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()

        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)