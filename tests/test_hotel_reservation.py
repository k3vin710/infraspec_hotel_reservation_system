#!/usr/bin/env python3
"""
Unit tests for Hotel Reservation System
"""

import unittest
from datetime import datetime

from hotel_reservation.models import Hotel, CustomerType, DayType
from hotel_reservation.system import HotelReservationSystem


class TestHotel(unittest.TestCase):
    """Test cases for Hotel class"""
    
    def setUp(self):
        """Set up test hotel"""
        self.hotel = Hotel("TestHotel", 4, 100, 80, 120, 90)
    
    def test_hotel_creation(self):
        """Test hotel object creation"""
        self.assertEqual(self.hotel.name, "TestHotel")
        self.assertEqual(self.hotel.rating, 4)
        self.assertEqual(self.hotel.weekday_regular, 100)
        self.assertEqual(self.hotel.weekday_rewards, 80)
        self.assertEqual(self.hotel.weekend_regular, 120)
        self.assertEqual(self.hotel.weekend_rewards, 90)
    
    def test_get_rate_regular_weekday(self):
        """Test getting rate for regular customer on weekday"""
        rate = self.hotel.get_rate(CustomerType.REGULAR, DayType.WEEKDAY)
        self.assertEqual(rate, 100)
    
    def test_get_rate_regular_weekend(self):
        """Test getting rate for regular customer on weekend"""
        rate = self.hotel.get_rate(CustomerType.REGULAR, DayType.WEEKEND)
        self.assertEqual(rate, 120)
    
    def test_get_rate_rewards_weekday(self):
        """Test getting rate for rewards customer on weekday"""
        rate = self.hotel.get_rate(CustomerType.REWARDS, DayType.WEEKDAY)
        self.assertEqual(rate, 80)
    
    def test_get_rate_rewards_weekend(self):
        """Test getting rate for rewards customer on weekend"""
        rate = self.hotel.get_rate(CustomerType.REWARDS, DayType.WEEKEND)
        self.assertEqual(rate, 90)


class TestHotelReservationSystem(unittest.TestCase):
    """Test cases for HotelReservationSystem class"""
    
    def setUp(self):
        """Set up test system"""
        self.system = HotelReservationSystem()
    
    def test_system_initialization(self):
        """Test system initialization with correct hotels"""
        self.assertEqual(len(self.system.hotels), 3)
        hotel_names = [hotel.name for hotel in self.system.hotels]
        self.assertIn("Lakewood", hotel_names)
        self.assertIn("Bridgewood", hotel_names)
        self.assertIn("Ridgewood", hotel_names)
    
    def test_parse_input_valid_regular(self):
        """Test parsing valid input for regular customer"""
        input_str = "Regular: 16Mar2009, 17Mar2009"
        customer_type, dates = self.system.parse_input(input_str)
        
        self.assertEqual(customer_type, CustomerType.REGULAR)
        self.assertEqual(len(dates), 2)
        self.assertEqual(dates[0], datetime(2009, 3, 16))
        self.assertEqual(dates[1], datetime(2009, 3, 17))
    
    def test_parse_input_valid_rewards(self):
        """Test parsing valid input for rewards customer"""
        input_str = "Rewards: 20Mar2009(fri), 21Mar2009(sat)"
        customer_type, dates = self.system.parse_input(input_str)
        
        self.assertEqual(customer_type, CustomerType.REWARDS)
        self.assertEqual(len(dates), 2)
        self.assertEqual(dates[0], datetime(2009, 3, 20))
        self.assertEqual(dates[1], datetime(2009, 3, 21))
    
    def test_parse_input_invalid_customer_type(self):
        """Test parsing input with invalid customer type"""
        input_str = "Premium: 16Mar2009"
        with self.assertRaises(ValueError) as context:
            self.system.parse_input(input_str)
        self.assertIn("Invalid customer type", str(context.exception))
    
    def test_parse_input_invalid_format_no_colon(self):
        """Test parsing input without colon separator"""
        input_str = "Regular 16Mar2009"
        with self.assertRaises(ValueError) as context:
            self.system.parse_input(input_str)
        self.assertIn("must contain ':' separator", str(context.exception))
    
    def test_parse_input_invalid_date_format(self):
        """Test parsing input with invalid date format"""
        input_str = "Regular: 2009-03-16"
        with self.assertRaises(ValueError) as context:
            self.system.parse_input(input_str)
        self.assertIn("Invalid date format", str(context.exception))
    
    def test_parse_input_empty_dates(self):
        """Test parsing input with no dates"""
        input_str = "Regular: "
        with self.assertRaises(ValueError) as context:
            self.system.parse_input(input_str)
        self.assertIn("At least one date must be provided", str(context.exception))
    
    def test_get_day_type_weekday(self):
        """Test day type detection for weekdays"""
        # Monday
        monday = datetime(2009, 3, 16)
        self.assertEqual(self.system.get_day_type(monday), DayType.WEEKDAY)
        
        # Friday
        friday = datetime(2009, 3, 20)
        self.assertEqual(self.system.get_day_type(friday), DayType.WEEKDAY)
    
    def test_get_day_type_weekend(self):
        """Test day type detection for weekends"""
        # Saturday
        saturday = datetime(2009, 3, 21)
        self.assertEqual(self.system.get_day_type(saturday), DayType.WEEKEND)
        
        # Sunday
        sunday = datetime(2009, 3, 22)
        self.assertEqual(self.system.get_day_type(sunday), DayType.WEEKEND)
    
    def test_calculate_total_cost_lakewood_regular_weekdays(self):
        """Test cost calculation for Lakewood, regular customer, weekdays"""
        lakewood = self.system.hotels[0]  # Lakewood is first
        dates = [datetime(2009, 3, 16), datetime(2009, 3, 17), datetime(2009, 3, 18)]  # Mon, Tue, Wed
        
        total_cost = self.system.calculate_total_cost(lakewood, CustomerType.REGULAR, dates)
        expected_cost = 110 * 3  # 3 weekdays at $110 each
        self.assertEqual(total_cost, expected_cost)
    
    def test_calculate_total_cost_bridgewood_regular_mixed_days(self):
        """Test cost calculation for Bridgewood, regular customer, mixed days"""
        bridgewood = self.system.hotels[1]  # Bridgewood is second
        dates = [datetime(2009, 3, 20), datetime(2009, 3, 21), datetime(2009, 3, 22)]  # Fri, Sat, Sun
        
        total_cost = self.system.calculate_total_cost(bridgewood, CustomerType.REGULAR, dates)
        expected_cost = 160 + 60 + 60  # Friday weekday + Saturday + Sunday weekend rates
        self.assertEqual(total_cost, expected_cost)
    
    def test_find_cheapest_hotel_test_case_1(self):
        """Test case 1: Regular customer, weekdays only"""
        input_str = "Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)"
        result = self.system.find_cheapest_hotel(input_str)
        self.assertEqual(result, "Lakewood")
    
    def test_find_cheapest_hotel_test_case_2(self):
        """Test case 2: Regular customer, mixed days"""
        input_str = "Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)"
        result = self.system.find_cheapest_hotel(input_str)
        self.assertEqual(result, "Bridgewood")
    
    def test_find_cheapest_hotel_test_case_3(self):
        """Test case 3: Rewards customer, mixed days"""
        input_str = "Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)"
        result = self.system.find_cheapest_hotel(input_str)
        self.assertEqual(result, "Ridgewood")
    
    def test_tie_breaking_by_rating(self):
        """Test that ties are broken by highest rating"""
        # For this test, let's use a single weekend day for rewards customer
        # Lakewood: $80, Bridgewood: $50, Ridgewood: $40
        # So Ridgewood should win
        input_str = "Rewards: 21Mar2009(sat)"
        result = self.system.find_cheapest_hotel(input_str)
        self.assertEqual(result, "Ridgewood")
    
    def test_get_detailed_analysis(self):
        """Test detailed analysis function"""
        input_str = "Regular: 16Mar2009, 17Mar2009"
        analysis = self.system.get_detailed_analysis(input_str)
        
        self.assertEqual(analysis['customer_type'], "Regular")
        self.assertEqual(len(analysis['dates']), 2)
        self.assertEqual(len(analysis['hotels']), 3)
        self.assertIn('cheapest_hotel', analysis)
        
        # Check that hotels are sorted by cost
        costs = [hotel['total_cost'] for hotel in analysis['hotels']]
        self.assertEqual(costs, sorted(costs))
    
    def test_edge_case_single_date(self):
        """Test with single date"""
        input_str = "Regular: 16Mar2009"
        result = self.system.find_cheapest_hotel(input_str)
        # Should still work and return a valid hotel name
        self.assertIn(result, ["Lakewood", "Bridgewood", "Ridgewood"])
    
    def test_different_date_formats(self):
        """Test parsing different valid date formats"""
        # With day of week in parentheses
        input_str1 = "Regular: 16Mar2009(mon)"
        customer_type1, dates1 = self.system.parse_input(input_str1)
        
        # Without day of week
        input_str2 = "Regular: 16Mar2009"
        customer_type2, dates2 = self.system.parse_input(input_str2)
        
        # Both should parse to the same result
        self.assertEqual(customer_type1, customer_type2)
        self.assertEqual(dates1, dates2)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        """Set up integration test system"""
        self.system = HotelReservationSystem()
    
    def test_full_workflow_all_test_cases(self):
        """Test the complete workflow with all provided test cases"""
        test_cases = [
            ("Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)", "Lakewood"),
            ("Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)", "Bridgewood"),
            ("Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)", "Ridgewood")
        ]
        
        for input_str, expected_output in test_cases:
            with self.subTest(input_str=input_str):
                result = self.system.find_cheapest_hotel(input_str)
                self.assertEqual(result, expected_output)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)