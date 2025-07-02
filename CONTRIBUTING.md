# Contributing to Plugged.in Random Number Generator MCP (Python)

We welcome contributions to the Plugged.in Random Number Generator MCP Python implementation! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pluggedin-random-number-generator-mcp-python.git
   cd pluggedin-random-number-generator-mcp-python
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Development Process

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure the code follows our standards:
   ```bash
   # Format code
   black src/ tests/
   
   # Lint code
   ruff src/ tests/
   
   # Type check
   mypy src/
   ```

3. Run the tests to ensure everything works:
   ```bash
   python tests/test_server.py
   # Or use pytest
   pytest
   ```

4. Commit your changes with a clear message:
   ```bash
   git commit -m "Add: brief description of changes"
   ```

## Code Standards

- Use Python 3.8+ features appropriately
- Follow PEP 8 style guide (enforced by Black and Ruff)
- Use type hints for all function signatures
- Ensure all random generation uses cryptographically secure methods (`secrets` module)
- Add appropriate error handling and validation
- Document any new tools or significant changes with docstrings

## Testing

- All new features must include tests
- Tests should cover both success and error cases
- Use `pytest` for unit tests when appropriate
- Run `python tests/test_server.py` for integration tests
- Ensure all existing tests pass
- Aim for high test coverage

## Code Quality Tools

We use several tools to maintain code quality:

```bash
# Format code
black src/ tests/

# Lint code
ruff src/ tests/

# Type checking
mypy src/

# Run all checks
black src/ tests/ && ruff src/ tests/ && mypy src/
```

## Submitting Changes

1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request on GitHub
3. Describe your changes clearly in the PR description
4. Link any related issues
5. Ensure all CI checks pass

## Reporting Issues

- Use the GitHub issue tracker
- Include clear reproduction steps
- Provide system information (Python version, OS)
- Include any relevant error messages
- For bugs, provide minimal reproducible examples

## Security

- Never commit secrets or API keys
- Report security vulnerabilities privately to the maintainers at cem@plugged.in
- Use only cryptographically secure random generation (Python `secrets` module)
- Follow OWASP secure coding practices

## Development Tips

### Running with Docker

```bash
# Build the Docker image
docker build -t mcp-python .

# Run tests in Docker
docker-compose --profile test up

# Development environment
docker-compose --profile dev up
```

### Using uvx for testing

```bash
# Run without installation
uvx pluggedin-random-number-generator-mcp-python
```

### Building for distribution

```bash
# Build wheel and source distribution
python -m build

# Check distribution
twine check dist/*
```

## Questions?

Feel free to open an issue for any questions about contributing!