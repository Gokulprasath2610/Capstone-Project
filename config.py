"""Configuration settings for the multi-agent loan approval system."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "127.0.0.1")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8000))

# Streamlit Configuration
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))

# Anthropic API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-sonnet-4-6"

# Loan Decision Thresholds
RISK_SCORE_APPROVE_THRESHOLD = 25
RISK_SCORE_REVIEW_THRESHOLD = 70

# DTI Limits
MAX_DTI_RATIO = 0.50
MAX_LIABILITIES_MULTIPLIER = 2.0

# Income Ranges
LOW_INCOME_THRESHOLD = 30000
MEDIUM_INCOME_THRESHOLD = 60000
HIGH_INCOME_THRESHOLD = 150000

# Loan Amount Limits
LOAN_TO_INCOME_LOW = 1.5
LOAN_TO_INCOME_MEDIUM = 3.0
LOAN_TO_INCOME_HIGH = 5.0

# Age Limits
MIN_AGE = 21
MAX_AGE = 70

# Employment Risk Mapping
EMPLOYMENT_RISK_MAP = {
    "Salaried": ("Low", 0.9),
    "Self-Employed": ("High", 0.6),
    "Contract": ("Medium", 0.7),
    "Unemployed": ("Very High", 0.1)
}

# Credit Score Ranges
CREDIT_SCORE_EXCELLENT = 750
CREDIT_SCORE_GOOD = 700
CREDIT_SCORE_FAIR = 650
CREDIT_SCORE_POOR = 600

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
