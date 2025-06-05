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

    # Create mock cursor with mocked to_list method
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value.skip.return_value.limit.return_value = mock_cursor
    mock_cursor.to_list = AsyncMock(return_value=mock_services)

    # Patch both find and count_documents using patch.object
    with patch.object(service_module.db.services, "find", return_value=mock_cursor):
        with patch.object(service_module.db.services, "count_documents", new=AsyncMock(return_value=2)):
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as ac:
                response = await ac.get("/services")

            # Assert results
            assert response.status_code == 200
            data = response.json()
            assert "data" in data
            assert "total" in data
            assert data["total"] == 2
            assert data["data"][0]["name"] == "Physiotherapist"
