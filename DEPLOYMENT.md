# Deployment Guide

This guide provides instructions for deploying the `pluggedin-random-number-generator-mcp-python` server.

## Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)
- `venv` (Python virtual environment module)

## Deployment Steps

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/pluggedin-random-number-generator-mcp-python.git
    cd pluggedin-random-number-generator-mcp-python
    ```

2.  **Create and activate a virtual environment**:
    It is highly recommended to deploy the server within a virtual environment to manage dependencies effectively and avoid conflicts with system-wide Python packages.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    Install the required Python packages using `pip`.
    ```bash
    pip install -e .
    ```

4.  **Run the server**:
    The server can be run directly using the Python interpreter. It communicates via standard input/output (stdio).
    ```bash
    python3 src/pluggedin_random_number_generator_mcp/server.py
    ```

## Running as a Service (Systemd Example)

For production environments, you might want to run the MCP server as a systemd service to ensure it starts automatically on boot and restarts if it crashes.

1.  **Create a systemd service file** (e.g., `/etc/systemd/system/mcp-rng.service`):

    ```ini
    [Unit]
    Description=Plugged.in Random Number Generator MCP Server
    After=network.target

    [Service]
    User=your_username  # Replace with your actual username
    Group=your_groupname # Replace with your actual groupname
    WorkingDirectory=/path/to/pluggedin-random-number-generator-mcp-python # Replace with the actual path
    ExecStart=/path/to/pluggedin-random-number-generator-mcp-python/venv/bin/python3 src/pluggedin_random_number_generator_mcp/server.py
    Restart=always
    StandardInput=socket
    StandardOutput=socket
    StandardError=journal

    [Install]
    WantedBy=multi-user.target
    ```

    **Important**: Replace `your_username`, `your_groupname`, and `/path/to/pluggedin-random-number-generator-mcp-python` with your actual values.

2.  **Reload systemd and enable the service**:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable mcp-rng.service
    sudo systemctl start mcp-rng.service
    ```

3.  **Check service status**:
    ```bash
    sudo systemctl status mcp-rng.service
    ```

## Docker Deployment (Coming Soon)

Docker images and deployment instructions will be provided in a future update for easier containerized deployment.

## Troubleshooting

-   **Permissions**: Ensure that the user running the server has appropriate read and execute permissions for the project directory and its contents.
-   **Virtual Environment**: Double-check that your virtual environment is activated and all dependencies are installed correctly.
-   **Logs**: Monitor the server's output for any error messages. If running as a systemd service, check the journal logs (`journalctl -u mcp-rng.service`).


