"""LangGraph-based orchestration engine for multi-agent loan evaluation workflow."""

from langgraph.graph import StateGraph
from typing import TypedDict, Annotated, Optional
import anthropic
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


# State definition for the graph
class LoanEvaluationState(TypedDict):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    loan_tenure: int
    existing_liabilities: float
    location: str

    # Results from different agents
    applicant_profile: Optional[dict]
    financial_risk: Optional[dict]
    decision: Optional[dict]
    compliance_action: Optional[dict]

    # Final outputs
    final_decision: str
    risk_score: float
    confidence_level: float
    explanation: str
    case_id: str
    key_factors: list


def create_orchestration_graph():
    """Create LangGraph workflow for loan evaluation."""

    # Initialize Anthropic client
    client = anthropic.Anthropic()

    def applicant_profile_agent(state: LoanEvaluationState) -> LoanEvaluationState:
        """Agent to analyze applicant profile, income stability, and employment risk."""
        logger.info(f"Running Applicant Profile Agent for {state['applicant_id']}")

        # Call MCP function for applicant analysis
        income_stability_map = {
            "Salaried": 0.9,
            "Self-Employed": 0.6,
            "Contract": 0.7,
            "Unemployed": 0.1
        }

        stability = income_stability_map.get(state["employment_type"], 0.5)

        employment_risk_map = {
            "Salaried": "Low",
            "Self-Employed": "High",
            "Contract": "Medium",
            "Unemployed": "Very High"
        }

        flags = []
        if state["age"] < 21:
            flags.append("Applicant below 21 years")
        elif state["age"] > 70:
            flags.append("Applicant above 70 years")
        if state["income"] < 30000:
            flags.append("Low income")

        credit_summary = "Excellent" if state["credit_score"] >= 750 else \
                        "Good" if state["credit_score"] >= 700 else \
                        "Fair" if state["credit_score"] >= 650 else "Poor"

        state["applicant_profile"] = {
            "income_stability_score": stability,
            "employment_risk": employment_risk_map.get(state["employment_type"], "Unknown"),
            "credit_history_summary": f"{credit_summary} credit history",
            "application_completeness_flags": flags
        }

        return state


    def financial_risk_agent(state: LoanEvaluationState) -> LoanEvaluationState:
        """Agent to analyze financial risk, DTI, and anomalies."""
        logger.info(f"Running Financial Risk Agent for {state['applicant_id']}")

        monthly_income = state["income"] / 12
        total_monthly_debt = (state["existing_liabilities"] / 12) + (state["loan_amount"] / state["loan_tenure"] / 12)
        dti_ratio = (total_monthly_debt / monthly_income) if monthly_income > 0 else 0

        credit_risk = "Very Low" if state["credit_score"] >= 750 else \
                     "Low" if state["credit_score"] >= 700 else \
                     "Medium" if state["credit_score"] >= 650 else \
                     "High" if state["credit_score"] >= 600 else "Very High"

        loan_risk = "Very High" if state["loan_amount"] > state["income"] * 5 else \
                   "High" if state["loan_amount"] > state["income"] * 3 else \
                   "Medium" if state["loan_amount"] > state["income"] * 1.5 else "Low"

        anomalies = []
        if dti_ratio > 0.5:
            anomalies.append(f"High DTI: {dti_ratio:.2f}")
        if state["existing_liabilities"] > state["income"] * 2:
            anomalies.append("High existing liabilities")

        state["financial_risk"] = {
            "debt_to_income_ratio": dti_ratio,
            "credit_score_risk_level": credit_risk,
            "loan_amount_risk": loan_risk,
            "anomaly_flags": anomalies,
            "reasoning": f"DTI: {dti_ratio:.2f}, Credit Risk: {credit_risk}, Loan Risk: {loan_risk}"
        }

        return state


    def decision_agent(state: LoanEvaluationState) -> LoanEvaluationState:
        """Agent to synthesize loan decision using Claude."""
        logger.info(f"Running Decision Agent for {state['applicant_id']}")

        prompt = f"""You are a loan decision agent. Based on the following analysis, make a clear loan decision (Approve, Reject, or Review).

APPLICANT DATA:
- ID: {state['applicant_id']}
- Age: {state['age']}
- Income: ${state['income']:.2f}
- Employment: {state['employment_type']}
- Credit Score: {state['credit_score']}
- Loan Amount: ${state['loan_amount']:.2f}
- Tenure: {state['loan_tenure']} years
- Existing Liabilities: ${state['existing_liabilities']:.2f}

APPLICANT PROFILE ANALYSIS:
{json.dumps(state['applicant_profile'], indent=2)}

FINANCIAL RISK ANALYSIS:
{json.dumps(state['financial_risk'], indent=2)}

Based on this analysis, provide your decision in JSON format with:
- classification: "Approve", "Reject", or "Review"
- risk_score: 0-100
- confidence_level: 0-1
- key_factors: list of top 3 factors
- explanation: brief explanation (1-2 sentences)

Respond ONLY with valid JSON."""

        try:
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            try:
                response_text = response.content[0].text
                decision_json = json.loads(response_text)
            except (json.JSONDecodeError, IndexError) as e:
                logger.warning(f"Error parsing Claude response: {e}. Using fallback decision.")
                decision_json = {
                    "classification": "Review",
                    "risk_score": 50,
                    "confidence_level": 0.5,
                    "key_factors": ["Unable to parse detailed analysis"],
                    "explanation": "Requires manual review due to analysis complexity."
                }
        except Exception as e:
            logger.warning(f"Claude API error: {str(e)[:100]}. Using deterministic decision.")
            # Fallback: Use deterministic decision logic when Claude is unavailable
            risk_score = state["financial_risk"]["debt_to_income_ratio"] * 50
            if state["financial_risk"]["credit_score_risk_level"] == "Very High":
                risk_score += 25
            elif state["financial_risk"]["credit_score_risk_level"] == "High":
                risk_score += 15

            if risk_score < 25:
                classification = "Approve"
                confidence = 0.95
            elif risk_score < 70:
                classification = "Review"
                confidence = 0.85
            else:
                classification = "Reject"
                confidence = 0.90

            decision_json = {
                "classification": classification,
                "risk_score": min(risk_score, 100),
                "confidence_level": confidence,
                "key_factors": state["financial_risk"]["anomaly_flags"][:3] if state["financial_risk"]["anomaly_flags"] else ["Standard processing"],
                "explanation": f"Decision based on financial risk analysis (deterministic mode). Risk score: {risk_score:.1f}"
            }

        state["decision"] = decision_json

        return state


    def compliance_action_agent(state: LoanEvaluationState) -> LoanEvaluationState:
        """Agent to execute compliance actions and notifications."""
        logger.info(f"Running Compliance Agent for {state['applicant_id']}")

        classification = state["decision"]["classification"]
        case_id = f"CASE-{state['applicant_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        if classification == "Approve":
            action = "Approved - Initiate fund disbursal"
        elif classification == "Reject":
            action = "Rejected - Send rejection notice"
        else:
            action = "Manual Review Required - Escalate to compliance officer"

        state["compliance_action"] = {
            "action_taken": action,
            "notification_sent": True,
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "summary": f"Loan application {state['applicant_id']} classified as {classification}"
        }

        return state


    def finalize_output(state: LoanEvaluationState) -> LoanEvaluationState:
        """Finalize the output state."""
        state["final_decision"] = state["decision"]["classification"]
        state["risk_score"] = state["decision"]["risk_score"]
        state["confidence_level"] = state["decision"]["confidence_level"]
        state["explanation"] = state["decision"]["explanation"]
        state["case_id"] = state["compliance_action"]["case_id"]
        state["key_factors"] = state["decision"]["key_factors"]

        return state


    # Create graph
    graph = StateGraph(LoanEvaluationState)

    # Add nodes
    graph.add_node("applicant_profile", applicant_profile_agent)
    graph.add_node("financial_risk", financial_risk_agent)
    graph.add_node("decision", decision_agent)
    graph.add_node("compliance", compliance_action_agent)
    graph.add_node("finalize", finalize_output)

    # Add edges - sequential workflow
    graph.add_edge("applicant_profile", "financial_risk")
    graph.add_edge("financial_risk", "decision")
    graph.add_edge("decision", "compliance")
    graph.add_edge("compliance", "finalize")

    # Set entry and end points
    graph.set_entry_point("applicant_profile")
    graph.set_finish_point("finalize")

    return graph.compile()


def process_loan_application(request):
    """Process a loan application through the multi-agent system."""

    # Get compiled graph
    graph = create_orchestration_graph()

    # Initialize state
    initial_state = {
        "applicant_id": request.applicant_id,
        "age": request.age,
        "income": request.income,
        "employment_type": request.employment_type,
        "credit_score": request.credit_score,
        "loan_amount": request.loan_amount,
        "loan_tenure": request.loan_tenure,
        "existing_liabilities": request.existing_liabilities,
        "location": request.location,
        "applicant_profile": None,
        "financial_risk": None,
        "decision": None,
        "compliance_action": None,
        "final_decision": "",
        "risk_score": 0.0,
        "confidence_level": 0.0,
        "explanation": "",
        "case_id": "",
        "key_factors": []
    }

    # Run workflow
    logger.info(f"Starting workflow for applicant {request.applicant_id}")
    final_state = graph.invoke(initial_state)

    # Extract results
    result = {
        "decision": final_state["final_decision"],
        "risk_score": final_state["risk_score"],
        "confidence_level": final_state["confidence_level"],
        "explanation": final_state["explanation"],
        "case_id": final_state["case_id"],
        "key_factors": final_state["key_factors"],
        "timestamp": datetime.now().isoformat(),
        "applicant_profile": final_state["applicant_profile"],
        "financial_risk": final_state["financial_risk"],
        "compliance_action": final_state["compliance_action"]
    }

    logger.info(f"Workflow completed for {request.applicant_id}")

    return result
