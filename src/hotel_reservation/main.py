#!/usr/bin/env python3
"""
Hotel Room Reservation System - Main Entry Point

A system to find the cheapest hotel for given dates and customer type.
Supports regular and rewards customers with different pricing tiers.
"""

from .system import HotelReservationSystem


def main():
    """Main function to demonstrate the system"""
    system = HotelReservationSystem()
    
    # Test cases from the problem statement
    test_cases = [
        "Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)",
        "Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)",
        "Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)"
    ]
    
    expected_outputs = ["Lakewood", "Bridgewood", "Ridgewood"]
    
    print("Hotel Reservation System")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            result = system.find_cheapest_hotel(test_case)
            expected = expected_outputs[i-1]
            status = "✓" if result == expected else "✗"
            
            print(f"\nTEST {i}: {status}")
            print(f"Input:    {test_case}")
            print(f"Output:   {result}")
            print(f"Expected: {expected}")
            
            # Show detailed analysis
            analysis = system.get_detailed_analysis(test_case)
            print(f"Customer: {analysis['customer_type']}")
            print(f"Dates:    {', '.join(analysis['dates'])}")
            print("\nCost Breakdown:")
            for hotel_info in analysis['hotels']:
                print(f"  {hotel_info['name']} (Rating {hotel_info['rating']}): ${hotel_info['total_cost']}")
            
        except Exception as e:
            print(f"\nTEST {i}: ✗")
            print(f"Input:  {test_case}")
            print(f"Error:  {str(e)}")


if __name__ == "__main__":
    main()