import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import FastAPI

from routes.services import router
import routes.services as service_module

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_get_services():
    # Mock service data
    mock_services = [
        {"_id": "123abc", "name": "Physiotherapist", "category": "Health", "is_active": True},
        {"_id": "456def", "name": "Swimming", "category": "Sports", "is_active": True}
    ]

    mock_cursor = MagicMock()
    mock_cursor.sort.return_value.skip.return_value.limit.return_value = mock_cursor
    mock_cursor.to_list = AsyncMock(return_value=mock_services)

    # Create mock services collection
    mock_services_collection = MagicMock()
    mock_services_collection.find.return_value = mock_cursor
    mock_services_collection.count_documents = AsyncMock(return_value=2)

    # Patch the db.services object itself
    with patch.object(service_module.db, "services", mock_services_collection):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/services")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert data["total"] == 2
        assert data["data"][0]["name"] == "Physiotherapist"