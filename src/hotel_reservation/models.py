from dataclasses import dataclass
from enum import Enum


class CustomerType(Enum):
    """Enum for customer types"""
    REGULAR = "Regular"
    REWARDS = "Rewards"


class DayType(Enum):
    """Enum for day types"""
    WEEKDAY = "weekday"
    WEEKEND = "weekend"


@dataclass
class Hotel:
    """Represents a hotel with its pricing and rating information"""
    name: str
    rating: int
    weekday_regular: int
    weekday_rewards: int
    weekend_regular: int
    weekend_rewards: int

    def get_rate(self, customer_type: CustomerType, day_type: DayType) -> int:
        """Get the rate for a specific customer type and day type"""
        if customer_type == CustomerType.REGULAR:
            return self.weekday_regular if day_type == DayType.WEEKDAY else self.weekend_regular
        else:  # REWARDS
            return self.weekday_rewards if day_type == DayType.WEEKDAY else self.weekend_rewards