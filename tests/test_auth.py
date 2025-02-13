import pytest
from flask import url_for
from flask_login import current_user
from app import app, User

def test_register(client):
    with client.application.app_context():
        # Test initial state - no users in database
        initial_user_count = User.query.count()
        assert initial_user_count == 0

        # Test POST request to register a new user
        test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        response = client.post(url_for('register'), 
                             data=test_user_data, 
                             follow_redirects=True)

        # Verify response
        assert response.status_code == 200
        assert b"Connexion" in response.data  # Check for "Inscription" instead of full message

        # Verify user creation in database
        new_user_count = User.query.count()
        assert new_user_count == initial_user_count + 1

        # Verify user data in database
        created_user = User.query.filter_by(email=test_user_data['email']).first()
        assert created_user is not None
        assert created_user.username == test_user_data['username']
        assert created_user.email == test_user_data['email']
        
        # Verify password is hashed (not stored as plaintext)
        assert created_user.password != test_user_data['password']
        
        # Test duplicate registration
        response = client.post(url_for('register'), 
                             data=test_user_data, 
                             follow_redirects=True)
        
        # Verify duplicate registration is prevented
        assert b"email" in response.data.lower()  # Check for email-related message
        assert User.query.count() == new_user_count  # User count shouldn't increase

def test_delete_account(client):
    client.post("/register", data={"username": "malika1000", "email": "malika1000@mail.com", "password": "mdp123"})
    client.post("/login", data={"email": "malika1000@mail.com", "password": "mdp123"})
    
    response = client.post("/delete_account", follow_redirects=True)
    assert "Votre compte a été supprimé".encode() in response.data

def test_logout(client):
    with client.application.app_context():
        # First, register a user
        client.post(url_for('register'), data={
            'username': 'testuser1',
            'email': 'test1@example.com',
            'password': 'password123'
        })
        
        # Then login
        client.post(url_for('login'), data={
            'email': 'test1@example.com',
            'password': 'password123'
        })
        
        # Verify user is logged in by accessing protected route
        chat_response = client.get(url_for('chat'))
        assert chat_response.status_code == 200

        # Test logout
        logout_response = client.get(url_for('logout'), follow_redirects=True)
        
        # Verify response
        assert logout_response.status_code == 200
        assert b"Connexion" in logout_response.data  # Check redirection to login page
        assert b"D\xc3\xa9connexion r\xc3\xa9ussie" in logout_response.data  # Check flash message

        # Try to access protected route after logout
        protected_response = client.get(url_for('chat'), follow_redirects=True)
        assert b"Connexion" in protected_response.data  # Should redirect to login page