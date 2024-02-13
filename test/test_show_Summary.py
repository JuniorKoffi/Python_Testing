
import sys
from pathlib import Path

# Obtenez le chemin absolu du répertoire racine de votre projet
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_show_summary_valid_client(client):
    # Simulate a valid POST request with the correct email
    response = client.post('/showSummary', data={'email': 'john@simplylift.com'})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 302

    # Add more assertions based on the expected behavior of your function
    # For example, you can check if certain content is present in the response HTML.


def test_show_summary_invalid_client(client):
    # Simulez une requête avec un email invalide
    response = client.post('/showSummary', data={'email': 'nonexistent@example.com'})

    # Assurez-vous que le statut de la réponse est 302 (redirection vers la page d'accueil)
    assert response.status_code == 302

    # Assurez-vous que l'URL de redirection se termine par "/"
    assert response.headers['Location'].endswith('/')


    # Add more assertions if needed

# You can add more test cases to cover different scenarios
