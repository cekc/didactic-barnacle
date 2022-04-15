import flights_storage
from fastapi import FastAPI, HTTPException
from models import Flight, UpdateFlightQuery
from pydantic import ValidationError

api = FastAPI()

@api.get("/get_flight")
def get_flight(id: str) -> Flight:
    flight = flights_storage.get(id)
    if flight is not None:
        return flight
    else:
        raise HTTPException(404, 'Flight not found')

@api.post("/update_flight")
def update_flight(q: UpdateFlightQuery):
    try:
        flight = Flight(id=q.id, departure=q.departure, arrival=q.arrival)
    except ValidationError as e:
        raise HTTPException(400, 'Invalid request')

    return flights_storage.update(flight)