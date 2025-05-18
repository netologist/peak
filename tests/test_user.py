def test_create_user(client):
    response = client.post(
        "/api/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_users(client):
    # Create a user first
    client.post(
        "/api/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1