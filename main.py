from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference  # pyright: ignore[reportUnknownVariableType]

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

app = FastAPI()

shipments = {
    12701: {
        "weight": 0.6,
        "content": "glassware",
        "status": "placed",
        "destination": 11234,
    },
    12702: {
        "weight": 2.3,
        "content": "electronics",
        "status": "in transit",
        "destination": 11222,
    },
    12703: {
        "weight": 0.9,
        "content": "books",
        "status": "delivered",
        "destination": 11333,
    },
    12704: {
        "weight": 5.5,
        "content": "furniture",
        "status": "delayed",
        "destination": 114444,
    },
    12705: {
        "weight": 0.2,
        "content": "perishables",
        "status": "pending",
        "destination": 11555,
    },
    12706: {
        "weight": 1.0,
        "content": "clothing",
        "status": "cancelled",
        "destination": 11666,
    },
    12707: {
        "weight": 3.8,
        "content": "toys",
        "status": "in transit",
        "destination": 11777,
    },
}


@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
def get_shipment(id: int | None = None):
    if not id:
        id = max(shipments.keys())

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist",
        )

    return shipments[id]


@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    if shipment.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kg",
        )

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        **shipment.model_dump(),
        "destination": shipment.destination,
    }

    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {field: shipments[id][field]}


@app.put("/shipment")
def shipment_update(
    id: int,
    content: str,
    weight: float,
    status: str,
) -> dict[str, Any]:
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": status,
    }
    return shipments[id]


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    shipments[id].update(body.model_dump(exclude_none=True))
    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return {"detail": f"Shipment with id {id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
