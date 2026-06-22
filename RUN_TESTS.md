# 🧪 How to Run All Tests

Quick guide to run all tests for the Loan Approval System.

---

## ✅ Prerequisites

Make sure you have:
1. ✅ FastAPI running: `python fastapi_service.py`
2. ✅ Streamlit running: `streamlit run streamlit_app.py`
3. ✅ Virtual environment activated: `source venv/bin/activate`

---

## 🎯 Test 1: Run Basic API Tests

**Purpose**: Test all 3 scenarios (Strong, Weak, Borderline applicants)

### Command
```bash
cd '/home/ubuntu/Downloads/capstone project'
source venv/bin/activate
python test_system.py
```

### What It Does
- ✅ Checks API health
- ✅ Tests 3 scenario cases
- ✅ Validates decisions
- ✅ Shows results summary

### Expected Output
```
✅ PASS - Strong Applicant (Should Approve)
✅ PASS - Weak Applicant (Should Reject)
✅ PASS - Borderline Applicant (Should Review)

Total: 3/3 tests passed
🎉 All tests passed!
```

---

## 🎭 Test 2: Run Playwright Tests (API)

**Purpose**: Advanced testing using Playwright framework

### Command
```bash
cd '/home/ubuntu/Downloads/capstone project'
source venv/bin/activate
python test_playwright.py
```

### What It Does
- ✅ Tests API health endpoint
- ✅ Tests single application submission
- ✅ Runs all 3 scenario cases
- ✅ Tests application history
- ✅ Provides comprehensive report

### Expected Output
```
✅ API is Healthy
✅ API Request Successful
✅ PASS - Strong Applicant
✅ PASS - Weak Applicant
✅ PASS - Borderline Applicant
✅ Successfully retrieved applications

Total: 3/3 scenarios passed
🎉 All tests passed!
```

---

## 🌐 Test 3: Run Playwright UI Tests

**Purpose**: Test the Streamlit web interface

### Command
```bash
cd '/home/ubuntu/Downloads/capstone project'
source venv/bin/activate
python test_playwright_ui.py
```

### What It Does
- ✅ Launches headless browser (Chromium)
- ✅ Tests page structure
- ✅ Tests tab navigation
- ✅ Tests form elements
- ✅ Captures screenshots

### Expected Output
```
✅ Page loaded successfully
✅ 'Submit Application' found in page
✅ 'Check Status' found in page
✅ 'View All Applications' found in page
✅ Found 11 input fields
✅ Found 15 buttons
✅ Screenshot saved

All UI tests completed successfully!
```

---

## 🚀 Run ALL Tests Together

**Purpose**: Run everything in sequence

### Command
```bash
cd '/home/ubuntu/Downloads/capstone project'
source venv/bin/activate

echo "Running Basic API Tests..."
python test_system.py

echo ""
echo "Running Playwright Tests..."
python test_playwright.py

echo ""
echo "Running Playwright UI Tests..."
python test_playwright_ui.py

echo ""
echo "✅ All test suites completed!"
```

### Or Create a Script

Save this as `run_all_tests.sh`:

```bash
#!/bin/bash

cd '/home/ubuntu/Downloads/capstone project'
source venv/bin/activate

echo "╔════════════════════════════════════════╗"
echo "║     RUNNING ALL TEST SUITES            ║"
echo "╚════════════════════════════════════════╝"

echo ""
echo "Test 1: Basic API Tests"
echo "─────────────────────────────────────────"
python test_system.py

echo ""
echo "Test 2: Playwright Tests"
echo "─────────────────────────────────────────"
python test_playwright.py

echo ""
echo "Test 3: Playwright UI Tests"
echo "─────────────────────────────────────────"
python test_playwright_ui.py

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     ALL TESTS COMPLETED!               ║"
echo "╚════════════════════════════════════════╝"
```

Then run:
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

---

## 🎯 Test 4: Interactive Testing

**Purpose**: Manually test with custom data

### Command
```bash
cd '/home/ubuntu/Downloads/capstone project'
source venv/bin/activate
python test_system.py single
```

### What It Does
- ✅ Prompts for applicant details
- ✅ Submits to API
- ✅ Shows decision with full JSON response
- ✅ Lets you test multiple times

### Example
```
Enter application details:
Applicant ID (e.g., APP-001): MY-TEST-001
Age [35]: 40
Annual Income [$75000]: 100000
Employment Type [Salaried]: Salaried
Credit Score [750]: 780
Loan Amount [$150000]: 120000
Loan Tenure (years) [5]: 5
Existing Liabilities [$50000]: 30000
Location [New York]: New York

Processing application...

Decision Result:
{
  "applicant_id": "MY-TEST-001",
  "decision": "Approve",
  "risk_score": 15.3,
  "confidence_level": 0.95,
  ...
}
```

---

## 📊 Test Coverage

### What Gets Tested

| Component | Test 1 | Test 2 | Test 3 |
|-----------|--------|--------|--------|
| API Health | ✅ | ✅ | ✅ |
| Endpoints | ✅ | ✅ | ✅ |
| Agent 1 | ✅ | ✅ | ✅ |
| Agent 2 | ✅ | ✅ | ✅ |
| Agent 3 | ✅ | ✅ | ✅ |
| Agent 4 | ✅ | ✅ | ✅ |
| Decisions | ✅ | ✅ | - |
| Web UI | - | - | ✅ |
| Forms | - | - | ✅ |
| Navigation | - | - | ✅ |

---

## 🔍 Understanding Test Results

### Success Indicators
- ✅ Green checkmark = Test passed
- ✅ All agents executed = System working
- ✅ Correct decisions = Logic working
- ✅ 100% pass rate = System healthy

### Failure Indicators
- ❌ Red X = Test failed
- ❌ API timeout = Service not running
- ❌ Wrong decision = Logic issue
- ❌ Less than 100% = Needs investigation

---

## 🛠️ Troubleshooting

### "Cannot connect to API"
```bash
# Make sure FastAPI is running
ps aux | grep fastapi_service.py

# If not running, start it
python fastapi_service.py
```

### "ModuleNotFoundError: playwright"
```bash
# Install playwright
pip install playwright
playwright install
```

### "Browser launch failed"
```bash
# Install browser dependencies
sudo apt-get install libwoff1 libavif16
playwright install-deps
```

### "Streamlit not responding"
```bash
# Restart Streamlit
pkill -f streamlit
streamlit run streamlit_app.py
```

---

## 📈 Test Results Interpretation

### Perfect Results (100% Pass)
```
✅ PASS - All 3 scenarios
Total: 3/3 tests passed
🎉 All tests passed!
```
→ **System is healthy and working correctly**

### Partial Results (Some Pass)
```
✅ PASS - Scenario 1
❌ FAIL - Scenario 2
✅ PASS - Scenario 3
```
→ **Investigate the failed scenario**

### All Failed
```
❌ Cannot connect to API
```
→ **Check if FastAPI is running**

---

## 📊 Sample Test Reports

### Test Output Example 1: Success
```
[1/3] Strong Applicant (Should Approve)
Decision: Approve ✅ PASS
Risk Score: 13.3 / 100
Confidence: 95%
```

### Test Output Example 2: Success
```
[2/3] Weak Applicant (Should Reject)
Decision: Reject ✅ PASS
Risk Score: 100.0 / 100
Confidence: 90%
```

### Test Output Example 3: Success
```
[3/3] Borderline Applicant (Should Review)
Decision: Review ✅ PASS
Risk Score: 57.7 / 100
Confidence: 85%
```

---

## 🎓 What Each Test Validates

### test_system.py
- Basic API connectivity
- Scenario processing
- Decision correctness
- Result formatting

### test_playwright.py
- API health monitoring
- Application submission
- History retrieval
- Performance metrics

### test_playwright_ui.py
- Page loading
- Element presence
- Form functionality
- Navigation accessibility

---

## 📝 Creating Custom Tests

To add your own test scenario:

1. Open `test_system.py`
2. Add to `TEST_CASES`:

```python
{
    "name": "My Custom Test",
    "data": {
        "applicant_id": "CUSTOM-001",
        "age": 30,
        "income": 80000,
        "employment_type": "Salaried",
        "credit_score": 720,
        "loan_amount": 100000,
        "loan_tenure": 5,
        "existing_liabilities": 40000,
        "location": "Boston"
    },
    "expected_decision": "Approve"
}
```

3. Run: `python test_system.py`

---

## ✨ Summary

| Test | Command | Purpose |
|------|---------|---------|
| **Basic** | `python test_system.py` | Quick validation |
| **Advanced** | `python test_playwright.py` | Comprehensive testing |
| **UI** | `python test_playwright_ui.py` | Web interface validation |
| **Interactive** | `python test_system.py single` | Manual testing |

---

**All tests passing = System ready for evaluation!** ✅

For more information, see:
- QUICK_START.md
- README.md
- EVALUATION_GUIDE.md
