"""
Main Streamlit Application - Phil Gustin AI Mortgage Assistant
"""
import streamlit as st
import json
from datetime import datetime
from components.chatbot import MortgageChatbot
from components.proposal_generator import ProposalGenerator
from components.visualizations import create_proposal_visualizations
from utils.config import load_config
from utils.lead_manager import LeadDataManager
from utils.conversation_manager import ConversationManager
from utils.pdf_generator import generate_proposal_pdf

# Page configuration
st.set_page_config(
    page_title="West Capital Lending - AI Mortgage Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lead_data" not in st.session_state:
    st.session_state.lead_data = {}
if "proposal_generated" not in st.session_state:
    st.session_state.proposal_generated = False
if "chatbot" not in st.session_state:
    config = load_config()
    st.session_state.chatbot = MortgageChatbot(config)
if "lead_manager" not in st.session_state:
    st.session_state.lead_manager = LeadDataManager()
if "conversation_manager" not in st.session_state:
    st.session_state.conversation_manager = ConversationManager()
if "current_lead_id" not in st.session_state:
    st.session_state.current_lead_id = None
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "chat"  # chat, manage_leads, import_lead, or conversations

# Header
col1, col2, col3 = st.columns([1, 4, 2])
with col1:
    st.image("https://via.placeholder.com/150x50?text=WEST+CAPITAL", width=150)
with col2:
    st.title("🏠 West Capital Lending - AI Mortgage Assistant")
    st.caption("Phil Gustin | Broker Associate | (949) 209-0989")
with col3:
    st.markdown("### Navigation")
    view_mode = st.radio(
        "Select Mode:",
        ["💬 Chat", "📋 Manage Leads", "📥 Import Lead", "💾 Conversations"],
        label_visibility="collapsed",
        key="nav_radio"
    )
    
    if view_mode == "💬 Chat":
        st.session_state.view_mode = "chat"
    elif view_mode == "📋 Manage Leads":
        st.session_state.view_mode = "manage_leads"
    elif view_mode == "💾 Conversations":
        st.session_state.view_mode = "conversations"
    else:
        st.session_state.view_mode = "import_lead"

# Sidebar - Lead Information Summary
with st.sidebar:
    st.header("📊 Lead Information")
    
    if st.session_state.lead_data:
        for key, value in st.session_state.lead_data.items():
            st.text(f"{key}: {value}")
    else:
        st.info("Chat with the assistant to provide your information")
    
    st.divider()
    
    st.header("⚙️ Daily Rates & Fees")
    st.caption("Update these values daily")
    
    # Rate inputs for different loan types
    with st.expander("FHA Rates"):
        fha_rate1 = st.number_input("Option 1 Rate", value=4.990, step=0.001, format="%.3f", key="fha_r1")
        fha_rate2 = st.number_input("Option 2 Rate", value=5.125, step=0.001, format="%.3f", key="fha_r2")
        fha_cost1 = st.number_input("Option 1 Costs", value=5600, step=100, key="fha_c1")
        fha_cost2 = st.number_input("Option 2 Costs", value=4050, step=100, key="fha_c2")
    
    with st.expander("VA Rates"):
        va_rate1 = st.number_input("Option 1 Rate", value=4.990, step=0.001, format="%.3f", key="va_r1")
        va_rate2 = st.number_input("Option 2 Rate", value=5.125, step=0.001, format="%.3f", key="va_r2")
        va_cost1 = st.number_input("Option 1 Costs", value=5600, step=100, key="va_c1")
        va_cost2 = st.number_input("Option 2 Costs", value=4050, step=100, key="va_c2")
    
    with st.expander("Conventional Rates"):
        conv_rate1 = st.number_input("Option 1 Rate", value=6.000, step=0.001, format="%.3f", key="conv_r1")
        conv_rate2 = st.number_input("Option 2 Rate", value=6.750, step=0.001, format="%.3f", key="conv_r2")
        conv_cost1 = st.number_input("Option 1 Costs", value=7000, step=100, key="conv_c1")
        conv_cost2 = st.number_input("Option 2 Costs", value=4500, step=100, key="conv_c2")
    
    with st.expander("HELOC/HELOAN"):
        heloc_rate = st.number_input("HELOC Rate", value=7.600, step=0.001, format="%.3f", key="heloc_r")
        heloc_fees = st.number_input("HELOC Fees", value=2892, step=100, key="heloc_f")
        heloan_rate1 = st.number_input("20-Year Rate", value=5.900, step=0.001, format="%.3f", key="heloan_r1")
        heloan_rate2 = st.number_input("30-Year Rate", value=6.525, step=0.001, format="%.3f", key="heloan_r2")
        heloan_cost1 = st.number_input("20-Year Costs", value=1700, step=100, key="heloan_c1")
        heloan_cost2 = st.number_input("30-Year Costs", value=2500, step=100, key="heloan_c2")
    
    if st.button("🔄 Reset Conversation"):
        # Save conversation before resetting
        if st.session_state.messages:
            st.session_state.conversation_manager.save_conversation(
                lead_id=st.session_state.current_lead_id,
                lead_name=st.session_state.lead_data.get("name", "Unknown"),
                messages=st.session_state.messages,
                lead_data=st.session_state.lead_data,
                proposal_generated=st.session_state.proposal_generated
            )
        
        st.session_state.messages = []
        st.session_state.lead_data = {}
        st.session_state.proposal_generated = False
        st.session_state.current_lead_id = None
        st.success("✅ Conversation saved and reset!")
        st.rerun()
    
    # Download conversation history
    st.divider()
    st.subheader("💾 Download Conversations")
    
    stats = st.session_state.conversation_manager.get_statistics()
    st.metric("Total Conversations", stats["total_conversations"])
    st.metric("With Proposals", stats["with_proposals"])
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download All (JSON)"):
            json_data = st.session_state.conversation_manager.export_to_json()
            st.download_button(
                label="💾 Save JSON File",
                data=json_data,
                file_name=f"conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Download Summary (CSV)"):
            csv_data = st.session_state.conversation_manager.export_to_csv()
            st.download_button(
                label="💾 Save CSV File",
                data=csv_data,
                file_name=f"conversation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# Main content area based on view mode
if st.session_state.view_mode == "manage_leads":
    # ==================== MANAGE LEADS VIEW ====================
    st.header("📋 Lead Management")
    
    all_leads = st.session_state.lead_manager.get_all_leads()
    
    if not all_leads:
        st.info("No leads found. Import leads using the 'Import Lead' tab or load sample data.")
        
        if st.button("📦 Load Sample Leads (Ronnie Yates & Peter Walker)"):
            sample_leads = st.session_state.lead_manager.get_sample_leads()
            for lead_id, lead_data in sample_leads.items():
                parsed = st.session_state.lead_manager.parse_bonzo_lead(lead_data)
                st.session_state.lead_manager.add_lead(parsed)
            st.success("Sample leads loaded!")
            st.rerun()
    else:
        st.subheader(f"Total Leads: {len(all_leads)}")
        
        # Display leads in a table
        for lead_id, lead in all_leads.items():
            with st.expander(f"🔹 {lead.get('name', 'Unknown')} - ID: {lead_id}"):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**Email:** {lead.get('email', 'N/A')}")
                    st.write(f"**Phone:** {lead.get('phone', 'N/A')}")
                    st.write(f"**Property Value:** ${lead.get('property_value', 0):,}")
                    st.write(f"**Current Balance:** ${lead.get('current_balance', 0):,}")
                    st.write(f"**Cash Out:** ${lead.get('cash_out_amount', 0):,}")
                    st.write(f"**Veteran:** {lead.get('is_veteran', 'N/A')}")
                    st.write(f"**Source:** {lead.get('lead_source', 'N/A')}")
                
                with col2:
                    if st.button("💬 Chat", key=f"chat_{lead_id}"):
                        # Load this lead into chat mode
                        st.session_state.lead_data = {
                            "name": lead.get('name'),
                            "property_value": lead.get('property_value'),
                            "current_balance": lead.get('current_balance'),
                            "cash_out_amount": lead.get('cash_out_amount'),
                            "is_veteran": lead.get('is_veteran'),
                            "annual_income": lead.get('annual_income')
                        }
                        st.session_state.current_lead_id = lead_id
                        st.session_state.view_mode = "chat"
                        st.session_state.proposal_generated = True
                        st.rerun()
                
                with col3:
                    if st.button("🗑️ Delete", key=f"del_{lead_id}"):
                        st.session_state.lead_manager.delete_lead(lead_id)
                        st.success(f"Deleted lead {lead_id}")
                        st.rerun()
                
                # Show full JSON data
                if st.checkbox("Show Full Data", key=f"show_{lead_id}"):
                    st.json(lead)

elif st.session_state.view_mode == "import_lead":
    # ==================== IMPORT LEAD VIEW ====================
    st.header("📥 Import Lead from Bonzo CRM")
    
    st.markdown("""
    Paste the JSON data from Bonzo CRM below. The system will automatically parse and store the lead information.
    
    **Example format:**
    ```json
    {
        "lead_id": "12345",
        "first_name": "John",
        "last_name": "Doe",
        ...
    }
    ```
    """)
    
    # JSON input area
    json_input = st.text_area(
        "Paste Bonzo CRM Lead JSON:",
        height=400,
        placeholder='{\n  "lead_id": "12345",\n  "first_name": "John",\n  ...\n}'
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Import Lead", type="primary"):
            if json_input.strip():
                try:
                    # Parse JSON
                    lead_json = json.loads(json_input)
                    
                    # Parse and store lead
                    parsed_lead = st.session_state.lead_manager.parse_bonzo_lead(lead_json)
                    lead_id = st.session_state.lead_manager.add_lead(parsed_lead)
                    
                    st.success(f"✅ Lead imported successfully! Lead ID: {lead_id}")
                    st.success(f"Name: {parsed_lead.get('name')}")
                    
                    # Show parsed data
                    with st.expander("View Parsed Lead Data"):
                        st.json(parsed_lead)
                    
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON format: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error importing lead: {str(e)}")
            else:
                st.warning("Please paste JSON data first")
    
    with col2:
        if st.button("📋 Load Sample (Ronnie Yates)"):
            sample_lead = st.session_state.lead_manager.get_sample_leads()["36391862"]
            json_input = json.dumps(sample_lead, indent=2)
            st.code(json_input, language="json")
    
    # Manual lead entry
    st.divider()
    st.subheader("✏️ Or Enter Lead Manually")
    
    with st.form("manual_lead_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name*")
            last_name = st.text_input("Last Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone")
            property_value = st.number_input("Property Value*", min_value=0, step=1000)
            current_balance = st.number_input("Current Mortgage Balance*", min_value=0, step=1000)
        
        with col2:
            cash_out = st.number_input("Cash Out Amount", min_value=0, step=1000)
            is_veteran = st.selectbox("Veteran Status*", ["no", "yes"])
            credit_score = st.text_input("Credit Score")
            annual_income = st.number_input("Annual Income", min_value=0, step=1000)
            property_address = st.text_input("Property Address")
            lead_source = st.text_input("Lead Source")
        
        submitted = st.form_submit_button("➕ Add Lead", type="primary")
        
        if submitted:
            if first_name and last_name and email and property_value and current_balance:
                # Create lead data
                manual_lead = {
                    "lead_id": f"MANUAL_{int(datetime.now().timestamp())}",
                    "first_name": first_name,
                    "last_name": last_name,
                    "name": f"{first_name} {last_name}",
                    "email": email,
                    "phone": phone,
                    "property_value": property_value,
                    "current_balance": current_balance,
                    "cash_out_amount": cash_out,
                    "is_veteran": is_veteran,
                    "credit_score": credit_score,
                    "annual_income": annual_income if annual_income > 0 else None,
                    "property_address": property_address,
                    "lead_source": lead_source,
                    "application_date": datetime.now().strftime("%Y-%m-%d")
                }
                
                lead_id = st.session_state.lead_manager.add_lead(manual_lead)
                st.success(f"✅ Lead added successfully! Lead ID: {lead_id}")
            else:
                st.error("❌ Please fill in all required fields (*)")

elif st.session_state.view_mode == "conversations":
    # ==================== CONVERSATIONS HISTORY VIEW ====================
    st.header("💾 Conversation History")
    
    all_conversations = st.session_state.conversation_manager.get_all_conversations()
    
    if not all_conversations:
        st.info("No conversations recorded yet. Start chatting to create conversation history!")
    else:
        # Statistics
        stats = st.session_state.conversation_manager.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Conversations", stats["total_conversations"])
        with col2:
            st.metric("With Proposals", stats["with_proposals"])
        with col3:
            st.metric("Avg Messages", stats["avg_messages_per_conversation"])
        with col4:
            st.metric("Today", stats["conversations_by_date"].get(datetime.now().strftime("%Y-%m-%d"), 0))
        
        st.divider()
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            json_data = st.session_state.conversation_manager.export_to_json()
            st.download_button(
                label="📥 Download All Conversations (JSON)",
                data=json_data,
                file_name=f"all_conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                type="primary"
            )
        
        with col2:
            csv_data = st.session_state.conversation_manager.export_to_csv()
            st.download_button(
                label="📊 Download Summary (CSV)",
                data=csv_data,
                file_name=f"conversation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        st.divider()
        st.subheader("Conversation List")
        
        # Display conversations (most recent first)
        for conv in reversed(all_conversations):
            conv_id = conv.get("conversation_id", "Unknown")
            lead_name = conv.get("lead_name", "Unknown")
            timestamp = conv.get("timestamp", "")
            msg_count = conv.get("message_count", 0)
            proposal_gen = conv.get("proposal_generated", False)
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = timestamp
            
            with st.expander(f"💬 {lead_name} - {formatted_time} ({msg_count} messages)"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Conversation ID:** {conv_id}")
                    st.write(f"**Lead:** {lead_name} (ID: {conv.get('lead_id', 'N/A')})")
                    st.write(f"**Date/Time:** {formatted_time}")
                    st.write(f"**Messages:** {msg_count}")
                    st.write(f"**Proposal Generated:** {'✅ Yes' if proposal_gen else '❌ No'}")
                    
                    # Show lead data
                    lead_data = conv.get("lead_data", {})
                    if lead_data:
                        st.write("**Lead Info:**")
                        st.write(f"- Property Value: ${lead_data.get('property_value', 0):,}")
                        st.write(f"- Current Balance: ${lead_data.get('current_balance', 0):,}")
                        st.write(f"- Cash Out: ${lead_data.get('cash_out_amount', 0):,}")
                        st.write(f"- Veteran: {lead_data.get('is_veteran', 'N/A')}")
                
                with col2:
                    # Download individual conversation transcript
                    transcript = st.session_state.conversation_manager.export_conversation_detail(conv_id)
                    if transcript:
                        st.download_button(
                            label="📄 Download Transcript",
                            data=transcript,
                            file_name=f"transcript_{conv_id}.txt",
                            mime="text/plain",
                            key=f"download_{conv_id}"
                        )
                
                # Show conversation messages
                if st.checkbox("Show Conversation", key=f"show_conv_{conv_id}"):
                    st.markdown("---")
                    st.markdown("**Conversation Messages:**")
                    for i, msg in enumerate(conv.get("messages", []), 1):
                        role = msg.get("role", "unknown")
                        content = msg.get("content", "")
                        
                        if role == "user":
                            st.markdown(f"**[{i}] 👤 User:**")
                        else:
                            st.markdown(f"**[{i}] 🤖 Assistant:**")
                        
                        st.markdown(f"> {content}")
                        st.markdown("")

else:
    # ==================== CHAT VIEW ====================
    st.header("💬 Chat with Phil's AI Assistant")
    
    # Show current lead info if loaded
    if st.session_state.current_lead_id:
        lead = st.session_state.lead_manager.get_lead(st.session_state.current_lead_id)
        if lead:
            st.info(f"📋 Currently working with: **{lead.get('name')}** (Lead ID: {st.session_state.current_lead_id})")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Tell me about your mortgage needs..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.get_response(
                    prompt, 
                    st.session_state.lead_data,
                    st.session_state.messages
                )
                st.markdown(response["message"])
                
                # Update lead data if extracted
                if "lead_data" in response:
                    st.session_state.lead_data.update(response["lead_data"])
                
                # Generate proposal if ready
                if response.get("generate_proposal", False):
                    st.session_state.proposal_generated = True
                    
                    # Auto-save conversation when proposal is generated
                    conv_id = st.session_state.conversation_manager.save_conversation(
                        lead_id=st.session_state.current_lead_id,
                        lead_name=st.session_state.lead_data.get("name", "Unknown"),
                        messages=st.session_state.messages + [{"role": "assistant", "content": response["message"]}],
                        lead_data=st.session_state.lead_data,
                        proposal_generated=True
                    )
                    st.toast(f"✅ Conversation saved: {conv_id}", icon="💾")
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response["message"]})
        st.rerun()

    # Display proposal if generated
    if st.session_state.proposal_generated and st.session_state.lead_data:
        st.divider()
        st.header("📄 Your Personalized Mortgage Proposals")
        
        # Collect rates from sidebar
        rates_config = {
            "fha": {"rate1": fha_rate1, "rate2": fha_rate2, "cost1": fha_cost1, "cost2": fha_cost2},
            "va": {"rate1": va_rate1, "rate2": va_rate2, "cost1": va_cost1, "cost2": va_cost2},
            "conventional": {"rate1": conv_rate1, "rate2": conv_rate2, "cost1": conv_cost1, "cost2": conv_cost2},
            "heloc": {"rate": heloc_rate, "fees": heloc_fees},
            "heloan": {"rate1": heloan_rate1, "rate2": heloan_rate2, "cost1": heloan_cost1, "cost2": heloan_cost2}
        }
        
        # Generate proposals
        generator = ProposalGenerator(st.session_state.lead_data, rates_config)
        proposals = generator.generate_all_proposals()
        
        # Display visualizations
        create_proposal_visualizations(proposals, st.session_state.lead_data)
        
        # Download button for proposal - Generate actual PDF
        try:
            pdf_bytes = generate_proposal_pdf(st.session_state.lead_data, proposals)
            st.download_button(
                label="📥 Download Full Proposal (PDF)",
                data=pdf_bytes,
                file_name=f"mortgage_proposal_{st.session_state.lead_data.get('name', 'client').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                help="Download a professionally formatted PDF of your proposals"
            )
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")
            st.info("PDF generation requires the reportlab package. Install it with: pip install reportlab")
