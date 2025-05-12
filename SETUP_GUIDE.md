# Setting Up PixelDojo MCP Server for Your Device

PixelDojo MCP (Model Context Protocol) servers enable AI assistants like Claude to perform image generation and retrieve image creation capabilities without leaving their interface. This guide will walk you through setting up a PixelDojo MCP server on your device to enhance your AI assistant capabilities with powerful image generation functionality.

## Understanding PixelDojo MCP Server

The PixelDojo MCP Server acts as a bridge between AI assistants and the PixelDojo API, allowing them to generate images directly within their interfaces[¹]. This integration is particularly useful for:

* Creating professional-quality AI-generated images
* Generating visual content for presentations, websites, and creative projects
* Enhancing AI assistant capabilities with visual content creation
* Testing different image generation prompts and styles

## Prerequisites

Before beginning the installation, ensure you have:

1. **A PixelDojo API Key**: You'll need to obtain this from PixelDojo's developer dashboard[²]
2. **Node.js installed**: Version 18 or higher is recommended for most implementations[³]
3. **Claude Desktop application**: This is the most common client used with PixelDojo MCP[⁴][⁵]
4. **Active PixelDojo subscription**: Required to use the API with credits available

## Installation Options

### Option 1: Using Homebrew (Recommended for macOS)

This is the simplest method for MacBook users:

```bash
brew tap silotech/ai/tap
brew install pixeldojo-mcp
```

### Option 2: Using npm

If you prefer using npm:

```bash
# Install directly from npm
npm install -g pixeldojo-mcp

# Or install using npx
npx -y @smithery/cli install pixeldojo-mcp --client claude
```

### Option 3: Installation from Source

For more advanced users who want to customize their installation:

1. Clone the repository:
```bash
git clone https://github.com/silotech/pixeldojo-mcp.git
cd pixeldojo-mcp
```

2. Install dependencies:
```bash
npm install
```

3. Build and install globally:
```bash
npm run build
npm install -g .
```

### Option 4: Using Python (pip)

If you prefer a Python-based implementation:

```bash
pip3 install pixeldojo-mcp
```

## Configuring Claude Desktop

After installing the PixelDojo MCP server, you need to configure Claude Desktop to use it:

1. Locate the Claude Desktop configuration file:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

2. Add the PixelDojo MCP configuration to the file. The exact configuration depends on your installation method:

For npm installation:
```json
{
  "mcpServers": {
    "pixeldojo-mcp": {
      "command": "pixeldojo-mcp",
      "env": {
        "PIXELDOJO_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

For Homebrew installation:
```json
{
  "mcpServers": {
    "pixeldojo-mcp": {
      "command": "pixeldojo-mcp-server",
      "env": {
        "PIXELDOJO_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

For npx installation:
```json
{
  "mcpServers": {
    "pixeldojo-mcp": {
      "command": "npx",
      "args": ["-y", "pixeldojo-mcp"],
      "env": {
        "PIXELDOJO_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Optional Configuration

You can customize your PixelDojo MCP server with additional environment variables:

* **PIXELDOJO_MODEL**: Specify the PixelDojo model to use (defaults to "flux-pro" if not specified)
* Available models include:
  * **flux-pro**: 1 credit per image - High-quality image generation with balanced performance
  * **flux-1.1-pro**: 1 credit per image - Improved version with better quality and detail
  * **flux-1.1-pro-ultra**: 1.5 credits per image - Highest quality with enhanced details and realism
  * **flux-dev-single-lora**: 1 credit per image - Advanced model with single LoRA support

## Testing Your Installation

To verify that your PixelDojo MCP server is working correctly:

1. Launch Claude Desktop application
2. Look for the tools icon (hammer) in the interface
3. Check if the PixelDojo image generation tools are available in the tools menu
4. Try a simple image generation query like "Generate an image of a mountain landscape with a sunset"

If Claude can successfully generate images and return results, your setup is working correctly.

## Troubleshooting

If you encounter issues:

* **API Key Problems**: Double-check your API key is correctly entered in the configuration file
* **Path Issues**: Ensure all paths are correctly specified, using absolute paths when necessary
* **Missing Dependencies**: Make sure Node.js is properly installed and updated
* **Permission Errors**: Check that you have the necessary permissions for the directories used[⁶]
* **Credit Issues**: Verify you have sufficient credits in your PixelDojo account

## Conclusion

With PixelDojo MCP server successfully set up on your device, your AI assistant now has the ability to generate images and provide you with visual content. This significantly enhances its capabilities beyond its training data, making it a more powerful tool for creative projects, content creation, and visual exploration.

The integration creates a seamless experience where you can ask for images to be generated based on your descriptions, and receive high-quality AI-generated images without having to switch between applications.

---

1. https://github.com/silotech/pixeldojo-mcp
2. https://pixeldojo.ai/account/api-keys
3. https://nodejs.org/en/download/package-manager/
4. https://www.anthropic.com/claude-desktop
5. https://github.com/silotech/claude-server-blob/main/docs/CLAUDE_DESKTOP_INTEGRATION.md
6. https://github.com/silotech/pixeldojo-mcp/blob/main/docs/troubleshooting.md
7. https://www.pixeldojo.ai/docs/getting-started/integration-guide
