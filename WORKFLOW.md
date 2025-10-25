# Application Workflow

## Lead Management & Proposal Generation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     STREAMLIT APPLICATION                        │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   💬 Chat    │  │ 📋 Manage    │  │ 📥 Import    │         │
│  │     Mode     │  │    Leads     │  │    Lead      │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │                  │                  │
          ▼                  ▼                  ▼
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │  AI Chatbot  │   │  Lead List   │   │ JSON Import  │
   │              │   │   Display    │   │   or Form    │
   │ Gathers Info │   │              │   │              │
   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
          │                  │                  │
          │                  │                  │
          ▼                  │                  ▼
   ┌──────────────┐          │           ┌──────────────┐
   │ Extract Lead │          │           │ Parse Bonzo  │
   │     Data     │          │           │  CRM JSON    │
   └──────┬───────┘          │           └──────┬───────┘
          │                  │                  │
          │                  │                  │
          ▼                  ▼                  ▼
   ┌──────────────────────────────────────────────────┐
   │          Lead Data Manager (JSON Storage)        │
   │                 leads_data.json                   │
   └──────────────────────┬───────────────────────────┘
                          │
                          │
                          ▼
                   ┌──────────────┐
                   │ Load Lead to │
                   │  Chat Mode   │
                   └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  Proposal    │
                   │  Generator   │
                   └──────┬───────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  3 Proposal Options:        │
            │  1. Primary (FHA/VA/Conv)   │
            │  2. HELOC                   │
            │  3. HELOAN                  │
            └─────────────┬───────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  Plotly      │
                   │ Visualizations│
                   └──────────────┘
```

## Data Flow

### Import Flow
```
Bonzo CRM → JSON → Parse → Validate → Store → Display
```

### Chat Flow
```
User Input → AI Extract → Update Lead Data → Check Complete → Generate Proposal
```

### Proposal Generation Flow
```
Lead Data + Daily Rates → Calculate Options → Format Results → Visualize
```

## Component Architecture

```
app.py (Main UI)
├── Navigation (Radio Select)
│   ├── Chat Mode
│   ├── Manage Leads Mode
│   └── Import Lead Mode
│
├── Sidebar (Rate Configuration)
│   ├── FHA Rates
│   ├── VA Rates
│   ├── Conventional Rates
│   ├── HELOC Rates
│   └── HELOAN Rates
│
└── Components
    ├── chatbot.py (AI Logic)
    │   ├── OpenAI Integration
    │   ├── LangChain
    │   └── Data Extraction
    │
    ├── proposal_generator.py (Calculations)
    │   ├── Monthly Payment Formula
    │   ├── APR Calculation
    │   └── Loan Amount Logic
    │
    ├── visualizations.py (Charts)
    │   ├── Comparison Charts
    │   ├── Cost Breakdown
    │   └── Detailed Tables
    │
    └── utils/
        ├── config.py (Environment)
        └── lead_manager.py (Data Storage)
            ├── Load Leads
            ├── Save Leads
            ├── Parse Bonzo JSON
            └── CRUD Operations
```

## File Structure

```
streamlit_app/
│
├── 📄 Main Application
│   └── app.py (Streamlit UI + Navigation)
│
├── 🧩 Components
│   ├── chatbot.py (OpenAI + LangChain)
│   ├── proposal_generator.py (Math & Logic)
│   └── visualizations.py (Plotly Charts)
│
├── 🔧 Utilities
│   ├── config.py (Environment Config)
│   └── lead_manager.py (Data Management)
│
├── 💾 Data Storage
│   └── leads_data.json (Auto-generated)
│
├── 📝 Configuration
│   ├── .env (API Keys - Not in repo)
│   ├── .env.example (Template)
│   └── requirements.txt (Dependencies)
│
└── 📚 Documentation
    ├── README.md (Main Guide)
    ├── LEAD_IMPORT_GUIDE.md (Import Help)
    └── WORKFLOW.md (This File)
```

## Session State Management

```python
st.session_state = {
    "messages": [],              # Chat history
    "lead_data": {},            # Current lead being worked on
    "proposal_generated": False, # Flag for proposal display
    "chatbot": MortgageChatbot, # AI chatbot instance
    "lead_manager": Manager,    # Lead database manager
    "current_lead_id": None,    # ID of active lead
    "view_mode": "chat"         # Current view: chat/manage/import
}
```

## Key Features Summary

✅ **Multi-Mode Interface**
- Seamless switching between chat, management, and import

✅ **Persistent Storage**
- All leads saved to JSON file
- Survives app restarts

✅ **Smart Parsing**
- Automatically converts Bonzo CRM format
- Handles various data types

✅ **Real-time Calculations**
- Dynamic proposal generation
- Live rate updates from sidebar

✅ **Interactive Visualizations**
- Multiple chart types
- Side-by-side comparisons

✅ **Production Ready**
- Error handling
- Input validation
- User-friendly messages
