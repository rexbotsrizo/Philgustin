"""
Lead Data Manager - Handle lead data storage and retrieval
"""
import json
import os
from datetime import datetime


class LeadDataManager:
    """Manages lead data storage and retrieval"""
    
    def __init__(self, data_file="leads_data.json"):
        """Initialize the lead data manager"""
        self.data_file = data_file
        self.leads = self._load_leads()
    
    def _load_leads(self):
        """Load leads from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_leads(self):
        """Save leads to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.leads, f, indent=2)
    
    def add_lead(self, lead_data):
        """Add or update a lead"""
        lead_id = lead_data.get("lead_id", str(datetime.now().timestamp()))
        self.leads[lead_id] = lead_data
        self._save_leads()
        return lead_id
    
    def get_lead(self, lead_id):
        """Get a specific lead by ID"""
        return self.leads.get(lead_id)
    
    def get_all_leads(self):
        """Get all leads"""
        return self.leads
    
    def delete_lead(self, lead_id):
        """Delete a lead"""
        if lead_id in self.leads:
            del self.leads[lead_id]
            self._save_leads()
            return True
        return False
    
    def update_lead(self, lead_id, updated_data):
        """Update an existing lead"""
        if lead_id in self.leads:
            self.leads[lead_id].update(updated_data)
            self._save_leads()
            return True
        return False
    
    def parse_bonzo_lead(self, bonzo_json):
        """
        Parse Bonzo CRM lead format to our internal format
        
        Args:
            bonzo_json: Dictionary with Bonzo CRM lead data
            
        Returns:
            Dictionary with parsed lead data for our system
        """
        # Handle veteran status variations
        is_veteran = bonzo_json.get("custom_is_veteran", "no")
        if isinstance(is_veteran, str):
            is_veteran = is_veteran.lower() in ["yes", "true", "1"]
        elif isinstance(is_veteran, bool):
            is_veteran = is_veteran
        else:
            is_veteran = False
        
        # Parse cash out amount
        cash_out = bonzo_json.get("cash_out_amount", "0")
        try:
            cash_out_amount = int(str(cash_out).replace(",", ""))
        except:
            cash_out_amount = 0
        
        # Parse property value
        try:
            property_value = int(str(bonzo_json.get("property_value", "0")).replace(",", ""))
        except:
            property_value = 0
        
        # Parse current loan amount
        try:
            current_balance = int(str(bonzo_json.get("loan_amount", "0")).replace(",", ""))
        except:
            current_balance = 0
        
        # Parse annual income if available
        annual_income = None
        if "annual_income" in bonzo_json:
            try:
                annual_income = int(str(bonzo_json.get("annual_income", "0")).replace(",", ""))
            except:
                annual_income = None
        
        parsed_data = {
            # Original Bonzo data
            "bonzo_data": bonzo_json,
            
            # Parsed data for our system
            "lead_id": bonzo_json.get("lead_id"),
            "name": f"{bonzo_json.get('first_name', '')} {bonzo_json.get('last_name', '')}".strip(),
            "first_name": bonzo_json.get("first_name"),
            "last_name": bonzo_json.get("last_name"),
            "email": bonzo_json.get("email"),
            "phone": bonzo_json.get("phone"),
            "property_value": property_value,
            "current_balance": current_balance,
            "cash_out_amount": cash_out_amount,
            "is_veteran": "yes" if is_veteran else "no",
            "credit_score": bonzo_json.get("credit_score"),
            "loan_purpose": bonzo_json.get("loan_purpose"),
            "property_type": bonzo_json.get("property_type"),
            "property_address": bonzo_json.get("property_address") or bonzo_json.get("address"),
            "property_city": bonzo_json.get("property_city") or bonzo_json.get("city"),
            "property_state": bonzo_json.get("property_state") or bonzo_json.get("state"),
            "property_zip": bonzo_json.get("property_zip") or bonzo_json.get("zip"),
            "birthday": bonzo_json.get("birthday"),
            "annual_income": annual_income,
            "lead_source": bonzo_json.get("lead_source"),
            "application_date": bonzo_json.get("application_date"),
        }
        
        return parsed_data
    
    def get_sample_leads(self):
        """Return sample leads for testing"""
        return {
            "36391862": {
                "lead_id": "36391862",
                "lead_source": "BROWN - CASHOUT - Good/Exc",
                "application_date": "2025-10-20",
                "timezone": "Eastern",
                "first_name": "Ronnie",
                "last_name": "Yates",
                "email": "yatesronnie@yahoo.com",
                "phone": "8595162730",
                "address": "196 W Jefferson Ave",
                "city": "Danville",
                "state": "KY",
                "zip": "40422",
                "property_address": "196 W Jefferson Ave",
                "property_city": "Danville",
                "property_state": "KY",
                "property_zip": "40422",
                "property_county": None,
                "company_name": None,
                "prospect_company": None,
                "credit_score": "EXCELLENT",
                "loan_program": None,
                "loan_purpose": "Refinance",
                "loan_amount": "145000",
                "new_loan_amount": "155000",
                "loan_type": "Fixed_or_Adjustable",
                "down_payment": None,
                "interest_rate": None,
                "purchase_price": "185000",
                "cash_out_amount": "10000",
                "property_type": "single_fam",
                "property_use": None,
                "property_value": "185000",
                "birthday": None,
                "field_1": "custom1",
                "field_2": "custom2",
                "field_3": "custom3",
                "custom_is_veteran": "no",
                "custom_current_va_loan": None,
                "custom_current_fha_loan": None,
                "notes": ["From LeadMailbox", None]
            },
            "36389389": {
                "lead_id": "36389389",
                "lead_source": "MAROON +",
                "application_date": "2025-10-20",
                "timezone": "Eastern",
                "first_name": "Peter",
                "last_name": "Walker",
                "email": "peterwalker2@gmail.com",
                "phone": "6143608535",
                "address": "1104 Clubview Blvd S",
                "city": "Columbus",
                "state": "OH",
                "zip": "43235",
                "property_address": None,
                "property_city": "Columbus",
                "property_state": "OH",
                "property_zip": "43235",
                "property_county": "FRANKLIN",
                "company_name": None,
                "prospect_company": None,
                "credit_score": "769",
                "loan_program": None,
                "loan_purpose": "REFINANCE CASHOUT",
                "loan_amount": "367034",
                "new_loan_amount": "277000",
                "loan_type": None,
                "down_payment": None,
                "interest_rate": None,
                "purchase_price": None,
                "cash_out_amount": "82000",
                "property_type": "SINGLEFAMDET",
                "property_use": "OWNEROCCUPIED",
                "property_value": "600000",
                "birthday": "7/24/1982",
                "field_1": "custom1",
                "field_2": "custom2",
                "field_3": "custom3",
                "custom_is_veteran": "False",
                "custom_current_va_loan": None,
                "custom_current_fha_loan": None,
                "notes": ["From LeadMailbox", None]
            }
        }
