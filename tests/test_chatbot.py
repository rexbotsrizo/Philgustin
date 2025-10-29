"""
Test Cases for Chatbot - Lead Data Extraction and Response Generation
Note: These tests use AI-based extraction with GPT-4o-mini, so they require an OpenAI API key.
For CI/CD environments, mock the OpenAI client or skip these tests.
"""
import pytest
from unittest.mock import Mock, patch
from components.chatbot import MortgageChatbot
from utils.config import load_config


class TestLeadDataExtraction:
    """Test AI-based lead data extraction from conversation"""
    
    def setup_method(self):
        """Setup chatbot instance"""
        config = load_config()
        self.chatbot = MortgageChatbot(config)
    
    @patch('openai.OpenAI')
    def test_extract_name(self, mock_openai):
        """Test extracting client name using AI"""
        # Mock the AI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"name": "John Smith"}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "My name is John Smith"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert "name" in lead_data
        assert lead_data["name"] == "John Smith"
    
    @patch('openai.OpenAI')
    def test_extract_property_value(self, mock_openai):
        """Test extracting property value using AI"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"property_value": 350000}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "My home is worth $350,000"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert "property_value" in lead_data
        assert lead_data["property_value"] == 350000
    
    @patch('openai.OpenAI')
    def test_extract_current_balance(self, mock_openai):
        """Test extracting current mortgage balance using AI"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"current_balance": 200000}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "I owe $200,000 on my current mortgage"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert "current_balance" in lead_data
        assert lead_data["current_balance"] == 200000
    
    @patch('openai.OpenAI')
    def test_extract_cash_out_amount(self, mock_openai):
        """Test extracting desired cash out amount using AI"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"cash_out_amount": 50000}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "I want to cash out $50,000"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert "cash_out_amount" in lead_data
        assert lead_data["cash_out_amount"] == 50000
    
    @patch('openai.OpenAI')
    def test_extract_cash_out_with_k_suffix(self, mock_openai):
        """Test extracting cash out amount with 'k' suffix (e.g., '20k') - AI should convert"""
        mock_client = Mock()
        mock_response = Mock()
        # AI converts "20k" to 20000
        mock_response.choices = [Mock(message=Mock(content='{"cash_out_amount": 20000}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "My desired cashout is 20k"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert "cash_out_amount" in lead_data
        assert lead_data["cash_out_amount"] == 20000, f"Expected 20000, got {lead_data.get('cash_out_amount')}"
    
    @patch('openai.OpenAI')
    def test_extract_cash_out_plain_number(self, mock_openai):
        """Test extracting plain number as cash out using AI"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"cash_out_amount": 30000}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "Actually make it 30000"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert "cash_out_amount" in lead_data
        assert lead_data["cash_out_amount"] == 30000
    
    @patch('openai.OpenAI')
    def test_extract_veteran_status_yes(self, mock_openai):
        """Test extracting veteran status (yes) using AI"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"is_veteran": "yes"}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "I am a veteran"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert "is_veteran" in lead_data
        assert lead_data["is_veteran"] == "yes"
    
    @patch('openai.OpenAI')
    def test_extract_veteran_status_no(self, mock_openai):
        """Test extracting veteran status (no) using AI"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"is_veteran": "no"}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "I am not a veteran"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert "is_veteran" in lead_data
        assert lead_data["is_veteran"] == "no"
    
    @patch('openai.OpenAI')
    def test_extract_multiple_fields(self, mock_openai):
        """Test extracting multiple fields from conversation using AI"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"name": "Sarah Johnson", "property_value": 450000, "current_balance": 300000, "cash_out_amount": 75000, "is_veteran": "yes"}'))]
        mock_client.chat.completions.create.return_value = mock_response
        self.chatbot.client = mock_client
        
        conversation = [
            {"role": "user", "content": "Hi, my name is Sarah Johnson"},
            {"role": "assistant", "content": "Nice to meet you Sarah"},
            {"role": "user", "content": "My property is valued at $450,000 and I owe $300,000"},
            {"role": "user", "content": "I want to get $75,000 cash out and I'm a veteran"}
        ]
        
        lead_data = self.chatbot.extract_lead_data(conversation)
        
        assert lead_data["name"] == "Sarah Johnson"
        assert lead_data["property_value"] == 450000
        assert lead_data["current_balance"] == 300000
        assert lead_data["cash_out_amount"] == 75000
        assert lead_data["is_veteran"] == "yes"


class TestChangeDetection:
    """Test detection of changes to lead data"""
    
    def setup_method(self):
        """Setup chatbot instance"""
        config = load_config()
        self.chatbot = MortgageChatbot(config)
    
    def test_detect_cash_out_change(self):
        """Test detecting when cash out amount changes"""
        current_lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 10000,
            "is_veteran": "no"
        }
        
        conversation = []
        user_message = "My desired cashout is 20k"
        
        response = self.chatbot.get_response(user_message, current_lead_data, conversation)
        
        # Should detect change and trigger regeneration
        assert response["generate_proposal"] == True, "Should trigger proposal regeneration"
        assert "20,000" in response["message"], "Should mention the new amount"
        assert "cash_out_amount" in response["lead_data"]
        assert response["lead_data"]["cash_out_amount"] == 20000
    
    def test_detect_property_value_change(self):
        """Test detecting when property value changes"""
        current_lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        conversation = []
        user_message = "Actually my property is worth $350,000"
        
        response = self.chatbot.get_response(user_message, current_lead_data, conversation)
        
        # Should detect change
        assert response["generate_proposal"] == True
        assert "property_value" in response["lead_data"]
        assert response["lead_data"]["property_value"] == 350000
    
    def test_detect_veteran_status_change(self):
        """Test detecting when veteran status changes"""
        current_lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "no"
        }
        
        conversation = []
        user_message = "Actually, I am a veteran"
        
        response = self.chatbot.get_response(user_message, current_lead_data, conversation)
        
        # Should detect change
        assert response["generate_proposal"] == True
        assert "is_veteran" in response["lead_data"]
        assert response["lead_data"]["is_veteran"] == "yes"
    
    def test_no_change_detection_for_first_time(self):
        """Test that first-time data entry doesn't trigger 'change' message"""
        current_lead_data = {}
        
        conversation = []
        user_message = "I want to cash out $50,000"
        
        response = self.chatbot.get_response(user_message, current_lead_data, conversation)
        
        # Should not have "Updated!" in message (this is first time)
        assert "Updated!" not in response["message"]


class TestProposalGenerationTrigger:
    """Test when chatbot should trigger proposal generation"""
    
    def setup_method(self):
        """Setup chatbot instance"""
        config = load_config()
        self.chatbot = MortgageChatbot(config)
    
    def test_should_generate_with_complete_data(self):
        """Test proposal generation when all required data is present"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "yes"
        }
        
        should_generate = self.chatbot.should_generate_proposal(lead_data)
        
        assert should_generate == True, "Should generate proposal with complete data"
    
    def test_should_not_generate_without_name(self):
        """Test that proposal doesn't generate without name"""
        lead_data = {
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "yes"
        }
        
        should_generate = self.chatbot.should_generate_proposal(lead_data)
        
        assert should_generate == False, "Should not generate without name"
    
    def test_should_not_generate_without_property_value(self):
        """Test that proposal doesn't generate without property value"""
        lead_data = {
            "name": "Test User",
            "current_balance": 200000,
            "cash_out_amount": 50000,
            "is_veteran": "yes"
        }
        
        should_generate = self.chatbot.should_generate_proposal(lead_data)
        
        assert should_generate == False, "Should not generate without property value"
    
    def test_should_not_generate_without_veteran_status(self):
        """Test that proposal doesn't generate without veteran status"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_amount": 50000
        }
        
        should_generate = self.chatbot.should_generate_proposal(lead_data)
        
        assert should_generate == False, "Should not generate without veteran status"
    
    def test_should_generate_with_cash_out_intent(self):
        """Test proposal generation with cash out intent but no specific amount"""
        lead_data = {
            "name": "Test User",
            "property_value": 300000,
            "current_balance": 200000,
            "cash_out_intent": True,
            "is_veteran": "no"
        }
        
        should_generate = self.chatbot.should_generate_proposal(lead_data)
        
        assert should_generate == True, "Should generate with cash out intent"


class TestLeadContextInjection:
    """Test that loaded lead data is injected into system prompt"""
    
    def setup_method(self):
        """Setup chatbot instance"""
        config = load_config()
        self.chatbot = MortgageChatbot(config)
    
    def test_system_prompt_includes_lead_data(self):
        """Test that existing lead data is added to system prompt"""
        current_lead_data = {
            "name": "Ronnie Yates",
            "property_value": 185000,
            "current_balance": 145000,
            "cash_out_amount": 10000,
            "is_veteran": "no"
        }
        
        conversation = []
        user_message = "What rates can I get?"
        
        # The chatbot should inject lead data into the system prompt
        # We can't directly test the internal prompt, but we can verify
        # that the response is generated (no errors)
        response = self.chatbot.get_response(user_message, current_lead_data, conversation)
        
        assert "message" in response
        assert isinstance(response["message"], str)
        assert len(response["message"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
