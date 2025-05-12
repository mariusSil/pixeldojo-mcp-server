# PixelDojo API Documentation

## Base URL
```
https://pixeldojo.ai/api/v1
```

## Authentication

All API requests must include your API key in the request headers.

**Example Request Header**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### Security Best Practices
- Never expose your API key in client-side code
- Rotate your API keys periodically
- Use environment variables to store your API keys
- Set appropriate CORS policies on your server

## Rate Limits

To ensure fair usage and system stability, the PixelDojo API has the following rate limits:

| Plan | Rate Limit | Notes |
|------|------------|-------|
| Standard | 60 requests per minute | Shared across all API endpoints |

**Rate Limit Headers**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1619284800
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests.

| Status Code | Description |
|-------------|-------------|
| 200 - OK | The request was successful |
| 400 - Bad Request | The request was invalid or missing required parameters |
| 401 - Unauthorized | Authentication failed or API key is missing |
| 403 - Forbidden | The API key doesn't have permission or insufficient credits |
| 429 - Too Many Requests | Rate limit exceeded |
| 500 - Internal Server Error | An error occurred on the server |

**Example Error Response**
```json
{
  "error": {
    "code": "insufficient_credits",
    "message": "Your account has insufficient credits",
    "status": 403
  }
}
```

## Flux API

### Generate images using the Flux model

**Endpoint**
```
POST /api/v1/flux
```

**Description**
Generate images using the Flux AI model. Each image generation costs 1 credit (1.5 for flux-1.1-pro-ultra).

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt | string | Yes | The text prompt for image generation |
| model | string | No | The model to use (default: "flux-pro") |
| raw | boolean | No | Return raw, unprocessed image data (default: false). Only supported for "flux-1.1-pro-ultra". |
| aspect_ratio | string | No | The aspect ratio of the generated image (default: "1:1") |
| num_outputs | integer | No | Number of images to generate (default: 1) |
| seed | integer | No | Random seed for reproducible results |
| output_format | string | No | Output format (png, jpg, webp) (default: "png") |
| output_quality | integer | No | Output quality (1-100) (default: 80) |

#### Parameter Details

**prompt**
The text description of the image you want to generate. Be as detailed as possible for best results.

Example: "A beautiful sunset over mountains with a lake in the foreground, highly detailed, realistic lighting, 4K"

**model**
The AI model to use for generation. Each model has different characteristics.

Options: "flux-pro", "flux-1.1-pro", "flux-1.1-pro-ultra", "flux-dev-single-lora"

**raw**
A boolean flag to return raw, unprocessed image data. Only available for the flux-1.1-pro-ultra model.

Example: "raw": true

**aspect_ratio**
The width-to-height ratio of the generated image.

Options: "1:1" (square), "16:9" (landscape), "9:16" (portrait), "4:3", "3:4", "3:2", "2:3"

### Supported Models

#### Model ID: flux-pro
- 1 credit per image
- High-quality image generation with balanced performance.

#### Model ID: flux-1.1-pro
- 1 credit per image
- Improved version with better quality and detail.

#### Model ID: flux-1.1-pro-ultra
- 1.5 credits per image
- Highest quality with enhanced details and realism. Supports raw mode.

#### Model ID: flux-dev-single-lora
- 1 credit per image
- Advanced model with single LoRA support.

### Example Request

**cURL**
```bash
curl -X POST https://pixeldojo.ai/api/v1/flux \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "prompt": "A beautiful landscape with mountains and a lake",
    "model": "flux-pro",
    "aspect_ratio": "16:9",
    "num_outputs": 1
  }'
```

**JavaScript**
```javascript
fetch('https://pixeldojo.ai/api/v1/flux', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    prompt: 'A beautiful landscape with mountains and a lake',
    model: 'flux-pro',
    aspect_ratio: '16:9',
    num_outputs: 1
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Python**
```python
import requests

url = "https://pixeldojo.ai/api/v1/flux"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}
data = {
    "prompt": "A beautiful landscape with mountains and a lake",
    "model": "flux-pro",
    "aspect_ratio": "16:9",
    "num_outputs": 1
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### Example Request with LoRA (Flux Dev)

```bash
curl -X POST https://pixeldojo.ai/api/v1/flux \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "prompt": "A beautiful sunset over a mountain landscape, highly detailed",
    "model": "flux-dev",
    "aspect_ratio": "16:9",
    "num_outputs": 1,
    "lora_weights": "https://huggingface.co/mylora.safetensors",
    "lora_scale": 0.7
  }'
```

### Example Response

```json
{
  "images": [
    "https://temp.pixeldojo.ai/pixeldojotemp/1686432789123-abc123-0.png"
  ],
  "credits_used": 1,
  "credits_remaining": 99
}
```

### Image Storage Policy

Generated images are stored temporarily on servers for 24 hours. The URL format is:

```
https://temp.pixeldojo.ai/pixeldojotemp/[timestamp]-[random]-[index].png
```

You should download and save images you wish to keep, as they will be automatically deleted after 24 hours.

## Using LoRA Models

### What is a LoRA?

LoRA (Low-Rank Adaptation) is a technique that allows you to fine-tune a base model with a small adapter. This enables customization of the model's output style or subject matter without retraining the entire model.

### How to Use LoRAs with the API

To use a LoRA with the flux-dev-single-lora model, you need to:

1. Find a compatible LoRA model (e.g., https://huggingface.co/mylora.safetensors)
2. Set the model parameter to flux-dev-single-lora
3. Set the lora_weights parameter to the LoRA model path
4. Optionally adjust the lora_scale parameter (default: 0.7)

**Example Request with LoRA:**

```json
{
  "prompt": "A portrait of a woman in a red dress",
  "model": "flux-dev-single-lora",
  "lora_weights": "https://huggingface.co/mylora.safetensors",
  "lora_scale": 0.7,
  "aspect_ratio": "1:1",
  "num_outputs": 1
}
```

### LoRA Tips

- **Adjust the scale**: The lora_scale parameter controls how strongly the LoRA affects the output. Higher values (0.8-1.0) produce stronger effects, while lower values (0.3-0.6) produce more subtle effects.
- **Use trigger words**: Many LoRAs have specific trigger words that activate their style. Check the LoRA's documentation for recommended trigger words to include in your prompt.
- **Combine with good prompts**: LoRAs work best when combined with well-crafted prompts that complement their style or subject matter.
- **Public models only**: The API can only access publicly available LoRA models on Hugging Face.

## Credit System

API usage consumes credits from your account:

- 1 credit per image for `flux-pro`, `flux-1.1-pro`, and `flux-dev-single-lora`
- 1.5 credits per image for `flux-1.1-pro-ultra`

You must have an active subscription and sufficient credits to use the API.

## Example Request for Flux Dev Single LoRA Model

```json
// POST https://pixeldojo.ai/api/v1/flux
// Headers:
// Authorization: Bearer your_api_key
// Content-Type: application/json

{
  "prompt": "A beautiful sunset over a mountain landscape, highly detailed",
  "model": "flux-dev-single-lora",
  "lora_weights": "https://huggingface.co/mylora.safetensors",
  "lora_scale": 0.7,
  "aspect_ratio": "16:9",
  "output_format": "png",
  "output_quality": 100,
  "num_outputs": 1,
  "seed": 42,
  "num_inference_steps": 28,
  "guidance_scale": 3.5,
  "megapixels": "1",
  "go_fast": false
}
```

Note: The go_fast parameter should always be set to false for the Flux Dev Single LoRA model.

## Example Response

```json
{
  "images": ["https://temp.pixeldojo.ai/pixeldojotemp/1234567890-abc123-0.png"],
  "credits_used": 1,
  "credits_remaining": 99
}
```

## Best Practices

### Tips for Effective API Usage

#### Write Detailed Prompts

The quality of your prompt directly affects the quality of the generated image. Be specific about style, lighting, composition, and details.

**Good**: "A serene mountain landscape at sunset with a crystal clear lake reflecting the orange sky, pine trees in the foreground, photorealistic, detailed, 4K"

**Less effective**: "Mountains and a lake"

#### Choose the Right Model

Different models excel at different types of images:

- flux-pro: Good all-around performance
- flux-1.1-pro: Better for detailed images
- flux-1.1-pro-ultra: Best for photorealistic images
- flux-dev-single-lora: Use when you need a specific style with a LoRA

#### Handle Errors Gracefully

Implement proper error handling in your application. Check for error responses and provide meaningful feedback to users.

```javascript
// Example error handling in JavaScript
try {
  const response = await fetch('https://pixeldojo.ai/api/v1/flux', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_API_KEY'
    },
    body: JSON.stringify({
      prompt: 'A beautiful landscape',
      model: 'flux-pro'
    })
  });
  
  const data = await response.json();
  
  if (!response.ok) {
    // Handle error response
    console.error('API Error:', data.error);
    // Show user-friendly message
  } else {
    // Process successful response
    const imageUrl = data.images[0];
    // Display or save the image
  }
} catch (error) {
  // Handle network or other errors
  console.error('Request failed:', error);
}
```

## Quick Reference

**Endpoint**
```
POST https://pixeldojo.ai/api/v1/flux
```

**Authentication**
```
Authorization: Bearer YOUR_API_KEY
```

**Required Parameters**
- prompt

**Credit Cost**
- 1 credit per image (1.5 for flux-1.1-pro-ultra)
