# West Capital Lending - AI Mortgage Assistant

A Streamlit-based chatbot application that simulates Phil Gustin's mortgage lending process, collecting lead information and generating personalized 3-option mortgage proposals with interactive visualizations.

## 🎯 Features

- **Interactive AI Chatbot**: Conversational interface that naturally gathers client information
- **Lead Management System**: Import, view, edit, and manage leads from Bonzo CRM
- **Bonzo CRM Integration**: Direct JSON import from Bonzo CRM format
- **Manual Lead Entry**: Add leads manually through a simple form
- **Smart Lead Analysis**: Automatically determines cash-out vs rate/term refinance scenarios
- **3-Option Proposals**: Generates personalized mortgage proposals based on client data
- **Interactive Visualizations**: Plotly-powered charts comparing all loan options
- **Modular Architecture**: Clean, maintainable code structure
- **Daily Rate Updates**: Easy sidebar interface to update current rates and fees
- **Sample Data**: Pre-loaded sample leads (Ronnie Yates & Peter Walker) for testing

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key

## 🚀 Installation

### 1. Clone or Navigate to Project Directory

```bash
cd "/home/tanzir/Downloads/Philgustin/AI Project/streamlit_app"
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=1000
```

## 🏃 Running the Application

### Quick Start (Linux/Mac)

```bash
./start.sh
```

This script will automatically:
1. Create a virtual environment
2. Install all dependencies
3. Check for `.env` file
4. Start the Streamlit application

### Manual Start

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud (step-by-step)

Follow these exact steps to publish the app to Streamlit Cloud. You do NOT upload your local `venv/` — Streamlit Cloud creates its own environment from `requirements.txt`.

1) Initialize git and commit your project

```bash
cd "/home/tanzir/Downloads/Philgustin/AI Project/streamlit_app"
git init
git add .
git commit -m "Initial commit - West Capital Lending AI Mortgage Assistant"
```

2) Create a GitHub repository and push (replace <YOUR_GIT_REMOTE_URL>)

```bash
# create a repo on GitHub (via website) and then:
git remote add origin <YOUR_GIT_REMOTE_URL>
git branch -M main
git push -u origin main
```

3) Deploy on Streamlit Cloud

- Go to https://share.streamlit.io and sign in with GitHub.
- Click **New app** → choose the repository and branch (`main`), set the path to `/` or `.` if `app.py` is in root.
- Click **Deploy**.

4) Add your OpenAI API key as a secret (DO NOT commit .env with real keys)

- On Streamlit Cloud, open your app's dashboard → Settings → Secrets (or the menu ⋮ → Edit secrets).
- Add a secret named `OPENAI_API_KEY` with your API key value.
- Optionally add `MODEL_NAME`, `TEMPERATURE`, and `MAX_TOKENS` if you want non-defaults.

Example secrets entries:

```
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
MODEL_NAME="gpt-4"
TEMPERATURE="0.7"
MAX_TOKENS="1000"
```

5) Confirm `requirements.txt` is present and complete (Streamlit Cloud installs these automatically).

6) After deployment the app will run on Streamlit's URL. To update, push commits to `main` and Streamlit Cloud will redeploy automatically.

Security note: Streamlit Cloud's `st.secrets` is used by the app (see `utils/config.py`) so the API key never appears in code or repo.

If you prefer another host (Render, Heroku, Fly), the same rules apply: push repo (without `venv/`), set environment variables / secrets in the host, and install from `requirements.txt`.

## 📁 Project Structure

```
streamlit_app/
├── app.py                          # Main Streamlit application
├── start.sh                        # Quick start script (Linux/Mac)
├── components/
│   ├── __init__.py
│   ├── chatbot.py                 # AI chatbot logic with LangChain
│   ├── proposal_generator.py     # Mortgage calculation engine
│   └── visualizations.py         # Plotly visualization components
├── utils/
│   ├── __init__.py
│   ├── config.py                  # Configuration loader
│   └── lead_manager.py            # Lead data management system
├── leads_data.json                # Stored leads database (auto-created)
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## 💬 How to Use

### Navigation

The app has three main modes accessible via the navigation panel:

1. **💬 Chat Mode** - Interact with the AI assistant
2. **📋 Manage Leads** - View and manage all stored leads
3. **📥 Import Lead** - Import new leads from Bonzo CRM or manually

### 1. Import Leads

**Option A: Import from Bonzo CRM**
1. Click "📥 Import Lead" in navigation
2. Paste the JSON data from Bonzo CRM
3. Click "✅ Import Lead"
4. The lead will be parsed and stored automatically

**Option B: Load Sample Data**
1. Go to "📋 Manage Leads"
2. Click "📦 Load Sample Leads"
3. Sample leads (Ronnie Yates & Peter Walker) will be loaded

**Option C: Manual Entry**
1. Click "📥 Import Lead" in navigation
2. Scroll to "✏️ Or Enter Lead Manually"
3. Fill in the form with lead details
4. Click "➕ Add Lead"

### 2. Manage Leads

1. Click "📋 Manage Leads" in navigation
2. View all stored leads with key information
3. Click "💬 Chat" to work with a specific lead
4. Click "🗑️ Delete" to remove a lead
5. Check "Show Full Data" to see complete lead information

### 3. Chat with Leads

**Starting from Manage Leads:**
1. In "📋 Manage Leads", click "💬 Chat" next to a lead
2. The system will automatically load the lead data
3. Chat interface opens with proposal already generated

**Starting Fresh:**
1. Click "💬 Chat" in navigation
2. Start chatting - AI will gather information naturally:
   - Your name
   - Property value
   - Current mortgage balance
   - Cash out needs (if any)
   - Veteran status
   - Income and other details

### 4. Update Daily Rates

Use the sidebar to input current rates and fees for:
- FHA loans
- VA loans
- Conventional loans
- HELOC
- HELOAN

### 5. Review Proposals

Once enough information is collected, the system automatically generates 3 proposal options:

**For Cash-Out Refinance:**
1. Primary Cash-Out Refinance (FHA or VA based on veteran status)
2. Home Equity Line of Credit (HELOC)
3. Home Equity Loan (HELOAN)

**For Rate/Term Refinance:**
1. Conventional Refinance
2. Alternative options

### 6. Compare Options

Use the interactive tabs to:
- View side-by-side comparisons
- Analyze monthly payment details
- Review cost breakdowns
- See complete proposal details

## 🔧 Configuration

### Adjusting the Chatbot Behavior

Edit `components/chatbot.py` to modify:
- Conversation style and personality
- Information gathering logic
- Lead qualification criteria

### Customizing Calculations

Edit `components/proposal_generator.py` to adjust:
- Loan calculation formulas
- APR calculations
- Proposal generation logic

### Modifying Visualizations

Edit `components/visualizations.py` to change:
- Chart types and styles
- Comparison metrics
- Visual layouts

## 🧪 Example Usage

### Importing a Bonzo CRM Lead

```json
{
  "lead_id": "36391862",
  "lead_source": "BROWN - CASHOUT - Good/Exc",
  "first_name": "Ronnie",
  "last_name": "Yates",
  "email": "yatesronnie@yahoo.com",
  "phone": "8595162730",
  "property_value": "185000",
  "loan_amount": "145000",
  "cash_out_amount": "10000",
  "custom_is_veteran": "no"
}
```

### Lead Data Structure (Internal Format)

```python
# After parsing Bonzo CRM data
lead_data = {
    "name": "Ronnie Yates",
    "property_value": 185000,
    "current_balance": 145000,
    "cash_out_amount": 10000,
    "is_veteran": "no",
    "email": "yatesronnie@yahoo.com",
    "phone": "8595162730"
}
```

## 📊 Loan Calculations

The system calculates:
- **Monthly Payment**: Using standard amortization formula
- **APR**: Annual Percentage Rate including fees
- **Loan Amount**: Based on balance, cash out, and costs
- **Total Costs**: Upfront fees and closing costs

## 🔐 Security Notes

- Never commit your `.env` file with real API keys
- Keep your OpenAI API key secure
- Consider rate limiting for production use
- Validate all user inputs in production

## 🛠️ Troubleshooting

### OpenAI API Errors
- Verify your API key is correct in `.env`
- Check your OpenAI account has available credits
- Ensure you're using a compatible model (gpt-4 or gpt-3.5-turbo)

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Visualization Issues
- Clear browser cache
- Try a different browser
- Check Plotly version compatibility

## 🚀 Future Enhancements

Potential improvements:
- ✅ Lead data management (COMPLETED)
- ✅ Bonzo CRM JSON import (COMPLETED)
- PDF proposal generation
- Email integration for drip campaigns
- Real-time Bonzo CRM API integration
- SMS notification system
- Lead scoring and prioritization
- Automated follow-up sequences
- Multi-language support
- Historical data analytics
- Appointment scheduling integration
- Document upload and management

## 📝 License

This is a proprietary application for West Capital Lending.

## 👤 Contact

**Phil Gustin**  
Broker Associate  
West Capital Lending  
(949) 209-0989  
www.philthemortgagepro.com

---

Built with ❤️ using Streamlit, OpenAI, and Plotly
