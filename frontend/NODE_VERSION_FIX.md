# Node.js Version Compatibility Issue

## Problem
You're running Node.js v14.17.2, but Vite requires Node.js 14.18.0+ or 16+.

## Solutions

### Option 1: Upgrade Node.js (Recommended)

Upgrade to Node.js 18 LTS or 20 LTS:

**Using nvm (Node Version Manager):**
```bash
# Install nvm if you don't have it
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install and use Node.js 18
nvm install 18
nvm use 18

# Verify version
node --version
```

**Or download from nodejs.org:**
- Visit https://nodejs.org/
- Download Node.js 18 LTS or 20 LTS
- Install the package

### Option 2: Use npm with ignore engines (Workaround)

Try installing with the ignore engines flag:
```bash
npm install --ignore-engines
```

Then try running:
```bash
npm run dev
```

Note: This may still cause issues if dependencies use features not available in Node 14.17.

### Option 3: Use a different build tool

If upgrading Node.js is not possible, we can switch to Create React App which has better Node 14 support.

## Recommended Action

**Upgrade to Node.js 18 LTS** - This is the recommended solution as it:
- Provides better compatibility
- Includes security updates
- Is the current LTS version
- Will work with all modern frontend tools

