"""MCP Servers for domain-specific data access and decision synthesis."""

from fastmcp import Server
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

# Data Models
class ApplicantData(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    existing_liabilities: float
    location: str


class ApplicantProfileResult(BaseModel):
    income_stability_score: float
    employment_risk: str
    credit_history_summary: str
    application_completeness_flags: list[str]


class FinancialRiskResult(BaseModel):
    debt_to_income_ratio: float
    credit_score_risk_level: str
    loan_amount_risk: str
    anomaly_flags: list[str]
    reasoning: str


class DecisionResult(BaseModel):
    classification: str  # Approve, Reject, Review
    risk_score: float
    confidence_level: float
    key_decision_factors: list[str]
    explanation: str


class ComplianceResult(BaseModel):
    action_taken: str
    notification_sent: bool
    case_id: str
    timestamp: str
    summary: str


# Applicant Profile MCP Server
def create_applicant_db_server():
    server = Server("applicant_db")

    @server.call_tool()
    def analyze_applicant_profile(applicant_id: str, age: int, income: float,
                                  employment_type: str, credit_score: int) -> dict:
        """Analyze applicant profile for income stability, employment risk, and credit history."""

        # Income stability scoring
        if income < 30000:
            stability_score = 0.3
            flags = ["Low income"]
        elif income < 60000:
            stability_score = 0.6
            flags = []
        elif income < 150000:
            stability_score = 0.8
            flags = []
        else:
            stability_score = 0.95
            flags = []

        # Employment risk assessment
        employment_risk_map = {
            "Salaried": "Low",
            "Self-Employed": "High",
            "Contract": "Medium",
            "Unemployed": "Very High"
        }
        employment_risk = employment_risk_map.get(employment_type, "Unknown")
        if employment_risk == "Very High":
            flags.append("Unemployed - high risk")

        # Credit history summary based on score
        if credit_score >= 750:
            credit_summary = "Excellent credit history with consistent payments"
        elif credit_score >= 700:
            credit_summary = "Good credit history with minor delinquencies"
        elif credit_score >= 650:
            credit_summary = "Fair credit history with some missed payments"
        else:
            credit_summary = "Poor credit history with significant delinquencies"
            flags.append("Low credit score")

        if age < 21:
            flags.append("Applicant below 21 years")
        elif age > 70:
            flags.append("Applicant above 70 years")

        return {
            "income_stability_score": stability_score,
            "employment_risk": employment_risk,
            "credit_history_summary": credit_summary,
            "application_completeness_flags": flags
        }

    return server


# Financial Risk Analysis MCP Server
def create_risk_rules_db_server():
    server = Server("risk_rules_db")

    @server.call_tool()
    def analyze_financial_risk(applicant_id: str, income: float, existing_liabilities: float,
                               loan_amount: float, credit_score: int, loan_tenure: int) -> dict:
        """Analyze financial risk including debt-to-income ratio and anomalies."""

        # Calculate debt-to-income ratio
        monthly_income = income / 12
        total_monthly_debt = (existing_liabilities / 12) + (loan_amount / loan_tenure / 12)
        dti_ratio = (total_monthly_debt / monthly_income) if monthly_income > 0 else 0

        # Credit score risk level
        if credit_score >= 750:
            credit_risk = "Very Low"
        elif credit_score >= 700:
            credit_risk = "Low"
        elif credit_score >= 650:
            credit_risk = "Medium"
        elif credit_score >= 600:
            credit_risk = "High"
        else:
            credit_risk = "Very High"

        # Loan amount risk
        if loan_amount > income * 5:
            loan_risk = "Very High"
        elif loan_amount > income * 3:
            loan_risk = "High"
        elif loan_amount > income * 1.5:
            loan_risk = "Medium"
        else:
            loan_risk = "Low"

        # Anomaly detection
        anomalies = []
        if dti_ratio > 0.5:
            anomalies.append(f"High DTI ratio: {dti_ratio:.2f}")
        if existing_liabilities > income * 2:
            anomalies.append("Existing liabilities exceed 2x annual income")
        if loan_tenure > 20:
            anomalies.append("Long loan tenure")

        reasoning = f"DTI ratio: {dti_ratio:.2f}, Credit Risk: {credit_risk}, Loan Risk: {loan_risk}"

        return {
            "debt_to_income_ratio": dti_ratio,
            "credit_score_risk_level": credit_risk,
            "loan_amount_risk": loan_risk,
            "anomaly_flags": anomalies,
            "reasoning": reasoning
        }

    return server


# Decision Synthesis MCP Server
def create_decision_synthesis_server():
    server = Server("decision_synthesis")

    @server.call_tool()
    def synthesize_decision(applicant_id: str, income_stability: float, employment_risk: str,
                           dti_ratio: float, credit_risk: str, loan_risk: str,
                           flags: list[str]) -> dict:
        """Synthesize loan decision based on multiple risk factors."""

        risk_score = 0.0
        decision_factors = []

        # Calculate risk score (0-100)
        if employment_risk == "Very High":
            risk_score += 30
            decision_factors.append("Very high employment risk")
        elif employment_risk == "High":
            risk_score += 20
            decision_factors.append("High employment risk")
        elif employment_risk == "Medium":
            risk_score += 10

        if credit_risk == "Very High":
            risk_score += 25
            decision_factors.append("Very high credit risk")
        elif credit_risk == "High":
            risk_score += 15
            decision_factors.append("High credit risk")
        elif credit_risk == "Medium":
            risk_score += 8

        if loan_risk == "Very High":
            risk_score += 20
            decision_factors.append("Loan amount too high relative to income")
        elif loan_risk == "High":
            risk_score += 12
            decision_factors.append("High loan amount relative to income")

        if dti_ratio > 0.5:
            risk_score += 15
            decision_factors.append(f"High DTI ratio: {dti_ratio:.2f}")

        risk_score += (1 - income_stability) * 20

        if flags:
            risk_score += len(flags) * 5
            decision_factors.extend(flags)

        # Determine classification
        if risk_score < 25:
            classification = "Approve"
            confidence = 0.95
        elif risk_score < 50:
            classification = "Approve"
            confidence = 0.80
        elif risk_score < 70:
            classification = "Review"
            confidence = 0.85
        else:
            classification = "Reject"
            confidence = 0.90

        explanation = f"Decision based on risk score {risk_score:.1f}/100. Key factors: {', '.join(decision_factors[:3])}"

        return {
            "classification": classification,
            "risk_score": min(risk_score, 100),
            "confidence_level": confidence,
            "key_decision_factors": decision_factors,
            "explanation": explanation
        }

    return server


# Compliance & Action Orchestrator MCP Server
def create_notification_system_server():
    server = Server("notification_system")

    @server.call_tool()
    def execute_compliance_action(applicant_id: str, classification: str, risk_score: float) -> dict:
        """Execute compliance actions and send notifications."""

        case_id = f"CASE-{applicant_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        timestamp = datetime.now().isoformat()

        # Determine action
        if classification == "Approve":
            action = "Approved - Initiate fund disbursal"
            notification_sent = True
        elif classification == "Reject":
            action = "Rejected - Send rejection notice"
            notification_sent = True
        else:
            action = "Manual Review Required - Escalate to compliance officer"
            notification_sent = True

        summary = f"Loan application {applicant_id} classified as {classification} with risk score {risk_score:.1f}. {action}"

        return {
            "action_taken": action,
            "notification_sent": notification_sent,
            "case_id": case_id,
            "timestamp": timestamp,
            "summary": summary
        }

    return server


# Initialize all MCP servers
def get_all_servers():
    return {
        "applicant_db": create_applicant_db_server(),
        "risk_rules_db": create_risk_rules_db_server(),
        "decision_synthesis": create_decision_synthesis_server(),
        "notification_system": create_notification_system_server()
    }
