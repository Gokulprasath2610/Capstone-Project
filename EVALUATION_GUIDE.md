# Evaluation & Live Code Walkthrough Guide

This document provides a structured walkthrough for the technical evaluation of the Multi-Agent Agentic AI Loan Approval System.

## 📋 Pre-Evaluation Checklist

- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] API key set: `export ANTHROPIC_API_KEY="your-key"`
- [ ] FastAPI service ready: `python fastapi_service.py`
- [ ] Streamlit UI ready: `streamlit run streamlit_app.py`
- [ ] Test script verified: `python test_system.py`

## 🎯 Evaluation Areas & Walkthrough

### 1. **Understanding of Agentic AI Architecture** (15 mins)

#### Key Points to Demonstrate:

**A. System Design Overview**
- Start with: `README.md` architecture diagram
- Explain the 4-layer stack:
  1. Presentation Layer (Streamlit)
  2. Microservice Layer (FastAPI)
  3. Orchestration Layer (LangGraph)
  4. Agent Layer (Domain-specific agents)

**B. Multi-Agent Pattern**
- Open: `orchestration_engine.py`
- Show the 4 agents and their responsibilities:
  ```
  applicant_profile_agent     → Income stability, employment risk
  financial_risk_agent        → DTI, credit risk, anomalies
  decision_agent              → Claude AI decision synthesis
  compliance_action_agent     → Notifications and case IDs
  ```

**C. Separation of Concerns**
- Each agent has a single responsibility
- Agents communicate via state (LoanEvaluationState)
- No direct agent-to-agent calls (loosely coupled)

---

### 2. **Correct Orchestration Using LangGraph** (20 mins)

#### Code Walkthrough: `orchestration_engine.py`

**Show this code block:**
```python
def create_orchestration_graph():
    graph = StateGraph(LoanEvaluationState)
    
    # Add nodes (agents)
    graph.add_node("applicant_profile", applicant_profile_agent)
    graph.add_node("financial_risk", financial_risk_agent)
    graph.add_node("decision", decision_agent)
    graph.add_node("compliance", compliance_action_agent)
    
    # Add edges (workflow)
    graph.add_edge("applicant_profile", "financial_risk")
    graph.add_edge("financial_risk", "decision")
    graph.add_edge("decision", "compliance")
    graph.set_entry_point("applicant_profile")
    graph.set_finish_point("finalize")
    
    return graph.compile()
```

**Explain:**
1. **StateGraph**: Manages state throughout workflow
2. **Nodes**: Each agent is a node
3. **Edges**: Define sequential workflow
4. **Entry/Exit**: Clear flow control

**Demonstrate Workflow:**
1. Show `LoanEvaluationState` TypedDict
2. Explain state evolution:
   - Initial: Empty fields
   - After applicant_profile: applicant_profile field populated
   - After financial_risk: financial_risk field populated
   - After decision: decision field populated
   - After compliance: compliance_action field populated

**Key Advantages:**
- ✅ Deterministic flow (no branching chaos)
- ✅ State visibility (inspect at each step)
- ✅ Easy to modify (add/remove agents)
- ✅ Debugging friendly (clear execution trail)

---

### 3. **Clear Agent Responsibilities & MCP Usage** (15 mins)

#### Agent Breakdown

**Agent 1: Applicant Profile Agent**
- **Input**: applicant_id, age, income, employment_type, credit_score
- **Output**: 
  - income_stability_score (0-1)
  - employment_risk (Low/Medium/High/Very High)
  - credit_history_summary
  - application_completeness_flags
- **Logic**: Rule-based assessment (deterministic)

**Agent 2: Financial Risk Agent**
- **Input**: income, existing_liabilities, loan_amount, tenure, credit_score
- **Output**:
  - debt_to_income_ratio
  - credit_score_risk_level
  - loan_amount_risk
  - anomaly_flags
  - reasoning
- **Logic**: Financial calculations + threshold-based assessment

**Agent 3: Decision Agent**
- **Input**: All previous agent outputs + applicant data
- **Output**:
  - classification (Approve/Reject/Review)
  - risk_score (0-100)
  - confidence_level (0-1)
  - key_decision_factors
  - explanation
- **Logic**: Claude AI synthesizes decision using prompt engineering

**Agent 4: Compliance Agent**
- **Input**: classification, risk_score, applicant_id
- **Output**:
  - action_taken
  - notification_sent
  - case_id (unique identifier)
  - timestamp
  - summary
- **Logic**: Audit trail generation

#### MCP Integration Points

**In production**, MCP servers would be:
```
ApplicantDB Server      ← Agent 1 queries here
RiskRulesDB Server      ← Agent 2 queries here
DecisionSynthesis       ← Agent 3 calls here
NotificationSystem      ← Agent 4 calls here
```

**Current implementation**: Agents contain logic directly
**In `mcp_servers.py`**: Server stubs ready for FastMCP deployment

---

### 4. **Ability to Modify Code Live** (20 mins)

Demonstrate quick modifications:

#### Modification 1: Change Decision Thresholds
File: `orchestration_engine.py`, line ~180

**Before:**
```python
if risk_score < 25:
    classification = "Approve"
elif risk_score < 50:
    classification = "Approve"
elif risk_score < 70:
    classification = "Review"
else:
    classification = "Reject"
```

**Change to stricter approval:**
```python
if risk_score < 15:
    classification = "Approve"
elif risk_score < 40:
    classification = "Review"
else:
    classification = "Reject"
```

**Test**: Rerun `python test_system.py` - see decisions change

#### Modification 2: Add New Risk Factor
File: `orchestration_engine.py`, financial_risk_agent

**Add:**
```python
# New: Age-based risk (example)
if state["age"] > 65:
    state["financial_risk"]["anomaly_flags"].append("Age risk: >65 years")
```

**Retest**: Run system and see new flags appear

#### Modification 3: Change Agent Order
File: `orchestration_engine.py`, create_orchestration_graph()

**Show parallelization potential:**
```python
# Could do financial_risk and applicant_profile in parallel:
graph.add_edge("applicant_profile", "decision")
graph.add_edge("financial_risk", "decision")
# But we keep sequential for clarity in this implementation
```

---

### 5. **Explainable AI Outputs** (15 mins)

#### Demonstrate via API Response

**Run test:**
```bash
python test_system.py
```

**Show response structure:**
```json
{
  "applicant_id": "APP-STRONG-001",
  "status": "processed",
  "decision": "Approve",
  "risk_score": 22.5,
  "confidence_level": 0.95,
  "explanation": "Strong financial profile with low risk indicators",
  "case_id": "CASE-APP-STRONG-001-20240617120530",
  "timestamp": "2024-06-17T12:05:30.123456",
  "key_factors": [
    "Good credit score",
    "Reasonable DTI ratio",
    "Stable employment"
  ]
}
```

**Explainability Features:**
1. **Risk Score**: Numeric scale (0-100) explains severity
2. **Confidence Level**: Shows decision certainty (0-1)
3. **Key Factors**: Top 3 decision drivers listed
4. **Explanation**: Human-readable summary
5. **Case ID**: Audit trail identifier
6. **Timestamp**: When decision was made

#### Show Decision Factors Calculation

**In code** (`orchestration_engine.py`):
```python
# Risk score is calculated transparently:
# - Employment risk: +30 points
# - Credit risk: +25 points
# - Loan risk: +20 points
# - DTI ratio: +15 points
# - Income stability: +20 points (based on 1-stability)
# - Flags: +5 per flag
# Total: Summed and capped at 100
```

---

## 🧪 Live Testing & Demonstration

### Test Scenario 1: Approve Decision

**Command:**
```bash
python test_system.py
```

**Test case shows:**
- Strong applicant (high income, good credit)
- Low risk profile
- System recommends "Approve"
- Confidence ~95%
- Key factors support decision

### Test Scenario 2: Reject Decision

**Same test output shows:**
- Weak applicant (low income, poor credit, unemployed)
- High risk profile
- System recommends "Reject"
- Confidence ~92%
- Clear factors for rejection

### Test Scenario 3: Manual Review

**Same test shows:**
- Borderline applicant (self-employed, fair credit)
- Medium risk profile
- System recommends "Review"
- Confidence ~85%
- Needs human judgment

### Interactive Testing

**Command:**
```bash
python test_system.py single
```

**Demonstrates:**
- Real-time API interaction
- Custom input handling
- Dynamic response generation
- Full JSON output

---

## 🏗️ Architecture Highlights for Evaluation

### Microservices Design
```
✅ Stateless API endpoints
✅ Easily scalable horizontally
✅ Independent service deployment
✅ Clear service boundaries
```

### LangGraph Benefits
```
✅ Deterministic workflow execution
✅ Full state traceability
✅ Easy debugging (inspect state after each node)
✅ Simple to add/remove agents
✅ Visual workflow representation
```

### Explainability
```
✅ Risk scores calculated step-by-step
✅ Each decision factor explained
✅ Confidence levels transparent
✅ Audit trail via Case IDs
✅ Claude AI reasoning visible
```

---

## 📊 Performance Notes

### Current Metrics
- **Average decision time**: 2-5 seconds (includes Claude API latency)
- **API response size**: ~500 bytes
- **State size**: ~2KB per application
- **Concurrent capacity**: Determined by FastAPI + Claude rate limits

### Scalability Improvements (Optional Discussion)
1. **Caching**: Cache applicant profiles by ID
2. **Async agents**: Run non-dependent agents in parallel
3. **Batch processing**: Process multiple applications together
4. **Database**: Store results for audit trail
5. **Monitoring**: Add logging/metrics collection

---

## 🔍 Code Review Checklist

**During evaluation, highlight:**

- [ ] Separation of concerns (each agent has 1 responsibility)
- [ ] State-based communication (no tight coupling)
- [ ] Claude integration (intelligent decision synthesis)
- [ ] Error handling (graceful degradation)
- [ ] Type hints (Pydantic validation)
- [ ] Documentation (docstrings on functions)
- [ ] Reproducibility (deterministic workflow)
- [ ] Auditability (case IDs, timestamps, factors)

---

## 💡 Discussion Points

**Potential questions and answers:**

**Q: Why LangGraph over just calling agents sequentially?**
A: LangGraph provides state management, visualization, error handling, and makes it trivial to add parallel agents later or modify workflow logic.

**Q: How would this scale to 10,000 applications/day?**
A: Deploy FastAPI with load balancing, add database for result storage, implement request queuing, parallelize non-dependent agents, consider batch processing.

**Q: What if Claude returns invalid JSON?**
A: Implemented fallback handling (see decision_agent function) that uses default decision when parsing fails.

**Q: How do you ensure consistency across decisions?**
A: Risk scoring algorithm is deterministic and consistent. Claude integration adds AI capability while maintaining explainability via decision factors.

**Q: Can you modify thresholds without redeploying?**
A: Yes - move thresholds to `config.py`, read from database, or use feature flags for real-time adjustment.

---

## 📈 Expected Outcomes

After evaluation, the system should demonstrate:

1. ✅ **Understanding**: Clear explanation of multi-agent pattern
2. ✅ **Implementation**: Working LangGraph orchestration
3. ✅ **Design**: Loosely coupled microservices
4. ✅ **Explainability**: Clear decision reasoning
5. ✅ **Modification**: Ability to change logic in seconds
6. ✅ **Testing**: Repeatable test scenarios with consistent results

---

## 📞 Troubleshooting During Demo

**If API fails to start:**
```bash
# Check port 8000 is free
lsof -i :8000
# Kill if needed: kill -9 <PID>
```

**If Streamlit fails:**
```bash
# Ensure FastAPI is running first
# Check port 8501
lsof -i :8501
```

**If Claude API times out:**
- Check ANTHROPIC_API_KEY is set
- Verify internet connection
- Retry operation (may be rate limited)

**If tests fail unexpectedly:**
```bash
# Run with verbose output
python test_system.py 2>&1 | tee test_output.log
```

---

## 🎬 Demo Script (5-minute version)

1. **Start services** (30 sec)
   - `python fastapi_service.py &`
   - `streamlit run streamlit_app.py`

2. **Show architecture** (1 min)
   - Open README.md, explain 4 layers
   - Point out separation of concerns

3. **Code walkthrough** (2 mins)
   - orchestration_engine.py - show LangGraph flow
   - Explain state evolution through agents

4. **Live test** (1 min)
   - Run `python test_system.py`
   - Show decision results and explainability

5. **UI demo** (30 sec)
   - Open Streamlit browser
   - Submit sample application
   - Show instant decision

---

**Total Demo Time**: ~5 minutes with deep-dive capability to 30 minutes for detailed evaluation.
