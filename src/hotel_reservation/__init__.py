"""
Hotel Reservation System

A Python system for finding the cheapest hotel from a chain of hotels
based on customer type, dates, and pricing rules.
"""

from .models import Hotel, CustomerType, DayType
from .system import HotelReservationSystem

__version__ = "1.0.0"
__author__ = "Kevin Pattni"
__email__ = "pattni.kevin@gmail.com"

__all__ = [
    "Hotel",
    "CustomerType", 
    "DayType",
    "HotelReservationSystem",
]