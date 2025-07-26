"""
Test package for Hotel Reservation System

This package contains comprehensive unit tests, integration tests,
and validation tests for the hotel reservation system.

Test Structure:
- TestHotel: Tests for the Hotel model class
- TestHotelReservationSystem: Tests for the core system logic
- TestIntegration: End-to-end integration tests

Coverage includes:
- Model validation and data integrity
- Input parsing and error handling
- Cost calculation algorithms
- Hotel selection logic with tie-breaking
- Edge cases and boundary conditions
- Integration workflows

Usage:
    # Run all tests
    pytest tests/
    
    # Run with coverage
    pytest --cov=hotel_reservation tests/
    
    # Run specific test class
    pytest tests/test_hotel_reservation.py::TestHotel
    
    # Run with verbose output
    pytest -v tests/
"""

import sys
from pathlib import Path

# Ensure the src directory is in the Python path for testing
# This helps with import resolution in development environments
project_root = Path(__file__).parent.parent
src_path = project_root / "src"

if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Test configuration constants
TEST_DATA_DIR = Path(__file__).parent / "data"
FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Common test utilities and fixtures can be defined here
class TestConstants:
    """Constants used across multiple test modules"""
    
    # Sample valid inputs for testing
    VALID_INPUTS = [
        "Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)",
        "Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)",
        "Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)",
        "Regular: 16Mar2009",  # Single date
        "Rewards: 21Mar2009(sat), 22Mar2009(sun)",  # Weekend only
    ]
    
    # Sample invalid inputs for error testing
    INVALID_INPUTS = [
        "Premium: 16Mar2009",  # Invalid customer type
        "Regular: 2009-03-16",  # Invalid date format
        "Regular 16Mar2009",  # Missing colon
        "Regular: ",  # Empty dates
        ": 16Mar2009",  # Missing customer type
        "Regular: 32Mar2009",  # Invalid date
        "Regular: 16Mar2025",  # Future date (could be valid depending on requirements)
    ]
    
    # Expected outputs for test validation
    EXPECTED_OUTPUTS = {
        "Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)": "Lakewood",
        "Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)": "Bridgewood",
        "Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)": "Ridgewood",
    }
    
    # Hotel information for validation
    HOTEL_INFO = {
        "Lakewood": {"rating": 3, "weekday_regular": 110, "weekday_rewards": 80, "weekend_regular": 90, "weekend_rewards": 80},
        "Bridgewood": {"rating": 4, "weekday_regular": 160, "weekday_rewards": 110, "weekend_regular": 60, "weekend_rewards": 50},
        "Ridgewood": {"rating": 5, "weekday_regular": 220, "weekday_rewards": 100, "weekend_regular": 150, "weekend_rewards": 40},
    }


def setup_test_environment():
    """
    Setup function that can be called to prepare the test environment.
    This could include creating test data, setting up mock objects, etc.
    """
    # Create test data directories if they don't exist
    TEST_DATA_DIR.mkdir(exist_ok=True)
    FIXTURES_DIR.mkdir(exist_ok=True)
    
    # Any other test environment setup can go here
    pass


def teardown_test_environment():
    """
    Cleanup function for test environment.
    This could include removing temporary files, clearing caches, etc.
    """
    # Cleanup operations can go here
    pass


# Test utilities that can be imported by test modules
class TestUtils:
    """Utility functions for testing"""
    
    @staticmethod
    def validate_hotel_structure(hotel_data):
        """
        Validate that hotel data has the expected structure
        
        Args:
            hotel_data: Dictionary containing hotel information
            
        Returns:
            bool: True if structure is valid
        """
        required_fields = ['name', 'rating', 'total_cost', 'daily_costs']
        return all(field in hotel_data for field in required_fields)
    
    @staticmethod
    def calculate_expected_cost(hotel_name, customer_type, dates):
        """
        Calculate expected cost for validation in tests
        
        Args:
            hotel_name: Name of the hotel
            customer_type: Type of customer ('Regular' or 'Rewards')
            dates: List of date strings
            
        Returns:
            int: Expected total cost
        """
        from datetime import datetime
        
        hotel_info = TestConstants.HOTEL_INFO[hotel_name]
        total_cost = 0
        
        for date_str in dates:
            # Parse date to determine if it's weekend
            date_obj = datetime.strptime(date_str, '%d%b%Y')
            is_weekend = date_obj.weekday() >= 5  # Saturday=5, Sunday=6
            
            # Get rate based on customer type and day type
            if customer_type == 'Regular':
                rate = hotel_info['weekend_regular'] if is_weekend else hotel_info['weekday_regular']
            else:  # Rewards
                rate = hotel_info['weekend_rewards'] if is_weekend else hotel_info['weekday_rewards']
            
            total_cost += rate
        
        return total_cost


# Initialize test environment when the module is imported
setup_test_environment()

# Export commonly used test components
__all__ = [
    'TestConstants',
    'TestUtils',
    'setup_test_environment',
    'teardown_test_environment',
    'TEST_DATA_DIR',
    'FIXTURES_DIR',
]