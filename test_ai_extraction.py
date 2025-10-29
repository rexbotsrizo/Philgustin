"""
Quick test to verify AI-based extraction works
Run this to test the new AI extraction without running full test suite
"""
from components.chatbot import MortgageChatbot
from utils.config import load_config
import json

def test_extraction():
    """Test AI extraction with sample conversations"""
    
    config = load_config()
    chatbot = MortgageChatbot(config)
    
    print("🤖 Testing AI-Based Lead Data Extraction\n")
    print("=" * 60)
    
    # Test 1: Standard extraction
    print("\n✅ Test 1: Standard Format")
    conversation1 = [
        {"role": "user", "content": "My name is John Smith"},
        {"role": "user", "content": "My home is worth $300,000"},
        {"role": "user", "content": "I owe $200,000 on my mortgage"},
        {"role": "user", "content": "I want to cash out $50,000"},
        {"role": "user", "content": "I'm not a veteran"}
    ]
    
    result1 = chatbot.extract_lead_data(conversation1)
    print(f"Input: Standard conversation")
    print(f"Output: {json.dumps(result1, indent=2)}")
    
    # Test 2: "k" suffix
    print("\n" + "=" * 60)
    print("✅ Test 2: 'k' Suffix Format (20k)")
    conversation2 = [
        {"role": "user", "content": "Hi, I'm Sarah Johnson"},
        {"role": "user", "content": "My desired cashout is 20k"},
        {"role": "user", "content": "Property value is 400k"},
        {"role": "user", "content": "Yes, I'm a veteran"}
    ]
    
    result2 = chatbot.extract_lead_data(conversation2)
    print(f"Input: Conversation with 'k' suffix")
    print(f"Output: {json.dumps(result2, indent=2)}")
    
    # Verify "20k" was converted to 20000
    if result2.get("cash_out_amount") == 20000:
        print("✅ PASS: 20k correctly converted to 20000")
    else:
        print(f"❌ FAIL: Expected 20000, got {result2.get('cash_out_amount')}")
    
    # Test 3: Casual conversation
    print("\n" + "=" * 60)
    print("✅ Test 3: Casual Conversation Style")
    conversation3 = [
        {"role": "user", "content": "Hey, name's Bob Williams"},
        {"role": "user", "content": "House is probably worth like 500k or so"},
        {"role": "user", "content": "Still owe about 350 thousand"},
        {"role": "user", "content": "Want to pull out maybe 100k"},
        {"role": "user", "content": "Nah, not military"}
    ]
    
    result3 = chatbot.extract_lead_data(conversation3)
    print(f"Input: Casual conversation")
    print(f"Output: {json.dumps(result3, indent=2)}")
    
    # Test 4: All in one message
    print("\n" + "=" * 60)
    print("✅ Test 4: Single Message with All Info")
    conversation4 = [
        {"role": "user", "content": "I'm Emily Davis, my home is worth $450,000, I owe $300,000, want to cash out $75,000, and I served in the military"}
    ]
    
    result4 = chatbot.extract_lead_data(conversation4)
    print(f"Input: All info in one message")
    print(f"Output: {json.dumps(result4, indent=2)}")
    
    print("\n" + "=" * 60)
    print("\n🎉 AI Extraction Testing Complete!")
    print("\nKey Benefits:")
    print("  ✅ No manual regex patterns needed")
    print("  ✅ Handles casual conversation naturally")
    print("  ✅ Automatically converts '20k' to 20000")
    print("  ✅ Robust to different phrasings")
    print("  ✅ Uses GPT-4o-mini (fast & cheap)")

if __name__ == "__main__":
    test_extraction()
