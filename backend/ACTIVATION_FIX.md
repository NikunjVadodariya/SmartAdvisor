# Virtual Environment Activation Fix

## Issue
The `venv/bin/activate` script had incorrect permissions, causing "permission denied" errors.

## Fix Applied
1. Added execute permissions to the activate script
2. Updated `run.sh` to automatically fix permissions when creating or using the venv

## How to Activate the Virtual Environment

### Method 1: Using the startup script (Recommended)
```bash
cd backend
./run.sh
```

This script will:
- Create venv if it doesn't exist
- Fix permissions automatically
- Activate the environment
- Install dependencies
- Start the server

### Method 2: Manual activation
```bash
cd backend
source venv/bin/activate
```

### Method 3: If permissions are still an issue
```bash
cd backend
chmod +x venv/bin/activate
source venv/bin/activate
```

## Verify Activation

After activating, you should see `(venv)` in your terminal prompt. You can verify with:
```bash
which python  # Should point to venv/bin/python
python --version
```

