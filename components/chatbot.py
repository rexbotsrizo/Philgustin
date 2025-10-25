"""
Chatbot Module - Handles conversation logic and lead data extraction
"""
from openai import OpenAI
import json
import re


class MortgageChatbot:
    """AI Chatbot that acts as Phil Gustin's mortgage assistant"""
    
    def __init__(self, config):
        """Initialize the chatbot with OpenAI"""
        self.config = config
        self.client = OpenAI(api_key=config.get("openai_api_key"))
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.7)
        
        # System prompt that defines Phil's personality and role
        self.system_prompt = """You are an AI assistant representing Phil Gustin, a mortgage broker at West Capital Lending.

Your personality:
- Friendly, professional, and knowledgeable
- Patient and helpful in explaining mortgage concepts
- Quick to respond and highly attentive to client needs
- Focus on understanding the client's goals first

Your primary objectives:
1. Greet the client warmly and introduce yourself
2. Gather essential information about their mortgage needs:
   - Full name
   - Property address and value
   - Current mortgage balance
   - Whether they want cash out (and how much)
   - If they are a veteran (for VA loan eligibility)
   - Date of birth
   - Annual household income
3. Determine if this is a "Cash Out" refinance (they want money) or "Rate/Term" refinance (better rate/lower payment)
4. Once you have: name, property value, current balance, cash out amount (or 0), and veteran status - inform them you'll generate their personalized 3-option proposal

Important rules:
- Always be conversational and natural
- Don't ask for all information at once - gather it naturally through conversation
- If they mention wanting money/cash, that's a cash-out refinance
- If they mention lowering payments or getting a better rate, that's rate/term
- Veterans are eligible for VA loans (better terms)
- Be encouraging and positive about their mortgage goals

When you have enough information to generate a proposal, end your response with: [GENERATE_PROPOSAL]
"""
    
    def extract_lead_data(self, conversation_history):
        """Extract structured lead data from conversation"""
        lead_data = {}
        
        # Join all messages into one text
        full_text = " ".join([msg["content"] for msg in conversation_history if msg["role"] == "user"])
        
        # Extract name (simple pattern matching)
        name_patterns = [
            r"my name is ([A-Z][a-z]+ [A-Z][a-z]+)",
            r"I'm ([A-Z][a-z]+ [A-Z][a-z]+)",
            r"I am ([A-Z][a-z]+ [A-Z][a-z]+)"
        ]
        for pattern in name_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                lead_data["name"] = match.group(1).title()
                break
        
        # Extract property value
        value_patterns = [
            r"property.*?worth.*?\$?([\d,]+)",
            r"home.*?value.*?\$?([\d,]+)",
            r"valued at.*?\$?([\d,]+)",
            r"\$?([\d,]+).*?property value"
        ]
        for pattern in value_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                lead_data["property_value"] = int(match.group(1).replace(",", ""))
                break
        
        # Extract current balance
        balance_patterns = [
            r"owe.*?\$?([\d,]+)",
            r"balance.*?\$?([\d,]+)",
            r"current mortgage.*?\$?([\d,]+)"
        ]
        for pattern in balance_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                lead_data["current_balance"] = int(match.group(1).replace(",", ""))
                break
        
        # Extract cash out amount
        cashout_patterns = [
            r"cash out.*?\$?([\d,]+)",
            r"need.*?\$?([\d,]+)",
            r"want.*?\$?([\d,]+).*?cash"
        ]
        for pattern in cashout_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                lead_data["cash_out_amount"] = int(match.group(1).replace(",", ""))
                break
        
        # Check for cash out intent even without specific amount
        if "cash_out_amount" not in lead_data:
            if any(word in full_text.lower() for word in ["cash out", "need money", "want cash", "get money"]):
                lead_data["cash_out_intent"] = True
            else:
                lead_data["cash_out_amount"] = 0
        
        # Extract veteran status
        if any(word in full_text.lower() for word in ["veteran", "served", "military", "va loan"]):
            lead_data["is_veteran"] = "yes"
        elif any(phrase in full_text.lower() for phrase in ["not a veteran", "not veteran", "no military"]):
            lead_data["is_veteran"] = "no"
        
        # Extract income
        income_patterns = [
            r"income.*?\$?([\d,]+)",
            r"make.*?\$?([\d,]+).*?year",
            r"earn.*?\$?([\d,]+)"
        ]
        for pattern in income_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                lead_data["annual_income"] = int(match.group(1).replace(",", ""))
                break
        
        return lead_data
    
    def should_generate_proposal(self, lead_data):
        """Check if we have enough data to generate a proposal"""
        required_fields = ["name", "property_value", "current_balance", "is_veteran"]
        
        # Must have cash out amount OR intent
        has_cashout_info = "cash_out_amount" in lead_data or "cash_out_intent" in lead_data
        
        has_required = all(field in lead_data for field in required_fields)
        
        return has_required and has_cashout_info
    
    def get_response(self, user_message, current_lead_data, conversation_history):
        """Generate a response to user message"""
        
        # Build conversation context
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history
        for msg in conversation_history[-6:]:  # Keep last 6 messages for context
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Get AI response using OpenAI directly
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )
            
            bot_message = response.choices[0].message.content
        except Exception as e:
            bot_message = f"I apologize, but I'm having trouble connecting right now. Error: {str(e)}"
        
        # Extract lead data from updated conversation
        updated_history = conversation_history + [{"role": "user", "content": user_message}]
        extracted_data = self.extract_lead_data(updated_history)
        
        # Merge with existing lead data
        merged_data = {**current_lead_data, **extracted_data}
        
        # Check if we should generate proposal
        generate_proposal = False
        if "[GENERATE_PROPOSAL]" in bot_message or self.should_generate_proposal(merged_data):
            generate_proposal = True
            bot_message = bot_message.replace("[GENERATE_PROPOSAL]", "").strip()
            
            if not bot_message.endswith("proposal"):
                bot_message += "\n\n✅ **Great! I have all the information I need. Let me generate your personalized 3-option mortgage proposal now...**"
        
        return {
            "message": bot_message,
            "lead_data": extracted_data,
            "generate_proposal": generate_proposal
        }
