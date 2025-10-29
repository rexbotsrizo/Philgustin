"""
Test that chatbot properly detects changes to cash_out_amount
"""
from components.chatbot import MortgageChatbot
from utils.config import load_config

# Initialize chatbot
config = load_config()
chatbot = MortgageChatbot(config)

# Simulate conversation with existing lead data
current_lead_data = {
    "name": "Ronnie Yates",
    "property_value": 185000,
    "current_balance": 145000,
    "cash_out_amount": 10000,  # Original: $10,000
    "is_veteran": "no"
}

print("=" * 70)
print("TEST: User changes cash out from $10,000 to $20,000")
print("=" * 70)
print()
print("Current lead data:")
print(f"  - Cash Out: ${current_lead_data['cash_out_amount']:,}")
print()

# User says "My desired cashout is 20k"
conversation_history = []
user_message = "My desired cashout is 20k"

print(f"User says: '{user_message}'")
print()

# Get chatbot response
response = chatbot.get_response(user_message, current_lead_data, conversation_history)

print("Chatbot response:")
print(f"  Message: {response['message']}")
print(f"  Generate Proposal: {response['generate_proposal']}")
print()

if "cash_out_amount" in response['lead_data']:
    new_amount = response['lead_data']['cash_out_amount']
    print(f"✅ Extracted new cash out amount: ${new_amount:,}")
    
    if new_amount == 20000:
        print("✅ PASS: Correctly converted '20k' to $20,000")
    else:
        print(f"❌ FAIL: Expected $20,000 but got ${new_amount:,}")
else:
    print("❌ FAIL: Did not extract cash_out_amount")

print()
print("Expected behavior:")
print("  1. Detect that cash_out_amount changed from $10,000 to $20,000")
print("  2. Return generate_proposal=True to trigger regeneration")
print("  3. Show message about updating the cash out amount")
print()

if response['generate_proposal']:
    print("✅ PASS: Will regenerate proposal with new amount")
else:
    print("❌ FAIL: Did not trigger proposal regeneration")

print()
print("=" * 70)
print("TEST 2: User says '30000' (testing plain number)")
print("=" * 70)
print()

user_message2 = "Actually make it 30000"
response2 = chatbot.get_response(user_message2, current_lead_data, conversation_history)

if "cash_out_amount" in response2['lead_data']:
    amount2 = response2['lead_data']['cash_out_amount']
    print(f"Extracted: ${amount2:,}")
    if amount2 == 30000:
        print("✅ PASS: Correctly extracted $30,000")
    else:
        print(f"❌ Got: ${amount2:,}")
else:
    print("❌ FAIL: Did not extract amount")

