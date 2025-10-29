# Test Suite Documentation

## Overview

Comprehensive test suite for the Mortgage Proposal Application using pytest framework.

## Test Coverage

### 1. **Proposal Generator Tests** (`test_proposal_generator.py`)
- **TestMonthlyPaymentCalculations** (6 tests)
  - Standard 30-year mortgages
  - FHA loans
  - HELOC (10-year)
  - HELOAN (20-year)
  - Edge cases (zero amounts, zero rates)

- **TestAPRCalculations** (4 tests)
  - APR > rate with fees validation
  - APR = rate with zero fees
  - High fees scenarios
  - HELOC APR calculations

- **TestLoanAmountCalculations** (5 tests)
  - Cashout refinance amounts
  - HELOC calculations
  - HELOAN calculations
  - VA vs FHA loan type selection

- **TestProposalGeneration** (3 tests)
  - Generate all 3 proposal types
  - Verify Option A and B structure
  - Validate required fields

**Total: 18 tests**

### 2. **Chatbot Tests** (`test_chatbot.py`)
- **TestLeadDataExtraction** (10 tests)
  - Extract name, property value, balance
  - Extract cash out amounts (standard, "20k" format, plain numbers)
  - Extract veteran status
  - Multiple field extraction from conversation

- **TestChangeDetection** (4 tests)
  - Detect cash out changes
  - Detect property value changes
  - Detect veteran status changes
  - First-time vs change distinction

- **TestProposalGenerationTrigger** (5 tests)
  - Complete data validation
  - Missing field detection
  - Cash out intent handling

- **TestLeadContextInjection** (2 tests)
  - System prompt injection
  - Response generation with context

**Total: 21 tests**

### 3. **Lead Manager Tests** (`test_lead_manager.py`)
- **TestLeadStorage** (6 tests)
  - Create, Read, Update, Delete operations
  - List all leads
  - Data persistence

- **TestLeadValidation** (3 tests)
  - Required field validation
  - Numeric field type checking
  - Optional field handling

- **TestBonzoDataParsing** (2 tests)
  - Parse Bonzo JSON format
  - Handle missing Bonzo fields

- **TestSampleLeadGeneration** (2 tests)
  - Generate sample leads
  - Validate realistic data

- **TestLeadSearch** (3 tests)
  - Search by name
  - Filter by veteran status
  - Filter by property value range

**Total: 16 tests**

### 4. **Campaign Manager Tests** (`test_campaign_manager.py`)
- **TestCampaignCreation** (3 tests)
  - Create cashout campaigns
  - Create responded campaigns
  - Verify 57 touchpoints

- **TestTouchpointScheduling** (5 tests)
  - Scheduled times validation
  - Business hours (8am-8pm) compliance
  - Chronological order
  - Immediate Day 1 touchpoint
  - Timezone handling

- **TestMessagePersonalization** (3 tests)
  - Name inclusion
  - Cash out amount references
  - Token replacement

- **TestCampaignStateManagement** (4 tests)
  - Active status on creation
  - Pause/resume functionality
  - Stop campaign permanently

- **TestCampaignTypes** (3 tests)
  - Campaign structure validation
  - 30-day duration verification

- **TestTouchpointTypes** (2 tests)
  - Type assignment (SMS, Email, Call)
  - Multiple type usage

**Total: 20 tests**

### 5. **PDF Generator Tests** (`test_pdf_generator.py`)
- **TestPDFGeneration** (5 tests)
  - Returns valid bytes
  - PDF readability
  - Client name inclusion
  - File saving

- **TestPDFContent** (4 tests)
  - All 3 proposals included
  - Interest rates displayed
  - Monthly payments shown
  - Option A and B labeling

- **TestPDFFormatting** (2 tests)
  - Multi-page support
  - Long name handling

- **TestPDFErrorHandling** (2 tests)
  - Missing data handling
  - Empty proposals list

**Total: 13 tests**

## Grand Total: **88 Tests**

## Running Tests

### Run All Tests
```bash
cd streamlit_app
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_proposal_generator.py
pytest tests/test_chatbot.py
pytest tests/test_lead_manager.py
pytest tests/test_campaign_manager.py
pytest tests/test_pdf_generator.py
```

### Run Specific Test Class
```bash
pytest tests/test_proposal_generator.py::TestAPRCalculations
pytest tests/test_chatbot.py::TestChangeDetection
```

### Run Specific Test
```bash
pytest tests/test_proposal_generator.py::TestAPRCalculations::test_apr_higher_than_rate_with_fees
pytest tests/test_chatbot.py::TestChangeDetection::test_detect_cash_out_change
```

### Run Tests by Marker
```bash
pytest -m calculations    # Only calculation tests
pytest -m chatbot        # Only chatbot tests
pytest -m campaign       # Only campaign tests
pytest -m pdf           # Only PDF tests
```

### Run with Coverage Report
```bash
pytest --cov=components --cov=utils --cov-report=html
```

This creates an HTML coverage report in `htmlcov/index.html`

### Run and Show Coverage in Terminal
```bash
pytest --cov=components --cov=utils --cov-report=term-missing
```

### Run Only Failed Tests from Last Run
```bash
pytest --lf
```

### Run Tests in Parallel (faster)
```bash
pip install pytest-xdist
pytest -n auto
```

## Test Markers

Tests are organized with markers for easy filtering:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slower running tests
- `@pytest.mark.calculations` - Mortgage calculation tests
- `@pytest.mark.chatbot` - Chatbot functionality tests
- `@pytest.mark.campaign` - Campaign management tests
- `@pytest.mark.pdf` - PDF generation tests

## Fixtures

Common test data is provided through fixtures in `conftest.py`:

- `sample_lead_data` - Standard lead data
- `veteran_lead_data` - Veteran lead data
- `high_value_lead_data` - High-value property
- `sample_proposal_data` - Complete proposal data
- `sample_conversation` - Chatbot conversation history
- `rate_config` - Rate configuration
- `bonzo_lead_json` - Bonzo JSON format
- `temp_storage_dir` - Temporary directory for file tests

### Using Fixtures

```python
def test_example(sample_lead_data):
    """Test using sample lead data"""
    assert sample_lead_data["name"] == "John Smith"
    assert sample_lead_data["property_value"] == 300000
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=components --cov=utils
```

## Writing New Tests

### Test Structure

```python
import pytest

class TestYourFeature:
    """Test your feature description"""
    
    def setup_method(self):
        """Setup before each test"""
        # Initialize objects
        pass
    
    def teardown_method(self):
        """Cleanup after each test"""
        # Clean up resources
        pass
    
    def test_something(self):
        """Test description"""
        # Arrange
        expected = "value"
        
        # Act
        result = your_function()
        
        # Assert
        assert result == expected
```

### Best Practices

1. **One assertion concept per test** - Tests should focus on one thing
2. **Use descriptive test names** - `test_apr_higher_than_rate_with_fees`
3. **Arrange-Act-Assert pattern** - Setup, execute, verify
4. **Use fixtures for common data** - Don't repeat setup code
5. **Clean up resources** - Use teardown or context managers
6. **Test edge cases** - Zero values, negative numbers, missing data
7. **Mock external services** - Don't rely on OpenAI API in tests

## Expected Results

All tests should pass with the current codebase:

```
========== 88 passed in X.XXs ==========
```

## Troubleshooting

### Import Errors
Make sure you're running tests from the `streamlit_app` directory:
```bash
cd streamlit_app
pytest
```

### OpenAI API Key Required
Some chatbot tests may require an OpenAI API key. Set it in your environment:
```bash
export OPENAI_API_KEY="your-key-here"
```

Or use mocking:
```python
@patch('openai.ChatCompletion.create')
def test_with_mock(mock_create):
    mock_create.return_value = {...}
```

### File Permission Errors
Ensure temp directories have write permissions. The test suite uses `tempfile.mkdtemp()` which should handle this automatically.

## Coverage Goals

Target coverage levels:
- **Proposal Generator**: 95%+ (critical calculation logic)
- **Chatbot**: 85%+ (AI integration has some external dependencies)
- **Lead Manager**: 90%+ (CRUD operations)
- **Campaign Manager**: 90%+ (scheduling logic)
- **PDF Generator**: 80%+ (formatting has many edge cases)

## Maintenance

- Run tests before each commit
- Update tests when adding new features
- Keep fixtures in sync with data models
- Review coverage reports monthly
- Add integration tests for new workflows

## Questions?

For test-related questions, review:
1. Test file docstrings
2. Individual test descriptions
3. Fixture definitions in `conftest.py`
4. pytest documentation: https://docs.pytest.org/
