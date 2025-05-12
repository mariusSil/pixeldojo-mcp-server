import asyncio
import aiohttp
import sys
import logging
import json
from datetime import datetime
import os

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
from pixeldojo_mcp import __version__

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize the MCP server
server = Server("pixeldojo-mcp")

# Check if API key is available
API_KEY = os.getenv('PIXELDOJO_API_KEY')
if not API_KEY:
    logging.warning("PIXELDOJO_API_KEY environment variable not set.")
    logging.warning("Please set your API key with: export PIXELDOJO_API_KEY=your_api_key_here")
elif not API_KEY.startswith("pd_") and not API_KEY.startswith("pdl_"):
    logging.warning(f"API key format may be incorrect. PixelDojo API keys usually start with 'pd_' or 'pdl_'. Your key starts with '{API_KEY[:3]}'")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="pixeldojo_generate_image",
            description="Generate images using PixelDojo AI with various models and settings",
            arguments=[
                types.PromptArgument(
                    name="prompt",
                    description="The text prompt for image generation",
                    required=True,
                ),
                types.PromptArgument(
                    name="model",
                    description="The model to use. Options: 'flux-pro', 'flux-1.1-pro', 'flux-1.1-pro-ultra', 'flux-dev-single-lora'",
                    required=False,
                ),
                types.PromptArgument(
                    name="aspect_ratio",
                    description="The aspect ratio of the generated image. Options: '1:1', '16:9', '9:16', '4:3', '3:4', '3:2', '2:3'",
                    required=False,
                ),
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> str:
    """
    Generate a prompt by combining arguments with server state.
    """
    if name != "pixeldojo_generate_image":
        return f"Unknown prompt: {name}"

    if arguments is None:
        arguments = {}

    prompt = arguments.get("prompt", "")
    model = arguments.get("model", "flux-pro")
    aspect_ratio = arguments.get("aspect_ratio", "1:1")

    return f"Generate an image of {prompt} using the {model} model with {aspect_ratio} aspect ratio."


@server.list_tools()
async def list_tools():
    """
    List available tools provided by the PixelDojo MCP server.
    Each tool can have optional arguments to customize its behavior.
    """
    return [
        types.Tool(
            name="pixeldojo_generate_image",
            description="Generate images using PixelDojo AI with various models and settings",
            argument_schema="""
            {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The text prompt for image generation"
                    },
                    "model": {
                        "type": "string",
                        "description": "The model to use.",
                        "enum": ["flux-pro", "flux-1.1-pro", "flux-1.1-pro-ultra", "flux-dev-single-lora"]
                    },
                    "aspect_ratio": {
                        "type": "string",
                        "description": "The aspect ratio of the generated image.",
                        "enum": ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]
                    },
                    "num_outputs": {
                        "type": "integer",
                        "description": "Number of images to generate",
                        "minimum": 1,
                        "maximum": 4
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducible results"
                    },
                    "output_format": {
                        "type": "string",
                        "description": "Output format",
                        "enum": ["png", "jpg", "webp"]
                    },
                    "output_quality": {
                        "type": "integer",
                        "description": "Output quality (1-100)",
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["prompt"]
            }
            """,
        ),
        types.Tool(
            name="pixeldojo_describe_models",
            description="Get information about available PixelDojo AI models",
            argument_schema="""
            {
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "Specific model ID to get details for (optional)"
                    }
                },
                "required": []
            }
            """,
        ),
        types.Tool(
            name="pixeldojo_get_credits",
            description="Get current credit balance information for the PixelDojo account",
            argument_schema="""
            {
                "type": "object",
                "properties": {},
                "required": []
            }
            """,
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> str:
    """
    Handle tool calls for the PixelDojo MCP server.
    """
    if name == "pixeldojo_generate_image":
        prompt = arguments.get("prompt", "")
        model = arguments.get("model", "flux-pro")
        aspect_ratio = arguments.get("aspect_ratio", "1:1")
        num_outputs = arguments.get("num_outputs", 1)
        seed = arguments.get("seed", None)
        output_format = arguments.get("output_format", "png")
        output_quality = arguments.get("output_quality", 80)

        return await generate_image(
            prompt, model, aspect_ratio, num_outputs, seed, output_format, output_quality
        )
    elif name == "pixeldojo_describe_models":
        model_id = arguments.get("model_id", None)
        return await describe_models(model_id)
    elif name == "pixeldojo_get_credits":
        return await get_credits()
    else:
        return f"Unknown tool: {name}"


async def generate_image(
    prompt: str,
    model: str = "flux-pro",
    aspect_ratio: str = "1:1",
    num_outputs: int = 1,
    seed: int = None,
    output_format: str = "png",
    output_quality: int = 80
) -> str:
    """
    Generate images using the PixelDojo API.
    
    Args:
        prompt: The text description of the image to generate
        model: The AI model to use for generation
        aspect_ratio: The width-to-height ratio of the generated image
        num_outputs: Number of images to generate
        seed: Random seed for reproducible results
        output_format: Output format (png, jpg, webp)
        output_quality: Output quality (1-100)
        
    Returns:
        A formatted string with image URLs and credit information
    """
    url = "https://pixeldojo.ai/api/v1/flux"
    
    # Prepare the request payload
    payload = {
        "prompt": prompt,
        "model": model,
        "aspect_ratio": aspect_ratio,
        "num_outputs": num_outputs,
        "output_format": output_format,
        "output_quality": output_quality
    }
    
    # Add optional seed if provided
    if seed is not None:
        payload["seed"] = seed
    
    # Use the global API_KEY variable that was validated at server startup
    if not API_KEY:
        return "Error: PIXELDOJO_API_KEY environment variable not set. Please configure your API key."
    
    # Prepare headers with API key
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    logging.info(f"Using API key: {API_KEY[:5]}...{API_KEY[-4:] if len(API_KEY) > 8 else '****'}")
    logging.info(f"Generating image with prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logging.error(f"Error from PixelDojo API: {response.status} - {error_text}")
                    return f"Error generating image: {response.status} - {error_text}"
                
                data = await response.json()
                
                # Format the response
                image_urls = data.get("images", [])
                credits_used = data.get("credits_used", 0)
                credits_remaining = data.get("credits_remaining", 0)
                
                result = f"Generated {len(image_urls)} image(s) using {model}:\n\n"
                
                for i, img in enumerate(image_urls):
                    if isinstance(img, dict) and "url" in img:
                        result += f"Image {i+1}: {img['url']}\n"
                    else:
                        result += f"Image {i+1}: {img}\n"
                
                result += f"\nCredits used: {credits_used}"
                result += f"\nCredits remaining: {credits_remaining}"
                result += "\n\nNote: Generated images are stored for 24 hours. Please download any images you wish to keep."
                
                return result
    except Exception as e:
        error_msg = f"Error calling PixelDojo API: {str(e)}"
        logging.error(error_msg)
        return error_msg


async def describe_models(model_id: str = None) -> str:
    """
    Get information about available PixelDojo AI models.
    
    Args:
        model_id: Specific model ID to get details for (optional)
        
    Returns:
        A formatted string with model information
    """
    # If a specific model ID is provided, return details for that model only
    if model_id:
        if model_id == "flux-pro":
            return """# Flux Pro (flux-pro)
High-quality image generation with balanced performance and cost.

**Features**:
- High-quality image generation
- Fast processing time (typically 2-5 seconds)
- Excellent for most general purposes

**Credit Cost**: 1 credit per image
"""
        elif model_id == "flux-1.1-pro":
            return """# Flux 1.1 Pro (flux-1.1-pro)
Enhanced version of Flux Pro with improved detail rendering and composition.

**Features**:
- Better detail retention than Flux Pro
- Improved composition and coherence
- Excellent text rendering

**Credit Cost**: 1 credit per image
"""
        elif model_id == "flux-1.1-pro-ultra":
            return """# Flux 1.1 Pro Ultra (flux-1.1-pro-ultra)
The highest quality model available, with exceptional detail and photorealism.

**Features**:
- Ultra-high detail and photorealism
- Best for complex scenes
- Superior composition
- Extended context understanding

**Credit Cost**: 1.5 credits per image
"""
        elif model_id == "flux-dev-single-lora":
            return """# Flux Dev Single LoRA (flux-dev-single-lora)
Experimental model with specialized capabilities (beta).

**Features**:
- Fine-tuned for specific use cases
- Single LoRA adaptation
- Specialized outputs
- Experimental features

**Credit Cost**: 1 credit per image
"""
        else:
            return f"Unknown model: {model_id}"
    
    # If no specific model is provided, return information about all models
    return """# PixelDojo AI Models

## Flux Pro (flux-pro)
High-quality image generation with balanced performance and cost.
- 1 credit per image

## Flux 1.1 Pro (flux-1.1-pro)
Enhanced version with improved detail rendering and composition.
- 1 credit per image

## Flux 1.1 Pro Ultra (flux-1.1-pro-ultra)
The highest quality model with exceptional detail and photorealism.
- 1.5 credits per image

## Flux Dev Single LoRA (flux-dev-single-lora)
Experimental model with specialized capabilities (beta).
- 1 credit per image

For detailed information about a specific model, use the model_id parameter.
"""


async def get_credits() -> str:
    """
    Get current credit balance information for the PixelDojo account.
    
    Returns:
        A formatted string with credit information
    """
    url = "https://pixeldojo.ai/api/v1/credits"
    
    # Use the global API_KEY variable that was validated at server startup
    if not API_KEY:
        return "Error: PIXELDOJO_API_KEY environment variable not set. Please configure your API key."
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return f"Error retrieving credit information: {response.status} - {error_text}"
                
                data = await response.json()
                
                credits_remaining = data.get("credits_remaining", 0)
                credits_used = data.get("credits_used", 0)
                monthly_allocation = data.get("monthly_allocation", 0)
                renewal_date = data.get("renewal_date", "Unknown")
                
                result = "# PixelDojo Credit Information\n\n"
                result += f"**Credits Remaining**: {credits_remaining}\n"
                result += f"**Credits Used This Month**: {credits_used}\n"
                result += f"**Monthly Allocation**: {monthly_allocation}\n"
                result += f"**Renewal Date**: {renewal_date}\n\n"
                result += "Note: The average cost is 1 credit per image, or 1.5 credits for Flux 1.1 Pro Ultra."
                
                return result
    except Exception as e:
        error_msg = f"Error retrieving credit information: {str(e)}"
        logging.error(error_msg)
        return "Unable to retrieve credit information. Please check your account on the PixelDojo website."


async def main_async():
    """
    Main async function to run the server.
    """
    logging.info(f"Starting PixelDojo MCP server version {__version__}")
    
    # Verify API key is set
    if not API_KEY:
        raise ValueError("PIXELDOJO_API_KEY environment variable is required")
    
    # Initialize the server using stdio server pattern like perplexity-mcp
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pixeldojo-mcp",
                server_version=__version__,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    """
    CLI entry point for pixeldojo-mcp
    """
    # Check for flags
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    # Configure logging based on verbose flag
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Verbose logging enabled")
    
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Error running server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
