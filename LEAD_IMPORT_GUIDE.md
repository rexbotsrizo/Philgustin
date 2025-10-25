# Lead Import Guide

## Quick Reference for Importing Leads into the AI Mortgage Assistant

### Method 1: Bonzo CRM JSON Import

1. **Get the JSON from Bonzo CRM**
   - Export or copy the lead data from Bonzo CRM in JSON format

2. **Navigate to Import Lead**
   - Click "📥 Import Lead" in the app navigation

3. **Paste the JSON**
   - Paste the complete JSON data in the text area
   
4. **Click Import**
   - Click "✅ Import Lead"
   - System will automatically parse and store the lead

### Method 2: Load Sample Leads

1. Go to "📋 Manage Leads"
2. Click "📦 Load Sample Leads (Ronnie Yates & Peter Walker)"
3. Two sample leads will be loaded

### Method 3: Manual Entry

1. Click "📥 Import Lead"
2. Scroll to "✏️ Or Enter Lead Manually"
3. Fill in the form:
   - First Name *
   - Last Name *
   - Email *
   - Property Value *
   - Current Balance *
   - Cash Out Amount
   - Veteran Status *
   - And more...
4. Click "➕ Add Lead"

---

## Bonzo CRM Field Mapping

The system automatically maps Bonzo CRM fields to internal format:

| Bonzo CRM Field | Internal Field | Description |
|----------------|----------------|-------------|
| `first_name` + `last_name` | `name` | Full name |
| `property_value` | `property_value` | Property value |
| `loan_amount` | `current_balance` | Current mortgage balance |
| `cash_out_amount` | `cash_out_amount` | Cash out requested |
| `custom_is_veteran` | `is_veteran` | Veteran status (yes/no) |
| `email` | `email` | Email address |
| `phone` | `phone` | Phone number |
| `credit_score` | `credit_score` | Credit score |
| `birthday` | `birthday` | Date of birth |

---

## Sample Bonzo CRM JSON

### Ronnie Yates (Cash-Out Refinance)

```json
{
  "lead_id": "36391862",
  "lead_source": "BROWN - CASHOUT - Good/Exc",
  "application_date": "2025-10-20",
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

### Peter Walker (Cash-Out Refinance - Larger Amount)

```json
{
  "lead_id": "36389389",
  "lead_source": "MAROON +",
  "application_date": "2025-10-20",
  "first_name": "Peter",
  "last_name": "Walker",
  "email": "peterwalker2@gmail.com",
  "phone": "6143608535",
  "property_value": "600000",
  "loan_amount": "367034",
  "cash_out_amount": "82000",
  "custom_is_veteran": "False",
  "birthday": "7/24/1982"
}
```

---

## Working with Imported Leads

### View All Leads
1. Click "📋 Manage Leads"
2. See all imported leads with summary info
3. Click "Show Full Data" to see complete details

### Chat with a Lead
1. In "📋 Manage Leads", find the lead
2. Click "💬 Chat" button
3. System automatically:
   - Loads lead data
   - Generates 3-option proposal
   - Opens chat interface

### Delete a Lead
1. In "📋 Manage Leads", find the lead
2. Click "🗑️ Delete" button
3. Confirm deletion

---

## Tips

✅ **Valid JSON Required**: Ensure your JSON is properly formatted
✅ **Required Fields**: At minimum, include name, property value, and current balance
✅ **Veteran Status**: Accepts "yes", "no", "true", "false", "True", "False"
✅ **Numbers**: Can be strings or integers (e.g., "185000" or 185000)
✅ **Persistent Storage**: All leads are saved to `leads_data.json`
✅ **Update Existing**: Re-importing a lead with same ID updates the existing record

---

## Troubleshooting

**"Invalid JSON format" error**
- Check for missing commas, brackets, or quotes
- Use a JSON validator online
- Try the "Load Sample" button first

**Lead not showing data correctly**
- Check the field names match Bonzo CRM format
- Use "Show Full Data" to see what was imported
- Manually edit using the manual entry form

**Can't find imported lead**
- Check you're in "📋 Manage Leads" view
- Look at the lead_id to match Bonzo CRM

---

For more information, see the main README.md file.
