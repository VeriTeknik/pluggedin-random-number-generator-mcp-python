# Plugged.in Random Number Generator MCP Server (Python)

A state-of-the-art cryptographically secure random number generator server implementing the Model Context Protocol (MCP). This Python implementation provides advanced random number generation capabilities for AI applications, LLMs, and other systems requiring high-quality randomness.

## 🚀 Features

- **Cryptographically Secure**: Uses Python's built-in `secrets` module and `os.urandom()` for cryptographically secure pseudorandom number generation (CSPRNG)
- **Multiple Data Types**: Generate integers, floats, bytes, UUIDs, strings, booleans, and random choices
- **Flexible Configuration**: Customizable ranges, counts, encodings, and character sets
- **MCP Compliant**: Full compatibility with Model Context Protocol specification
- **Type Safety**: Written with comprehensive type hints and strict type checking
- **Error Handling**: Robust input validation and error reporting
- **Performance Optimized**: Efficient algorithms suitable for high-throughput applications
- **Async Support**: Built with FastMCP for efficient async operations

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip or uv package manager

### Install with uvx (Recommended for Claude Desktop)

For Claude Desktop users, you can run this server without installation using uvx:

```bash
# Run directly with uvx
uvx pluggedin-random-number-generator-mcp-python
```

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "random-generator-python": {
      "command": "uvx",
      "args": ["pluggedin-random-number-generator-mcp-python"]
    }
  }
}
```

### Install from PyPI

```bash
pip install pluggedin-random-number-generator-mcp-python
```

Or install globally with pipx:

```bash
pipx install pluggedin-random-number-generator-mcp-python
```

### Install from Source

```bash
git clone https://github.com/VeriTeknik/pluggedin-random-number-generator-mcp-python.git
cd pluggedin-random-number-generator-mcp-python
pip install -e .

# For development
pip install -e ".[dev]"
```

### Deploy with Docker

Multiple Docker configurations are available:

```bash
# Standard Python image
docker build -t mcp-random-python .
docker run --rm -i mcp-random-python

# Alpine Linux (lightweight)
docker build -f Dockerfile.alpine -t mcp-random-python:alpine .

# Minimal distroless image
docker build -f Dockerfile.minimal -t mcp-random-python:minimal .

# Using docker-compose
docker-compose up mcp-server
```

### Deploy with Smithery

Deploy this MCP server to the cloud using [Smithery](https://smithery.ai/):

1. Fork this repository
2. Connect your GitHub account to Smithery
3. Navigate to the Deployments tab
4. Click "Deploy"

The server includes a `smithery.yaml` configuration file for easy deployment.

## 🛠️ Usage

### Running the Server

The server communicates via stdio (standard input/output) following the MCP protocol:

```bash
# Using the installed command
pluggedin-random-number-generator-mcp-python

# Using Python module
python -m pluggedin_random_number_generator_mcp.server

# Development mode
python src/pluggedin_random_number_generator_mcp/server.py
```

### Integration with MCP Clients

#### For uvx installation (recommended):

```json
{
  "mcpServers": {
    "random-generator-python": {
      "command": "uvx",
      "args": ["pluggedin-random-number-generator-mcp-python"]
    }
  }
}
```

#### For pip/pipx installation:

```json
{
  "mcpServers": {
    "random-generator-python": {
      "command": "pluggedin-random-number-generator-mcp-python"
    }
  }
}
```

## 🔧 Available Tools

### 1. Generate Random Integers

Generate cryptographically secure random integers within a specified range.

**Parameters:**
- `min` (integer, optional): Minimum value (inclusive), default: 0
- `max` (integer, optional): Maximum value (inclusive), default: 100  
- `count` (integer, optional): Number of integers to generate, default: 1, max: 1000

**Example:**
```json
{
  "name": "generate_random_integer",
  "arguments": {
    "min": 1,
    "max": 100,
    "count": 5
  }
}
```

### 2. Generate Random Floats

Generate cryptographically secure random floating-point numbers.

**Parameters:**
- `min` (number, optional): Minimum value (inclusive), default: 0.0
- `max` (number, optional): Maximum value (exclusive), default: 1.0
- `count` (integer, optional): Number of floats to generate, default: 1, max: 1000
- `precision` (integer, optional): Decimal places to round to, default: 6, max: 15

**Example:**
```json
{
  "name": "generate_random_float", 
  "arguments": {
    "min": 0.0,
    "max": 1.0,
    "count": 3,
    "precision": 4
  }
}
```

### 3. Generate Random Bytes

Generate cryptographically secure random bytes in various encodings.

**Parameters:**
- `length` (integer, optional): Number of bytes to generate, default: 32, max: 1024
- `encoding` (string, optional): Output encoding ("hex", "base64"), default: "hex"

**Example:**
```json
{
  "name": "generate_random_bytes",
  "arguments": {
    "length": 32,
    "encoding": "hex"
  }
}
```

### 4. Generate UUIDs

Generate cryptographically secure UUID version 4 identifiers.

**Parameters:**
- `count` (integer, optional): Number of UUIDs to generate, default: 1, max: 100
- `format` (string, optional): UUID format ("standard", "compact"), default: "standard"

**Example:**
```json
{
  "name": "generate_uuid",
  "arguments": {
    "count": 3,
    "format": "standard"
  }
}
```

### 5. Generate Random Strings

Generate cryptographically secure random strings with customizable character sets.

**Parameters:**
- `length` (integer, optional): String length, default: 16, max: 256
- `charset` (string, optional): Character set ("alphanumeric", "alphabetic", "numeric", "hex", "base64", "ascii_printable"), default: "alphanumeric"
- `count` (integer, optional): Number of strings to generate, default: 1, max: 100

**Example:**
```json
{
  "name": "generate_random_string",
  "arguments": {
    "length": 12,
    "charset": "alphanumeric",
    "count": 2
  }
}
```

### 6. Generate Random Choices

Randomly select items from a provided list using cryptographically secure randomness.

**Parameters:**
- `choices` (array, required): Array of string items to choose from
- `count` (integer, optional): Number of items to select, default: 1
- `allow_duplicates` (boolean, optional): Whether to allow duplicate selections, default: true

**Example:**
```json
{
  "name": "generate_random_choice",
  "arguments": {
    "choices": ["apple", "banana", "cherry", "date"],
    "count": 2,
    "allow_duplicates": false
  }
}
```

### 7. Generate Random Booleans

Generate cryptographically secure random boolean values with configurable probability.

**Parameters:**
- `count` (integer, optional): Number of booleans to generate, default: 1, max: 1000
- `probability` (number, optional): Probability of true (0.0 to 1.0), default: 0.5

**Example:**
```json
{
  "name": "generate_random_boolean",
  "arguments": {
    "count": 10,
    "probability": 0.7
  }
}
```

## 🔒 Security Features

This server implements several security best practices:

- **Cryptographically Secure Randomness**: All random number generation uses Python's `secrets` module which provides access to the most secure source of randomness provided by the operating system.

- **Input Validation**: Comprehensive validation of all input parameters to prevent injection attacks and ensure data integrity.

- **Rate Limiting**: Built-in limits on generation counts to prevent resource exhaustion attacks.

- **Error Handling**: Secure error messages that don't leak sensitive information about the system state.

## 🧪 Testing

The server includes a comprehensive test suite that validates all functionality:

```bash
# Run the test suite
python tests/test_server.py

# Run with pytest (if installed)
pytest

# Run with coverage
pytest --cov=pluggedin_random_number_generator_mcp
```

The test suite covers:
- Tool discovery and listing
- All random generation functions
- Input validation and error handling
- Output format verification
- Statistical properties validation

## 📊 Performance

The server is optimized for performance while maintaining security:

- **Efficient Algorithms**: Uses optimized native Python functions
- **Memory Management**: Minimal memory footprint with efficient data handling
- **Async Operations**: Built with FastMCP for concurrent request handling
- **Scalability**: Suitable for high-throughput applications

## 🔧 Development

### Project Structure

```
pluggedin-random-number-generator-mcp-python/
├── src/
│   └── pluggedin_random_number_generator_mcp/
│       ├── __init__.py
│       └── server.py          # Main server implementation
├── tests/
│   └── test_server.py        # Comprehensive test suite
├── pyproject.toml           # Project configuration
├── Dockerfile              # Standard Docker image
├── Dockerfile.alpine       # Alpine Linux variant
├── Dockerfile.minimal      # Distroless variant
├── docker-compose.yml      # Docker compose configuration
└── README.md              # This documentation
```

### Development Setup

```bash
# Clone the repository
git clone https://github.com/VeriTeknik/pluggedin-random-number-generator-mcp-python.git
cd pluggedin-random-number-generator-mcp-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run code quality checks
black src/ tests/      # Format code
ruff src/ tests/      # Lint code
mypy src/            # Type checking
```

### Building

```bash
# Build distribution packages
python -m build

# Check distribution
twine check dist/*
```

### Testing with Docker

```bash
# Build and test
docker-compose --profile test up

# Development environment
docker-compose --profile dev up
```

### Using MCP Inspector

The MCP Inspector provides a web interface to interact with and test the server:

```bash
# Install MCP Inspector (if not already installed)
npm install -g @modelcontextprotocol/inspector

# Run inspector with the Python server
make inspector
```

The inspector will start on `http://localhost:5173` where you can:
- View available tools and prompts
- Test tool execution with different parameters
- Inspect request/response payloads
- Debug server behavior

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Follow PEP 8 and use Black for formatting
2. Add type hints to all functions
3. Maintain test coverage above 90%
4. Update documentation for new features
5. Ensure all tests pass before submitting
6. Follow semantic versioning for releases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Node.js/TypeScript Implementation](https://github.com/VeriTeknik/pluggedin-random-number-generator-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/) - The official MCP specification
- [Plugged.in](https://plugged.in/) - MCP server management and discovery platform
- [FastMCP](https://github.com/jlowin/fastmcp) - Python framework for building MCP servers

## 📞 Support

For support, questions, or feature requests:

- Open an issue on [GitHub](https://github.com/VeriTeknik/pluggedin-random-number-generator-mcp-python/issues)
- Visit the [Plugged.in platform](https://plugged.in/) for MCP server management
- Check the [MCP documentation](https://modelcontextprotocol.io/docs) for protocol details
- Email: cem@plugged.in