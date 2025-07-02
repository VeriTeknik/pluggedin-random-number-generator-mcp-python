# Smithery Deployment Guide

This guide explains how to deploy the Plugged.in Random Number Generator MCP Server (Python) to [Smithery](https://smithery.ai/).

## Prerequisites

- GitHub account
- Smithery account (sign up at [smithery.ai](https://smithery.ai/))
- This repository forked to your GitHub account

## Deployment Steps

1. **Fork the Repository**
   - Visit https://github.com/VeriTeknik/pluggedin-random-number-generator-mcp-python
   - Click the "Fork" button to create your own copy

2. **Connect GitHub to Smithery**
   - Log in to your Smithery account
   - Navigate to Settings → Integrations
   - Connect your GitHub account
   - Authorize Smithery to access your repositories

3. **Deploy the Server**
   - Go to the Deployments tab in Smithery
   - Select your forked repository
   - Click "Deploy"
   - Smithery will automatically detect the `smithery.yaml` configuration

4. **Configure Your MCP Client**
   - Once deployed, Smithery will provide an endpoint URL
   - Add this to your MCP client configuration:

   ```json
   {
     "mcpServers": {
       "random-generator-python": {
         "url": "https://your-deployment.smithery.ai/",
         "transport": "http"
       }
     }
   }
   ```

## Configuration

The `smithery.yaml` file contains:

```yaml
runtime: "docker"
```

The project uses a custom Dockerfile (`Dockerfile.smithery`) that:
- Installs Python dependencies
- Creates a non-root user for security
- Runs the Python MCP server directly
- Optimizes for Smithery's cloud environment

## Supported Features

All 7 random generation tools are available through Smithery:
- `generate_random_integer`
- `generate_random_float`
- `generate_random_bytes`
- `generate_uuid`
- `generate_random_string`
- `generate_random_choice`
- `generate_random_boolean`

## Environment Variables

The Smithery deployment automatically sets:
- `SMITHERY_RUNTIME=docker`
- `PYTHONUNBUFFERED=1` for real-time logging

## Monitoring

Smithery provides:
- Automatic scaling
- Request logs
- Performance metrics
- Error tracking
- Python-specific metrics

## Updating Your Deployment

To update your deployed server:

1. Push changes to your forked repository
2. In Smithery, navigate to your deployment
3. Click "Redeploy" to update to the latest version

## Performance Optimization

The Python implementation is optimized for Smithery:
- Uses FastMCP for efficient MCP protocol handling
- Minimal Docker image for fast cold starts
- Async/await for concurrent request handling
- Efficient memory usage with Python 3.11+

## Troubleshooting

If deployment fails:
- Check that `smithery.yaml` exists in the repository root
- Ensure all Python dependencies are listed in `pyproject.toml`
- Verify that `pip install -e .` completes successfully
- Check Smithery deployment logs for specific errors
- Ensure Python version compatibility (requires Python 3.8+)

## Local Testing Before Deployment

Test your server locally using Docker:

```bash
# Build and run the Smithery-optimized image
docker build -f Dockerfile.smithery -t mcp-python-smithery .
docker run --rm -i mcp-python-smithery
```

## Support

- Smithery Documentation: https://smithery.ai/docs
- MCP Server Issues: https://github.com/VeriTeknik/pluggedin-random-number-generator-mcp-python/issues
- Smithery Support: support@smithery.ai