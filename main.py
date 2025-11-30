from typing import Any
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    12701: {
        "weight": 0.6,
        "content": "glassware",
        "status": "placed",
    },
    12702: {
        "weight": 2.3,
        "content": "electronics",
        "status": "in transit",
    },
    12703: {
        "weight": 0.9,
        "content": "books",
        "status": "delivered",
    },
    12704: {
        "weight": 5.5,
        "content": "furniture",
        "status": "delayed",
    },
    12705: {
        "weight": 0.2,
        "content": "perishables",
        "status": "pending",
    },
    12706: {
        "weight": 1.0,
        "content": "clothing",
        "status": "cancelled",
    },
    12707: {
        "weight": 3.8,
        "content": "toys",
        "status": "in transit",
    },
}


@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        return {"detail": "Given id doesn't exist!"}

    return shipments[id]


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
