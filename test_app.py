import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"DreamCars" in response.data

def test_wishlist(client):
    response = client.get('/wishlist')
    assert response.status_code == 200
    assert b"Your Wishlist" in response.data