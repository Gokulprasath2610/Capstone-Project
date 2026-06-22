"""FastAPI microservice for loan application processing."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Loan Application API",
    description="Multi-Agent AI system for loan approval decisions",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Request Models
class LoanApplicationRequest(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    loan_tenure: int  # in years
    existing_liabilities: float
    location: str
    application_timestamp: Optional[str] = None


class ApplicationResponse(BaseModel):
    applicant_id: str
    status: str
    decision: str
    risk_score: float
    confidence_level: float
    explanation: str
    case_id: str
    timestamp: str
    key_factors: list[str]


# In-memory storage for application results (in production, use database)
application_store = {}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "loan-application-api"}


@app.post("/api/submit-application", response_model=ApplicationResponse)
def submit_application(request: LoanApplicationRequest):
    """Submit a loan application for processing."""
    try:
        logger.info(f"Processing application for applicant {request.applicant_id}")

        # Import orchestration engine
        from orchestration_engine import process_loan_application

        # Process application through multi-agent system
        result = process_loan_application(request)

        # Store result
        application_store[request.applicant_id] = result

        logger.info(f"Application processed: {request.applicant_id} - Decision: {result['decision']}")

        return ApplicationResponse(
            applicant_id=request.applicant_id,
            status="processed",
            decision=result["decision"],
            risk_score=result["risk_score"],
            confidence_level=result["confidence_level"],
            explanation=result["explanation"],
            case_id=result["case_id"],
            timestamp=result["timestamp"],
            key_factors=result["key_factors"]
        )

    except Exception as e:
        logger.error(f"Error processing application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/application-status/{applicant_id}")
def get_application_status(applicant_id: str):
    """Get the status of a submitted application."""
    if applicant_id not in application_store:
        raise HTTPException(status_code=404, detail="Application not found")

    result = application_store[applicant_id]
    return ApplicationResponse(
        applicant_id=applicant_id,
        status="completed",
        decision=result["decision"],
        risk_score=result["risk_score"],
        confidence_level=result["confidence_level"],
        explanation=result["explanation"],
        case_id=result["case_id"],
        timestamp=result["timestamp"],
        key_factors=result["key_factors"]
    )


@app.get("/api/applications")
def list_applications():
    """List all processed applications."""
    return {
        "total_applications": len(application_store),
        "applications": [
            {
                "applicant_id": app_id,
                "decision": result["decision"],
                "risk_score": result["risk_score"],
                "timestamp": result["timestamp"]
            }
            for app_id, result in application_store.items()
        ]
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("FASTAPI_PORT", 8000))
    host = os.getenv("FASTAPI_HOST", "127.0.0.1")

    uvicorn.run(app, host=host, port=port, log_level="info")
