# Makefile for Hotel Reservation System with UV

.PHONY: all install test lint format type-check run clean dev-install help validate ci

# Default target
all: install test lint

# Install dependencies
install:
	@echo "Installing dependencies with UV..."
	uv sync

# Install with development dependencies  
dev-install:
	@echo "Installing development dependencies with UV..."
	uv sync --dev

# Run tests
test:
	@echo "Running tests..."
	uv run pytest -v

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	uv run pytest --cov --cov-report=html --cov-report=term

# Lint code
lint:
	@echo "Linting code..."
	uv run flake8 src tests

# Format code
format:
	@echo "Formatting code..."
	uv run black src tests

# Type checking
type-check:
	@echo "Running type checks..."
	uv run mypy src

# Run all quality checks
check: format lint type-check test

# Run the application
run:
	@echo "Running hotel reservation system..."
	uv run hotel-reservation

# Run the application directly with Python
run-python:
	@echo "Running hotel reservation system with Python..."
	uv run python -m hotel_reservation.main

# Clean generated files
clean:
	@echo "Cleaning up generated files..."
	rm -rf .pytest_cache/ htmlcov/ .coverage .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Development setup
setup-dev: dev-install
	@echo "Development environment ready!"
	@echo "Available commands:"
	@echo "  make test      - Run tests"
	@echo "  make test-cov  - Run tests with coverage"
	@echo "  make lint      - Lint code"
	@echo "  make format    - Format code"
	@echo "  make check     - Run all quality checks"
	@echo "  make run       - Run the application"

# Validate that the system works with all test cases
validate: test
	@echo ""
	@echo "Validation Test - Running all provided test cases:"
	@echo "================================================="
	@uv run python -c "
import sys
sys.path.insert(0, 'src')
from hotel_reservation.system import HotelReservationSystem

system = HotelReservationSystem()
test_cases = [
    ('Regular: 16Mar2009(mon), 17Mar2009(tues), 18Mar2009(wed)', 'Lakewood'),
    ('Regular: 20Mar2009(fri), 21Mar2009(sat), 22Mar2009(sun)', 'Bridgewood'),
    ('Rewards: 26Mar2009(thur), 27Mar2009(fri), 28Mar2009(sat)', 'Ridgewood')
]

all_passed = True
for i, (input_str, expected) in enumerate(test_cases, 1):
    try:
        result = system.find_cheapest_hotel(input_str)
        status = '✓ PASS' if result == expected else '✗ FAIL'
        if result != expected:
            all_passed = False
        print(f'Test {i}: {status}')
        print(f'  Input:    {input_str}')
        print(f'  Expected: {expected}')
        print(f'  Got:      {result}')
        print()
    except Exception as e:
        print(f'Test {i}: ✗ ERROR - {str(e)}')
        all_passed = False

if all_passed:
    print('All validation tests passed! ✓')
    sys.exit(0)
else:
    print('Some validation tests failed! ✗')
    sys.exit(1)
"

# Continuous Integration target
ci: dev-install format lint type-check test validate
	@echo "All CI checks passed! ✓"

# Build distribution packages
build:
	@echo "Building distribution packages..."
	uv build

# Install the package in development mode
install-dev:
	@echo "Installing package in development mode..."
	uv pip install -e .

# Create a new UV project (for reference)
init-project:
	@echo "This would initialize a new UV project:"
	@echo "uv init hotel-reservation-system"
	@echo "cd hotel-reservation-system"

# Help target
help:
	@echo "Hotel Reservation System - Available Make Targets:"
	@echo "=================================================="
	@echo ""
	@echo "Setup:"
	@echo "  install       - Install dependencies"
	@echo "  dev-install   - Install with development dependencies"
	@echo "  setup-dev     - Complete development environment setup"
	@echo ""
	@echo "Development:"
	@echo "  test          - Run unit tests"
	@echo "  test-cov      - Run tests with coverage report"
	@echo "  lint          - Run code linting"
	@echo "  format        - Format code with black"
	@echo "  type-check    - Run type checking with mypy"
	@echo "  check         - Run all quality checks (format, lint, type-check, test)"
	@echo ""
	@echo "Execution:"
	@echo "  run           - Run the application using UV"
	@echo "  run-python    - Run the application directly with Python"
	@echo "  validate      - Run validation tests with expected outputs"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean         - Clean up generated files"
	@echo "  build         - Build distribution packages"
	@echo "  ci            - Run all CI checks"
	@echo ""
	@echo "Info:"
	@echo "  help          - Show this help message"

# Show project status
status:
	@echo "Project Status:"
	@echo "==============="
	@echo "Python version: $$(python3 --version)"
	@echo "UV version: $$(uv --version)"
	@echo "Project structure:"
	@tree -I '__pycache__|*.pyc|.pytest_cache|htmlcov|.coverage|.mypy_cache' || ls -la