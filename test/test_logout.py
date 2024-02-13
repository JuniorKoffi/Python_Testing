import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_logout_redirects_to_index(client):
    # Effectuer une demande GET pour se déconnecter
    response = client.get('/logout', follow_redirects=True)
    
    # Vérifier que la réponse a un code d'état 200 (OK)
    assert response.status_code == 200
    
