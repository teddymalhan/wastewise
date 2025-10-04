#!/bin/bash
# Test runner script for WasteWise backend
# This script makes it easy to run tests with various options

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Change to backend directory if not already there
if [ ! -f "pytest.ini" ]; then
    if [ -d "backend" ]; then
        cd backend
        print_info "Changed to backend directory"
    else
        print_error "Cannot find pytest.ini or backend directory"
        exit 1
    fi
fi

# Parse command line arguments
case "${1:-all}" in
    "all")
        print_info "Running all tests with coverage..."
        pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=xml -v
        print_info "Coverage report generated in htmlcov/index.html"
        ;;
    
    "quick")
        print_info "Running all tests without coverage..."
        pytest -v
        ;;
    
    "coverage")
        print_info "Running tests and opening HTML coverage report..."
        pytest --cov=. --cov-report=html --cov-report=term
        
        # Try to open the HTML report
        if [ -f "htmlcov/index.html" ]; then
            if command -v open &> /dev/null; then
                open htmlcov/index.html
            elif command -v xdg-open &> /dev/null; then
                xdg-open htmlcov/index.html
            else
                print_warning "Please open htmlcov/index.html manually"
            fi
        fi
        ;;
    
    "unit")
        print_info "Running only unit tests..."
        pytest -m unit -v
        ;;
    
    "file")
        if [ -z "$2" ]; then
            print_error "Please specify a test file"
            print_info "Usage: ./run_tests.sh file <test_file_name>"
            exit 1
        fi
        print_info "Running tests in test/$2..."
        pytest "test/$2" -v
        ;;
    
    "watch")
        print_info "Running tests in watch mode (requires pytest-watch)..."
        if command -v ptw &> /dev/null; then
            ptw -- --cov=. --cov-report=term-missing
        else
            print_error "pytest-watch not installed. Install with: pip install pytest-watch"
            exit 1
        fi
        ;;
    
    "install")
        print_info "Installing test dependencies..."
        pip install -r requirements.txt
        print_info "Dependencies installed successfully"
        ;;
    
    "clean")
        print_info "Cleaning test artifacts..."
        rm -rf .pytest_cache htmlcov .coverage coverage.xml
        find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
        print_info "Cleaned test artifacts"
        ;;
    
    "ci")
        print_info "Running tests in CI mode..."
        pytest --cov=. --cov-report=xml --cov-report=term --cov-fail-under=95
        print_info "CI tests completed"
        ;;
    
    "help"|"--help"|"-h")
        echo "WasteWise Test Runner"
        echo ""
        echo "Usage: ./run_tests.sh [command]"
        echo ""
        echo "Commands:"
        echo "  all       - Run all tests with coverage (default)"
        echo "  quick     - Run all tests without coverage"
        echo "  coverage  - Run tests and open HTML coverage report"
        echo "  unit      - Run only unit tests"
        echo "  file      - Run tests in a specific file (usage: ./run_tests.sh file test_main.py)"
        echo "  watch     - Run tests in watch mode (requires pytest-watch)"
        echo "  install   - Install test dependencies"
        echo "  clean     - Clean test artifacts and cache"
        echo "  ci        - Run tests in CI mode with coverage threshold"
        echo "  help      - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh                    # Run all tests with coverage"
        echo "  ./run_tests.sh quick              # Quick test run"
        echo "  ./run_tests.sh file test_main.py  # Test specific file"
        echo "  ./run_tests.sh coverage           # Generate and view coverage"
        ;;
    
    *)
        print_error "Unknown command: $1"
        print_info "Run './run_tests.sh help' for usage information"
        exit 1
        ;;
esac

exit 0
