"""Main FastAPI application for SmartAdvisor backend."""
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from app.config import settings
from app.context_engine import ContextEngine
from app.llm_service import LLMService
from app.models import init_db, get_db, ConversationLog, ContextPreset, ConversationSession
from app.logger import logger
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

import os


# Initialize FastAPI app
app = FastAPI(
    title="SmartAdvisor API",
    description="Internal business assistant API",
    version="1.0.0"
)

api_router = APIRouter(prefix="/api")


# FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
# FRONTEND_DIR = os.path.abspath(FRONTEND_DIR)

# INDEX_FILE = os.path.join(FRONTEND_DIR, "index.html")

FRONTEND_DIR = os.environ.get("FRONTEND_DIR") or os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend/dist")
)
INDEX_FILE = os.path.join(FRONTEND_DIR, "index.html")


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
context_engine = ContextEngine()
llm_service = LLMService()

# Initialize database
init_db()


# Request/Response models
class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict] = None
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    session_id: str


class ContextUpdateRequest(BaseModel):
    context: Dict
    merge: bool = True


class ContextPresetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    context_data: Dict


class ContextPresetResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    context_data: Dict
    created_at: datetime
    updated_at: datetime


class ConversationHistoryResponse(BaseModel):
    session_id: str
    messages: List[Dict]
    context: Optional[Dict]


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("SmartAdvisor API starting up...")
    logger.info(f"LLM Provider: {llm_service.get_provider_info()}")
    
    # Load default context presets if they exist
    db = next(get_db())
    try:
        # Check if we have default presets, if not create them
        preset_count = db.query(ContextPreset).count()
        if preset_count == 0:
            _create_default_presets(db)
            db.commit()
    except Exception as e:
        logger.error(f"Error initializing presets: {str(e)}")
        db.rollback()
    finally:
        db.close()
    
    logger.info("SmartAdvisor API ready!")


def _create_default_presets(db: Session):
    """Create default context presets."""
    default_presets = [
        {
            "name": "sales",
            "description": "Sales mode - Focus on customer acquisition and revenue",
            "context_data": {
                "role": "Sales Advisor",
                "mode": "Sales",
                "instructions": [
                    "Focus on customer needs and value proposition",
                    "Be consultative and solution-oriented",
                    "Highlight benefits and ROI",
                    "Address objections proactively"
                ]
            }
        },
        {
            "name": "technical",
            "description": "Technical mode - Focus on implementation and technical details",
            "context_data": {
                "role": "Technical Advisor",
                "mode": "Technical",
                "instructions": [
                    "Provide detailed technical information",
                    "Include code examples when relevant",
                    "Focus on best practices and architecture",
                    "Explain complex concepts clearly"
                ]
            }
        },
        {
            "name": "support",
            "description": "Support mode - Focus on customer service and problem resolution",
            "context_data": {
                "role": "Support Advisor",
                "mode": "Support",
                "instructions": [
                    "Be empathetic and patient",
                    "Focus on problem resolution",
                    "Provide clear step-by-step guidance",
                    "Ensure customer satisfaction"
                ]
            }
        }
    ]
    
    for preset_data in default_presets:
        preset = ContextPreset(**preset_data)
        db.add(preset)


# @app.get("/")
# async def root():
#     """Root endpoint."""
#     return {"message": "SmartAdvisor API is running", "version": "1.0.0"}

@api_router.get("/")
async def root():
    """Root endpoint."""
    return FileResponse(INDEX_FILE)


@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@api_router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Process a user query with optional context override.
    Returns only the processed response without LLM metadata.
    """
    try:
        logger.info(f"Processing query: {request.query[:100]}...")
        
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        session = db.query(ConversationSession).filter(
            ConversationSession.session_id == session_id
        ).first()
        
        if not session:
            session = ConversationSession(
                session_id=session_id,
                context=context_engine.get_context(),
                messages=[]
            )
            db.add(session)
            db.commit()
            db.refresh(session)
        
        # Build messages with context and history
        conversation_history = session.messages if session.messages else []
        messages = context_engine.build_chat_messages(
            user_query=request.query,
            context_override=request.context,
            conversation_history=conversation_history[-10:]  # Last 10 messages for context
        )
        
        # Generate response from LLM
        response_text = await llm_service.generate_response(messages)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": request.query})
        conversation_history.append({"role": "assistant", "content": response_text})
        session.messages = conversation_history
        session.updated_at = datetime.utcnow()
        
        # Update context if override provided
        if request.context:
            context_engine.update_context(request.context, merge=True)
            session.context = context_engine.get_context()
        
        db.commit()
        
        # Log the interaction for audit
        log_entry = ConversationLog(
            timestamp=datetime.utcnow(),
            user_query=request.query,
            context_used=request.context or context_engine.get_context(),
            response=response_text,
            session_id=session_id
        )
        db.add(log_entry)
        db.commit()
        
        logger.info(f"Query processed successfully for session: {session_id}")
        
        return QueryResponse(
            response=response_text,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@api_router.get("/context")
async def get_context():
    """Get the current business context."""
    return {"context": context_engine.get_context()}


@api_router.post("/context")
async def update_context(request: ContextUpdateRequest):
    """Update the business context dynamically."""
    try:
        context_engine.update_context(request.context, merge=request.merge)
        logger.info(f"Context updated: {list(request.context.keys())}")
        return {"message": "Context updated successfully", "context": context_engine.get_context()}
    except Exception as e:
        logger.error(f"Error updating context: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.delete("/context")
async def clear_context():
    """Clear the current business context."""
    context_engine.clear_context()
    logger.info("Context cleared")
    return {"message": "Context cleared successfully"}


@api_router.get("/presets", response_model=List[ContextPresetResponse])
async def get_presets(db: Session = Depends(get_db)):
    """Get all available context presets."""
    presets = db.query(ContextPreset).all()
    return [
        ContextPresetResponse(
            id=preset.id,
            name=preset.name,
            description=preset.description,
            context_data=preset.context_data,
            created_at=preset.created_at,
            updated_at=preset.updated_at
        )
        for preset in presets
    ]


@api_router.post("/presets", response_model=ContextPresetResponse)
async def create_preset(preset: ContextPresetCreate, db: Session = Depends(get_db)):
    """Create a new context preset."""
    try:
        db_preset = ContextPreset(
            name=preset.name,
            description=preset.description,
            context_data=preset.context_data
        )
        db.add(db_preset)
        db.commit()
        db.refresh(db_preset)
        logger.info(f"Created preset: {preset.name}")
        return ContextPresetResponse(
            id=db_preset.id,
            name=db_preset.name,
            description=db_preset.description,
            context_data=db_preset.context_data,
            created_at=db_preset.created_at,
            updated_at=db_preset.updated_at
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating preset: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/presets/{preset_name}/apply")
async def apply_preset(preset_name: str, db: Session = Depends(get_db)):
    """Apply a context preset."""
    preset = db.query(ContextPreset).filter(ContextPreset.name == preset_name).first()
    if not preset:
        raise HTTPException(status_code=404, detail=f"Preset '{preset_name}' not found")
    
    context_engine.update_context(preset.context_data, merge=False)
    logger.info(f"Applied preset: {preset_name}")
    return {"message": f"Preset '{preset_name}' applied", "context": context_engine.get_context()}


@api_router.get("/conversations/{session_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(session_id: str, db: Session = Depends(get_db)):
    """Get conversation history for a session."""
    session = db.query(ConversationSession).filter(
        ConversationSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return ConversationHistoryResponse(
        session_id=session.session_id,
        messages=session.messages or [],
        context=session.context
    )


@api_router.delete("/conversations/{session_id}")
async def delete_conversation(session_id: str, db: Session = Depends(get_db)):
    """Delete a conversation session."""
    session = db.query(ConversationSession).filter(
        ConversationSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    logger.info(f"Deleted session: {session_id}")
    return {"message": "Session deleted successfully"}

app.include_router(api_router)   # <- important: include router BEFORE mounting static files

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)

