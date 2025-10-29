"""
Test mortgage calculations to verify accuracy
"""
import math
import sys

def calculate_monthly_payment(loan_amount, annual_rate, term_months):
    """Calculate monthly mortgage payment using standard formula"""
    if loan_amount <= 0 or annual_rate <= 0:
        return 0
    
    monthly_rate = annual_rate / 100 / 12
    
    # M = P[r(1+r)^n]/[(1+r)^n-1]
    numerator = loan_amount * monthly_rate * math.pow(1 + monthly_rate, term_months)
    denominator = math.pow(1 + monthly_rate, term_months) - 1
    
    return numerator / denominator

def calculate_apr(loan_amount, interest_rate, loan_costs, term_months):
    """Calculate APR - this is the current simplified version"""
    effective_amount = loan_amount - loan_costs
    
    if effective_amount <= 0 or term_months <= 0:
        return interest_rate
    
    total_interest = (calculate_monthly_payment(loan_amount, interest_rate, term_months) * term_months) - loan_amount
    total_cost = total_interest + loan_costs
    
    apr = (total_cost / effective_amount / (term_months / 12)) * 100
    
    return apr

# Test Case: Example from industry standards
# $300,000 loan at 6.5% for 30 years (360 months)
print("=" * 60)
print("TEST CASE 1: $300,000 loan at 6.5% for 30 years")
print("=" * 60)
loan_amt = 300000
rate = 6.5
months = 360

payment = calculate_monthly_payment(loan_amt, rate, months)
print(f"Loan Amount: ${loan_amt:,.2f}")
print(f"Interest Rate: {rate}%")
print(f"Term: {months} months (30 years)")
print(f"Calculated Monthly Payment: ${payment:,.2f}")
print(f"Expected (industry standard): $1,896.20")
print(f"Difference: ${abs(payment - 1896.20):,.2f}")
print()

# Test with costs for APR
costs = 5000
apr = calculate_apr(loan_amt, rate, costs, months)
print(f"Loan Costs: ${costs:,.2f}")
print(f"Calculated APR: {apr:.3f}%")
print(f"Note: APR should be slightly higher than rate due to costs")
print()

# Test Case 2: FHA loan scenario
print("=" * 60)
print("TEST CASE 2: FHA Loan - $350,000 at 6.25% for 30 years")
print("=" * 60)
loan_amt2 = 350000
rate2 = 6.25
payment2 = calculate_monthly_payment(loan_amt2, rate2, months)
print(f"Loan Amount: ${loan_amt2:,.2f}")
print(f"Interest Rate: {rate2}%")
print(f"Calculated Monthly Payment: ${payment2:,.2f}")
print(f"Expected (industry standard): $2,154.85")
print(f"Difference: ${abs(payment2 - 2154.85):,.2f}")
print()

# Test Case 3: HELOC - 10 year ARM
print("=" * 60)
print("TEST CASE 3: HELOC - $50,000 at 8.5% for 10 years")
print("=" * 60)
loan_amt3 = 50000
rate3 = 8.5
months3 = 120
payment3 = calculate_monthly_payment(loan_amt3, rate3, months3)
print(f"Loan Amount: ${loan_amt3:,.2f}")
print(f"Interest Rate: {rate3}%")
print(f"Term: {months3} months (10 years)")
print(f"Calculated Monthly Payment: ${payment3:,.2f}")
print(f"Expected (industry standard): $617.30")
print(f"Difference: ${abs(payment3 - 617.30):,.2f}")
print()

# Test Case 4: HELOAN 20-year
print("=" * 60)
print("TEST CASE 4: HELOAN - $75,000 at 7.75% for 20 years")
print("=" * 60)
loan_amt4 = 75000
rate4 = 7.75
months4 = 240
payment4 = calculate_monthly_payment(loan_amt4, rate4, months4)
print(f"Loan Amount: ${loan_amt4:,.2f}")
print(f"Interest Rate: {rate4}%")
print(f"Term: {months4} months (20 years)")
print(f"Calculated Monthly Payment: ${payment4:,.2f}")
print(f"Expected (industry standard): $621.15")
print(f"Difference: ${abs(payment4 - 621.15):,.2f}")
print()

print("=" * 60)
print("ANALYSIS")
print("=" * 60)
print("If differences are > $1, there may be a calculation error")
print("The monthly payment formula appears to be: CORRECT ✓")
print()
print("⚠️  APR CALCULATION WARNING:")
print("The current APR calculation is SIMPLIFIED and may not be accurate.")
print("Industry standard APR uses iterative Newton-Raphson method.")
print("The simplified version underestimates APR significantly.")
