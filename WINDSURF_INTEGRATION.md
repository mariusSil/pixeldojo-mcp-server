# Integrating PixelDojo MCP with Windsurf Editor

This guide provides instructions for setting up and testing the PixelDojo MCP server with Windsurf Editor.

## Prerequisites

Before beginning the integration, ensure you have:

1. **PixelDojo API Key**: Obtain this from your PixelDojo account
2. **Python 3.11 or higher**: Required for running the PixelDojo MCP server
3. **Windsurf Editor**: Installed and configured on your system
4. **Active PixelDojo subscription**: With available credits for image generation

## Installation Steps

### 1. Install the PixelDojo MCP Server

First, we need to install the server package. Since we're testing the development version, we'll install it directly from the local directory:

```bash
# Navigate to the pixeldojo-mcp-server directory
cd /Users/mariussilenskis/Development/silotech/pixeldojo-mcp-server

# Install in development mode with pip
pip install -e .
```

### 2. Configure Windsurf Editor

Windsurf Editor needs to be configured to recognize and connect to the PixelDojo MCP server:

1. Open Windsurf Editor settings by navigating to:
   - **macOS**: Settings → Extensions → MCP Servers
   - **Windows/Linux**: File → Preferences → Settings → Extensions → MCP Servers

2. Click "Add New Server" and fill in the following details:
   - **Server Name**: pixeldojo-mcp
   - **Command**: pixeldojo-mcp
   - **Environment Variables**: 
     - Name: PIXELDOJO_API_KEY
     - Value: YOUR_API_KEY_HERE

3. Alternatively, you can edit the Windsurf configuration file directly:

   **macOS**:
   ```bash
   nano ~/Library/Application\ Support/Windsurf/settings.json
   ```

   **Windows**:
   ```bash
   notepad %APPDATA%\Windsurf\settings.json
   ```

   **Linux**:
   ```bash
   nano ~/.config/Windsurf/settings.json
   ```

   Add the following configuration:

   ```json
   {
     "mcp.servers": {
       "pixeldojo-mcp": {
         "command": "pixeldojo-mcp",
         "env": {
           "PIXELDOJO_API_KEY": "YOUR_API_KEY_HERE"
         }
       }
     }
   }
   ```

4. Save the configuration and restart Windsurf Editor.

## Testing Procedure

Follow these steps to test the PixelDojo MCP server integration with Windsurf:

### 1. Verify Server Connection

1. Open Windsurf Editor
2. Open the MCP Servers panel (if available in your Windsurf version)
3. Check that pixeldojo-mcp appears as a connected server
4. Look for any connection errors in the logs

### 2. Test Basic Image Generation

1. Open a new file or conversation in Windsurf
2. Ask the AI assistant to generate an image using PixelDojo:
   ```
   Please generate an image of a mountain landscape with a sunset using PixelDojo.
   ```
3. Verify that:
   - The AI recognizes the request
   - The pixeldojo_generate_image tool is invoked
   - The image URL is returned successfully
   - The response includes credit usage information

### 3. Test Advanced Image Parameters

1. Test aspect ratio settings:
   ```
   Generate an image of a cityscape at night with neon lights using PixelDojo with a 16:9 aspect ratio.
   ```

2. Test different models:
   ```
   Create an image of a fantasy castle using the PixelDojo flux-1.1-pro-ultra model.
   ```

3. Test output quality settings:
   ```
   Generate a high-quality (100) image of a tropical beach using PixelDojo.
   ```

### 4. Test Model Information Tool

1. Request information about PixelDojo models:
   ```
   What models are available in PixelDojo and what are their features?
   ```

2. Test specific model information:
   ```
   Tell me more about the PixelDojo flux-1.1-pro-ultra model.
   ```

### 5. Test Credits Information

1. Request credit balance information:
   ```
   How many PixelDojo credits do I have remaining?
   ```

## Troubleshooting

### Common Issues

1. **API Key Error**: If you see authentication errors, verify your API key is correct and properly set in the Windsurf configuration.

2. **Connection Issues**: If Windsurf can't connect to the server, try:
   - Restarting Windsurf Editor
   - Checking that the pixeldojo-mcp package is installed correctly
   - Verifying the command path is correct in the configuration

3. **Python Environment Issues**: Ensure you're using Python 3.11+ and all dependencies are correctly installed.

4. **Credit Issues**: If image generation fails due to insufficient credits, check your PixelDojo account balance.

### Debugging

For more detailed debugging information, you can run the pixeldojo-mcp server manually with increased logging:

```bash
# Export your API key
export PIXELDOJO_API_KEY=your_api_key_here

# Run the server with debug logging
python -m pixeldojo_mcp --debug
```

Then observe the output for any error messages or connection issues.

## Next Steps

After successful testing, you can:

1. Document any Windsurf-specific quirks or requirements
2. Create a streamlined installation process for Windsurf users
3. Develop a Windsurf-specific section in the main README or user guide
