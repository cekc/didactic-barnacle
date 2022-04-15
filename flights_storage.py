from flights_csv import dump_csv, read_csv
from models import Flight
from threading import Lock
from typing import Optional

csv_filename = 'flights.csv'
max_flights = 20

storage_lock = Lock()
storage_cache: Optional[dict[str, Flight]] = None

def get(id: str) -> Optional[Flight]:
    global storage_cache
    with storage_lock:
        if storage_cache is None:
            storage_cache = read_csv(csv_filename)
            
        f = storage_cache.get(id)
        if f is not None:
            return f.copy()

def update(flight: Flight):
    global storage_cache
    with storage_lock:
        if storage_cache is None:
            storage_cache = read_csv(csv_filename)

        success_count = sum(1 for f in storage_cache.values() if f.success)

        old_flight = storage_cache.get(id)
        if old_flight is not None:
            success_count -= old_flight.success

        flight.success = flight.duration_minutes() >= 180 and success_count < max_flights
        storage_cache[flight.id] = flight

        dump_csv(csv_filename, storage_cache)