import secrets
import uuid
import base64
from datetime import datetime
from typing import List, Optional, Literal, Dict, Any

from fastmcp import FastMCP


server = FastMCP("pluggedin-random-number-generator-mcp-python")


def get_current_timestamp() -> str:
    """Get the current ISO timestamp."""
    return datetime.utcnow().isoformat() + "Z"


@server.tool(description="Generate cryptographically secure random integers within a specified range")
async def generate_random_integer(min: int = 0, max: int = 100, count: int = 1) -> Dict[str, Any]:
    """Generate random integers.
    
    Args:
        min: Minimum value (inclusive), default 0
        max: Maximum value (inclusive), default 100
        count: Number of integers to generate (1-1000), default 1
    """
    if min > max:
        raise ValueError("Minimum value cannot be greater than maximum value")
    if not (1 <= count <= 1000):
        raise ValueError("Count must be between 1 and 1000")

    results = []
    for _ in range(count):
        # secrets.randbelow(n) generates a random number in range [0, n-1]
        # To get a number in [min, max], we need randbelow(max - min + 1) + min
        results.append(secrets.randbelow(max - min + 1) + min)

    return {
        "type": "random_integers",
        "values": results,
        "parameters": {"min": min, "max": max, "count": count},
        "timestamp": get_current_timestamp()
    }


@server.tool(description="Generate cryptographically secure random floating-point numbers")
async def generate_random_float(
    min: float = 0.0, 
    max: float = 1.0, 
    count: int = 1, 
    precision: int = 6
) -> Dict[str, Any]:
    """Generate random floats.
    
    Args:
        min: Minimum value (inclusive), default 0.0
        max: Maximum value (exclusive), default 1.0
        count: Number of floats to generate (1-1000), default 1
        precision: Decimal places to round to (0-15), default 6
    """
    if min >= max:
        raise ValueError("Minimum value must be less than maximum value")
    if not (1 <= count <= 1000):
        raise ValueError("Count must be between 1 and 1000")
    if not (0 <= precision <= 15):
        raise ValueError("Precision must be between 0 and 15")

    results = []
    for _ in range(count):
        # Generate random bits and convert to float in [0, 1)
        random_float = secrets.randbits(53) / (1 << 53)
        # Scale to [min, max)
        scaled = min + (max - min) * random_float
        # Round to specified precision
        results.append(round(scaled, precision))

    return {
        "type": "random_floats",
        "values": results,
        "parameters": {"min": min, "max": max, "count": count, "precision": precision},
        "timestamp": get_current_timestamp()
    }


@server.tool(description="Generate cryptographically secure random bytes in various encodings")
async def generate_random_bytes(
    length: int = 32, 
    encoding: Literal["hex", "base64"] = "hex"
) -> Dict[str, Any]:
    """Generate random bytes.
    
    Args:
        length: Number of bytes to generate (1-1024), default 32
        encoding: Output encoding ('hex' or 'base64'), default 'hex'
    """
    if not (1 <= length <= 1024):
        raise ValueError("Length must be between 1 and 1024")

    random_bytes = secrets.token_bytes(length)
    
    if encoding == "hex":
        value = random_bytes.hex()
    elif encoding == "base64":
        value = base64.b64encode(random_bytes).decode('ascii')
    else:
        raise ValueError("Encoding must be 'hex' or 'base64'")

    return {
        "type": "random_bytes",
        "value": value,
        "parameters": {"length": length, "encoding": encoding},
        "timestamp": get_current_timestamp()
    }


@server.tool(description="Generate cryptographically secure UUID version 4 identifiers")
async def generate_uuid(
    count: int = 1, 
    format: Literal["standard", "compact"] = "standard"
) -> Dict[str, Any]:
    """Generate UUID v4 identifiers.
    
    Args:
        count: Number of UUIDs to generate (1-100), default 1
        format: UUID format ('standard' with hyphens or 'compact' without), default 'standard'
    """
    if not (1 <= count <= 100):
        raise ValueError("Count must be between 1 and 100")

    results = []
    for _ in range(count):
        new_uuid = str(uuid.uuid4())
        if format == "compact":
            new_uuid = new_uuid.replace("-", "")
        results.append(new_uuid)

    return {
        "type": "uuids",
        "values": results,
        "parameters": {"count": count, "format": format},
        "timestamp": get_current_timestamp()
    }


@server.tool(description="Generate cryptographically secure random strings with customizable character sets")
async def generate_random_string(
    length: int = 16, 
    charset: Literal["alphanumeric", "alphabetic", "numeric", "hex", "base64", "ascii_printable"] = "alphanumeric",
    count: int = 1
) -> Dict[str, Any]:
    """Generate random strings.
    
    Args:
        length: String length (1-256), default 16
        charset: Character set to use, default 'alphanumeric'
        count: Number of strings to generate (1-100), default 1
    """
    if not (1 <= length <= 256):
        raise ValueError("Length must be between 1 and 256")
    if not (1 <= count <= 100):
        raise ValueError("Count must be between 1 and 100")

    charsets = {
        "alphanumeric": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "alphabetic": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "numeric": "0123456789",
        "hex": "0123456789abcdef",
        "base64": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
        "ascii_printable": "".join(chr(i) for i in range(33, 127))
    }

    char_pool = charsets.get(charset)
    if not char_pool:
        raise ValueError(f"Invalid charset: {charset}")

    results = []
    for _ in range(count):
        result = ''.join(secrets.choice(char_pool) for _ in range(length))
        results.append(result)

    return {
        "type": "random_strings",
        "values": results,
        "parameters": {"length": length, "charset": charset, "count": count},
        "timestamp": get_current_timestamp()
    }


@server.tool(description="Randomly select items from a provided list using cryptographically secure randomness")
async def generate_random_choice(
    choices: List[str],
    count: int = 1,
    allow_duplicates: bool = True
) -> Dict[str, Any]:
    """Make random selections from a list.
    
    Args:
        choices: Array of items to choose from
        count: Number of items to select, default 1
        allow_duplicates: Whether to allow duplicate selections, default True
    """
    if not choices:
        raise ValueError("Choices array cannot be empty")
    
    if not allow_duplicates and count > len(choices):
        raise ValueError(f"Cannot select {count} unique items from {len(choices)} choices")

    results = []
    if allow_duplicates:
        for _ in range(count):
            results.append(secrets.choice(choices))
    else:
        # Sample without replacement
        available_choices = list(choices)
        for _ in range(count):
            choice = secrets.choice(available_choices)
            results.append(choice)
            available_choices.remove(choice)

    return {
        "type": "random_choices",
        "values": results,
        "parameters": {"choices": choices, "count": count, "allow_duplicates": allow_duplicates},
        "timestamp": get_current_timestamp()
    }


@server.tool(description="Generate cryptographically secure random boolean values with configurable probability")
async def generate_random_boolean(
    count: int = 1,
    probability: float = 0.5
) -> Dict[str, Any]:
    """Generate random booleans.
    
    Args:
        count: Number of booleans to generate (1-1000), default 1
        probability: Probability of True (0.0-1.0), default 0.5
    """
    if not (1 <= count <= 1000):
        raise ValueError("Count must be between 1 and 1000")
    if not (0.0 <= probability <= 1.0):
        raise ValueError("Probability must be between 0.0 and 1.0")

    results = []
    for _ in range(count):
        # Generate random float in [0, 1) and compare with probability
        random_value = secrets.randbits(53) / (1 << 53)
        results.append(random_value < probability)

    return {
        "type": "random_booleans",
        "values": results,
        "parameters": {"count": count, "probability": probability},
        "timestamp": get_current_timestamp()
    }


@server.prompt(description="Help me generate random values using cryptographically secure methods")
async def generate_random(
    type: Optional[str] = None,
    requirements: Optional[str] = None
) -> str:
    """Guide users in generating cryptographically secure random values.
    
    Args:
        type: Type of random value needed (integer, float, uuid, string, bytes, choice, boolean)
        requirements: Specific requirements for the random generation
    """
    type_info = f"Type: {type}" if type else ""
    req_info = f"Requirements: {requirements}" if requirements else ""
    
    return f"""I'll help you generate cryptographically secure random values. {req_info} {type_info}

As an AI, I cannot generate truly random numbers myself, but I have access to a cryptographically secure random number generator through MCP tools.

Available random generation tools:

1. **generate_random_integer** - Generate random integers within a range
2. **generate_random_float** - Generate random floating-point numbers  
3. **generate_random_bytes** - Generate random bytes (hex/base64)
4. **generate_uuid** - Generate UUID v4 identifiers
5. **generate_random_string** - Generate random strings with custom character sets
6. **generate_random_choice** - Make random selections from arrays
7. **generate_random_boolean** - Generate random booleans with probability control

All randomness is generated using Python's secrets module, which provides cryptographically strong pseudo-random data suitable for security-sensitive applications.

What type of random value would you like me to generate?"""


def main():
    """Main entry point for the server."""
    import os
    import sys
    
    # Check if we should show the banner
    show_banner = True
    if os.getenv("MCP_NO_BANNER") == "1" or "--no-banner" in sys.argv:
        show_banner = False
    
    # Run the server
    server.run(show_banner=show_banner)


# Also export for backward compatibility
class RandomNumberGeneratorMCP:
    """Compatibility wrapper."""
    pass


if __name__ == "__main__":
    main()