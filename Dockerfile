# ---------- Stage 1: build frontend ----------
    FROM node:18-alpine AS frontend_builder
    WORKDIR /app/frontend
    
    # Copy only package files first (cache-friendly)
    COPY frontend/package*.json ./
    
    # Install dependencies (uses package-lock.json if present in context after next copy)
    RUN npm install
    
    # Copy the rest of the frontend sources and build
    COPY frontend/ ./
    RUN npm run build
    
    # ---------- Stage 2: build backend image and copy frontend build into it ----------
    FROM python:3.11-slim
    
    # set a non-root user (optional but recommended)
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1
    
    # Install system deps required for some Python packages + curl for health checks
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        && rm -rf /var/lib/apt/lists/*
    
    WORKDIR /app
    
    # Install Python dependencies
    # Copy requirements first to leverage Docker cache
    COPY backend/requirements.txt /app/requirements.txt
    RUN pip install --no-cache-dir -r /app/requirements.txt
    
    # Copy backend source
    COPY backend/ /app/
    
    # Copy built frontend from the previous stage into backend (so FastAPI can serve it)
    # Assumes frontend build output is at /app/frontend/dist in the frontend_builder stage
    RUN mkdir -p /app/frontend_dist
    COPY --from=frontend_builder /app/frontend/dist /app/frontend_dist
    
    # (Optional) Expose port
    EXPOSE 8000
    
    # Ensure the FastAPI app knows where to find frontend assets.
    # The default main.py examples in the conversation look for "../../frontend/dist" relative to app/main.py.
    # With this Docker layout, it's easiest to have your main.py refer to an absolute or container-relative path:
    # e.g. FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend_dist"))
    #
    # Start uvicorn
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
    