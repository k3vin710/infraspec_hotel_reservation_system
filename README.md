# Hotel Room Reservation System

A Python-based system to help online customers find the cheapest hotel from a chain of hotels in Miami. The system supports different customer types (Regular and Rewards) with special pricing and handles both weekday and weekend rates.

## 🏨 Features

- **Multiple Hotels**: Supports Lakewood, Bridgewood, and Ridgewood hotels with different ratings
- **Customer Types**: Regular and Rewards customers with different pricing tiers  
- **Dynamic Pricing**: Different rates for weekdays vs weekends
- **Smart Selection**: Cheapest hotel selection with tie-breaking by highest rating
- **Robust Input Parsing**: Flexible date format parsing with comprehensive error handling
- **Comprehensive Testing**: Full unit test coverage with edge cases and integration tests
- **Clean Architecture**: Object-oriented design with proper separation of concerns
- **Modern Tooling**: Built with UV, Black, Flake8, MyPy, and pytest
- **Interactive Demo**: Command-line demo showcasing all capabilities

## 🏢 Hotel Information

| Hotel | Rating | Weekday Regular | Weekday Rewards | Weekend Regular | Weekend Rewards |
|-------|--------|----------------|----------------|----------------|----------------|
| Lakewood | ⭐⭐⭐ | $110 | $80 | $90 | $80 |
| Bridgewood | ⭐⭐⭐⭐ | $160 | $110 | $60 | $50 |
| Ridgewood | ⭐⭐⭐⭐⭐ | $220 | $100 | $150 | $40 |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [UV](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/hotel-reservation-system.git
cd hotel-reservation-system

# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and setup development environment
uv sync --dev
uv pip install -e .

# Verify installation
make validate
```

### Basic Usage

```bash
# Run the main application with test cases
make run

# Try the interactive demo
uv run python scripts/run_demo.py

# Run tests
make test

# Run all quality checks
make check
```

## 📖 Usage

### Command Line Interface

```bash
# Run with UV
uv run hotel-reservation

# Run directly with Python
uv run python -m hotel_reservation.main
```

### Programmatic Usage

```python
from hotel_reservation import HotelReservationSystem

# Create system instance
system = HotelReservationSystem()

# Find cheapest hotel
result = system.find_cheapest_hotel("Regular: 16Mar2009, 17Mar2009, 18Mar2009")
print(result)  # Output: Lakewood

# Get detailed cost analysis
analysis = system.get_detailed_analysis("Rewards: 26Mar2009, 27Mar2009, 28Mar2009")
print(f"Cheapest hotel: {analysis['cheapest_hotel']}")
print(f"Customer type: {analysis['customer_type']}")

for hotel in analysis['hotels']:
    print(f"{hotel['name']} (Rating {hotel['rating']}): ${hotel['total_cost']}")
```

### Input Format

```
<CustomerType>: <date1>, <date2>, <date3>, ...
```

- **CustomerType**: `Regular` or `Rewards`
- **Date Format**: `DDMmmYYYY` (e.g., `16Mar2009`)
- **Optional**: Day of week in parentheses (e.g., `16Mar2009(mon)`)

### Examples

```python
# Valid input examples
"Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)"
"Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)"  
"Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)"
"Regular: 16Mar2009, 17Mar2009"  # Without day names
"Rewards: 21Mar2009"             # Single date
```

## 🧪 Test Cases

The system has been validated against the following test cases:

### Test Case 1: Regular Customer, Weekdays Only
- **Input**: `Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)`
- **Expected Output**: `Lakewood`
- **Reasoning**: 3 weekdays × $110 = $330 (cheapest option)

### Test Case 2: Regular Customer, Mixed Days
- **Input**: `Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)`
- **Expected Output**: `Bridgewood`
- **Cost Breakdown**:
  - Lakewood: $110 + $90 + $90 = $290
  - Bridgewood: $160 + $60 + $60 = $280 ✅ (cheapest)
  - Ridgewood: $220 + $150 + $150 = $520

### Test Case 3: Rewards Customer, Mixed Days
- **Input**: `Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)`
- **Expected Output**: `Ridgewood`
- **Cost Breakdown**:
  - Lakewood: $80 + $80 + $80 = $240
  - Bridgewood: $110 + $110 + $50 = $270
  - Ridgewood: $100 + $100 + $40 = $240 ✅ (tied cost, highest rating)

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
make dev-install

# Or manually with UV
uv sync --dev
uv pip install -e .
```

### Available Commands

```bash
# Testing
make test          # Run unit tests
make test-cov      # Run tests with coverage report
make validate      # Validate against expected outputs

# Code Quality
make format        # Format code with Black
make lint          # Lint code with Flake8
make type-check    # Type checking with MyPy
make check         # Run all quality checks

# Development
make run           # Run the application
make demo          # Run interactive demo
make clean         # Clean generated files
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_hotel_reservation.py

# Run specific test method
uv run pytest tests/test_hotel_reservation.py::TestHotel::test_hotel_creation

# Verbose output
uv run pytest -v -s
```

### Code Style

This project uses modern Python development practices:

- **Formatting**: [Black](https://black.readthedocs.io/) for consistent code formatting
- **Linting**: [Flake8](https://flake8.pycqa.org/) for style guide enforcement
- **Type Checking**: [MyPy](https://mypy.readthedocs.io/) for static type analysis
- **Testing**: [pytest](https://pytest.org/) with coverage reporting

```bash
# Format code
uv run black src tests

# Check linting
uv run flake8 src tests

# Type checking
uv run mypy src
```

## 🏗️ Architecture

### Project Structure

```
hotel-reservation-system/
├── src/hotel_reservation/    # Main package
│   ├── __init__.py          # Package exports
│   ├── models.py           # Data models (Hotel, CustomerType, DayType)
│   ├── system.py           # Core reservation logic
│   └── main.py             # CLI entry point and demo
├── tests/                   # Test suite
│   ├── __init__.py         # Test package initialization
│   └── test_hotel_reservation.py  # Comprehensive unit tests
├── scripts/                 # Utility scripts
│   └── run_demo.py         # Interactive demonstration
├── pyproject.toml          # Project configuration
├── Makefile               # Development automation
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

### Design Principles

- **Single Responsibility**: Each class has a clear, focused purpose
- **Open/Closed**: Easy to extend with new hotels or customer types
- **Dependency Inversion**: Core logic doesn't depend on external details
- **Error Handling**: Comprehensive validation and meaningful error messages
- **Type Safety**: Full type hints for better IDE support and error detection

### Key Components

#### Models (`models.py`)
- `Hotel`: Represents a hotel with pricing and rating information
- `CustomerType`: Enum for Regular/Rewards customer types
- `DayType`: Enum for weekday/weekend classification

#### System (`system.py`)
- `HotelReservationSystem`: Core business logic
  - Input parsing and validation
  - Cost calculation algorithms
  - Hotel selection with tie-breaking
  - Detailed analysis generation

#### Main (`main.py`)
- CLI interface and demonstration
- Test case validation
- User-friendly output formatting


## 📊 Performance

The system is optimized for performance:

- **O(n)** time complexity for cost calculations (where n = number of dates)
- **O(h log h)** for hotel selection (where h = number of hotels, typically 3)
- **Memory efficient**: Minimal object creation and reuse of data structures
- **Fast parsing**: Efficient regex-based date parsing

## 🔧 Configuration

### Adding New Hotels

```python
# In system.py, update the __init__ method
self.hotels = [
    Hotel("Lakewood", 3, 110, 80, 90, 80),
    Hotel("Bridgewood", 4, 160, 110, 60, 50),
    Hotel("Ridgewood", 5, 220, 100, 150, 40),
    Hotel("NewHotel", 4, 150, 100, 120, 90),  # Add new hotel
]
```

### Extending Customer Types

```python
# In models.py, extend the CustomerType enum
class CustomerType(Enum):
    REGULAR = "Regular"
    REWARDS = "Rewards"
    PREMIUM = "Premium"  # Add new customer type
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Fix: Install package in development mode
   uv pip install -e .
   ```

2. **Test Failures**
   ```bash
   # Check test environment
   uv run python -c "import hotel_reservation; print('✅ Package found')"
   
   # Run with verbose output
   uv run pytest -v -s
   ```

3. **UV Command Not Found**
   ```bash
   # Install UV
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Restart terminal
   ```

4. **Date Parsing Issues**
   - Ensure dates are in `DDMmmYYYY` format (e.g., `16Mar2009`)
   - Month abbreviations must be 3 letters with proper capitalization
   - Day of week in parentheses is optional

### Getting Help

- Check the [Issues](https://github.com/yourusername/hotel-reservation-system/issues) page
- Run the interactive demo: `uv run python scripts/run_demo.py`
- Review test cases in `tests/test_hotel_reservation.py`

## 🚀 Future Enhancements

The system is designed to be easily extensible. Potential future features:

### Part 2 Features
- **Blackout Dates**: Add date ranges where hotels are unavailable
- **Seasonal Pricing**: Different rate structures for different seasons
- **Room Types**: Multiple room categories (Standard, Deluxe, Suite)
- **Minimum Stay Requirements**: Enforce minimum night stays
- **Early Booking Discounts**: Time-based pricing incentives

### Advanced Features
- **Database Integration**: Persistent data storage
- **REST API**: Web service interface for online booking systems
- **Web UI**: Browser-based booking interface
- **Real-time Availability**: Dynamic inventory management
- **User Accounts**: Customer profiles and booking history
- **Payment Processing**: Integration with payment gateways
- **Notifications**: Email/SMS booking confirmations

### Technical Improvements
- **Caching**: Redis-based caching for improved performance
- **Logging**: Comprehensive application logging
- **Monitoring**: Application performance monitoring
- **Docker**: Containerization for easy deployment
- **API Documentation**: OpenAPI/Swagger documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run quality checks (`make check`)
6. Commit your changes (`git commit -m 'feat: add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Maintenance tasks
