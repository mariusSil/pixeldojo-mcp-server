# PixelDojo MCP Server

[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-blue)](https://modelcontextprotocol.io/)

A Model Context Protocol (MCP) server that provides AI image generation functionality using [PixelDojo's](https://pixeldojo.ai/) API. Works with the [Anthropic](https://www.anthropic.com/news/model-context-protocol) Claude desktop client and other MCP-compatible hosts.

## Features

The PixelDojo MCP server allows AI assistants like Claude to:

- Generate AI images using various PixelDojo models
- Choose different aspect ratios, image formats, and quality settings
- View available models and capabilities
- Check credit balance and usage

## Tools

The server provides several tools to interact with the PixelDojo API:

### 1. `pixeldojo_generate_image`

Generate images using the PixelDojo AI image generation capabilities.

**Parameters**:
- `prompt` (required): Text description of the image you want to generate
- `model` (optional): The model to use (e.g., "flux-pro", "flux-1.1-pro", "flux-1.1-pro-ultra")
- `aspect_ratio` (optional): Image aspect ratio (e.g., "1:1", "16:9", "9:16")
- `num_outputs` (optional): Number of images to generate (default: 1)
- `seed` (optional): Random seed for reproducible results
- `output_format` (optional): Output format (png, jpg, webp)
- `output_quality` (optional): Output quality (1-100)

### 2. `pixeldojo_describe_models`

Get information about available models.

**Parameters**:
- `model_id` (optional): Specific model ID to get details for

### 3. `pixeldojo_get_credits`

Get current credit balance information for the PixelDojo account.

## Installation

### Prerequisites

- Python 3.11 or higher
- An active PixelDojo subscription and API key
- Credits for generating images (1 credit per image; 1.5 credits for flux-1.1-pro-ultra)

### Using UV (Recommended)

[UV](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
# Install UV if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package
uv pip install pixeldojo-mcp
```

### Using pip

```bash
pip install pixeldojo-mcp
```

### Using Homebrew (macOS)

```bash
# Add the tap (only needed once)
brew tap mariusSil/pixeldojo

# Install the package
brew install pixeldojo-mcp
```

This is the recommended installation method for team use as it provides the simplest setup experience.

## Setting Up with Windsurf

1. Get your PixelDojo API key from the [PixelDojo website](https://pixeldojo.ai/).

2. There are two ways to configure Windsurf to use the PixelDojo MCP server:

   ### Option 1: Using the Windsurf UI (Recommended)

   1. Open Windsurf Editor settings by navigating to:
      - **macOS**: Settings → Extensions → MCP Servers
      - **Windows/Linux**: File → Preferences → Settings → Extensions → MCP Servers

   2. Click "Add New Server" and fill in the following details:
      - **Server Name**: pixeldojo-mcp
      - **Command**: /opt/homebrew/bin/pixeldojo-mcp  (or the path where Homebrew installed it)
      - **Environment Variables**: 
        - Name: PIXELDOJO_API_KEY
        - Value: YOUR_API_KEY_HERE

   ### Option 2: Edit settings.json directly

   1. Open your Windsurf settings.json file:

      **macOS**:
      ```bash
      nano ~/Library/Application\ Support/Windsurf/User/settings.json
      ```

      **Windows**:
      ```bash
      notepad %APPDATA%\Windsurf\User\settings.json
      ```

   2. Add or update the "mcpServers" section with the PixelDojo configuration:

      ```json
      "mcpServers": {
        "pixeldojo-mcp": {
          "command": "/opt/homebrew/bin/pixeldojo-mcp",
          "env": {
            "PIXELDOJO_API_KEY": "YOUR_API_KEY_HERE"
          }
        }
      }
      ```

3. Save the file and restart Windsurf.

## Setting Up with Claude Desktop

1. Get your PixelDojo API key from the [PixelDojo website](https://pixeldojo.ai/).

2. Edit your Claude Desktop configuration file:

   **macOS**:
   ```bash
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

   **Windows**:
   ```bash
   notepad %APPDATA%\Claude\claude_desktop_config.json
   ```

3. Add the following configuration (create the file if it doesn't exist):

   ```json
   {
     "mcpServers": {
       "pixeldojo-mcp": {
         "env": {
           "PIXELDOJO_API_KEY": "YOUR_API_KEY_HERE"
         },
         "command": "pixeldojo-mcp"
       }
     }
   }
   ```

4. Save the file and restart Claude Desktop.

## Setting Up with Cursor

1. Get your PixelDojo API key from the [PixelDojo website](https://pixeldojo.ai/).

2. Edit your Cursor configuration file:

   **macOS**:
   ```bash
   nano ~/.cursor/mcp.json
   ```

   **Windows**:
   ```bash
   notepad %USERPROFILE%\.cursor\mcp.json
   ```

3. Add the following configuration (create the file if it doesn't exist):

    ```json
    {
      "pixeldojo-mcp": {
        "env": {
          "PIXELDOJO_API_KEY": "YOUR_API_KEY_HERE"
        },
        "command": "/opt/homebrew/bin/pixeldojo-mcp"
      }
    }
    ```

4. Save the file and restart Cursor.

## Environment Variables

The following environment variable is required:

- `PIXELDOJO_API_KEY`: Your PixelDojo API key

## Team Deployment Guide

To deploy this for your development team, follow these steps:

1. **Setup the Homebrew Tap Repository**:
   - Ensure your team has access to the mariusSil/homebrew-pixeldojo repository
   - The repository should contain the pixeldojo-mcp.rb formula

2. **Team Installation**:
   Share these simple instructions with your team:
   ```bash
   # Add the tap
   brew tap mariusSil/pixeldojo

   # Install the PixelDojo MCP server
   brew install pixeldojo-mcp

   # Configure in Windsurf: Settings → Extensions → MCP Servers
   # Add server with the following details:
   # - Server Name: pixeldojo-mcp
   # - Command: /opt/homebrew/bin/pixeldojo-mcp
   # - Environment Variables: PIXELDOJO_API_KEY=your_api_key_here
   ```

3. **API Key Management**:
   - Each team member will need their own PixelDojo API key
   - Enterprise users may contact PixelDojo for team licensing options

## Examples

### Generating an Image with Windsurf

Once the server is set up, you can ask Cascade in Windsurf to generate images for you:

> "Could you generate an image of a beautiful landscape with mountains and a lake using PixelDojo?"

Cascade will use the pixeldojo_generate_image tool and present the generated image to you.

### Generating an Image with Claude Desktop

Once the server is set up, you can ask Claude to generate images for you:

> "Could you generate an image of a beautiful landscape with mountains and a lake using PixelDojo?"

Claude will use the pixeldojo_generate_image tool and present the generated image to you.

### Advanced Image Generation

You can specify advanced parameters:

> "Generate an image of a cyberpunk city at night with neon lights using PixelDojo's flux-1.1-pro-ultra model with 16:9 aspect ratio."

Claude will pass these parameters to the tool.

### Checking Your Credit Balance

You can ask about your credit balance:

> "How many PixelDojo credits do I have left?"

Claude will use the pixeldojo_get_credits tool to check your balance.

## Security Best Practices

- Never expose your API key in public repositories or client-side code
- Rotate your API keys periodically
- Use environment variables to store your API keys
- Set appropriate CORS policies on your server

## Developing

For contributing to the project, please see our [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) file.

## License

MIT

## Acknowledgements

- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP specification
- [Anthropic](https://www.anthropic.com/) for Claude and the Claude Desktop client
- [PixelDojo](https://pixeldojo.ai/) for their image generation API
