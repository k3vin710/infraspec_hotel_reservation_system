#!/usr/bin/env python3
"""
Demo script for Hotel Reservation System

This script demonstrates the system with interactive examples
and additional test cases beyond the basic requirements.
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hotel_reservation.system import HotelReservationSystem
from hotel_reservation.models import CustomerType


def print_separator(title=""):
    """Print a nice separator line"""
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    else:
        print("=" * 60)


def demonstrate_basic_functionality():
    """Demonstrate the basic functionality with provided test cases"""
    print_separator("BASIC FUNCTIONALITY DEMO")
    
    system = HotelReservationSystem()
    
    test_cases = [
        ("Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)", "Lakewood"),
        ("Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)", "Bridgewood"),
        ("Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)", "Ridgewood")
    ]
    
    for i, (input_str, expected) in enumerate(test_cases, 1):
        print(f"\n🏨 Test Case {i}:")
        print(f"Input: {input_str}")
        
        try:
            result = system.find_cheapest_hotel(input_str)
            status = "✅ PASS" if result == expected else "❌ FAIL"
            
            print(f"Result: {result}")
            print(f"Expected: {expected}")
            print(f"Status: {status}")
            
            # Show detailed breakdown
            analysis = system.get_detailed_analysis(input_str)
            print(f"\n📊 Cost Breakdown:")
            for hotel_info in analysis['hotels']:
                print(f"  {hotel_info['name']} (⭐{hotel_info['rating']}): ${hotel_info['total_cost']}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")


def demonstrate_detailed_analysis():
    """Show detailed analysis capabilities"""
    print_separator("DETAILED ANALYSIS DEMO")
    
    system = HotelReservationSystem()
    input_str = "Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)"
    
    print(f"📋 Analyzing: {input_str}")
    
    try:
        analysis = system.get_detailed_analysis(input_str)
        
        print(f"\n👤 Customer Type: {analysis['customer_type']}")
        print(f"📅 Dates: {', '.join(analysis['dates'])}")
        print(f"🏆 Cheapest Hotel: {analysis['cheapest_hotel']}")
        
        print(f"\n📊 Detailed Cost Analysis:")
        for hotel_info in analysis['hotels']:
            print(f"\n🏨 {hotel_info['name']} (Rating: ⭐{hotel_info['rating']})")
            print(f"   Total Cost: ${hotel_info['total_cost']}")
            print(f"   Daily Breakdown:")
            for daily in hotel_info['daily_costs']:
                day_emoji = "📅" if daily['day_type'] == 'weekday' else "🌅"
                print(f"     {day_emoji} {daily['date']} ({daily['day_type']}): ${daily['rate']}")
                
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def demonstrate_edge_cases():
    """Demonstrate edge cases and error handling"""
    print_separator("EDGE CASES & ERROR HANDLING")
    
    system = HotelReservationSystem()
    
    edge_cases = [
        ("Single date", "Regular: 16Mar2009"),
        ("Weekend heavy", "Regular: 21Mar2009(sat), 22Mar2009(sun)"),
        ("Long stay", "Rewards: 16Mar2009, 17Mar2009, 18Mar2009, 19Mar2009, 20Mar2009"),
        ("Mixed format", "Regular: 16Mar2009(mon), 17Mar2009"),
    ]
    
    error_cases = [
        ("Invalid customer type", "Premium: 16Mar2009"),
        ("Invalid date format", "Regular: 2009-03-16"),
        ("Missing colon", "Regular 16Mar2009"),
        ("Empty dates", "Regular: "),
    ]
    
    print("✅ Valid Edge Cases:")
    for description, input_str in edge_cases:
        print(f"\n🔍 {description}:")
        print(f"   Input: {input_str}")
        try:
            result = system.find_cheapest_hotel(input_str)
            print(f"   Result: {result} ✅")
        except Exception as e:
            print(f"   Error: {str(e)} ❌")
    
    print(f"\n❌ Error Cases (Expected to Fail):")
    for description, input_str in error_cases:
        print(f"\n🔍 {description}:")
        print(f"   Input: {input_str}")
        try:
            result = system.find_cheapest_hotel(input_str)
            print(f"   Unexpected Success: {result} ⚠️")
        except Exception as e:
            print(f"   Expected Error: {str(e)} ✅")


def interactive_demo():
    """Allow user to input their own test cases"""
    print_separator("INTERACTIVE DEMO")
    
    system = HotelReservationSystem()
    
    print("🎮 Try your own inputs! (Enter 'quit' to exit)")
    print("Format: <CustomerType>: <date1>, <date2>, ...")
    print("Example: Regular: 16Mar2009, 17Mar2009")
    
    while True:
        try:
            user_input = input("\n💬 Enter your test case: ").strip()
            
            if user_input.lower() in ['quit', 'q', 'exit']:
                print("👋 Thanks for trying the demo!")
                break
                
            if not user_input:
                continue
                
            result = system.find_cheapest_hotel(user_input)
            analysis = system.get_detailed_analysis(user_input)
            
            print(f"🏆 Cheapest Hotel: {result}")
            print(f"📊 All Options:")
            for hotel_info in analysis['hotels']:
                print(f"   {hotel_info['name']} (⭐{hotel_info['rating']}): ${hotel_info['total_cost']}")
                
        except KeyboardInterrupt:
            print("\n👋 Thanks for trying the demo!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def show_hotel_info():
    """Display hotel information table"""
    print_separator("HOTEL INFORMATION")
    
    system = HotelReservationSystem()
    
    print("🏨 Miami Hotel Chain Information:")
    print()
    print("| Hotel      | Rating | Weekday Reg | Weekday Rew | Weekend Reg | Weekend Rew |")
    print("|------------|--------|-------------|-------------|-------------|-------------|")
    
    for hotel in system.hotels:
        print(f"| {hotel.name:<10} | ⭐{hotel.rating}    | ${hotel.weekday_regular:<10} | ${hotel.weekday_rewards:<10} | ${hotel.weekend_regular:<10} | ${hotel.weekend_rewards:<10} |")


def main():
    """Main demo function"""
    print("🏨 Hotel Reservation System - Interactive Demo")
    print("=" * 60)
    
    try:
        show_hotel_info()
        demonstrate_basic_functionality()
        demonstrate_detailed_analysis()
        demonstrate_edge_cases()
        
        # Ask if user wants interactive demo
        print_separator()
        response = input("Would you like to try the interactive demo? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_demo()
        else:
            print("👋 Demo completed! Thank you for trying the Hotel Reservation System.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying the Hotel Reservation System!")
    except Exception as e:
        print(f"\n❌ Unexpected error in demo: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())