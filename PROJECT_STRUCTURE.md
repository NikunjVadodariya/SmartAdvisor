# Project Structure

```
SmartAdvisor/
│
├── backend/                          # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py              # Package initialization
│   │   ├── main.py                  # FastAPI application & API endpoints
│   │   ├── config.py                # Configuration management
│   │   ├── context_engine.py        # Dynamic context engine
│   │   ├── llm_service.py           # LLM provider abstraction
│   │   ├── models.py                # SQLAlchemy database models
│   │   └── logger.py                # Logging configuration
│   ├── logs/                        # Log files directory (created at runtime)
│   ├── requirements.txt             # Python dependencies
│   ├── env.example                  # Environment variables template
│   └── run.sh                       # Backend startup script
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── App.jsx                  # Main React component
│   │   ├── App.css                  # Component styles
│   │   ├── main.jsx                 # React entry point
│   │   └── index.css                # Global styles
│   ├── index.html                   # HTML template
│   ├── package.json                 # Node.js dependencies
│   ├── vite.config.js               # Vite configuration
│   └── run.sh                       # Frontend startup script
│
├── README.md                         # Main documentation
├── QUICKSTART.md                     # Quick start guide
├── ARCHITECTURE.md                   # Architecture & design document
├── PROJECT_STRUCTURE.md              # This file
└── .gitignore                        # Git ignore rules

```

## Key Files Explained

### Backend Files

- **main.py**: Contains all API endpoints, request handlers, and FastAPI app setup
- **context_engine.py**: Core logic for merging queries with business context
- **llm_service.py**: Abstraction layer for different LLM providers (OpenAI, Azure, etc.)
- **models.py**: Database schema definitions using SQLAlchemy ORM
- **config.py**: Centralized configuration management using environment variables
- **logger.py**: Logging setup for file and console output

### Frontend Files

- **App.jsx**: Main React component handling UI state and API communication
- **App.css**: Styling for the chat interface
- **main.jsx**: React application entry point
- **vite.config.js**: Vite bundler configuration with API proxy setup

### Documentation Files

- **README.md**: Comprehensive project documentation
- **QUICKSTART.md**: Step-by-step setup guide
- **ARCHITECTURE.md**: Detailed system architecture and design decisions
- **PROJECT_STRUCTURE.md**: This file - project structure overview

## Database Schema

The application uses SQLite (configurable) with three main tables:

1. **conversation_logs**: Audit trail of all queries and responses
2. **context_presets**: Stored context configurations (Sales, Technical, Support)
3. **conversation_sessions**: Multi-turn conversation history

## Configuration

Configuration is managed via environment variables in `.env` file:
- LLM provider settings
- API keys
- Server ports
- CORS origins
- Database URL
- Logging configuration

## Runtime Files

These are created at runtime and should not be committed:
- `backend/logs/` - Log files
- `backend/smartadvisor.db` - SQLite database
- `frontend/node_modules/` - Node.js dependencies
- `frontend/dist/` - Production build files

