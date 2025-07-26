"""
Core hotel reservation system logic.
"""

import re
from datetime import datetime
from typing import List, Tuple, Dict, Any

from .models import Hotel, CustomerType, DayType


class HotelReservationSystem:
    """Main system for handling hotel reservations"""

    def __init__(self):
        """Initialize the system with Miami hotels data"""
        self.hotels = [
            Hotel("Lakewood", 3, 110, 80, 90, 80),
            Hotel("Bridgewood", 4, 160, 110, 60, 50),
            Hotel("Ridgewood", 5, 220, 100, 150, 40),
        ]

    def parse_input(self, input_str: str) -> Tuple[CustomerType, List[datetime]]:
        """
        Parse the input string to extract customer type and dates

        Args:
            input_str: Input in format "CustomerType: date1, date2, ..."

        Returns:
            Tuple of (customer_type, list_of_dates)

        Raises:
            ValueError: If input format is invalid
        """
        try:
            # Split by colon and clean whitespace
            parts = [part.strip() for part in input_str.split(":", 1)]
            if len(parts) != 2:
                raise ValueError("Input must contain ':' separator")

            customer_str, dates_str = parts

            # Parse customer type
            try:
                customer_type = CustomerType(customer_str)
            except ValueError:
                raise ValueError(
                    f"Invalid customer type: {customer_str}. Must be 'Regular' or 'Rewards'"
                )

            # Parse dates
            date_strings = [date.strip() for date in dates_str.split(",")]
            dates = []

            for date_str in date_strings:
                # Remove day of week in parentheses if present
                clean_date = re.sub(r"\([^)]*\)", "", date_str).strip()
                try:
                    # Parse date in format like "16Mar2009"
                    date_obj = datetime.strptime(clean_date, "%d%b%Y")
                    dates.append(date_obj)
                except ValueError:
                    raise ValueError(
                        f"Invalid date format: {date_str}. Expected format: DDMmmYYYY"
                    )

            if not dates:
                raise ValueError("At least one date must be provided")

            return customer_type, dates

        except Exception as e:
            raise ValueError(f"Failed to parse input '{input_str}': {str(e)}")

    def get_day_type(self, date: datetime) -> DayType:
        """
        Determine if a date is a weekday or weekend

        Args:
            date: Date to check

        Returns:
            DayType enum value
        """
        # weekday() returns 0-6 where 0=Monday, 6=Sunday
        # Saturday=5, Sunday=6 are weekends
        return DayType.WEEKEND if date.weekday() >= 5 else DayType.WEEKDAY

    def calculate_total_cost(
        self, hotel: Hotel, customer_type: CustomerType, dates: List[datetime]
    ) -> int:
        """
        Calculate total cost for a hotel given customer type and dates

        Args:
            hotel: Hotel object
            customer_type: Type of customer
            dates: List of dates for the stay

        Returns:
            Total cost for the stay
        """
        total_cost = 0
        for date in dates:
            day_type = self.get_day_type(date)
            rate = hotel.get_rate(customer_type, day_type)
            total_cost += rate
        return total_cost

    def find_cheapest_hotel(self, input_str: str) -> str:
        """
        Find the cheapest hotel for the given input

        Args:
            input_str: Input string in the required format

        Returns:
            Name of the cheapest hotel

        Raises:
            ValueError: If input is invalid
        """
        customer_type, dates = self.parse_input(input_str)

        hotel_costs = []
        for hotel in self.hotels:
            total_cost = self.calculate_total_cost(hotel, customer_type, dates)
            hotel_costs.append((hotel, total_cost))

        # Sort by cost (ascending), then by rating (descending) for tie-breaking
        hotel_costs.sort(key=lambda x: (x[1], -x[0].rating))

        cheapest_hotel = hotel_costs[0][0]
        return cheapest_hotel.name

    def get_detailed_analysis(self, input_str: str) -> Dict[str, Any]:
        """
        Get detailed cost analysis for all hotels

        Args:
            input_str: Input string in the required format

        Returns:
            Dictionary with detailed analysis
        """
        customer_type, dates = self.parse_input(input_str)

        analysis = {
            "customer_type": customer_type.value,
            "dates": [date.strftime("%d%b%Y") for date in dates],
            "hotels": [],
        }

        for hotel in self.hotels:
            total_cost = self.calculate_total_cost(hotel, customer_type, dates)
            daily_costs = []

            for date in dates:
                day_type = self.get_day_type(date)
                rate = hotel.get_rate(customer_type, day_type)
                daily_costs.append(
                    {
                        "date": date.strftime("%d%b%Y"),
                        "day_type": day_type.value,
                        "rate": rate,
                    }
                )

            analysis["hotels"].append(
                {
                    "name": hotel.name,
                    "rating": hotel.rating,
                    "total_cost": total_cost,
                    "daily_costs": daily_costs,
                }
            )

        # Sort by cost, then by rating for tie-breaking
        analysis["hotels"].sort(key=lambda x: (x["total_cost"], -x["rating"]))
        analysis["cheapest_hotel"] = analysis["hotels"][0]["name"]

        return analysis
