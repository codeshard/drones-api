from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

_drone_id = str(uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6", version=4))


def test_create_drone(client: TestClient, db: Session) -> None:
    response = client.post(
        "/drones",
        json={
            "id": _drone_id,
            "created_at": "2021-12-23T22:37:43.918640",
            "serial_number": "test-drone-007",
            "weight_limit": 500,
            "battery_capacity": 100,
        },
    )
    assert response.status_code == 200


def test_retrieve_drone(client: TestClient, db: Session):
    response = client.get(f"/drones/{_drone_id}")
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-12-23T22:37:43.918640",
        "model": 1,
        "state": 1,
        "serial_number": "test-drone-007",
        "weight_limit": 500.0,
        "battery_capacity": 100.0,
    }


def test_update_drone(client: TestClient, db: Session) -> None:
    response = client.patch(
        f"/drones/{_drone_id}",
        json={
            "weight_limit": 400,
            "battery_capacity": 90,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2021-12-23T22:37:43.918640",
        "model": 1,
        "state": 1,
        "serial_number": "test-drone-007",
        "weight_limit": 400.0,
        "battery_capacity": 90.0,
    }


def test_list_drones(client: TestClient, db: Session) -> None:
    response = client.get("/drones")
    assert response.status_code == 200


def test_delete_drone(client: TestClient, db: Session) -> None:
    response = client.post(
        f"/drones/{_drone_id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {"ok": True}
