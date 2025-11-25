# SmartAdvisor Architecture & Design Document

## Overview

SmartAdvisor is an internal business assistant system designed to provide intelligent responses while maintaining dynamic business context. The system abstracts away LLM implementation details, providing a clean interface for business users.

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         React Frontend (Port 5173)                     │  │
│  │  - Query Input                                         │  │
│  │  - Context Editor                                      │  │
│  │  - Preset Selector                                     │  │
│  │  - Message Display                                     │  │
│  └───────────────────────┬───────────────────────────────┘  │
└──────────────────────────┼───────────────────────────────────┘
                           │ HTTP/REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Port 8000)               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              API Layer (main.py)                       │  │
│  │  - /api/query                                          │  │
│  │  - /api/context                                        │  │
│  │  - /api/presets                                        │  │
│  │  - /api/conversations                                  │  │
│  └───────┬───────────────────────┬───────────────────────┘  │
│          │                       │                           │
│  ┌───────▼──────────┐  ┌────────▼──────────┐               │
│  │ Context Engine   │  │   LLM Service     │               │
│  │ (context_engine) │  │  (llm_service)    │               │
│  │                  │  │                   │               │
│  │ - Merge query    │  │ - OpenAI          │               │
│  │ - Context mgmt   │  │ - Azure OpenAI    │               │
│  │ - History        │  │ - Compatible APIs │               │
│  │ - Presets        │  │                   │               │
│  └───────┬──────────┘  └────────┬──────────┘               │
│          │                       │                           │
│  ┌───────▼───────────────────────▼──────────┐              │
│  │         Database Layer (SQLite)           │              │
│  │  - conversation_logs (audit)              │              │
│  │  - context_presets (presets)              │              │
│  │  - conversation_sessions (history)        │              │
│  └───────────────────────────────────────────┘              │
│                                                              │
│  ┌──────────────────────────────────────────┐              │
│  │         Logging System                    │              │
│  │  - File logs (logs/smartadvisor.log)     │              │
│  │  - Database logs                         │              │
│  └──────────────────────────────────────────┘              │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    External LLM Providers                    │
│  - OpenAI API                                               │
│  - Azure OpenAI                                             │
│  - OpenAI-compatible APIs (Ollama, LocalAI, etc.)          │
└─────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. Frontend (React Application)

**Location:** `frontend/src/`

**Responsibilities:**
- Provide user interface for queries
- Display responses without exposing LLM details
- Manage context editing interface
- Handle preset selection
- Maintain conversation history in UI

**Key Components:**
- `App.jsx`: Main application component
- Manages state for messages, context, presets
- Handles API communication via Axios

**Features:**
- Real-time query submission
- Context editor with JSON validation
- Preset dropdown for quick context switching
- Message history display
- Error handling with user-friendly messages

### 2. Backend API (FastAPI)

**Location:** `backend/app/main.py`

**Responsibilities:**
- Handle HTTP requests from frontend
- Route requests to appropriate services
- Manage sessions and conversation state
- Return only processed responses (no LLM metadata)
- Handle errors gracefully

**API Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/query` | POST | Process user query with context |
| `/api/context` | GET | Get current business context |
| `/api/context` | POST | Update business context |
| `/api/context` | DELETE | Clear business context |
| `/api/presets` | GET | List all context presets |
| `/api/presets` | POST | Create new preset |
| `/api/presets/{name}/apply` | POST | Apply a preset |
| `/api/conversations/{session_id}` | GET | Get conversation history |
| `/api/conversations/{session_id}` | DELETE | Delete conversation |

### 3. Dynamic Context Engine

**Location:** `backend/app/context_engine.py`

**Responsibilities:**
- Merge user queries with business context
- Manage context state dynamically
- Build structured prompts for LLM
- Support context overrides per request
- Maintain context history

**Key Methods:**
- `update_context(context, merge=True)`: Update context dynamically
- `build_chat_messages(query, context_override, history)`: Build LLM messages
- `get_context()`: Retrieve current context
- `clear_context()`: Reset context

**Context Structure:**
```python
{
    "role": "Sales Advisor",           # Persona/role
    "mode": "Sales",                   # Operating mode
    "instructions": [...],             # Behavioral instructions
    "company_name": "Acme Corp",       # Additional context fields
    "target_audience": "Enterprise"    # Custom fields
}
```

**Context Injection Flow:**
1. User query received
2. Context engine retrieves current context or override
3. Context merged into system message
4. System message + conversation history + user query sent to LLM
5. Response generated and returned

### 4. LLM Service

**Location:** `backend/app/llm_service.py`

**Responsibilities:**
- Abstract LLM provider interface
- Support multiple providers (OpenAI, Azure, compatible APIs)
- Handle API communication
- Return only response content (no metadata)
- Error handling for LLM failures

**Supported Providers:**
- **OpenAI**: Direct OpenAI API integration
- **Azure OpenAI**: Azure-hosted OpenAI deployments
- **OpenAI-Compatible**: Any API compatible with OpenAI format (Ollama, LocalAI, etc.)

**Configuration:**
- Provider selected via `LLM_PROVIDER` environment variable
- API keys and endpoints configured in `.env` file
- Model names configurable per provider

### 5. Database Layer

**Location:** `backend/app/models.py`

**Database:** SQLite (configurable to PostgreSQL, MySQL, etc.)

**Tables:**

1. **conversation_logs**
   - Purpose: Audit logging of all interactions
   - Fields: id, timestamp, user_query, context_used, response, session_id, user_id, metadata
   - Used for: Compliance, debugging, analytics

2. **context_presets**
   - Purpose: Store reusable context configurations
   - Fields: id, name, description, context_data, created_at, updated_at
   - Default presets: Sales, Technical, Support

3. **conversation_sessions**
   - Purpose: Maintain conversation history across requests
   - Fields: id, session_id, user_id, context, messages, created_at, updated_at
   - Used for: Multi-turn conversations, context continuity

### 6. Logging System

**Location:** `backend/app/logger.py`

**Logging Targets:**
- **File Logging**: `backend/logs/smartadvisor.log`
- **Console Logging**: Standard output (development)
- **Database Logging**: `conversation_logs` table

**Logged Information:**
- Request timestamps
- User queries
- Context used
- Responses generated
- Errors and exceptions
- Session information

## User Flow

### 1. Initial Query Flow

```
User enters query in UI
    ↓
Frontend sends POST /api/query
    ↓
Backend receives request
    ↓
Context Engine merges query + context
    ↓
LLM Service generates response
    ↓
Response logged to database
    ↓
Response returned to frontend
    ↓
UI displays response
```

### 2. Context Update Flow

```
User edits context in UI
    ↓
Frontend sends POST /api/context
    ↓
Backend updates Context Engine
    ↓
Context stored in memory
    ↓
Confirmation returned
    ↓
UI updates context display
```

### 3. Preset Application Flow

```
User selects preset from dropdown
    ↓
Frontend sends POST /api/presets/{name}/apply
    ↓
Backend retrieves preset from database
    ↓
Context Engine updates with preset data
    ↓
Confirmation returned
    ↓
UI shows preset active
```

## Context Injection Mechanism

### How Context Works

1. **Default Context**: Stored in Context Engine memory
2. **Per-Request Override**: Can be passed with each query
3. **Preset Context**: Loaded from database presets
4. **Merging Strategy**: 
   - `merge=True`: New context fields merge with existing
   - `merge=False`: New context replaces existing

### Prompt Structure

The context engine builds a structured prompt:

```
System Message:
- Role definition
- Mode specification
- Instructions
- Additional context fields

User Messages:
- Conversation history (last 10 messages)
- Current user query

Assistant Messages:
- Previous assistant responses
```

**Example Prompt Structure:**
```
System: You are SmartAdvisor, an internal business assistant.
You are operating in the role of: Sales Advisor
You are in Sales mode.
Follow these instructions:
- Focus on customer needs and value proposition
- Be consultative and solution-oriented
- Highlight benefits and ROI
Company Name: Acme Corp
Target Audience: Enterprise customers

Important: Do not mention that you are an AI, model name, tokens, or any technical details.

User: What are our pricing options?
```

## Error Handling

### Error Categories

1. **LLM Service Errors**
   - API failures
   - Rate limiting
   - Invalid API keys
   - Network issues
   - **Response**: Generic error message to user, detailed error logged

2. **Context Errors**
   - Invalid JSON format
   - Missing required fields
   - **Response**: Validation error with helpful message

3. **Database Errors**
   - Connection failures
   - Query errors
   - **Response**: Graceful degradation, errors logged

4. **Frontend Errors**
   - Network failures
   - API errors
   - **Response**: User-friendly error messages

### Error Handling Strategy

- All errors logged with full details
- User-facing errors are generic (no technical details)
- System continues operating when possible
- Critical errors trigger alerts

## Security & Privacy Considerations

### Security Measures

1. **API Key Protection**
   - Keys stored in `.env` files (not in code)
   - `.env` files in `.gitignore`
   - Keys never exposed to frontend

2. **CORS Configuration**
   - Restricted to configured origins
   - Prevents unauthorized frontend access

3. **Input Validation**
   - All inputs validated via Pydantic models
   - JSON context validated before use
   - SQL injection prevention via ORM

4. **Rate Limiting** (Recommended for production)
   - Implement middleware for rate limiting
   - Protect against abuse

### Privacy Considerations

1. **Data Storage**
   - Conversations logged for audit
   - No sensitive PII stored unless explicitly provided
   - Data retention policies configurable

2. **Data Transmission**
   - HTTPS recommended for production
   - Sensitive data encrypted in transit

3. **LLM Provider Privacy**
   - Consider data residency requirements
   - Review LLM provider privacy policies
   - Option to use self-hosted models

4. **Access Control** (Recommended for production)
   - Implement authentication/authorization
   - Role-based access control
   - Session management

### Recommendations for Production

1. **Authentication**: Add JWT or OAuth2 authentication
2. **Authorization**: Implement role-based access control
3. **HTTPS**: Use SSL/TLS certificates
4. **Rate Limiting**: Implement request rate limiting
5. **Data Encryption**: Encrypt sensitive data at rest
6. **Audit Trail**: Enhanced logging for compliance
7. **Monitoring**: Add application monitoring (e.g., Prometheus, Grafana)

## Scalability Considerations

### Current Design

- Single instance architecture
- SQLite database (suitable for small teams)
- In-memory context storage

### Scaling Recommendations

1. **Horizontal Scaling**
   - Use shared database (PostgreSQL, MySQL)
   - Session state in Redis
   - Load balancer for multiple instances

2. **Context Storage**
   - Move context to database or Redis
   - Support distributed context updates

3. **Caching**
   - Cache frequently used presets
   - Cache common queries (if applicable)

4. **Async Processing**
   - Queue long-running requests
   - WebSocket for real-time updates

## Deployment

### Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Production

1. **Backend**
   - Use production ASGI server (Gunicorn with Uvicorn workers)
   - Environment variables for configuration
   - Database migration scripts
   - Process manager (systemd, supervisor)

2. **Frontend**
   - Build static files: `npm run build`
   - Serve via Nginx or CDN
   - Configure proxy for API calls

3. **Database**
   - Use production database (PostgreSQL recommended)
   - Regular backups
   - Migration strategy

## Future Enhancements

1. **Multi-step Workflows**
   - Agent-like behavior with tool calling
   - Task decomposition
   - Workflow orchestration

2. **Advanced Features**
   - File upload and processing
   - Document search and retrieval
   - Integration with business systems

3. **Analytics**
   - Usage analytics dashboard
   - Query analysis
   - Context effectiveness metrics

4. **Enterprise Features**
   - SSO integration
   - Advanced access control
   - Compliance features
   - Multi-tenancy support

## Conclusion

SmartAdvisor provides a clean, secure, and scalable architecture for an internal business assistant. The design separates concerns, maintains flexibility for context management, and provides a foundation for future enhancements while keeping the user experience simple and intuitive.

