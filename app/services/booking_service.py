import json
from pathlib import Path
from app.models.booking import Booking

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
BOOKINGS_FILE = DATA_DIR / "bookings.json"

def get_booking(booking_id: str) -> Booking:
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        bookings = json.load(f)

    booking = next(
        (b for b in bookings if b["booking_id"] == booking_id),
        None
    )

    if booking is None:
        raise ValueError(f"Booking {booking_id} not found")

    return Booking(**booking)

def update_seat(booking_id: str, new_seat: str) -> dict:
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        bookings = json.load(f)

    booking_found = False
    for b in bookings:
        if b["booking_id"] == booking_id:
            b["seat"] = new_seat
            booking_found = True
            break

    if not booking_found:
        raise ValueError(f"Booking {booking_id} not found")

    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=2)

    return {"status": "success", "booking_id": booking_id, "new_seat": new_seat}