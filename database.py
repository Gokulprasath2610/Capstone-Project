"""Database integration for loan application persistence."""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class LoanApplicationRecord(Base):
    """SQLAlchemy model for loan applications."""
    __tablename__ = "loan_applications"

    applicant_id = Column(String, primary_key=True)
    case_id = Column(String, unique=True, index=True)
    age = Column(Integer)
    income = Column(Float)
    employment_type = Column(String)
    credit_score = Column(Integer)
    loan_amount = Column(Float)
    loan_tenure = Column(Integer)
    existing_liabilities = Column(Float)
    location = Column(String)

    # Decision outputs
    decision = Column(String)
    risk_score = Column(Float)
    confidence_level = Column(Float)
    explanation = Column(String)
    key_factors = Column(JSON)

    # Agent outputs
    applicant_profile = Column(JSON)
    financial_risk = Column(JSON)
    compliance_action = Column(JSON)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Metadata
    approved = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    rejected = Column(Boolean, default=False)


class DatabaseManager:
    """Manages database operations for loan applications."""

    def __init__(self, database_url: Optional[str] = None):
        """Initialize database connection."""
        if database_url is None:
            database_url = os.getenv("DATABASE_URL", "sqlite:///./loan_applications.db")

        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info(f"Database initialized: {database_url}")

    def save_application(self, application_data: Dict) -> bool:
        """Save a loan application to database."""
        try:
            db: Session = self.SessionLocal()

            record = LoanApplicationRecord(
                applicant_id=application_data.get("applicant_id"),
                case_id=application_data.get("case_id"),
                age=application_data.get("age"),
                income=application_data.get("income"),
                employment_type=application_data.get("employment_type"),
                credit_score=application_data.get("credit_score"),
                loan_amount=application_data.get("loan_amount"),
                loan_tenure=application_data.get("loan_tenure"),
                existing_liabilities=application_data.get("existing_liabilities"),
                location=application_data.get("location"),
                decision=application_data.get("decision"),
                risk_score=application_data.get("risk_score"),
                confidence_level=application_data.get("confidence_level"),
                explanation=application_data.get("explanation"),
                key_factors=application_data.get("key_factors"),
                applicant_profile=application_data.get("applicant_profile"),
                financial_risk=application_data.get("financial_risk"),
                compliance_action=application_data.get("compliance_action"),
                approved=application_data.get("decision") == "Approve",
                reviewed=application_data.get("decision") == "Review",
                rejected=application_data.get("decision") == "Reject"
            )

            db.add(record)
            db.commit()
            db.close()
            logger.info(f"Application {application_data.get('applicant_id')} saved to database")
            return True
        except Exception as e:
            logger.error(f"Error saving application: {str(e)}")
            return False

    def get_application(self, applicant_id: str) -> Optional[Dict]:
        """Retrieve a specific application from database."""
        try:
            db: Session = self.SessionLocal()
            record = db.query(LoanApplicationRecord).filter(
                LoanApplicationRecord.applicant_id == applicant_id
            ).first()
            db.close()

            if record:
                return self._record_to_dict(record)
            return None
        except Exception as e:
            logger.error(f"Error retrieving application: {str(e)}")
            return None

    def get_all_applications(self, limit: int = 100) -> List[Dict]:
        """Retrieve all applications from database."""
        try:
            db: Session = self.SessionLocal()
            records = db.query(LoanApplicationRecord).order_by(
                LoanApplicationRecord.created_at.desc()
            ).limit(limit).all()
            db.close()

            return [self._record_to_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Error retrieving applications: {str(e)}")
            return []

    def get_applications_by_decision(self, decision: str, limit: int = 100) -> List[Dict]:
        """Retrieve applications filtered by decision."""
        try:
            db: Session = self.SessionLocal()
            records = db.query(LoanApplicationRecord).filter(
                LoanApplicationRecord.decision == decision
            ).order_by(
                LoanApplicationRecord.created_at.desc()
            ).limit(limit).all()
            db.close()

            return [self._record_to_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Error retrieving applications: {str(e)}")
            return []

    def get_statistics(self) -> Dict:
        """Get statistics about all applications."""
        try:
            db: Session = self.SessionLocal()
            total = db.query(LoanApplicationRecord).count()
            approved = db.query(LoanApplicationRecord).filter(
                LoanApplicationRecord.approved == True
            ).count()
            reviewed = db.query(LoanApplicationRecord).filter(
                LoanApplicationRecord.reviewed == True
            ).count()
            rejected = db.query(LoanApplicationRecord).filter(
                LoanApplicationRecord.rejected == True
            ).count()
            db.close()

            return {
                "total_applications": total,
                "approved_count": approved,
                "review_count": reviewed,
                "rejected_count": rejected,
                "approval_rate": (approved / total * 100) if total > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {}

    @staticmethod
    def _record_to_dict(record: LoanApplicationRecord) -> Dict:
        """Convert database record to dictionary."""
        return {
            "applicant_id": record.applicant_id,
            "case_id": record.case_id,
            "age": record.age,
            "income": record.income,
            "employment_type": record.employment_type,
            "credit_score": record.credit_score,
            "loan_amount": record.loan_amount,
            "loan_tenure": record.loan_tenure,
            "existing_liabilities": record.existing_liabilities,
            "location": record.location,
            "decision": record.decision,
            "risk_score": record.risk_score,
            "confidence_level": record.confidence_level,
            "explanation": record.explanation,
            "key_factors": record.key_factors,
            "applicant_profile": record.applicant_profile,
            "financial_risk": record.financial_risk,
            "compliance_action": record.compliance_action,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        }


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get or create database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
