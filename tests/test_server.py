import asyncio
import json
import subprocess
import sys
import os
import re
import secrets

class MCPTester:
    def __init__(self):
        self.test_results = []
        self.server_process = None

    async def run_tests(self):
        print("🧪 Starting Python MCP Server Tests...\n")
        
        try:
            await self.start_server()
            await self.run_test_suite()
            await self.stop_server()
            
            self.print_results()
        except Exception as e:
            print(f"❌ Test suite failed: {e}")
            if self.server_process:
                self.server_process.kill()
            sys.exit(1)

    async def start_server(self):
        print("🚀 Starting MCP server...")
        # Use sys.executable to ensure the correct python interpreter is used
        # Adjust the path to server.py based on the project structure
        server_path = os.path.join(os.getcwd(), "src", "pluggedin_random_number_generator_mcp", "server.py")
        self.server_process = await asyncio.create_subprocess_exec(
            sys.executable, server_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the server to indicate it's running
        try:
            while True:
                line = await asyncio.wait_for(self.server_process.stderr.readline(), timeout=5.0)
                if b"running on stdio" in line:
                    print("✅ Server started successfully\n")
                    break
        except asyncio.TimeoutError:
            raise Exception("Server startup timeout")
        except Exception as e:
            raise Exception(f"Error during server startup: {e}")

    async def stop_server(self):
        if self.server_process:
            self.server_process.kill()
            await self.server_process.wait()
            print("🛑 Server stopped\n")

    async def send_request(self, method, params=None):
        if params is None:
            params = {}

        request_id = secrets.randbelow(1_000_000)
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params
        }

        request_str = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_str.encode())
        await self.server_process.stdin.drain()

        response_data = b""
        try:
            while True:
                line = await asyncio.wait_for(self.server_process.stdout.readline(), timeout=3.0)
                response_data += line
                try:
                    # Attempt to parse each line as a JSON object
                    # MCP responses are typically single-line JSON objects
                    response = json.loads(line.decode().strip())
                    if response.get("id") == request_id:
                        return response
                except json.JSONDecodeError:
                    # Not a complete JSON line, continue reading
                    pass
        except asyncio.TimeoutError:
            raise Exception(f"Request timeout for {method}")
        except Exception as e:
            raise Exception(f"Error during request: {e}")

    async def run_test_suite(self):
        await self.test_list_tools()
        await self.test_random_integers()
        await self.test_random_floats()
        await self.test_random_bytes()
        await self.test_uuids()
        await self.test_random_strings()
        await self.test_random_choices()
        await self.test_random_booleans()
        await self.test_error_handling()

    async def test_list_tools(self):
        try:
            print("📋 Testing list tools...")
            response = await self.send_request("tools/list")
            
            if "error" in response:
                raise Exception(f"List tools failed: {response['error']['message']}")
            
            tools = response["result"]["tools"]
            expected_tools = [
                "generate_random_integer",
                "generate_random_float", 
                "generate_random_bytes",
                "generate_uuid",
                "generate_random_string",
                "generate_random_choice",
                "generate_random_boolean"
            ]
            
            for expected_tool in expected_tools:
                found = any(tool["name"] == expected_tool for tool in tools)
                if not found:
                    raise Exception(f"Tool {expected_tool} not found in tools list")
            
            self.add_test_result("List Tools", True, f"Found {len(tools)} tools")
        except Exception as e:
            self.add_test_result("List Tools", False, str(e))

    async def test_random_integers(self):
        try:
            print("🔢 Testing random integers...")
            response = await self.send_request("tools/call", {
                "name": "generate_random_integer",
                "arguments": {"min": 1, "max": 100, "count": 5}
            })
            
            if "error" in response:
                raise Exception(f"Random integers failed: {response['error']['message']}")
            
            result = response["result"]
            
            if result["values"] is None or len(result["values"]) != 5:
                raise Exception(f"Expected 5 values, got {len(result.get('values', []))}")
            
            for value in result["values"]:
                if not (1 <= value <= 100):
                    raise Exception(f"Value {value} out of range [1, 100]")
            
            self.add_test_result("Random Integers", True, f"Generated {len(result['values'])} integers in range [1, 100]")
        except Exception as e:
            self.add_test_result("Random Integers", False, str(e))

    async def test_random_floats(self):
        try:
            print("🔢 Testing random floats...")
            response = await self.send_request("tools/call", {
                "name": "generate_random_float",
                "arguments": {"min": 0.0, "max": 1.0, "count": 3, "precision": 4}
            })
            
            if "error" in response:
                raise Exception(f"Random floats failed: {response['error']['message']}")
            
            result = response["result"]
            
            if result["values"] is None or len(result["values"]) != 3:
                raise Exception(f"Expected 3 values, got {len(result.get('values', []))}")
            
            for value in result["values"]:
                if not (0.0 <= value < 1.0):
                    raise Exception(f"Value {value} out of range [0.0, 1.0)")
            
            self.add_test_result("Random Floats", True, f"Generated {len(result['values'])} floats in range [0.0, 1.0)")
        except Exception as e:
            self.add_test_result("Random Floats", False, str(e))

    async def test_random_bytes(self):
        try:
            print("🔐 Testing random bytes...")
            response = await self.send_request("tools/call", {
                "name": "generate_random_bytes",
                "arguments": {"length": 16, "encoding": "hex"}
            })
            
            if "error" in response:
                raise Exception(f"Random bytes failed: {response['error']['message']}")
            
            result = response["result"]
            
            if len(result["value"]) != 32: # 16 bytes = 32 hex characters
                raise Exception(f"Expected 32 hex characters, got {len(result['value'])}")
            
            if not re.fullmatch(r"[0-9a-fA-F]+", result["value"]):
                raise Exception("Invalid hex encoding")
            
            self.add_test_result("Random Bytes", True, f"Generated {result['parameters']['length'] if 'parameters' in result and 'length' in result['parameters'] else 'N/A'} bytes as hex")
        except Exception as e:
            self.add_test_result("Random Bytes", False, str(e))

    async def test_uuids(self):
        try:
            print("🆔 Testing UUIDs...")
            response = await self.send_request("tools/call", {
                "name": "generate_uuid",
                "arguments": {"count": 2, "format": "standard"}
            })
            
            if "error" in response:
                raise Exception(f"UUIDs failed: {response['error']['message']}")
            
            result = response["result"]
            
            if result["values"] is None or len(result["values"]) != 2:
                raise Exception(f"Expected 2 UUIDs, got {len(result.get('values', []))}")
            
            uuid_regex = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", re.IGNORECASE)
            for uuid_val in result["values"]:
                if not uuid_regex.fullmatch(uuid_val):
                    raise Exception(f"Invalid UUID format: {uuid_val}")
            
            self.add_test_result("UUIDs", True, f"Generated {len(result['values'])} valid UUIDs")
        except Exception as e:
            self.add_test_result("UUIDs", False, str(e))

    async def test_random_strings(self):
        try:
            print("🔤 Testing random strings...")
            response = await self.send_request("tools/call", {
                "name": "generate_random_string",
                "arguments": {"length": 10, "charset": "alphanumeric", "count": 2}
            })
            
            if "error" in response:
                raise Exception(f"Random strings failed: {response['error']['message']}")
            
            result = response["result"]
            
            if result["values"] is None or len(result["values"]) != 2:
                raise Exception(f"Expected 2 strings, got {len(result.get('values', []))}")
            
            for s in result["values"]:
                if len(s) != 10:
                    raise Exception(f"Expected length 10, got {len(s)}")
                if not re.fullmatch(r"[A-Za-z0-9]+", s):
                    raise Exception(f"Invalid alphanumeric string: {s}")
            
            self.add_test_result("Random Strings", True, f"Generated {len(result['values'])} alphanumeric strings")
        except Exception as e:
            self.add_test_result("Random Strings", False, str(e))

    async def test_random_choices(self):
        try:
            print("🎯 Testing random choices...")
            choices = ["apple", "banana", "cherry", "date"]
            response = await self.send_request("tools/call", {
                "name": "generate_random_choice",
                "arguments": {"choices": choices, "count": 3, "allow_duplicates": True}
            })
            
            if "error" in response:
                raise Exception(f"Random choices failed: {response['error']['message']}")
            
            result = response["result"]
            
            if result["values"] is None or len(result["values"]) != 3:
                raise Exception(f"Expected 3 choices, got {len(result.get('values', []))}")
            
            for choice in result["values"]:
                if choice not in choices:
                    raise Exception(f"Invalid choice: {choice}")
            
            self.add_test_result("Random Choices", True, f"Selected {len(result['values'])} items from choices")
        except Exception as e:
            self.add_test_result("Random Choices", False, str(e))

    async def test_random_booleans(self):
        try:
            print("✅ Testing random booleans...")
            response = await self.send_request("tools/call", {
                "name": "generate_random_boolean",
                "arguments": {"count": 10, "probability": 0.5}
            })
            
            if "error" in response:
                raise Exception(f"Random booleans failed: {response['error']['message']}")
            
            result = response["result"]
            
            if result["values"] is None or len(result["values"]) != 10:
                raise Exception(f"Expected 10 booleans, got {len(result.get('values', []))}")
            
            for value in result["values"]:
                if not isinstance(value, bool):
                    raise Exception(f"Expected boolean, got {type(value)}")
            
            self.add_test_result("Random Booleans", True, f"Generated {len(result['values'])} boolean values")
        except Exception as e:
            self.add_test_result("Random Booleans", False, str(e))

    async def test_error_handling(self):
        try:
            print("⚠️  Testing error handling...")
            
            # Test invalid tool name
            response = await self.send_request("tools/call", {
                "name": "invalid_tool",
                "arguments": {}
            })
            
            if "error" not in response or "message" not in response["error"] or "Unknown tool" not in response["error"]["message"]:
                raise Exception("Expected error for invalid tool name")
            
            # Test invalid arguments for generate_random_integer
            response = await self.send_request("tools/call", {
                "name": "generate_random_integer",
                "arguments": {"min": 100, "max": 0}
            })
            if "error" not in response or "message" not in response["error"] or "Minimum value cannot be greater than maximum value" not in response["error"]["message"]:
                raise Exception("Expected error for invalid integer range")

            self.add_test_result("Error Handling", True, "Properly handles invalid tool names and arguments")
        except Exception as e:
            self.add_test_result("Error Handling", False, str(e))

    def add_test_result(self, test_name, passed, message):
        self.test_results.append({"test_name": test_name, "passed": passed, "message": message})
        status = "✅" if passed else "❌"
        print(f"{status} {test_name}: {message}\n")

    def print_results(self):
        print("📊 Test Results Summary:")
        print("========================\n")
        
        passed_count = sum(1 for r in self.test_results if r["passed"])
        total_count = len(self.test_results)
        
        for result in self.test_results:
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {result['test_name']}: {result['message']}")
        
        print(f"\n🎯 Overall: {passed_count}/{total_count} tests passed")
        
        if passed_count == total_count:
            print("🎉 All tests passed! The MCP server is working correctly.")
        else:
            print("⚠️  Some tests failed. Please review the implementation.")
            sys.exit(1)

if __name__ == "__main__":
    # Create tests directory if it doesn't exist
    os.makedirs("tests", exist_ok=True)
    # Change to the project root directory before running tests
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..")
    asyncio.run(MCPTester().run_tests())


