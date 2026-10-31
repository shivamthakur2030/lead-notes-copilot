
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Lead Notes Copilot API"
    }


def test_get_leads(client):
    response = client.get("/leads")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_lead(client):
    response = client.get("/leads/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Lead not found"


def test_create_lead(client):
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "company": "Test Company"
    }

    response = client.post("/leads", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["company"] == payload["company"]
    assert "id" in data


def test_create_note(client):
    lead_payload = {
        "name": "Notes Test User",
        "email": "notes-test@example.com",
        "company": "Notes Test Company"
    }

    lead_response = client.post("/leads", json=lead_payload)
    assert lead_response.status_code == 200

    lead_id = lead_response.json()["id"]

    note_payload = {
        "content": "Discussed pricing and scheduled a demo."
    }

    response = client.post(
        f"/leads/{lead_id}/notes",
        json=note_payload
    )

    assert response.status_code == 200
    data = response.json()

    assert data["content"] == note_payload["content"]
    assert data["lead_id"] == lead_id
    assert "id" in data

def test_create_lead_invalid_email(client):
    payload = {
        "name": "Invalid Email User",
        "email": "not-an-email",
        "company": "Test Company"
    }

    response = client.post("/leads", json=payload)

    assert response.status_code == 422


def test_create_lead_missing_field(client):
    payload = {
        "name": "Missing Field User",
        "email": "missing@example.com"
    }

    response = client.post("/leads", json=payload)

    assert response.status_code == 422


def test_create_note_empty_content(client):
    lead_payload = {
        "name": "Empty Note Test",
        "email": "empty-note@example.com",
        "company": "Test Company"
    }

    lead_response = client.post("/leads", json=lead_payload)
    assert lead_response.status_code == 200

    lead_id = lead_response.json()["id"]

    response = client.post(
        f"/leads/{lead_id}/notes",
        json={"content": ""}
    )

    assert response.status_code == 422


def test_update_lead(client):
    payload = {
        "name": "Update Test User",
        "email": "update-test@example.com",
        "company": "Old Company"
    }

    created = client.post("/leads", json=payload)
    assert created.status_code == 200
    lead_id = created.json()["id"]

    response = client.patch(
        f"/leads/{lead_id}",
        json={"company": "New Company"}
    )

    assert response.status_code == 200
    assert response.json()["company"] == "New Company"
    assert response.json()["name"] == "Update Test User"


def test_delete_lead(client):
    payload = {
        "name": "Delete Test User",
        "email": "delete-test@example.com",
        "company": "Delete Company"
    }

    created = client.post("/leads", json=payload)
    assert created.status_code == 200
    lead_id = created.json()["id"]

    deleted = client.delete(f"/leads/{lead_id}")
    assert deleted.status_code == 200

    fetched = client.get(f"/leads/{lead_id}")
    assert fetched.status_code == 404


def test_analytics_overview(client):
    response = client.get("/analytics/overview")

    assert response.status_code == 200

    data = response.json()
    assert "total_leads" in data
    assert "total_notes" in data
    assert "leads_without_notes" in data

