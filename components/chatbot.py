"""
Chatbot Module - Handles conversation logic and lead data extraction
"""
from openai import OpenAI
import json


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
        """Extract structured lead data from conversation using AI"""
        
        # Join user messages into context
        user_messages = [msg["content"] for msg in conversation_history if msg["role"] == "user"]
        
        if not user_messages:
            return {}
        
        conversation_text = "\n".join(user_messages)
        
        # Use AI to extract structured data
        extraction_prompt = f"""You are a data extraction AI. Extract mortgage lead information from this conversation.

Conversation:
{conversation_text}

Extract the following information if mentioned (return ONLY valid JSON):
- name: Full name (string)
- property_value: Property value in dollars (number, no commas)
- current_balance: Current mortgage balance in dollars (number, no commas)
- cash_out_amount: Desired cash out amount in dollars (number, no commas). Convert "20k" to 20000, "50k" to 50000, etc.
- is_veteran: Veteran status ("yes" or "no" or null if not mentioned)
- annual_income: Annual income in dollars (number, no commas)
- address: Property address (string)
- cash_out_intent: If they mention wanting cash/money but no specific amount (boolean)

Important rules:
- Only include fields that were explicitly mentioned
- Convert all "k" suffix numbers to thousands (e.g., "20k" = 20000)
- If they say "not a veteran" or "no" to veteran, set is_veteran to "no"
- If they say "veteran" or "yes" to veteran, set is_veteran to "yes"
- Return valid JSON only, no explanations

Example output:
{{"name": "John Smith", "property_value": 300000, "cash_out_amount": 20000, "is_veteran": "no"}}

JSON:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cheap model for extraction
                messages=[
                    {"role": "system", "content": "You are a precise data extraction AI. Return only valid JSON."},
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                response_format={"type": "json_object"}
            )
            
            extracted_json = response.choices[0].message.content
            lead_data = json.loads(extracted_json)
            
            # Clean up the data - remove None values and ensure proper types
            cleaned_data = {}
            for key, value in lead_data.items():
                if value is not None and value != "":
                    # Convert numeric strings to integers
                    if key in ["property_value", "current_balance", "cash_out_amount", "annual_income"]:
                        try:
                            cleaned_data[key] = int(value)
                        except (ValueError, TypeError):
                            pass
                    else:
                        cleaned_data[key] = value
            
            return cleaned_data
            
        except Exception as e:
            print(f"Error in AI extraction: {str(e)}")
            # Fallback to empty dict if extraction fails
            return {}
    
    def should_generate_proposal(self, lead_data):
        """Check if we have enough data to generate a proposal"""
        required_fields = ["name", "property_value", "current_balance", "is_veteran"]
        
        # Must have cash out amount OR intent
        has_cashout_info = "cash_out_amount" in lead_data or "cash_out_intent" in lead_data
        
        has_required = all(field in lead_data for field in required_fields)
        
        return has_required and has_cashout_info
    
    def get_response(self, user_message, current_lead_data, conversation_history):
        """Generate a response to user message"""
        
        # Build conversation context with lead data if available
        system_prompt = self.system_prompt
        
        # If we have lead data already, add it to the system context
        if current_lead_data:
            lead_context = "\n\n**CURRENT LEAD INFORMATION (Already Known):**\n"
            if "name" in current_lead_data:
                lead_context += f"- Client Name: {current_lead_data['name']}\n"
            if "property_value" in current_lead_data:
                lead_context += f"- Property Value: ${current_lead_data['property_value']:,}\n"
            if "current_balance" in current_lead_data:
                lead_context += f"- Current Mortgage Balance: ${current_lead_data['current_balance']:,}\n"
            if "cash_out_amount" in current_lead_data:
                lead_context += f"- Desired Cash Out: ${current_lead_data['cash_out_amount']:,}\n"
            if "is_veteran" in current_lead_data:
                vet_status = "Yes" if current_lead_data['is_veteran'].lower() == 'yes' else "No"
                lead_context += f"- Veteran Status: {vet_status}\n"
            if "address" in current_lead_data:
                lead_context += f"- Property Address: {current_lead_data['address']}\n"
            
            lead_context += "\n**IMPORTANT**: You already have this information. DO NOT ask for it again. Use it to provide personalized guidance."
            system_prompt += lead_context
        
        messages = [
            {"role": "system", "content": system_prompt}
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
        
        # Check if key values changed (like cash_out_amount)
        significant_change = False
        change_description = []
        
        if extracted_data.get("cash_out_amount") is not None:
            old_cashout = current_lead_data.get("cash_out_amount", 0)
            new_cashout = extracted_data.get("cash_out_amount")
            if new_cashout != old_cashout:
                significant_change = True
                change_description.append(f"cash-out amount to ${new_cashout:,}")
        
        if extracted_data.get("property_value") is not None:
            old_value = current_lead_data.get("property_value")
            new_value = extracted_data.get("property_value")
            if new_value != old_value and old_value is not None:
                significant_change = True
                change_description.append(f"property value to ${new_value:,}")
        
        if extracted_data.get("current_balance") is not None:
            old_balance = current_lead_data.get("current_balance")
            new_balance = extracted_data.get("current_balance")
            if new_balance != old_balance and old_balance is not None:
                significant_change = True
                change_description.append(f"current balance to ${new_balance:,}")
        
        if extracted_data.get("is_veteran") is not None:
            old_vet = current_lead_data.get("is_veteran", "").lower()
            new_vet = extracted_data.get("is_veteran", "").lower()
            if new_vet != old_vet and old_vet:
                significant_change = True
                vet_status = "a veteran" if new_vet == "yes" else "not a veteran"
                change_description.append(f"veteran status to {vet_status}")
        
        # If significant data changed, trigger regeneration
        if significant_change and current_lead_data:
            changes = ", ".join(change_description)
            bot_message = f"✅ **Updated!** I've changed your {changes}. Let me regenerate your proposal with this new information..."
            return {
                "message": bot_message,
                "lead_data": extracted_data,
                "generate_proposal": True
            }
        
        # Check if we should generate proposal (first time)
        generate_proposal = False
        if "[GENERATE_PROPOSAL]" in bot_message or self.should_generate_proposal(merged_data):
            generate_proposal = True
            bot_message = bot_message.replace("[GENERATE_PROPOSAL]", "").strip()
            
            # Only add the checkmark message if we're actually generating
            if generate_proposal and not bot_message.endswith("proposal"):
                bot_message += "\n\n✅ **Great! I have all the information I need. Let me generate your personalized 3-option mortgage proposal now...**"
        
        return {
            "message": bot_message,
            "lead_data": extracted_data,
            "generate_proposal": generate_proposal
        }
