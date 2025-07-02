# Plugged.in Random Number Generator MCP (Python)

This repository contains a state-of-the-art random number generator MCP (Model Context Protocol) server implemented in Python. It provides a suite of tools for generating various types of random data, including cryptographically secure numbers, UUIDs, strings, and more.

## Features

- **Cryptographically Secure Randomness**: Utilizes Python's `secrets` module and `os.urandom` for high-quality, unpredictable random number generation.
- **Comprehensive Random Data Generation**: Supports:
    - Random integers within a specified range.
    - Random floating-point numbers with configurable precision.
    - Random bytes in various encodings (hex, base64).
    - Universally Unique Identifiers (UUIDs).
    - Random strings with customizable character sets (alphanumeric, alphabetic, numeric, special characters).
    - Random selections from a given list of choices.
    - Random booleans with adjustable probability.
- **Model Context Protocol (MCP) Compliance**: Implements the MCP specification for seamless integration with other MCP-compatible systems and large language models.
- **Extensible Architecture**: Designed for easy addition of new random generation tools.
- **Thoroughly Tested**: Includes a comprehensive test suite to ensure reliability and correctness.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/pluggedin-random-number-generator-mcp-python.git
    cd pluggedin-random-number-generator-mcp-python
    ```

2.  **Create a virtual environment (recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -e .
    ```

## Usage

The server can be run as a standard MCP server, communicating via standard input/output (stdio).

### Running the Server

```bash
python3 src/pluggedin_random_number_generator_mcp/server.py
```

Once running, the server will listen for MCP requests on `stdin` and respond on `stdout`.

### Example MCP Requests

You can interact with the server by sending JSON-RPC 2.0 requests. Here are some examples:

#### List Available Tools

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

#### Generate Random Integer

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "generate_random_integer",
    "arguments": {
      "min": 1,
      "max": 100,
      "count": 5
    }
  }
}
```

#### Generate Random UUID

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "generate_uuid",
    "arguments": {
      "count": 1,
      "format": "standard"
    }
  }
}
```

#### Generate Random String

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "generate_random_string",
    "arguments": {
      "length": 12,
      "charset": "alphanumeric",
      "count": 1
    }
  }
}
```

## Development

### Running Tests

To run the test suite, execute the `test_server.py` script:

```bash
python3 tests/test_server.py
```

This will start the server in a subprocess, run all defined tests, and then shut down the server.

## Project Structure

```
.gitignore
LICENSE
pyproject.toml
README.md
src/
└── pluggedin_random_number_generator_mcp/
    ├── __init__.py
    └── server.py
tests/
└── test_server.py
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please open an issue on GitHub. 


# pluggedin-random-number-generator-mcp-python
