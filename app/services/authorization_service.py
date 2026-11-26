from app.models.booking import Booking
from app.models.user import User


def can_access_booking(user: User, booking: Booking) -> bool:
    return user.user_id == booking.user_id