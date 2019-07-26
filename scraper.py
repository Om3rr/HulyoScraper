from alchemy import get_session
import requests
from flight import Flight


session = get_session()

def get_flights():
    resp = requests.get("https://s3.eu-central-1.amazonaws.com/catalogs.hulyo.co.il/catalogs/Production/Flights/v1.4/above199FlightsWebOnly.js")
    return resp.json().get("Flights")

for f_raw in get_flights():
    flight = Flight.factory(f_raw)
    if flight.already_exists(session): continue
    session.add(flight)
session.commit()