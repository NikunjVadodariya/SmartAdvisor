# OpenRouter Integration Guide

OpenRouter provides unified access to multiple LLM models through a single API. This guide explains how to use OpenRouter with SmartAdvisor.

## What is OpenRouter?

OpenRouter is a service that allows you to:
- Access multiple LLM models (OpenAI, Anthropic, Google, Meta, etc.) through one API
- Compare model performance
- Use the best model for your use case
- Switch between models easily

## Setup Instructions

### Step 1: Create OpenRouter Account

1. Visit https://openrouter.ai/
2. Sign up for an account
3. Get your API key from the dashboard

### Step 2: Configure Environment Variables

Edit your `.env` file in the `backend` directory:

```env
# Set provider to openrouter
LLM_PROVIDER=openrouter

# Your OpenRouter API key
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# Choose your model (see model list below)
OPENROUTER_MODEL=openai/gpt-3.5-turbo

# Base URL (usually doesn't need to change)
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### Step 3: Restart Your Backend

```bash
cd backend
./run.sh
```

## Available Models

OpenRouter supports many models. Here are popular options:

### OpenAI Models
- `openai/gpt-4-turbo`
- `openai/gpt-4`
- `openai/gpt-3.5-turbo`
- `openai/gpt-4o`

### Anthropic Models
- `anthropic/claude-3-opus`
- `anthropic/claude-3-sonnet`
- `anthropic/claude-3-haiku`

### Google Models
- `google/gemini-pro`
- `google/gemini-pro-vision`

### Meta Models
- `meta-llama/llama-2-70b-chat`
- `meta-llama/llama-2-13b-chat`

### Other Models
- `mistralai/mistral-large`
- `perplexity/llama-3-sonar-large-32k-online`
- And many more!

Browse all models: https://openrouter.ai/models

## Model Pricing

OpenRouter shows pricing for each model. Check pricing at:
https://openrouter.ai/models

Prices vary by model and are typically pay-per-token.

## Example Configuration

### Using GPT-4 Turbo
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openai/gpt-4-turbo
```

### Using Claude 3 Opus
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=anthropic/claude-3-opus
```

### Using Gemini Pro
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=google/gemini-pro
```

## Benefits of OpenRouter

1. **Single API**: Access all models through one API
2. **Easy Switching**: Change models without code changes
3. **Cost Comparison**: See which models work best for your use case
4. **Reliability**: Automatic fallbacks and retries
5. **Analytics**: Track usage across all models

## Testing the Integration

1. Start your backend server
2. Check the health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

3. Make a test query:
   ```bash
   curl -X POST http://localhost:8000/api/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Hello, what models do you support?"}'
   ```

## Troubleshooting

### Error: "OPENROUTER_API_KEY is required"
- Make sure you've set `OPENROUTER_API_KEY` in your `.env` file
- Check that `LLM_PROVIDER=openrouter` is set

### Error: "Model not found"
- Verify the model name is correct
- Check https://openrouter.ai/models for available models
- Model names are case-sensitive

### Error: "Insufficient credits"
- Add credits to your OpenRouter account
- Check your account balance at https://openrouter.ai/account

### Error: "Rate limit exceeded"
- You've hit the rate limit
- Wait a moment and try again
- Consider upgrading your OpenRouter plan

## Switching Between Providers

You can easily switch between providers by changing `LLM_PROVIDER`:

```env
# Use OpenAI directly
LLM_PROVIDER=openai

# Use OpenRouter
LLM_PROVIDER=openrouter

# Use Azure OpenAI
LLM_PROVIDER=azure
```

## Cost Optimization Tips

1. **Use cheaper models for simple tasks**: GPT-3.5-turbo is cheaper than GPT-4
2. **Test with different models**: Find the best balance of cost and quality
3. **Monitor usage**: Check your OpenRouter dashboard regularly
4. **Set budgets**: OpenRouter allows you to set spending limits

## Additional Resources

- OpenRouter Documentation: https://openrouter.ai/docs
- Model Comparison: https://openrouter.ai/models
- API Reference: https://openrouter.ai/docs/api-reference
- Community: https://discord.gg/openrouter

## Support

- OpenRouter Support: https://openrouter.ai/support
- GitHub Issues: For SmartAdvisor-specific issues

