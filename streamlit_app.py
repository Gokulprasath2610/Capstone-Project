"""Streamlit chatbot UI for loan application submission and status display."""

import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="AI Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 20px;
    }
    .decision-approve {
        padding: 15px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 4px;
    }
    .decision-reject {
        padding: 15px;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 4px;
    }
    .decision-review {
        padding: 15px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
    }
    .metric-card {
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
API_HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
API_SUBMIT_ENDPOINT = f"{API_BASE_URL}/api/submit-application"
API_STATUS_ENDPOINT = f"{API_BASE_URL}/api/application-status"
API_LIST_ENDPOINT = f"{API_BASE_URL}/api/applications"


def check_api_health():
    """Check if API is running."""
    try:
        response = requests.get(API_HEALTH_ENDPOINT, timeout=2)
        return response.status_code == 200
    except:
        return False


def submit_application(form_data):
    """Submit application to API."""
    try:
        response = requests.post(
            API_SUBMIT_ENDPOINT,
            json=form_data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to API. Make sure FastAPI service is running on http://127.0.0.1:8000")
        return None
    except Exception as e:
        st.error(f"Error submitting application: {str(e)}")
        return None


def get_application_status(applicant_id):
    """Get status of a submitted application."""
    try:
        response = requests.get(
            f"{API_STATUS_ENDPOINT}/{applicant_id}",
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Application not found")
            return None
    except Exception as e:
        st.error(f"Error retrieving application: {str(e)}")
        return None


def display_decision_result(result):
    """Display the loan decision with styling."""
    decision = result.get("decision", "Unknown")

    # Choose styling based on decision
    if decision == "Approve":
        st.markdown(
            f"""<div class="decision-approve">
            <h3>✅ Decision: APPROVED</h3>
            <p>Your loan application has been approved!</p>
            </div>""",
            unsafe_allow_html=True
        )
    elif decision == "Reject":
        st.markdown(
            f"""<div class="decision-reject">
            <h3>❌ Decision: REJECTED</h3>
            <p>Unfortunately, your loan application has been rejected.</p>
            </div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""<div class="decision-review">
            <h3>⏳ Decision: REQUIRES MANUAL REVIEW</h3>
            <p>Your application requires additional review by our team.</p>
            </div>""",
            unsafe_allow_html=True
        )

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""<div class="metric-card">
            <strong>Risk Score</strong><br>{result.get('risk_score', 0):.1f} / 100
            </div>""",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""<div class="metric-card">
            <strong>Confidence</strong><br>{result.get('confidence_level', 0) * 100:.0f}%
            </div>""",
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""<div class="metric-card">
            <strong>Case ID</strong><br>{result.get('case_id', 'N/A')}
            </div>""",
            unsafe_allow_html=True
        )

    # Display explanation and factors
    st.markdown("### Decision Details")
    st.markdown(f"**Explanation:** {result.get('explanation', 'N/A')}")

    if result.get("key_factors"):
        st.markdown("**Key Decision Factors:**")
        for factor in result.get("key_factors", []):
            st.markdown(f"- {factor}")

    # Display timestamp
    st.markdown(f"**Processed:** {result.get('timestamp', 'N/A')}")


def main():
    # Header
    st.title("🏦 AI Loan Approval System")
    st.markdown("---")

    # Check API health
    api_healthy = check_api_health()

    if not api_healthy:
        st.warning("⚠️ FastAPI service is not running. Please start it with: `python fastapi_service.py`")
    else:
        st.success("✅ API is running")

    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Select Page", ["Submit Application", "Check Status", "View All Applications"])

    st.markdown("---")

    # Page: Submit Application
    if page == "Submit Application":
        st.header("📝 Submit Loan Application")
        st.markdown("Fill in your details below to apply for a loan. Our AI system will evaluate your application instantly.")

        with st.form("loan_application_form"):
            col1, col2 = st.columns(2)

            with col1:
                applicant_id = st.text_input(
                    "Applicant ID",
                    value="APP-001",
                    help="Unique identifier for the applicant"
                )
                age = st.number_input(
                    "Age",
                    min_value=18,
                    max_value=100,
                    value=35
                )
                income = st.number_input(
                    "Annual Income ($)",
                    min_value=0.0,
                    value=75000.0,
                    step=1000.0
                )
                employment_type = st.selectbox(
                    "Employment Type",
                    ["Salaried", "Self-Employed", "Contract", "Unemployed"]
                )
                credit_score = st.slider(
                    "Credit Score",
                    min_value=300,
                    max_value=850,
                    value=750
                )

            with col2:
                loan_amount = st.number_input(
                    "Loan Amount ($)",
                    min_value=0.0,
                    value=150000.0,
                    step=1000.0
                )
                loan_tenure = st.number_input(
                    "Loan Tenure (Years)",
                    min_value=1,
                    max_value=30,
                    value=5
                )
                existing_liabilities = st.number_input(
                    "Existing Liabilities ($)",
                    min_value=0.0,
                    value=50000.0,
                    step=1000.0
                )
                location = st.selectbox(
                    "Location",
                    ["New York", "California", "Texas", "Florida", "Other"]
                )

            submit_button = st.form_submit_button(
                label="🚀 Submit Application",
                use_container_width=True
            )

            if submit_button:
                if not api_healthy:
                    st.error("API is not available. Please start the FastAPI service.")
                else:
                    with st.spinner("Processing your application... This may take a moment."):
                        form_data = {
                            "applicant_id": applicant_id,
                            "age": age,
                            "income": income,
                            "employment_type": employment_type,
                            "credit_score": credit_score,
                            "loan_amount": loan_amount,
                            "loan_tenure": loan_tenure,
                            "existing_liabilities": existing_liabilities,
                            "location": location,
                            "application_timestamp": datetime.now().isoformat()
                        }

                        result = submit_application(form_data)

                        if result:
                            st.session_state.last_application = result
                            st.success("✅ Application submitted successfully!")
                            st.markdown("---")
                            display_decision_result(result)

    # Page: Check Status
    elif page == "Check Status":
        st.header("🔍 Check Application Status")

        applicant_id = st.text_input(
            "Enter your Applicant ID",
            placeholder="e.g., APP-001"
        )

        if st.button("Check Status", use_container_width=True):
            if applicant_id:
                with st.spinner("Retrieving application status..."):
                    result = get_application_status(applicant_id)
                    if result:
                        display_decision_result(result)
            else:
                st.warning("Please enter an Applicant ID")

    # Page: View All Applications
    else:
        st.header("📊 All Applications")

        if st.button("Refresh", use_container_width=True):
            st.rerun()

        try:
            response = requests.get(API_LIST_ENDPOINT, timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.markdown(f"**Total Applications Processed:** {data.get('total_applications', 0)}")

                if data.get("applications"):
                    # Create DataFrame for display
                    import pandas as pd
                    df = pd.DataFrame(data.get("applications", []))
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No applications processed yet.")
            else:
                st.error("Failed to retrieve applications")
        except Exception as e:
            st.error(f"Error retrieving applications: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: gray; font-size: 12px;">
        AI Loan Approval System | Multi-Agent Agentic AI Architecture
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
