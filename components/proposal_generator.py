"""
Proposal Generator - Creates loan proposals with calculations
"""
import math


class ProposalGenerator:
    """Generates mortgage proposals based on lead data and current rates"""
    
    def __init__(self, lead_data, rates_config):
        """
        Initialize with lead data and daily rates
        
        Args:
            lead_data: Dictionary with client information
            rates_config: Dictionary with current rates and fees
        """
        self.lead_data = lead_data
        self.rates = rates_config
        
        # Extract key values
        self.name = lead_data.get("name", "Client")
        self.property_value = lead_data.get("property_value", 0)
        self.current_balance = lead_data.get("current_balance", 0)
        self.cash_out_amount = lead_data.get("cash_out_amount", 0)
        self.is_veteran = lead_data.get("is_veteran", "no").lower() == "yes"
        
        # Determine loan goal
        self.is_cashout = self.cash_out_amount > 0
    
    def calculate_monthly_payment(self, loan_amount, annual_rate, term_months):
        """Calculate monthly mortgage payment using standard formula"""
        if loan_amount <= 0 or annual_rate <= 0:
            return 0
        
        monthly_rate = annual_rate / 100 / 12
        
        # M = P[r(1+r)^n]/[(1+r)^n-1]
        numerator = loan_amount * monthly_rate * math.pow(1 + monthly_rate, term_months)
        denominator = math.pow(1 + monthly_rate, term_months) - 1
        
        return numerator / denominator
    
    def calculate_apr(self, loan_amount, interest_rate, loan_costs, term_months):
        """
        Calculate APR (simplified version)
        APR accounts for the total cost including fees
        """
        # Effective loan amount after fees
        effective_amount = loan_amount - loan_costs
        
        # Prevent division by zero
        if effective_amount <= 0 or term_months <= 0:
            return interest_rate  # Return base rate if calculation not possible
        
        # This is a simplified APR calculation
        # Real APR calculation is more complex
        total_interest = (self.calculate_monthly_payment(loan_amount, interest_rate, term_months) * term_months) - loan_amount
        total_cost = total_interest + loan_costs
        
        apr = (total_cost / effective_amount / (term_months / 12)) * 100
        
        return apr
    
    def generate_cashout_primary(self):
        """Generate primary cash-out refinance option (FHA or VA based on veteran status)"""
        loan_type = "VA" if self.is_veteran else "FHA"
        config_key = "va" if self.is_veteran else "fha"
        
        # Calculate loan amount: current balance + cash out + costs
        loan_amount_opt1 = self.current_balance + self.cash_out_amount + self.rates[config_key]["cost1"]
        loan_amount_opt2 = self.current_balance + self.cash_out_amount + self.rates[config_key]["cost2"]
        
        term_months = 360  # 30 year fixed
        
        # Option A
        rate1 = self.rates[config_key]["rate1"]
        cost1 = self.rates[config_key]["cost1"]
        payment1 = self.calculate_monthly_payment(loan_amount_opt1, rate1, term_months)
        apr1 = self.calculate_apr(loan_amount_opt1, rate1, cost1, term_months)
        
        # Option B
        rate2 = self.rates[config_key]["rate2"]
        cost2 = self.rates[config_key]["cost2"]
        payment2 = self.calculate_monthly_payment(loan_amount_opt2, rate2, term_months)
        apr2 = self.calculate_apr(loan_amount_opt2, rate2, cost2, term_months)
        
        return {
            "type": f"Cash Out Refinance ({loan_type})",
            "description": f"This option replaces your current mortgage with a new {loan_type} loan, giving you ${self.cash_out_amount:,} in cash.",
            "options": [
                {
                    "name": "Option A",
                    "loan_amount": loan_amount_opt1,
                    "interest_rate": rate1,
                    "apr": apr1,
                    "term": "30 Year Fixed",
                    "monthly_payment": payment1,
                    "loan_costs": cost1,
                    "cash_to_borrower": self.cash_out_amount
                },
                {
                    "name": "Option B",
                    "loan_amount": loan_amount_opt2,
                    "interest_rate": rate2,
                    "apr": apr2,
                    "term": "30 Year Fixed",
                    "monthly_payment": payment2,
                    "loan_costs": cost2,
                    "cash_to_borrower": self.cash_out_amount
                }
            ]
        }
    
    def generate_heloc(self):
        """Generate HELOC option (Home Equity Line of Credit)"""
        # HELOC amount = cash out + fees
        heloc_amount = self.cash_out_amount + self.rates["heloc"]["fees"]
        
        rate = self.rates["heloc"]["rate"]
        fees = self.rates["heloc"]["fees"]
        term_months = 360  # 30 years (10 draw + 20 repayment typically)
        
        # For HELOC, payment is typically interest-only during draw period
        # We'll calculate based on 10-year ARM style
        payment = self.calculate_monthly_payment(heloc_amount, rate, 120)  # 10 year ARM
        apr = self.calculate_apr(heloc_amount, rate, fees, 120)
        
        return {
            "type": "Home Equity Line of Credit (HELOC)",
            "description": "A revolving line of credit (like a credit card) secured by your home. This is a second mortgage.",
            "options": [
                {
                    "name": "HELOC",
                    "loan_amount": heloc_amount,
                    "interest_rate": rate,
                    "apr": apr,
                    "term": "10 Year ARM",
                    "monthly_payment": payment,
                    "loan_costs": fees,
                    "cash_to_borrower": self.cash_out_amount,
                    "note": "You keep your existing mortgage"
                }
            ]
        }
    
    def generate_heloan(self):
        """Generate HELOAN option (Home Equity Loan)"""
        # Calculate loan amounts for 20-year and 30-year options
        loan_amount_20yr = self.cash_out_amount + self.rates["heloan"]["cost1"]
        loan_amount_30yr = self.cash_out_amount + self.rates["heloan"]["cost2"]
        
        # 20-year option
        rate1 = self.rates["heloan"]["rate1"]
        cost1 = self.rates["heloan"]["cost1"]
        payment1 = self.calculate_monthly_payment(loan_amount_20yr, rate1, 240)
        apr1 = self.calculate_apr(loan_amount_20yr, rate1, cost1, 240)
        
        # 30-year option
        rate2 = self.rates["heloan"]["rate2"]
        cost2 = self.rates["heloan"]["cost2"]
        payment2 = self.calculate_monthly_payment(loan_amount_30yr, rate2, 360)
        apr2 = self.calculate_apr(loan_amount_30yr, rate2, cost2, 360)
        
        return {
            "type": "Home Equity Loan (HELOAN)",
            "description": "A fixed-rate second mortgage with predictable monthly payments. You keep your existing mortgage.",
            "options": [
                {
                    "name": "20-Year Fixed",
                    "loan_amount": loan_amount_20yr,
                    "interest_rate": rate1,
                    "apr": apr1,
                    "term": "20 Year Fixed",
                    "monthly_payment": payment1,
                    "loan_costs": cost1,
                    "cash_to_borrower": self.cash_out_amount
                },
                {
                    "name": "30-Year Fixed",
                    "loan_amount": loan_amount_30yr,
                    "interest_rate": rate2,
                    "apr": apr2,
                    "term": "30 Year Fixed",
                    "monthly_payment": payment2,
                    "loan_costs": cost2,
                    "cash_to_borrower": self.cash_out_amount
                }
            ]
        }
    
    def generate_rateterm_primary(self):
        """Generate primary rate/term refinance option"""
        # For rate/term, we're just replacing the existing mortgage
        # Use Conventional loan type for rate/term
        
        loan_amount_opt1 = self.current_balance + self.rates["conventional"]["cost1"]
        loan_amount_opt2 = self.current_balance + self.rates["conventional"]["cost2"]
        
        term_months = 360  # 30 year fixed
        
        # Option A
        rate1 = self.rates["conventional"]["rate1"]
        cost1 = self.rates["conventional"]["cost1"]
        payment1 = self.calculate_monthly_payment(loan_amount_opt1, rate1, term_months)
        apr1 = self.calculate_apr(loan_amount_opt1, rate1, cost1, term_months)
        
        # Option B
        rate2 = self.rates["conventional"]["rate2"]
        cost2 = self.rates["conventional"]["cost2"]
        payment2 = self.calculate_monthly_payment(loan_amount_opt2, rate2, term_months)
        apr2 = self.calculate_apr(loan_amount_opt2, rate2, cost2, term_months)
        
        return {
            "type": "Rate/Term Refinance (Conventional)",
            "description": "This option replaces your current mortgage with a new loan at a better rate, potentially lowering your monthly payment.",
            "options": [
                {
                    "name": "Option A",
                    "loan_amount": loan_amount_opt1,
                    "interest_rate": rate1,
                    "apr": apr1,
                    "term": "30 Year Fixed",
                    "monthly_payment": payment1,
                    "loan_costs": cost1,
                    "cash_to_borrower": 0
                },
                {
                    "name": "Option B",
                    "loan_amount": loan_amount_opt2,
                    "interest_rate": rate2,
                    "apr": apr2,
                    "term": "30 Year Fixed",
                    "monthly_payment": payment2,
                    "loan_costs": cost2,
                    "cash_to_borrower": 0
                }
            ]
        }
    
    def generate_all_proposals(self):
        """Generate all 3 proposal options"""
        proposals = []
        
        if self.is_cashout:
            # Cash out refinance scenario
            proposals.append(self.generate_cashout_primary())
            proposals.append(self.generate_heloc())
            proposals.append(self.generate_heloan())
        else:
            # Rate/term refinance scenario
            proposals.append(self.generate_rateterm_primary())
            # For rate/term, we still show alternative options
            # but they would be different rate/term structures
            # For simplicity, showing HELOC/HELOAN with 0 cash out
            self.cash_out_amount = 0  # Override for these calculations
            proposals.append(self.generate_heloc())
            proposals.append(self.generate_heloan())
        
        return proposals
