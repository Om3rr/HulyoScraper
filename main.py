from alchemy import get_session
from flight import Flight
import requests

USERNAME = "Omertesttbot"
CHAT_ID = "@iloveaya"
API_KEY = "317083529:AAGnk7pMo301Kp3FW164OB5n4y7xUVn1HnI"

def send_flights(flights):
    chunk_size = 10
    for chunk in range(0, len(flights), chunk_size):
        body = "\n=============\n".join([str(f) for f in flights[chunk: chunk+chunk_size]])
        requests.post(
            "https://api.telegram.org/bot{API_KEY}/sendMessage".format(API_KEY=API_KEY),
            data={
                "chat_id": CHAT_ID,
                "text": body,
                "parse_mode": "Markdown"
            }
        )

def get_flights():
    resp = requests.get("https://s3.eu-central-1.amazonaws.com/catalogs.hulyo.co.il/catalogs/Production/Flights/v1.4/above199FlightsWebOnly.js")
    return resp.json().get("Flights")


if __name__ == "__main__":
    session = get_session()
    to_send = []
    for f_raw in get_flights():
        flight = Flight.factory(f_raw)
        if flight.already_exists(session): continue
        to_send.append(flight)
        session.add(flight)
    send_flights(to_send)
    session.commit()