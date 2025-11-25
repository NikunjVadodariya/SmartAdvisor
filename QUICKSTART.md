# Quick Start Guide

Get SmartAdvisor up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher (Node.js 18+ recommended)
- An OpenAI API key (or Azure OpenAI credentials)

## Step 1: Clone and Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

## Step 2: Start Backend Server

```bash
# Using the startup script
./run.sh

# Or manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start on `http://localhost:8000`

## Step 3: Setup Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:5173`

## Step 4: Open in Browser

Navigate to `http://localhost:5173` and start using SmartAdvisor!

## Testing

1. **Test Basic Query:**
   - Type "What can you help me with?" in the input field
   - Press Send

2. **Test Context Presets:**
   - Select "Sales" from the mode dropdown
   - Ask: "How should I approach a potential client?"
   - Notice the sales-focused response

3. **Test Custom Context:**
   - Click "Edit Context"
   - Add custom context (e.g., `{"company": "MyCompany"}`)
   - Click "Update Context"
   - Ask a question that uses the context

## Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Verify your `.env` file has the correct API key
- Check Python version: `python3 --version` (should be 3.8+)

### Frontend won't start
- Check if port 5173 is already in use
- Verify Node.js version: `node --version` (should be 16+)
- Try deleting `node_modules` and running `npm install` again

### API errors
- Check backend logs in `backend/logs/smartadvisor.log`
- Verify backend is running on port 8000
- Check browser console for errors

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design details
- Customize context presets for your business needs

## Production Deployment

For production deployment, see the README.md section on "Deployment".

