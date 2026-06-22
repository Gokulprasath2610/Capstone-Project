# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set API Key
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
# Or update the .env file
```

### Step 3: Start Services

**Terminal 1 - FastAPI Backend:**
```bash
python fastapi_service.py
# Output: Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 - Streamlit Frontend:**
```bash
streamlit run streamlit_app.py
# Output: You can now view your Streamlit app in your browser at http://127.0.0.1:8501
```

### Step 4: Use the System

**Option A - Web UI:**
- Open browser to http://127.0.0.1:8501
- Fill form → Submit → Get decision

**Option B - Run Tests:**
```bash
python test_system.py
```

**Option C - API Only:**
```bash
curl -X POST http://127.0.0.1:8000/api/submit-application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST-001",
    "age": 35,
    "income": 75000,
    "employment_type": "Salaried",
    "credit_score": 750,
    "loan_amount": 150000,
    "loan_tenure": 5,
    "existing_liabilities": 50000,
    "location": "New York"
  }'
```

## 📁 Project Files

```
├── requirements.txt                 # Python dependencies
├── .env                            # Configuration (set your API key here)
├── config.py                       # System configuration
│
├── orchestration_engine.py         # LangGraph workflow ⭐
├── fastapi_service.py             # REST API service
├── streamlit_app.py               # Web UI
├── mcp_servers.py                 # MCP server stubs
│
├── test_system.py                 # Integration tests
├── start_services.sh              # Startup script
│
├── README.md                      # Full documentation
├── QUICK_START.md                 # This file
├── EVALUATION_GUIDE.md            # Evaluation walkthrough
```

## 🔑 Key Features

- ✅ Multi-agent system with LangGraph orchestration
- ✅ Claude AI-powered decision synthesis
- ✅ Explainable loan decisions with risk scores
- ✅ REST API + Streamlit web UI
- ✅ Real-time processing (2-5 seconds per decision)

## 📊 Test It

### Pre-loaded Test Cases:
```bash
python test_system.py
```

This runs 3 scenarios:
1. **Strong applicant** → Approve
2. **Weak applicant** → Reject
3. **Borderline applicant** → Review

### Interactive Test:
```bash
python test_system.py single
```

Prompts for custom input and processes.

## 🎯 Understanding the System

### How It Works:
```
User submits application
        ↓
FastAPI receives request
        ↓
LangGraph orchestrator starts
        ↓
Agent 1: Analyze applicant profile
        ↓
Agent 2: Analyze financial risk
        ↓
Agent 3: Claude makes decision
        ↓
Agent 4: Generate compliance action
        ↓
Return result to user
```

### Decision Classification:
- **Risk Score < 25** → Approve
- **Risk Score 25-70** → Review
- **Risk Score > 70** → Reject

## 🔧 API Endpoints

### Submit Application
```
POST /api/submit-application
Input: Loan application details
Output: Decision, risk score, factors
```

### Check Status
```
GET /api/application-status/{applicant_id}
Output: Previous decision result
```

### List Applications
```
GET /api/applications
Output: All processed applications
```

### Health Check
```
GET /health
Output: {"status": "healthy"}
```

## 💻 Modifying the System

### Change Decision Thresholds
File: `orchestration_engine.py` (lines ~215-230)
```python
if risk_score < 25:  # Change this number
    classification = "Approve"
```

### Add New Risk Factor
File: `orchestration_engine.py` (financial_risk_agent function)
```python
if state["age"] > 65:
    anomalies.append("Age risk detected")
```

### Change Agent Order
File: `orchestration_engine.py` (create_orchestration_graph function)
```python
graph.add_edge("agent_a", "agent_b")  # Define workflow
```

## 📝 Example Response

```json
{
  "applicant_id": "APP-001",
  "decision": "Approve",
  "risk_score": 22.5,
  "confidence_level": 0.95,
  "explanation": "Strong financial profile with low risk indicators",
  "case_id": "CASE-APP-001-20240617120530",
  "key_factors": [
    "Good credit score",
    "Reasonable DTI ratio",
    "Stable employment"
  ]
}
```

## 🚨 Troubleshooting

**"Cannot connect to API"**
- Make sure FastAPI is running: `python fastapi_service.py`

**"ANTHROPIC_API_KEY not found"**
- Set it: `export ANTHROPIC_API_KEY="your-key"`
- Or update `.env` file

**"Port 8000/8501 already in use"**
- Kill the process: `lsof -i :8000` then `kill -9 <PID>`
- Or change port in `.env`

**"ModuleNotFoundError"**
- Install dependencies: `pip install -r requirements.txt`

## 📚 Learn More

- **Full documentation**: [README.md](README.md)
- **Evaluation guide**: [EVALUATION_GUIDE.md](EVALUATION_GUIDE.md)
- **Config options**: [config.py](config.py)

## 🎓 Key Concepts

**LangGraph**: Orchestration framework for multi-agent workflows
**FastAPI**: Modern Python web framework for APIs
**Streamlit**: Rapid prototyping framework for data apps
**Claude**: Anthropic's AI model for intelligent decisions
**MCP**: Model Context Protocol for agent communication

Enjoy! 🚀
