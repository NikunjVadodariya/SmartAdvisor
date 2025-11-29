# SmartAdvisor

SmartAdvisor is an internal business assistant system that provides intelligent responses while maintaining dynamic business context. It acts as a wrapper around LLM services, providing a clean interface without exposing technical details to end users.

## Features

- **Dynamic Context Engine**: Merge user queries with editable business context in real-time
- **LLM Microservice**: Backend API that handles requests, manages context, and connects to LLM providers
- **Clean Web Interface**: Modern React-based UI that hides all LLM implementation details
- **Role-based Presets**: Pre-configured modes (Sales, Technical, Support) for quick context switching
- **Message History**: Persistent conversation history with session management
- **Audit Logging**: Complete request/response logging for compliance and audit purposes

## Architecture

```
┌─────────────┐
│   Frontend  │ (React UI)
│  (Port 5173)│
└──────┬──────┘
       │ HTTP/REST
       ▼
┌──────────────────────┐
│   FastAPI Backend    │ (Port 8000)
│  ┌────────────────┐  │
│  │ Context Engine │  │
│  │  - Merge query │  │
│  │  - Context mgmt│  │
│  └────────┬───────┘  │
│           │          │
│  ┌────────▼───────┐  │
│  │  LLM Service   │  │
│  │  - OpenAI      │  │
│  │  - Azure OpenAI│  │
│  │  - Compatible  │  │
│  └────────┬───────┘  │
│           │          │
│  ┌────────▼───────┐  │
│  │   Database     │  │
│  │  - SQLite      │  │
│  │  - Logs        │  │
│  │  - Sessions    │  │
│  └────────────────┘  │
└──────────────────────┘
       │
       ▼
┌─────────────┐
│  LLM API    │
│  (OpenAI/   │
│   Azure)    │
└─────────────┘
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+ (Node.js 18+ recommended for best compatibility)
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from example:
```bash
cp env.example .env
```

5. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
LLM_PROVIDER=openai
```

6. Start the backend server:
```bash
python -m app.main
# Or use uvicorn directly:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to `http://localhost:5173`

## Usage

### Basic Usage

1. Start both backend and frontend servers
2. Open the web interface
3. Type your question in the input field
4. SmartAdvisor will respond based on the current context

### Changing Context

**Using Presets:**
- Select a mode from the dropdown (Sales, Technical, Support)
- The context will automatically update

**Custom Context:**
1. Click "Edit Context" button
2. Modify the JSON context
3. Click "Update Context"

Example context:
```json
{
  "role": "Sales Advisor",
  "mode": "Sales",
  "instructions": [
    "Focus on customer needs",
    "Highlight ROI and benefits"
  ],
  "company_name": "Acme Corp",
  "target_audience": "Enterprise customers"
}
```

### API Endpoints

- `POST /api/query` - Send a query and get response
- `GET /api/context` - Get current context
- `POST /api/context` - Update context
- `GET /api/presets` - List all presets
- `POST /api/presets` - Create new preset
- `POST /api/presets/{name}/apply` - Apply a preset
- `GET /api/conversations/{session_id}` - Get conversation history

## Configuration

### LLM Providers

**OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
```

**Azure OpenAI:**
```env
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_DEPLOYMENT_NAME=deployment-name
```

**OpenAI-Compatible (Ollama, LocalAI, etc.):**
```env
LLM_PROVIDER=openai-compatible
AZURE_OPENAI_ENDPOINT=http://localhost:11434/v1
OPENAI_MODEL=llama2
```

**OpenRouter (Unified access to multiple LLM models):**
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```

See [OpenRouter Setup Guide](backend/OPENROUTER_SETUP.md) for detailed instructions.

## Project Structure

```
SmartAdvisor/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration management
│   │   ├── context_engine.py    # Dynamic context engine
│   │   ├── llm_service.py       # LLM provider integration
│   │   ├── models.py            # Database models
│   │   └── logger.py            # Logging setup
│   ├── requirements.txt
│   ├── env.example
│   └── logs/                    # Log files
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── App.css              # Styles
│   │   ├── main.jsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── package.json
│   └── vite.config.js
├── ARCHITECTURE.md              # Detailed architecture document
└── README.md                    # This file
```

## Security Considerations

- API keys are stored in `.env` files (not committed to git)
- CORS is configured to restrict origins
- Database logs don't store sensitive user data
- Context data is validated before use
- All requests are logged for audit purposes

## Error Handling

- Frontend gracefully handles API errors
- Backend returns appropriate HTTP status codes
- All errors are logged for debugging
- User-friendly error messages in UI

## Logging

All interactions are logged to:
- Database: `conversation_logs` table
- File: `backend/logs/smartadvisor.log`
- Console: During development

## License

Internal use only.

## Support

For issues or questions, please contact the development team.

