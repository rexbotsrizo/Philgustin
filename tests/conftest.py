"""
Pytest Configuration and Shared Fixtures
"""
import pytest
import os
import tempfile
from utils.config import load_config


@pytest.fixture(scope="session")
def config():
    """Load configuration for tests"""
    return load_config()


@pytest.fixture
def sample_lead_data():
    """Sample lead data for testing"""
    return {
        "name": "John Smith",
        "phone": "555-1234",
        "email": "john.smith@example.com",
        "property_value": 300000,
        "current_balance": 200000,
        "cash_out_amount": 50000,
        "is_veteran": "no",
        "credit_score": 720
    }


@pytest.fixture
def veteran_lead_data():
    """Sample veteran lead data"""
    return {
        "name": "Jane Veteran",
        "phone": "555-5678",
        "email": "jane.veteran@example.com",
        "property_value": 400000,
        "current_balance": 250000,
        "cash_out_amount": 75000,
        "is_veteran": "yes",
        "credit_score": 740
    }


@pytest.fixture
def high_value_lead_data():
    """Sample high-value property lead"""
    return {
        "name": "Bob Wealthy",
        "phone": "555-9999",
        "email": "bob.wealthy@example.com",
        "property_value": 800000,
        "current_balance": 400000,
        "cash_out_amount": 150000,
        "is_veteran": "no",
        "credit_score": 780
    }


@pytest.fixture
def minimal_lead_data():
    """Minimal lead data (only required fields)"""
    return {
        "name": "Minimal User",
        "property_value": 250000
    }


@pytest.fixture
def temp_storage_dir():
    """Temporary directory for test file storage"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Cleanup
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_proposal_data():
    """Sample proposal data for PDF testing"""
    return {
        "client_name": "John Smith",
        "property_value": 300000,
        "current_balance": 200000,
        "cash_out_amount": 50000,
        "proposals": [
            {
                "loan_type": "30-Year Fixed Cashout Refinance",
                "option_a": {
                    "interest_rate": 6.5,
                    "apr": 6.662,
                    "monthly_payment": 1896.20,
                    "loan_amount": 265000,
                    "total_closing_costs": 7950
                },
                "option_b": {
                    "interest_rate": 6.25,
                    "apr": 6.565,
                    "monthly_payment": 1850.50,
                    "loan_amount": 267000,
                    "total_closing_costs": 10025
                }
            },
            {
                "loan_type": "HELOC",
                "option_a": {
                    "interest_rate": 8.5,
                    "apr": 8.750,
                    "monthly_payment": 619.93,
                    "loan_amount": 50000,
                    "total_closing_costs": 1500
                },
                "option_b": {
                    "interest_rate": 8.25,
                    "apr": 8.625,
                    "monthly_payment": 600.00,
                    "loan_amount": 51000,
                    "total_closing_costs": 2550
                }
            },
            {
                "loan_type": "HELOAN (20-Year Fixed)",
                "option_a": {
                    "interest_rate": 7.75,
                    "apr": 7.850,
                    "monthly_payment": 615.71,
                    "loan_amount": 75000,
                    "total_closing_costs": 2250
                },
                "option_b": {
                    "interest_rate": 7.5,
                    "apr": 7.750,
                    "monthly_payment": 600.00,
                    "loan_amount": 76000,
                    "total_closing_costs": 3800
                }
            }
        ]
    }


@pytest.fixture
def sample_conversation():
    """Sample conversation history for chatbot testing"""
    return [
        {"role": "assistant", "content": "Hello! I'm here to help you explore mortgage options. What's your name?"},
        {"role": "user", "content": "Hi, my name is John Smith"},
        {"role": "assistant", "content": "Nice to meet you, John! What's the estimated value of your property?"},
        {"role": "user", "content": "My home is worth about $300,000"},
        {"role": "assistant", "content": "Great! What's your current mortgage balance?"},
        {"role": "user", "content": "I owe $200,000 on my current mortgage"},
        {"role": "assistant", "content": "How much cash would you like to take out?"},
        {"role": "user", "content": "I'd like to get $50,000 cash out"},
        {"role": "assistant", "content": "Are you a military veteran?"},
        {"role": "user", "content": "No, I'm not a veteran"}
    ]


@pytest.fixture
def rate_config():
    """Sample rate configuration"""
    return {
        "rates": {
            "30_year_fixed": {
                "base_rate": 6.5,
                "fha_rate": 6.25,
                "va_rate": 6.0,
                "conventional_rate": 6.75
            },
            "heloc": {
                "base_rate": 8.5,
                "term_years": 10
            },
            "heloan": {
                "base_rate": 7.75,
                "term_years": 20
            }
        },
        "fees": {
            "origination": 0.01,  # 1%
            "appraisal": 500,
            "title": 1200,
            "recording": 250,
            "credit_report": 50
        }
    }


@pytest.fixture
def bonzo_lead_json():
    """Sample Bonzo-style JSON lead data"""
    return {
        "FullName": "Peter Walker",
        "PhoneNumber": "555-0001",
        "EmailAddress": "peter.walker@example.com",
        "PropertyValue": "350000",
        "CurrentMortgageBalance": "280000",
        "DesiredCashOut": "25000",
        "VeteranStatus": "No",
        "CreditScore": "720",
        "LeadSource": "LendingTree"
    }


@pytest.fixture
def campaign_lead_data():
    """Lead data formatted for campaign management"""
    return {
        "lead_id": "test_lead_12345",
        "name": "Campaign Test User",
        "phone": "555-CAMPAIGN",
        "email": "campaign@test.com",
        "property_value": 300000,
        "cash_out_amount": 50000,
        "timezone": "US/Eastern",
        "preferred_contact": "SMS"
    }


# Markers for test categorization
def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow-running tests")
    config.addinivalue_line("markers", "pdf: PDF generation tests")
    config.addinivalue_line("markers", "chatbot: Chatbot tests")
    config.addinivalue_line("markers", "campaign: Campaign management tests")
    config.addinivalue_line("markers", "calculations: Mortgage calculation tests")
