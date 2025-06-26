# Claude API Setup Guide

This guide will help you set up Claude API integration for enhanced security policy generation.

## Prerequisites

1. An Anthropic Claude API account
2. Python 3.7 or higher
3. The required Python packages (see requirements.txt)

## Step 1: Get Your Claude API Key

1. Visit [Anthropic's Console](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Navigate to the API Keys section
4. Create a new API key
5. Copy the API key (it starts with `sk-ant-`)

## Step 2: Set Environment Variable

### Option A: Set Environment Variable (Recommended)

**macOS/Linux:**
```bash
export CLAUDE_API_KEY="sk-ant-your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set CLAUDE_API_KEY=sk-ant-your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:CLAUDE_API_KEY="sk-ant-your-api-key-here"
```

### Option B: Create .env File

Create a `.env` file in the project root:
```
CLAUDE_API_KEY=sk-ant-your-api-key-here
```

### Option C: Set in Python Code

You can also set the API key directly in the code by modifying `app.py`:
```python
claude_generator = ClaudePolicyGenerator(api_key="sk-ant-your-api-key-here")
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Test the Integration

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://localhost:5013`

3. Fill out the form and try generating a policy

4. If Claude integration is working, you'll see:
   - "Claude API integration enabled" in the console
   - Additional buttons for Claude-powered features
   - Enhanced policy generation with AI assistance

## Features Available with Claude

### 1. Enhanced Policy Generation
- More sophisticated and contextual policies
- Industry-specific considerations
- Better compliance mapping
- Professional formatting

### 2. Security Controls Generation
- Detailed technical controls
- Implementation guidance
- Configuration examples
- Risk assessment criteria

### 3. Implementation Guide
- Step-by-step deployment roadmap
- Resource requirements
- Timeline and milestones
- Change management considerations

### 4. Complete Security Package
- All three components in one generation
- Consistent formatting and structure
- Comprehensive security program

## Troubleshooting

### "Claude API is not available" Error
- Check that your API key is correctly set
- Verify the environment variable is accessible
- Ensure the API key format is correct (starts with `sk-ant-`)

### API Rate Limits
- Claude has rate limits based on your plan
- Large policies may take longer to generate
- Consider upgrading your plan for higher limits

### Network Issues
- Ensure you have internet connectivity
- Check if your network allows API calls to Anthropic
- Verify firewall settings

## Security Considerations

1. **Never commit API keys to version control**
2. **Use environment variables for production**
3. **Rotate API keys regularly**
4. **Monitor API usage for unexpected charges**

## Cost Considerations

- Claude API usage is charged per token
- Policy generation typically costs $0.01-$0.05 per policy
- Complete packages may cost $0.05-$0.15
- Monitor your usage in the Anthropic console

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your API key is valid
3. Test with a simple policy first
4. Check Anthropic's status page for service issues

## Example Usage

Once configured, you can:

1. **Generate a basic policy** - Uses Claude for enhanced content
2. **Generate controls** - Creates detailed security controls
3. **Generate implementation guide** - Provides deployment guidance
4. **Generate complete package** - All three components together

The system will automatically fall back to the standard generator if Claude is not available. 