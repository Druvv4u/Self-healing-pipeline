# 🔥 Self-Healing CI/CD Pipeline

> Intelligent infrastructure that detects failures, 
> diagnoses root cause using AI, and heals itself.
> Zero human involvement.

## 🏗️ Architecture
Push code → Tests run → Deploy to AWS EC2 → 
Health monitor watches → Failure detected → 
AI diagnoses → Auto restart → Back online

## ⚡ What It Does
- ✅ Automated testing on every push
- ✅ Auto-deploy to AWS EC2 via GitHub Actions
- ✅ Health check every 10 seconds
- ✅ AI-powered root cause analysis (Groq Llama 3.3)
- ✅ Auto-restart on failure
- ✅ Zero manual incident response

## 🛠️ Stack
Python · Flask · Docker · GitHub Actions · 
AWS EC2 · Groq AI · Bash

## 📊 Impact
| Metric | Before | After |
|--------|--------|-------|
| Incident detection | Manual | 30 seconds |
| Root cause analysis | 30-60 mins | 10 seconds |
| Recovery | Manual | Automatic |
| Human involvement | Required | Zero |

## 🚀 How It Works
1. Code pushed to GitHub
2. GitHub Actions runs tests
3. If tests pass → deploys to EC2
4. Health monitor pings /health every 10s
5. Failure detected → logs captured
6. Logs sent to Groq AI
7. AI returns root cause + fixes
8. Container auto-restarts
9. Back online in < 60 seconds