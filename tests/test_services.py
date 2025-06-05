import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI

from routes.services import router
import routes.services as service_module

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_get_services(monkeypatch):
    # Mock data
    mock_services = [
        {"_id": "123abc", "name": "Physiotherapist", "category": "Health", "is_active": True},
        {"_id": "456def", "name": "Swimming", "category": "Sports", "is_active": True}
    ]

    # Define mock cursor
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value.skip.return_value.limit.return_value = mock_cursor
    mock_cursor.to_list = AsyncMock(return_value=mock_services)

    # Mock db methods
    mock_find = MagicMock(return_value=mock_cursor)
    mock_count = AsyncMock(return_value=5)

    # Monkeypatch db access
    monkeypatch.setattr(service_module.db.services, "find", mock_find)
    monkeypatch.setattr(service_module.db.services, "count_documents", mock_count)

    # Run test
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/services")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total" in data
    assert data["total"] == 5
    assert data["data"][0]["name"] == "Physiotherapist"
