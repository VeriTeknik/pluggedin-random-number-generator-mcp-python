#!/bin/bash

# PyPI Publishing Script
# This script builds and publishes the package to PyPI

set -e  # Exit on error

echo "🚀 Starting PyPI publishing process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found. Are you in the project root?"
    exit 1
fi

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Run tests first
print_status "Running tests..."
python tests/test_server.py || {
    print_error "Tests failed! Fix them before publishing."
    exit 1
}

# Run code quality checks
print_status "Running code quality checks..."

# Format check
if command -v black &> /dev/null; then
    print_status "Checking code formatting with Black..."
    black --check src/ tests/ || {
        print_warning "Code formatting issues found. Run 'black src/ tests/' to fix."
    }
fi

# Lint check
if command -v ruff &> /dev/null; then
    print_status "Linting with Ruff..."
    ruff src/ tests/ || {
        print_warning "Linting issues found. Fix them or add appropriate ignores."
    }
fi

# Type check
if command -v mypy &> /dev/null; then
    print_status "Type checking with mypy..."
    mypy src/ || {
        print_warning "Type checking issues found. Consider fixing them."
    }
fi

# Build the package
print_status "Building distribution packages..."
python -m build || {
    print_error "Build failed!"
    exit 1
}

# Check the distribution
print_status "Checking distribution with twine..."
twine check dist/* || {
    print_error "Distribution check failed!"
    exit 1
}

# Show what will be uploaded
print_status "Files to be uploaded:"
ls -la dist/

# Ask for confirmation
echo ""
read -p "Do you want to upload to PyPI? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if TEST_PYPI is set to upload to test PyPI first
    if [ "${TEST_PYPI}" = "1" ]; then
        print_warning "Uploading to Test PyPI first..."
        twine upload --repository testpypi dist/* || {
            print_error "Test PyPI upload failed!"
            exit 1
        }
        print_status "Test PyPI upload successful!"
        print_status "Test with: pip install -i https://test.pypi.org/simple/ pluggedin-random-number-generator-mcp-python"
        
        echo ""
        read -p "Continue with production PyPI upload? (y/N) " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_warning "Production upload cancelled."
            exit 0
        fi
    fi
    
    # Upload to PyPI
    print_status "Uploading to PyPI..."
    twine upload dist/* || {
        print_error "PyPI upload failed!"
        exit 1
    }
    
    print_status "🎉 Successfully published to PyPI!"
    print_status "Install with: pip install pluggedin-random-number-generator-mcp-python"
    print_status "Or run with: uvx pluggedin-random-number-generator-mcp-python"
else
    print_warning "Upload cancelled."
fi