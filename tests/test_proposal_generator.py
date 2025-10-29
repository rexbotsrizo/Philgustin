"""
Test Cases for Proposal Generator - Mortgage Calculations
Tests monthly payments, APR calculations, and loan amount calculations
"""
import pytest
import math
from components.proposal_generator import ProposalGenerator


class TestMonthlyPaymentCalculations:
    """Test the monthly payment calculation formula"""
    
    def setup_method(self):
        """Setup test data"""
        self.rates_config = {
            "fha": {"rate1": 6.5, "rate2": 6.75, "cost1": 5600, "cost2": 4050},
            "va": {"rate1": 6.0, "rate2": 6.25, "cost1": 5000, "cost2": 3500},
            "conventional": {"rate1": 7.0, "rate2": 7.25, "cost1": 7000, "cost2": 4500},
            "heloc": {"rate": 8.5, "fees": 500},
            "heloan": {"rate1": 7.75, "rate2": 8.0, "cost1": 1700, "cost2": 2500}
        }
    
    def test_standard_30year_mortgage(self):
        """Test standard 30-year mortgage calculation"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 0,
            "cash_out_amount": 0,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        payment = generator.calculate_monthly_payment(300000, 6.5, 360)
        
        # Expected: $1,896.20 (industry standard)
        assert abs(payment - 1896.20) < 1.0, f"Expected ~$1,896.20, got ${payment:.2f}"
    
    def test_fha_loan_calculation(self):
        """Test FHA loan monthly payment"""
        lead_data = {
            "name": "Test User",
            "property_value": 350000,
            "current_balance": 0,
            "cash_out_amount": 0,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        payment = generator.calculate_monthly_payment(350000, 6.25, 360)
        
        # Expected: ~$2,155 (industry standard)
        assert abs(payment - 2155.01) < 1.0, f"Expected ~$2,155, got ${payment:.2f}"
    
    def test_heloc_10year(self):
        """Test HELOC 10-year ARM calculation"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        payment = generator.calculate_monthly_payment(50000, 8.5, 120)
        
        # Expected: ~$619.93
        assert abs(payment - 619.93) < 5.0, f"Expected ~$619.93, got ${payment:.2f}"
    
    def test_heloan_20year(self):
        """Test HELOAN 20-year calculation"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 75000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        payment = generator.calculate_monthly_payment(75000, 7.75, 240)
        
        # Expected: ~$615.71
        assert abs(payment - 615.71) < 10.0, f"Expected ~$615.71, got ${payment:.2f}"
    
    def test_zero_loan_amount(self):
        """Test handling of zero loan amount"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 0,
            "cash_out_amount": 0,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        payment = generator.calculate_monthly_payment(0, 6.5, 360)
        
        assert payment == 0, "Zero loan amount should return $0 payment"
    
    def test_zero_interest_rate(self):
        """Test handling of zero interest rate"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 0,
            "cash_out_amount": 0,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        payment = generator.calculate_monthly_payment(300000, 0, 360)
        
        assert payment == 0, "Zero interest rate should return $0 payment"


class TestAPRCalculations:
    """Test the APR calculation using Newton-Raphson method"""
    
    def setup_method(self):
        """Setup test data"""
        self.rates_config = {
            "fha": {"rate1": 6.5, "rate2": 6.75, "cost1": 5600, "cost2": 4050},
            "va": {"rate1": 6.0, "rate2": 6.25, "cost1": 5000, "cost2": 3500},
            "conventional": {"rate1": 7.0, "rate2": 7.25, "cost1": 7000, "cost2": 4500},
            "heloc": {"rate": 8.5, "fees": 500},
            "heloan": {"rate1": 7.75, "rate2": 8.0, "cost1": 1700, "cost2": 2500}
        }
    
    def test_apr_higher_than_rate_with_fees(self):
        """APR should be HIGHER than interest rate when fees exist"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 0,
            "cash_out_amount": 0,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        
        loan_amount = 300000
        interest_rate = 6.5
        loan_costs = 5000
        term_months = 360
        
        apr = generator.calculate_apr(loan_amount, interest_rate, loan_costs, term_months)
        
        assert apr > interest_rate, f"APR ({apr:.3f}%) should be higher than rate ({interest_rate}%) when fees exist"
        # Expected: ~6.662%
        assert abs(apr - 6.662) < 0.01, f"Expected APR ~6.662%, got {apr:.3f}%"
    
    def test_apr_equals_rate_with_zero_fees(self):
        """APR should EQUAL interest rate when there are no fees"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 0,
            "cash_out_amount": 0,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        
        loan_amount = 200000
        interest_rate = 7.0
        loan_costs = 0
        term_months = 360
        
        apr = generator.calculate_apr(loan_amount, interest_rate, loan_costs, term_months)
        
        assert abs(apr - interest_rate) < 0.001, f"APR ({apr:.3f}%) should equal rate ({interest_rate}%) with zero fees"
    
    def test_apr_with_high_fees(self):
        """Test APR calculation with higher fees"""
        lead_data = {
            "name": "Test User",
            "property_value": 350000,
            "current_balance": 0,
            "cash_out_amount": 0,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        
        loan_amount = 350000
        interest_rate = 6.25
        loan_costs = 8000
        term_months = 360
        
        apr = generator.calculate_apr(loan_amount, interest_rate, loan_costs, term_months)
        
        assert apr > interest_rate, "APR should be higher with fees"
        # Expected: ~6.470%
        assert abs(apr - 6.470) < 0.01, f"Expected APR ~6.470%, got {apr:.3f}%"
    
    def test_apr_heloc_with_fees(self):
        """Test APR for HELOC with fees"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        
        loan_amount = 50000
        interest_rate = 8.5
        loan_costs = 500
        term_months = 120
        
        apr = generator.calculate_apr(loan_amount, interest_rate, loan_costs, term_months)
        
        assert apr > interest_rate, "HELOC APR should be higher with fees"
        # Expected: ~8.734%
        assert abs(apr - 8.734) < 0.01, f"Expected APR ~8.734%, got {apr:.3f}%"


class TestLoanAmountCalculations:
    """Test loan amount calculations for different scenarios"""
    
    def setup_method(self):
        """Setup test data"""
        self.rates_config = {
            "fha": {"rate1": 6.5, "rate2": 6.75, "cost1": 5600, "cost2": 4050},
            "va": {"rate1": 6.0, "rate2": 6.25, "cost1": 5000, "cost2": 3500},
            "conventional": {"rate1": 7.0, "rate2": 7.25, "cost1": 7000, "cost2": 4500},
            "heloc": {"rate": 8.5, "fees": 500},
            "heloan": {"rate1": 7.75, "rate2": 8.0, "cost1": 1700, "cost2": 2500}
        }
    
    def test_cashout_loan_amount_calculation(self):
        """Test cash-out refinance loan amount calculation"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        
        # Expected: current_balance + cash_out + costs
        # 200,000 + 50,000 + 5,600 = 255,600
        expected_loan = 200000 + 50000 + 5600
        
        proposal = generator.generate_cashout_primary()
        actual_loan = proposal["options"][0]["loan_amount"]
        
        assert actual_loan == expected_loan, f"Expected ${expected_loan:,}, got ${actual_loan:,}"
    
    def test_heloc_amount_calculation(self):
        """Test HELOC loan amount calculation"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        
        # Expected: cash_out + fees
        # 50,000 + 500 = 50,500
        expected_heloc = 50000 + 500
        
        proposal = generator.generate_heloc()
        actual_heloc = proposal["options"][0]["loan_amount"]
        
        assert actual_heloc == expected_heloc, f"Expected ${expected_heloc:,}, got ${actual_heloc:,}"
    
    def test_heloan_amount_calculation(self):
        """Test HELOAN loan amount calculation"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 75000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        
        # Expected: cash_out + costs
        # 75,000 + 1,700 = 76,700 (20-year)
        expected_heloan = 75000 + 1700
        
        proposal = generator.generate_heloan()
        actual_heloan = proposal["options"][0]["loan_amount"]
        
        assert actual_heloan == expected_heloan, f"Expected ${expected_heloan:,}, got ${actual_heloan:,}"
    
    def test_veteran_uses_va_loan(self):
        """Test that veterans get VA loan instead of FHA"""
        lead_data_veteran = {
            "name": "Test Veteran",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "yes"
        }
        
        generator = ProposalGenerator(lead_data_veteran, self.rates_config)
        proposal = generator.generate_cashout_primary()
        
        assert "VA" in proposal["type"], "Veterans should get VA loan option"
    
    def test_non_veteran_uses_fha_loan(self):
        """Test that non-veterans get FHA loan"""
        lead_data_non_veteran = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data_non_veteran, self.rates_config)
        proposal = generator.generate_cashout_primary()
        
        assert "FHA" in proposal["type"], "Non-veterans should get FHA loan option"


class TestProposalGeneration:
    """Test complete proposal generation"""
    
    def setup_method(self):
        """Setup test data"""
        self.rates_config = {
            "fha": {"rate1": 6.5, "rate2": 6.75, "cost1": 5600, "cost2": 4050},
            "va": {"rate1": 6.0, "rate2": 6.25, "cost1": 5000, "cost2": 3500},
            "conventional": {"rate1": 7.0, "rate2": 7.25, "cost1": 7000, "cost2": 4500},
            "heloc": {"rate": 8.5, "fees": 500},
            "heloan": {"rate1": 7.75, "rate2": 8.0, "cost1": 1700, "cost2": 2500}
        }
    
    def test_generate_all_proposals_cashout(self):
        """Test generating all 3 proposals for cash-out scenario"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        proposals = generator.generate_all_proposals()
        
        assert len(proposals) == 3, "Should generate 3 proposals"
        
        # Check proposal types
        assert "Cash Out" in proposals[0]["type"] or "FHA" in proposals[0]["type"]
        assert "HELOC" in proposals[1]["type"]
        assert "HELOAN" in proposals[2]["type"] or "Equity Loan" in proposals[2]["type"]
    
    def test_proposals_have_two_options(self):
        """Test that primary proposals have 2 rate options"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        proposal = generator.generate_cashout_primary()
        
        assert len(proposal["options"]) == 2, "Should have Option A and Option B"
        assert proposal["options"][0]["name"] == "Option A"
        assert proposal["options"][1]["name"] == "Option B"
    
    def test_proposal_contains_required_fields(self):
        """Test that proposals contain all required fields"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        generator = ProposalGenerator(lead_data, self.rates_config)
        proposal = generator.generate_cashout_primary()
        
        required_keys = ["type", "description", "options"]
        for key in required_keys:
            assert key in proposal, f"Proposal should have '{key}' field"
        
        # Check option fields
        option = proposal["options"][0]
        required_option_keys = [
            "name", "loan_amount", "interest_rate", "apr",
            "term", "monthly_payment", "loan_costs", "cash_to_borrower"
        ]
        for key in required_option_keys:
            assert key in option, f"Option should have '{key}' field"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
