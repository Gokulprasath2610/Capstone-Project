# Multi-Agent Agentic AI System for Loan Approval

A comprehensive implementation of a distributed, microservices-based Multi-Agent system for automating loan application analysis and decision-making using Anthropic's Claude AI.

## 📋 System Overview

This system automates loan application evaluation through specialized agents that collaborate in a LangGraph-orchestrated workflow:

1. **Applicant Profile Agent** - Analyzes income stability, employment risk, and credit history
2. **Financial Risk Agent** - Calculates debt-to-income ratios and identifies anomalies
3. **Loan Decision Agent** - Synthesizes decisions using Claude AI
4. **Compliance & Action Orchestrator** - Executes notifications and generates case IDs

## 🏗️ Architecture

```
┌─────────────────────┐
│  Streamlit UI       │  (Web Interface)
└──────────┬──────────┘
           │
┌──────────▼──────────────────┐
│  FastAPI Microservice       │  (REST API)
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────────────┐
│  LangGraph Orchestration Engine      │  (Workflow Coordinator)
└──────────┬──────────────────────────┘
           │
    ┌──────┼──────┬──────────┐
    │      │      │          │
┌───▼──┐ ┌─▼──┐ ┌─▼─────┐ ┌─▼──────────┐
│Agent1│ │Ag2 │ │Agent3 │ │Agent4      │
│(App) │ │(Fi)│ │(Decn) │ │(Comply)    │
└──────┘ └────┘ └───────┘ └────────────┘
    │      │      │          │
    └──────┼──────┼──────────┘
           │
    ┌──────▼─────────────────┐
    │  Claude Sonnet 4.6     │  (LLM)
    └────────────────────────┘
```

## 📦 Components

### 1. **mcp_servers.py** - MCP (Model Context Protocol) Servers
- **ApplicantDB Server** - Profiles and flags applicant data
- **RiskRulesDB Server** - Calculates financial risk metrics
- **DecisionSynthesis Server** - Synthesizes loan decisions
- **NotificationSystem Server** - Manages compliance actions

### 2. **orchestration_engine.py** - LangGraph Workflow
- Defines `LoanEvaluationState` TypedDict for state management
- Four sequential agents coordinated by LangGraph
- Claude AI integration for intelligent decision synthesis
- Full audit trail and explainability

### 3. **fastapi_service.py** - REST Microservice
- `/api/submit-application` - Process new applications
- `/api/application-status/{id}` - Check application status
- `/api/applications` - List all processed applications
- CORS enabled for Streamlit frontend

### 4. **streamlit_app.py** - User Interface
- Submit applications with form validation
- Check application status by ID
- View all processed applications
- Real-time decision display with styling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Anthropic API Key ([Get one here](https://console.anthropic.com))
- pip or conda

### Installation

1. **Clone/navigate to project directory:**
```bash
cd /path/to/capstone\ project
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# Linux/Mac
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows
set ANTHROPIC_API_KEY=your-api-key-here
```

Or update `.env` file:
```
ANTHROPIC_API_KEY=your_api_key_here
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
STREAMLIT_PORT=8501
```

### Running the System

**Option 1: Using the start script (Linux/Mac)**
```bash
chmod +x start_services.sh
./start_services.sh
```

**Option 2: Manual startup (all platforms)**

Terminal 1 - FastAPI Service:
```bash
python fastapi_service.py
```

Terminal 2 - Streamlit UI:
```bash
streamlit run streamlit_app.py
```

The system will be available at:
- **Streamlit UI**: http://127.0.0.1:8501
- **FastAPI API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## 📊 Usage Example

### Via Streamlit UI

1. Navigate to http://127.0.0.1:8501
2. Fill in application details:
   - Applicant ID: APP-001
   - Age: 35
   - Annual Income: $75,000
   - Employment Type: Salaried
   - Credit Score: 750
   - Loan Amount: $150,000
   - Loan Tenure: 5 years
   - Existing Liabilities: $50,000
   - Location: New York
3. Click "Submit Application"
4. View instant decision with explanation

### Via API (cURL)

```bash
curl -X POST http://127.0.0.1:8000/api/submit-application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP-001",
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

### Via Python

```python
import requests

data = {
    "applicant_id": "APP-001",
    "age": 35,
    "income": 75000,
    "employment_type": "Salaried",
    "credit_score": 750,
    "loan_amount": 150000,
    "loan_tenure": 5,
    "existing_liabilities": 50000,
    "location": "New York"
}

response = requests.post(
    "http://127.0.0.1:8000/api/submit-application",
    json=data
)

print(response.json())
```

## 🔄 Workflow Explanation

### Step 1: Application Submission
User submits loan application data via Streamlit UI or API.

### Step 2: Applicant Profile Analysis
- Calculates income stability score (0-1)
- Determines employment risk level
- Summarizes credit history
- Flags completeness issues

### Step 3: Financial Risk Analysis
- Computes debt-to-income ratio
- Assesses credit score risk
- Evaluates loan amount risk
- Detects anomalies

### Step 4: Decision Synthesis
Claude AI synthesizes a decision based on:
- All agent outputs
- Risk metrics
- Compliance requirements

Possible decisions:
- **Approve**: Low risk (<25 score)
- **Review**: Medium risk (25-70 score)
- **Reject**: High risk (>70 score)

### Step 5: Compliance & Notification
- Generates unique case ID
- Logs timestamp
- Sends notification
- Records action taken

## 📈 Example Responses

### Approved Application
```json
{
  "applicant_id": "APP-001",
  "status": "processed",
  "decision": "Approve",
  "risk_score": 22.5,
  "confidence_level": 0.95,
  "explanation": "Strong financial profile with low risk indicators",
  "case_id": "CASE-APP-001-20240617120530",
  "timestamp": "2024-06-17T12:05:30.123456",
  "key_factors": [
    "Good credit score",
    "Reasonable DTI ratio",
    "Stable employment"
  ]
}
```

### Rejected Application
```json
{
  "applicant_id": "APP-002",
  "status": "processed",
  "decision": "Reject",
  "risk_score": 78.5,
  "confidence_level": 0.92,
  "explanation": "High credit risk combined with excessive debt load",
  "case_id": "CASE-APP-002-20240617120600",
  "timestamp": "2024-06-17T12:06:00.123456",
  "key_factors": [
    "Low credit score",
    "Very high DTI ratio",
    "High existing liabilities"
  ]
}
```

## 🧪 Testing

### Test Scenarios

**Scenario 1: Strong Applicant (Should Approve)**
```
Age: 35, Income: $150k, Employment: Salaried, Credit: 800, 
Loan: $100k, Liabilities: $20k
```

**Scenario 2: Weak Applicant (Should Reject)**
```
Age: 28, Income: $30k, Employment: Unemployed, Credit: 500,
Loan: $150k, Liabilities: $80k
```

**Scenario 3: Borderline (Should Review)**
```
Age: 45, Income: $65k, Employment: Self-Employed, Credit: 650,
Loan: $120k, Liabilities: $60k
```

## 🔐 Security Considerations

- API keys stored in `.env` (never commit to git)
- CORS configured for localhost
- Input validation via Pydantic
- Audit trail via Case IDs and timestamps
- All decisions traceable and explainable

## 📚 Technology Stack

| Component | Technology |
|-----------|-----------|
| UI | Streamlit |
| API | FastAPI + Uvicorn |
| Orchestration | LangGraph |
| LLM | Claude Sonnet 4.6 |
| MCP | FastMCP |
| Language | Python 3.8+ |

## 🎯 Key Features

✅ **Multi-Agent Architecture** - Specialized agents for each domain
✅ **LangGraph Orchestration** - Deterministic workflow coordination
✅ **Claude AI Integration** - Intelligent decision synthesis
✅ **Explainable AI** - Clear reasoning for every decision
✅ **Microservices Design** - Loosely coupled, independently deployable
✅ **REST API** - Standard HTTP interface for integration
✅ **User-Friendly UI** - Streamlit for quick prototyping
✅ **Audit Trail** - Case IDs and timestamps for compliance
✅ **Scalable** - Ready for production deployment

## 📝 Notes for Evaluation

### Live Code Walkthrough Points

1. **Orchestration Layer** (`orchestration_engine.py`)
   - Show LangGraph state management
   - Explain sequential agent invocation
   - Demonstrate Claude integration

2. **Agent Responsibilities**
   - Each agent's specific role
   - Input/output contracts
   - State updates

3. **Explainability**
   - Decision factors clearly listed
   - Risk scores calculated transparently
   - Reasoning accessible via API

4. **Scalability**
   - Microservices architecture
   - Stateless API design
   - Can add more agents easily

## 🔄 Future Enhancements

- [ ] Database persistence for production
- [ ] Authentication and authorization
- [ ] Rate limiting and request throttling
- [ ] Monitoring and logging dashboards
- [ ] Additional agents (fraud detection, market analysis)
- [ ] Batch processing capabilities
- [ ] A/B testing framework for decision rules
- [ ] Model versioning and rollback

## 📞 Support

For issues or questions:
1. Check API logs in terminal
2. Verify Anthropic API key is set
3. Ensure FastAPI service is running
4. Check Streamlit logs

## 📄 License

This project is created for educational and evaluation purposes.
