# OpenAI Quota/ billing Error - Troubleshooting Guide

## Error Message
```
You exceeded your current quota, please check your plan and billing details.
```

## What This Means
Your OpenAI API account has run out of credits or hit usage limits. This can happen if:
1. **Free tier credits exhausted**: Free tier has limited credits per month
2. **Billing limit reached**: You've hit your spending limit
3. **Account needs payment method**: Some models require a paid account
4. **Rate limits**: Too many requests in a short time

## Solutions

### Option 1: Use a Cheaper Model (Quick Fix)

The default model has been changed to `gpt-3.5-turbo` which is:
- Much cheaper (10x-20x less expensive)
- Higher rate limits
- Still very capable

**Update your `.env` file:**
```bash
OPENAI_MODEL=gpt-3.5-turbo
```

Or if you want to try other models:
- `gpt-3.5-turbo` - Recommended, cheapest and fast
- `gpt-4` - More expensive but better quality (requires paid account)
- `gpt-4-turbo-preview` - Latest GPT-4 (requires paid account and may have quota limits)

### Option 2: Check Your OpenAI Account

1. **Visit OpenAI Dashboard**: https://platform.openai.com/account/usage
2. **Check Usage & Billing**: 
   - View your current usage
   - Check billing limits
   - Add payment method if needed
   - Add credits if needed
3. **Check Rate Limits**: https://platform.openai.com/account/rate-limits

### Option 3: Add Payment Method / Credits

1. Go to: https://platform.openai.com/account/billing
2. Add a payment method
3. Set up billing limits (optional but recommended)
4. Add credits as needed

### Option 4: Use Alternative Providers

The system supports multiple LLM providers:

**Azure OpenAI:**
```env
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment
```

**OpenAI-Compatible APIs (Ollama, LocalAI):**
```env
LLM_PROVIDER=openai-compatible
AZURE_OPENAI_ENDPOINT=http://localhost:11434/v1
OPENAI_MODEL=llama2
```

## Quick Fix Steps

1. **Edit your `.env` file** in the backend directory:
   ```bash
   cd backend
   nano .env  # or use your preferred editor
   ```

2. **Change the model**:
   ```env
   OPENAI_MODEL=gpt-3.5-turbo
   ```

3. **Restart the server**:
   ```bash
   ./run.sh
   ```

## Model Comparison

| Model | Cost (approx) | Speed | Quality | Quota |
|-------|--------------|-------|---------|-------|
| gpt-3.5-turbo | $0.0015/1K tokens | Fast | Good | High |
| gpt-4 | $0.03/1K tokens | Slower | Excellent | Limited |
| gpt-4-turbo-preview | $0.01/1K tokens | Medium | Excellent | Limited |

## Verify Your API Key

Make sure your API key is correct:
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

If this fails, your API key might be invalid or expired.

## Need Help?

- OpenAI Support: https://help.openai.com/
- API Documentation: https://platform.openai.com/docs
- Status Page: https://status.openai.com/

