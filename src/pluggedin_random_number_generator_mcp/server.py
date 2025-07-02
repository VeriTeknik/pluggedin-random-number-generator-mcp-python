import secrets
import uuid
import math
import json
from typing import List, Union, Any, Literal

from fastmcp import FastMCP

class RandomNumberGeneratorMCP(FastMCP):
    def __init__(self):
        super().__init__(
            name="pluggedin-random-number-generator-mcp-python",
            version="1.0.0",
            description="A state-of-the-art cryptographically secure random number generator MCP server in Python."
        )

    @FastMCP.tool(
        name="generate_random_integer",
        description="Generate cryptographically secure random integers within a specified range.",
        input_schema={
            "type": "object",
            "properties": {
                "min": {"type": "integer", "description": "Minimum value (inclusive)", "default": 0},
                "max": {"type": "integer", "description": "Maximum value (inclusive)", "default": 100},
                "count": {"type": "integer", "description": "Number of random integers to generate", "default": 1, "minimum": 1, "maximum": 1000}
            },
            "required": []
        }
    )
    async def generate_random_integer(self, min: int = 0, max: int = 100, count: int = 1) -> dict:
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
            "timestamp": self.get_current_timestamp()
        }

    @FastMCP.tool(
        name="generate_random_float",
        description="Generate cryptographically secure random floating-point numbers.",
        input_schema={
            "type": "object",
            "properties": {
                "min": {"type": "number", "description": "Minimum value (inclusive)", "default": 0.0},
                "max": {"type": "number", "description": "Maximum value (exclusive)", "default": 1.0},
                "count": {"type": "integer", "description": "Number of random floats to generate", "default": 1, "minimum": 1, "maximum": 1000},
                "precision": {"type": "integer", "description": "Number of decimal places to round to", "default": 6, "minimum": 1, "maximum": 15}
            },
            "required": []
        }
    )
    async def generate_random_float(self, min: float = 0.0, max: float = 1.0, count: int = 1, precision: int = 6) -> dict:
        if min >= max:
            raise ValueError("Minimum value must be less than maximum value")
        if not (1 <= count <= 1000):
            raise ValueError("Count must be between 1 and 1000")
        if not (1 <= precision <= 15):
            raise ValueError("Precision must be between 1 and 15")

        results = []
        for _ in range(count):
            # Generate a cryptographically secure random float between 0 and 1
            # by generating random bytes and scaling them.
            # This is a common method when secrets.SystemRandom().random() is not sufficient
            # or when more direct control over the source of randomness is desired.
            num_bytes = 8  # Use 8 bytes for a 64-bit integer to ensure good precision
            random_int = int.from_bytes(secrets.token_bytes(num_bytes), byteorder='big')
            # Scale to a float between 0 and 1
            random_float_0_1 = random_int / (2**(num_bytes * 8) - 1)
            
            scaled_value = min + (random_float_0_1 * (max - min))
            results.append(round(scaled_value, precision))

        return {
            "type": "random_floats",
            "values": results,
            "parameters": {"min": min, "max": max, "count": count, "precision": precision},
            "timestamp": self.get_current_timestamp()
        }

    @FastMCP.tool(
        name="generate_random_bytes",
        description="Generate cryptographically secure random bytes.",
        input_schema={
            "type": "object",
            "properties": {
                "length": {"type": "integer", "description": "Number of random bytes to generate", "default": 32, "minimum": 1, "maximum": 1024},
                "encoding": {"type": "string", "description": "Output encoding format", "enum": ["hex", "base64"], "default": "hex"}
            },
            "required": []
        }
    )
    async def generate_random_bytes(self, length: int = 32, encoding: Literal["hex", "base64"] = "hex") -> dict:
        if not (1 <= length <= 1024):
            raise ValueError("Length must be between 1 and 1024")

        random_bytes = secrets.token_bytes(length)
        if encoding == "hex":
            result = random_bytes.hex()
        elif encoding == "base64":
            import base64
            result = base64.b64encode(random_bytes).decode("utf-8")
        else:
            raise ValueError("Invalid encoding. Must be 'hex' or 'base64'")

        return {
            "type": "random_bytes",
            "value": result,
            "parameters": {"length": length, "encoding": encoding},
            "timestamp": self.get_current_timestamp()
        }

    @FastMCP.tool(
        name="generate_uuid",
        description="Generate cryptographically secure UUID (v4) identifiers.",
        input_schema={
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of UUIDs to generate", "default": 1, "minimum": 1, "maximum": 100},
                "format": {"type": "string", "description": "UUID format", "enum": ["standard", "compact"], "default": "standard"}
            },
            "required": []
        }
    )
    async def generate_uuid(self, count: int = 1, format: Literal["standard", "compact"] = "standard") -> dict:
        if not (1 <= count <= 100):
            raise ValueError("Count must be between 1 and 100")

        results = []
        for _ in range(count):
            new_uuid = str(uuid.uuid4())
            if format == "compact":
                results.append(new_uuid.replace("-", ""))
            else:
                results.append(new_uuid)

        return {
            "type": "uuids",
            "values": results,
            "parameters": {"count": count, "format": format},
            "timestamp": self.get_current_timestamp()
        }

    @FastMCP.tool(
        name="generate_random_string",
        description="Generate a cryptographically secure random string.",
        input_schema={
            "type": "object",
            "properties": {
                "length": {"type": "integer", "description": "Length of the random string", "default": 16, "minimum": 1, "maximum": 256},
                "charset": {"type": "string", "description": "Character set to use", "enum": ["alphanumeric", "alphabetic", "numeric", "hex", "base64", "ascii_printable"], "default": "alphanumeric"},
                "count": {"type": "integer", "description": "Number of random strings to generate", "default": 1, "minimum": 1, "maximum": 100}
            },
            "required": []
        }
    )
    async def generate_random_string(self, length: int = 16, charset: Literal["alphanumeric", "alphabetic", "numeric", "hex", "base64", "ascii_printable"] = "alphanumeric", count: int = 1) -> dict:
        if not (1 <= length <= 256):
            raise ValueError("Length must be between 1 and 256")
        if not (1 <= count <= 100):
            raise ValueError("Count must be between 1 and 100")

        charsets = {
            "alphanumeric": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            "alphabetic": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "numeric": "0123456789",
            "hex": "0123456789abcdef",
            "base64": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
            "ascii_printable": "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        }

        chars = charsets.get(charset)
        if not chars:
            raise ValueError(f"Invalid charset: {charset}")

        results = []
        for _ in range(count):
            result_string = ''.join(secrets.choice(chars) for _ in range(length))
            results.append(result_string)

        return {
            "type": "random_strings",
            "values": results,
            "parameters": {"length": length, "charset": charset, "count": count},
            "timestamp": self.get_current_timestamp()
        }

    @FastMCP.tool(
        name="generate_random_choice",
        description="Randomly select items from a given list using cryptographically secure randomness.",
        input_schema={
            "type": "object",
            "properties": {
                "choices": {"type": "array", "description": "Array of items to choose from", "items": {"type": "string"}, "minItems": 1},
                "count": {"type": "integer", "description": "Number of items to select", "default": 1, "minimum": 1},
                "allow_duplicates": {"type": "boolean", "description": "Whether to allow duplicate selections", "default": True}
            },
            "required": ["choices"]
        }
    )
    async def generate_random_choice(self, choices: List[Any], count: int = 1, allow_duplicates: bool = True) -> dict:
        if not isinstance(choices, list) or not choices:
            raise ValueError("Choices must be a non-empty array")
        if count < 1:
            raise ValueError("Count must be at least 1")
        if not allow_duplicates and count > len(choices):
            raise ValueError("Count cannot exceed choices length when duplicates are not allowed")

        results = []
        if allow_duplicates:
            for _ in range(count):
                results.append(secrets.choice(choices))
        else:
            # For no duplicates, shuffle a copy of the choices and pick the first 'count' elements
            shuffled_choices = choices[:]
            secrets.SystemRandom().shuffle(shuffled_choices)
            results = shuffled_choices[:count]

        return {
            "type": "random_choices",
            "values": results,
            "parameters": {"choices": choices, "count": count, "allow_duplicates": allow_duplicates},
            "timestamp": self.get_current_timestamp()
        }

    @FastMCP.tool(
        name="generate_random_boolean",
        description="Generate cryptographically secure random boolean values.",
        input_schema={
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of random booleans to generate", "default": 1, "minimum": 1, "maximum": 1000},
                "probability": {"type": "number", "description": "Probability of true (0.0 to 1.0)", "default": 0.5, "minimum": 0.0, "maximum": 1.0}
            },
            "required": []
        }
    )
    async def generate_random_boolean(self, count: int = 1, probability: float = 0.5) -> dict:
        if not (1 <= count <= 1000):
            raise ValueError("Count must be between 1 and 1000")
        if not (0.0 <= probability <= 1.0):
            raise ValueError("Probability must be between 0.0 and 1.0")

        results = []
        for _ in range(count):
            # Generate a random float between 0 and 1 and compare with probability
            num_bytes = 4 # Use 4 bytes for a 32-bit integer
            random_int = int.from_bytes(secrets.token_bytes(num_bytes), byteorder='big')
            random_float_0_1 = random_int / (2**(num_bytes * 8) - 1)
            results.append(random_float_0_1 < probability)

        return {
            "type": "random_booleans",
            "values": results,
            "parameters": {"count": count, "probability": probability},
            "timestamp": self.get_current_timestamp()
        }

    def get_current_timestamp(self) -> str:
        """Helper to get current timestamp in ISO format."""
        import datetime
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

if __name__ == "__main__":
    server = RandomNumberGeneratorMCP()
    server.run_stdio_server()




def main():
    server = RandomNumberGeneratorMCP()
    server.run_stdio_server()

if __name__ == "__main__":
    main()


