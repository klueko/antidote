import pytest
from app import app

def test_query_with_greeting(authenticated_client):
    # Test a greeting message
    response = authenticated_client.post(
        '/query',
        json={'message': 'bonjour'},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    assert response.json == {"answer": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"}

def test_query_with_medical_question(authenticated_client, mocker):
    # Mock the search_bites and query_ollama functions
    mocker.patch('app.search_bites', return_value=["Bite 1", "Bite 2"])
    mocker.patch('app.query_ollama', return_value="Recommandation médicale")

    # Test a medical question
    response = authenticated_client.post(
        '/query',
        json={'message': 'morsure'},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    assert response.json == {"answer": "Recommandation médicale"}

def test_query_with_no_message(authenticated_client):
    # Test with no message
    response = authenticated_client.post(
        '/query',
        json={},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    assert response.json == {"answer": "Je n'ai pas compris votre question."}

def test_query_with_no_results(authenticated_client, mocker):
    # Mock the search_bites function to return no results
    mocker.patch('app.search_bites', return_value=["❌ Aucun résultat trouvé"])

    # Test a query with no results
    response = authenticated_client.post(
        '/query',
        json={'message': 'invalid query'},
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    assert response.json == {"answer": "❌ Aucun résultat trouvé"}