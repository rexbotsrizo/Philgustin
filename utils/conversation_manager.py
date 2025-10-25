"""
Conversation Manager - Tracks and saves chat conversations
"""
import json
import os
from datetime import datetime
import csv


class ConversationManager:
    """Manages conversation history storage and retrieval"""
    
    def __init__(self, data_file="conversations.json"):
        """Initialize the conversation manager"""
        self.data_file = data_file
        self.conversations = self._load_conversations()
    
    def _load_conversations(self):
        """Load conversations from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_conversations(self):
        """Save conversations to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.conversations, f, indent=2)
    
    def save_conversation(self, lead_id, lead_name, messages, lead_data, proposal_generated=False):
        """
        Save a conversation session
        
        Args:
            lead_id: ID of the lead
            lead_name: Name of the lead
            messages: List of chat messages
            lead_data: Lead information extracted
            proposal_generated: Whether proposal was generated
        """
        conversation = {
            "conversation_id": f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lead_id or 'unknown'}",
            "lead_id": lead_id,
            "lead_name": lead_name,
            "timestamp": datetime.now().isoformat(),
            "message_count": len(messages),
            "messages": messages,
            "lead_data": lead_data,
            "proposal_generated": proposal_generated,
            "session_duration": None  # Could be calculated if needed
        }
        
        self.conversations.append(conversation)
        self._save_conversations()
        
        return conversation["conversation_id"]
    
    def get_conversations_by_lead(self, lead_id):
        """Get all conversations for a specific lead"""
        return [c for c in self.conversations if c.get("lead_id") == lead_id]
    
    def get_all_conversations(self):
        """Get all conversations"""
        return self.conversations
    
    def get_conversation_by_id(self, conversation_id):
        """Get a specific conversation by ID"""
        for conv in self.conversations:
            if conv.get("conversation_id") == conversation_id:
                return conv
        return None
    
    def export_to_json(self, conversation_ids=None):
        """
        Export conversations to JSON string
        
        Args:
            conversation_ids: List of conversation IDs to export (None = all)
        """
        if conversation_ids:
            conversations = [c for c in self.conversations if c.get("conversation_id") in conversation_ids]
        else:
            conversations = self.conversations
        
        return json.dumps(conversations, indent=2)
    
    def export_to_csv(self, conversation_ids=None):
        """
        Export conversation summary to CSV format
        
        Args:
            conversation_ids: List of conversation IDs to export (None = all)
        """
        if conversation_ids:
            conversations = [c for c in self.conversations if c.get("conversation_id") in conversation_ids]
        else:
            conversations = self.conversations
        
        # Create CSV data
        csv_data = []
        csv_data.append([
            "Conversation ID", "Lead ID", "Lead Name", "Timestamp", 
            "Message Count", "Proposal Generated", "Property Value", 
            "Cash Out Amount", "Veteran Status"
        ])
        
        for conv in conversations:
            lead_data = conv.get("lead_data", {})
            csv_data.append([
                conv.get("conversation_id", ""),
                conv.get("lead_id", ""),
                conv.get("lead_name", ""),
                conv.get("timestamp", ""),
                conv.get("message_count", 0),
                "Yes" if conv.get("proposal_generated") else "No",
                lead_data.get("property_value", ""),
                lead_data.get("cash_out_amount", ""),
                lead_data.get("is_veteran", "")
            ])
        
        # Convert to CSV string
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(csv_data)
        return output.getvalue()
    
    def export_conversation_detail(self, conversation_id):
        """
        Export detailed conversation transcript
        
        Args:
            conversation_id: ID of conversation to export
        """
        conv = self.get_conversation_by_id(conversation_id)
        if not conv:
            return None
        
        # Create detailed transcript
        transcript = f"""
CONVERSATION TRANSCRIPT
======================
Conversation ID: {conv.get('conversation_id')}
Lead: {conv.get('lead_name')} (ID: {conv.get('lead_id')})
Date/Time: {conv.get('timestamp')}
Proposal Generated: {'Yes' if conv.get('proposal_generated') else 'No'}

LEAD INFORMATION
----------------
{json.dumps(conv.get('lead_data', {}), indent=2)}

CONVERSATION
------------
"""
        
        for i, msg in enumerate(conv.get('messages', []), 1):
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '')
            transcript += f"\n[{i}] {role}:\n{content}\n"
        
        return transcript
    
    def get_statistics(self):
        """Get conversation statistics"""
        total = len(self.conversations)
        with_proposals = sum(1 for c in self.conversations if c.get('proposal_generated'))
        
        # Average messages per conversation
        avg_messages = sum(c.get('message_count', 0) for c in self.conversations) / total if total > 0 else 0
        
        # Conversations by date
        dates = {}
        for conv in self.conversations:
            date = conv.get('timestamp', '')[:10]  # YYYY-MM-DD
            dates[date] = dates.get(date, 0) + 1
        
        return {
            "total_conversations": total,
            "with_proposals": with_proposals,
            "without_proposals": total - with_proposals,
            "avg_messages_per_conversation": round(avg_messages, 2),
            "conversations_by_date": dates
        }
