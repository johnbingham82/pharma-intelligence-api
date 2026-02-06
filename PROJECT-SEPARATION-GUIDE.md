# Project Separation Guide

## ⚠️ CRITICAL: Two Different Projects in Same Repository

---

## Quick Reference

| Aspect | Pharma Intelligence API | Novartis NHS Project |
|--------|------------------------|----------------------|
| **Purpose** | Multi-country pharma data platform | NHS CWP proposal generator |
| **Location** | Repository ROOT | `novartis-nhs-project/` subdirectory |
| **Tech** | Python + Node.js + React | React SPA + Vercel serverless |
| **Deployment** | Git-connected (auto) | Manual Vercel CLI only |
| **Work From** | `/Users/administrator/.openclaw/workspace/` | `/Users/administrator/.openclaw/workspace/novartis-nhs-project/` |
| **Git Repo** | `pharma-intelligence-api` | Same repo (subdirectory) |
| **Production** | Various (AWS, Heroku, etc.) | https://novartis-nhs-project.vercel.app |

---

## Before Starting Work: Check Which Project!

### How to Identify Current Project

```bash
pwd
# If output is: /Users/administrator/.openclaw/workspace
# → You're in PHARMA INTELLIGENCE root

# If output is: /Users/administrator/.openclaw/workspace/novartis-nhs-project
# → You're in NOVARTIS NHS PROJECT
```

### Quick Visual Check
```bash
ls -la | head -20
# Pharma Intelligence: See .py files, api/, frontend/, pbs_data/
# Novartis NHS: See index.html, server.js, api/, vercel.json
```

---

## Pharma Intelligence API (Root Level)

### Location
```bash
cd /Users/administrator/.openclaw/workspace
```

### Key Indicators You're in Right Project
- ✅ See `.py` files (data_sources_*.py, analyze_*.py, etc.)
- ✅ See `frontend/` directory with React dashboard
- ✅ See `pbs_data/` directory
- ✅ See many `.md` documentation files
- ✅ No `vercel.json` at this level

### What It Does
- Fetches pharmaceutical prescribing data from 9 countries
- APIs for UK (OpenPrescribing), US (CMS), France (Open Medic), etc.
- Backend Express API + React frontend dashboard
- Python data processing scripts

### Deployment
- Git-connected (pushes auto-deploy)
- Multiple platforms (AWS, Heroku)
- Standard CI/CD workflow

---

## Novartis NHS Project (Subdirectory)

### Location
```bash
cd /Users/administrator/.openclaw/workspace/novartis-nhs-project
```

### Key Indicators You're in Right Project
- ✅ See `index.html` (large file, 90KB+)
- ✅ See `vercel.json`
- ✅ See `api/` directory with serverless functions
- ✅ See `.vercel/` directory
- ✅ See `package.json` (Node.js dependencies)
- ✅ NO `.py` files

### What It Does
- Web app for NHS Confed Expo 2026
- AI-powered proposal generator using Claude
- Adaptive conversation flow
- Generates personalized NHS transformation stories

### Deployment (⚠️ SPECIAL PROCESS)
**NOT Git-connected!** Must deploy manually:
```bash
cd novartis-nhs-project
vercel --prod --yes
```

### Verify Deployment
```bash
curl https://novartis-nhs-project.vercel.app/api/status
# Should return: {"status":"operational",...}
```

---

## Common Confusion Scenarios

### Scenario 1: Made changes but site didn't update
**Likely cause:** You're in Novartis NHS Project and forgot to run `vercel --prod`

**Solution:**
```bash
cd novartis-nhs-project
vercel --prod --yes
```

### Scenario 2: Git push didn't trigger deployment
**Check:** Are you working on Novartis NHS Project?
- Novartis NHS is NOT connected to Git deployment
- Only manual Vercel CLI deployment works

### Scenario 3: Can't find expected files
**Check:** Are you in the right directory?
```bash
pwd  # Check current directory
ls   # List files - do they match the project?
```

---

## File Structure Overview

```
pharma-intelligence-api/                    # Git repo root
│
├── PHARMA INTELLIGENCE PROJECT FILES       # Project 1 (root level)
├── api/                                    # Express API routes
├── frontend/                               # React dashboard
├── data_sources_*.py                       # Data fetchers
├── test_*.py                               # Tests
├── *.md                                    # Docs
├── pbs_data/                               # Australia data
├── ...many other files...
│
└── novartis-nhs-project/                   # Project 2 (subdirectory)
    ├── index.html                          # Main SPA (1,957 lines)
    ├── server.js                           # Backend reference
    ├── enhance-conversation.js             # Helpers
    ├── package.json                        # Dependencies
    ├── vercel.json                         # Vercel config
    ├── .env                                # API keys (DO NOT COMMIT)
    ├── .vercel/                            # Vercel metadata
    └── api/                                # Serverless functions
        ├── generate-proposal.js            # Claude API integration
        └── status.js                       # Health check
```

---

## Switching Between Projects

### To Pharma Intelligence
```bash
cd /Users/administrator/.openclaw/workspace
ls *.py  # Should see Python files
```

### To Novartis NHS
```bash
cd /Users/administrator/.openclaw/workspace/novartis-nhs-project
ls index.html  # Should exist
```

### Both Share Same Git
```bash
# From either location:
git status  # Shows all changes in repo
git commit  # Commits from root OR subdirectory both go to same repo
```

---

## Emergency Checklist

### If Something Seems Wrong

1. **Check location:**
   ```bash
   pwd
   ls -la | head -10
   ```

2. **Check Git status:**
   ```bash
   git status
   git branch
   ```

3. **If Novartis NHS, check deployment:**
   ```bash
   curl https://novartis-nhs-project.vercel.app/api/status
   ```

4. **If just made changes to Novartis NHS:**
   ```bash
   cd novartis-nhs-project
   vercel --prod --yes
   ```

---

## Key Takeaway

🔴 **PHARMA INTELLIGENCE** = Root directory, Git-connected deployment
🔵 **NOVARTIS NHS** = Subdirectory, manual Vercel deployment

**Always check `pwd` before working!**
