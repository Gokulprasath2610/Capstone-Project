"""Integration tests for the multi-agent loan approval system."""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

# Test scenarios
TEST_CASES = [
    {
        "name": "Strong Applicant (Should Approve)",
        "data": {
            "applicant_id": "APP-STRONG-001",
            "age": 35,
            "income": 150000,
            "employment_type": "Salaried",
            "credit_score": 800,
            "loan_amount": 100000,
            "loan_tenure": 5,
            "existing_liabilities": 20000,
            "location": "New York"
        },
        "expected_decision": "Approve"
    },
    {
        "name": "Weak Applicant (Should Reject)",
        "data": {
            "applicant_id": "APP-WEAK-002",
            "age": 28,
            "income": 30000,
            "employment_type": "Unemployed",
            "credit_score": 500,
            "loan_amount": 150000,
            "loan_tenure": 10,
            "existing_liabilities": 80000,
            "location": "Texas"
        },
        "expected_decision": "Reject"
    },
    {
        "name": "Borderline Applicant (Should Review)",
        "data": {
            "applicant_id": "APP-MEDIUM-003",
            "age": 45,
            "income": 65000,
            "employment_type": "Self-Employed",
            "credit_score": 650,
            "loan_amount": 120000,
            "loan_tenure": 8,
            "existing_liabilities": 60000,
            "location": "California"
        },
        "expected_decision": "Review"
    }
]


def check_api_health() -> bool:
    """Check if API is running."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def submit_application(data: Dict[str, Any]) -> Dict[str, Any]:
    """Submit an application and return the response."""
    response = requests.post(
        f"{BASE_URL}/api/submit-application",
        json=data,
        timeout=30
    )
    return response.json()


def run_tests():
    """Run all test cases."""
    print("\n" + "=" * 70)
    print("Multi-Agent Loan Approval System - Integration Tests")
    print("=" * 70)

    # Check API health
    print("\n[1/2] Checking API health...")
    if not check_api_health():
        print("❌ API is not running. Start FastAPI service first:")
        print("   python fastapi_service.py")
        return

    print("✅ API is healthy")

    # Run test cases
    print("\n[2/2] Running test cases...\n")

    results = []
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print("-" * 70)

        try:
            result = submit_application(test_case["data"])

            decision = result.get("decision")
            risk_score = result.get("risk_score")
            confidence = result.get("confidence_level")
            case_id = result.get("case_id")

            print(f"Applicant ID:      {test_case['data']['applicant_id']}")
            print(f"Decision:          {decision}")
            print(f"Risk Score:        {risk_score:.1f} / 100")
            print(f"Confidence:        {confidence * 100:.0f}%")
            print(f"Case ID:           {case_id}")
            print(f"Explanation:       {result.get('explanation')}")

            # Check if decision matches expectation
            expected = test_case["expected_decision"]
            match = "✅ PASS" if decision == expected else "⚠️  PARTIAL"
            print(f"Expected Decision: {expected} {match}")

            print(f"Key Factors:")
            for factor in result.get("key_factors", []):
                print(f"  • {factor}")

            results.append({
                "name": test_case["name"],
                "passed": decision == expected,
                "decision": decision,
                "expected": expected
            })

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                "name": test_case["name"],
                "passed": False,
                "error": str(e)
            })

        print()

    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)

    passed = sum(1 for r in results if r.get("passed", False))
    total = len(results)

    for result in results:
        status = "✅ PASS" if result.get("passed") else "❌ FAIL"
        print(f"{status} - {result['name']}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) did not match expected decisions")


def run_single_test():
    """Run a single interactive test."""
    print("\n" + "=" * 70)
    print("Single Test Mode")
    print("=" * 70)

    if not check_api_health():
        print("❌ API is not running")
        return

    # Get user input
    print("\nEnter application details:")
    try:
        applicant_id = input("Applicant ID (e.g., APP-001): ").strip() or "APP-001"
        age = int(input("Age [35]: ") or "35")
        income = float(input("Annual Income [$75000]: ") or "75000")
        employment = input("Employment Type [Salaried]: ").strip() or "Salaried"
        credit_score = int(input("Credit Score [750]: ") or "750")
        loan_amount = float(input("Loan Amount [$150000]: ") or "150000")
        tenure = int(input("Loan Tenure (years) [5]: ") or "5")
        liabilities = float(input("Existing Liabilities [$50000]: ") or "50000")
        location = input("Location [New York]: ").strip() or "New York"

        data = {
            "applicant_id": applicant_id,
            "age": age,
            "income": income,
            "employment_type": employment,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "loan_tenure": tenure,
            "existing_liabilities": liabilities,
            "location": location
        }

        print("\nProcessing application...")
        result = submit_application(data)

        print("\n" + "=" * 70)
        print("Decision Result")
        print("=" * 70)
        print(json.dumps(result, indent=2))

    except ValueError as e:
        print(f"❌ Invalid input: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "single":
        run_single_test()
    else:
        run_tests()
