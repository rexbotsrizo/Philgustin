"""
Campaign Manager - Automated drip campaigns for lead nurturing
Based on Phil Gustin's 57-step campaign schedule
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
import pytz


class CampaignManager:
    """
    Manages automated drip campaigns with SMS, Email, and Voicemail touchpoints
    """
    
    def __init__(self):
        self.campaigns_file = Path("data/campaigns.json")
        self.campaigns_file.parent.mkdir(exist_ok=True)
        
        # Campaign definitions (from your detailed schedule)
        self.campaign_templates = {
            "new_lead_cashout": self.get_cashout_campaign(),
            "responded": self.get_responded_campaign()
        }
    
    def get_cashout_campaign(self):
        """Campaign for new cash-out leads (Days 1-30)"""
        return [
            # Day 1
            {"day": 1, "type": "SMS", "delay_minutes": 0, "template": "initial_contact"},
            {"day": 1, "type": "Email", "delay_minutes": 0, "template": "confirmation_email"},
            {"day": 1, "type": "VM", "delay_minutes": 3, "template": "vm1_long_honest"},
            {"day": 1, "type": "SMS", "delay_minutes": 15, "template": "purpose_question"},
            {"day": 1, "type": "SMS", "delay_minutes": 170, "manual": True, "template": "send_proposal"},
            {"day": 1, "type": "Email", "delay_minutes": 170, "manual": True, "template": "proposal_email"},
            {"day": 1, "type": "SMS", "delay_minutes": 228, "template": "followup_proposal"},
            {"day": 1, "type": "Email", "delay_minutes": 233, "template": "custom_quote_finetune"},
            {"day": 1, "type": "SMS", "delay_minutes": 297, "template": "background_value"},
            
            # Day 2
            {"day": 2, "type": "SMS", "time": "9:02am", "template": "good_morning"},
            {"day": 2, "type": "SMS", "time": "10:31am", "template": "texting_or_call"},
            {"day": 2, "type": "SMS", "time": "11:16am", "template": "5star_reviews"},
            {"day": 2, "type": "Email", "time": "12:16pm", "template": "know_who_working_with"},
            {"day": 2, "type": "SMS", "time": "3:16pm", "template": "gentle_reminder"},
            {"day": 2, "type": "SMS", "time": "5:06pm", "template": "shopping_best_deal"},
            
            # Days 3-30 continue...
            {"day": 3, "type": "SMS", "time": "8:17am", "template": "easy_dob_income"},
            {"day": 3, "type": "SMS", "time": "8:30am", "manual": True, "template": "day3_quote"},
            {"day": 3, "type": "VM", "time": "10:52am", "template": "vm_999_time"},
            {"day": 3, "type": "SMS", "time": "12:22pm", "template": "verify_details"},
            {"day": 3, "type": "SMS", "time": "3:22pm", "template": "skip_2_payments"},
            {"day": 3, "type": "Email", "time": "4:27pm", "template": "couple_questions"},
            {"day": 3, "type": "SMS", "time": "5:37pm", "template": "evening_available"},
            
            {"day": 4, "type": "SMS", "time": "8:30am", "manual": True, "template": "day4_quote"},
            {"day": 4, "type": "SMS", "time": "9:06am", "template": "not_be_bother"},
            {"day": 4, "type": "VM", "time": "12:06pm", "template": "vm_short_sweet"},
            {"day": 4, "type": "SMS", "time": "4:36pm", "template": "told_no_elsewhere"},
            {"day": 4, "type": "Email", "time": "5:36pm", "template": "heloc_1day_close"},
            {"day": 4, "type": "SMS", "time": "6:36pm", "template": "heloc_fast_close"},
            
            {"day": 5, "type": "SMS", "time": "8:30am", "manual": True, "template": "day5_quote"},
            {"day": 5, "type": "VM", "time": "8:45am", "template": "vm_followup_proposal"},
            {"day": 5, "type": "SMS", "time": "9:30am", "template": "defer_payment"},
            {"day": 5, "type": "SMS", "time": "9:55am", "template": "payoff_high_interest"},
            {"day": 5, "type": "SMS", "time": "12:55pm", "template": "ensure_saw_texts"},
            {"day": 5, "type": "Email", "time": "2:19pm", "template": "figure_intro_video"},
            {"day": 5, "type": "SMS", "time": "4:49pm", "template": "rates_went_down"},
            
            {"day": 6, "type": "SMS", "time": "10:30am", "template": "confirm_name"},
            {"day": 6, "type": "VM", "time": "12:52pm", "template": "vm_didnt_hear"},
            
            {"day": 7, "type": "Email", "time": "11:33am", "template": "rates_down_half_percent"},
            {"day": 7, "type": "SMS", "time": "2:48pm", "template": "updated_numbers_offer"},
            {"day": 7, "type": "VM", "time": "5:48pm", "template": "vm_beat_anyone"},
            
            {"day": 9, "type": "Email", "time": "10:20am", "template": "cashout_great_idea"},
            {"day": 9, "type": "SMS", "time": "2:58pm", "template": "equity_purpose"},
            
            {"day": 11, "type": "SMS", "time": "8:44am", "template": "told_dont_qualify"},
            {"day": 11, "type": "Email", "time": "1:44pm", "template": "low_credit_no_problem"},
            
            {"day": 14, "type": "SMS", "time": "9:40am", "template": "started_elsewhere"},
            {"day": 14, "type": "Email", "time": "1:40pm", "template": "already_in_process"},
            
            {"day": 17, "type": "SMS", "time": "10:00am", "template": "rates_dropped"},
            
            {"day": 21, "type": "SMS", "time": "8:00am", "template": "updated_quote_question"},
            
            {"day": 24, "type": "SMS", "time": "12:36pm", "template": "ghost_me"},
            
            {"day": 27, "type": "SMS", "time": "4:00pm", "template": "rates_3_percent_joke"},
            
            {"day": 30, "type": "SMS", "time": "8:30am", "template": "last_ditch_effort"},
            {"day": 30, "type": "Email", "time": "1:00pm", "template": "rates_getting_better"},
        ]
    
    def get_responded_campaign(self):
        """Campaign when lead responds positively (after proposal sent)"""
        return [
            {"day": 1, "type": "SMS", "delay_minutes": 5, "template": "numbers_sent_confirm"},
            {"day": 1, "type": "SMS", "delay_minutes": 25, "template": "review_proposal_which_option"},
            {"day": 1, "type": "Email", "delay_minutes": 40, "template": "saw_texts_above"},
            {"day": 1, "type": "SMS", "delay_minutes": 70, "template": "custom_loan_quote"},
            {"day": 1, "type": "SMS", "delay_minutes": 134, "template": "not_automated_reviews"},
            
            {"day": 2, "type": "SMS", "time": "8:52am", "template": "saw_numbers_yesterday"},
            {"day": 2, "type": "SMS", "time": "8:52am", "manual": True, "template": "day2_quote_manual"},
            {"day": 2, "type": "SMS", "time": "9:31am", "template": "hope_reviewed_proposal"},
            {"day": 2, "type": "VM", "time": "12:06pm", "template": "vm_150_lenders"},
            {"day": 2, "type": "SMS", "time": "12:51pm", "template": "5star_reviews"},
            {"day": 2, "type": "Email", "time": "1:51pm", "template": "know_who_working_with"},
            {"day": 2, "type": "SMS", "time": "4:51pm", "template": "gentle_reminder_email"},
            {"day": 2, "type": "SMS", "time": "5:40pm", "template": "what_think_numbers"},
        ]
    
    def get_message_templates(self):
        """All message templates with personalization tokens"""
        return {
            # Day 1 - Initial Contact
            "initial_contact": {
                "subject": "Working on Your Proposal",
                "body": "Hi {first_name}, this is Phil from West Cap. I am working on your proposal now. Can you confirm how much equity you are looking for? And does texting work for communicating?",
                "attachment": "business_card"
            },
            "confirmation_email": {
                "subject": "Confirmation: Your Inquiry with West Capital Lending",
                "body": "Thank you for your interest in West Capital Lending. We've received your inquiry and Phil Gustin is working on your personalized proposal..."
            },
            "vm1_long_honest": {
                "subject": "Voicemail: Long Honest VM",
                "script": "Hi {first_name}, this is Phil Gustin from West Capital Lending..."
            },
            "purpose_question": {
                "body": "{first_name}, I am working on your numbers. Is this for home improvement or debt consolidation?"
            },
            "send_proposal": {
                "body": "{first_name}, here is a prelim quote based on the info you provided with our starting rates, and I also just sent it via email. Let me know what you think and if you have any adjustments. A lot of times the info is not entirely accurate, but happy to update if needed. 👍",
                "attachment": "proposal"
            },
            "proposal_email": {
                "subject": "{first_name} {last_name} - West Capital Lending Rate Options",
                "body": "Attached is your personalized rate quote..."
            },
            "followup_proposal": {
                "body": "{first_name}, did you see my texts above? ☝️ Providing your goals and what you are looking to do and any other details will help provide the best possible service to you and get exactly what you need. Let me know when you have a few mins to talk. 5 mins max!"
            },
            "custom_quote_finetune": {
                "subject": "Your Custom Loan Quote - Let's fine tune it (product overview)",
                "body": "Here's a detailed breakdown of your options..."
            },
            "background_value": {
                "body": "Hopefully you are not getting too blown up by text and calls... but I hope we can connect and you can see my background and value that I can provide to you giving you honest feedback you can trust. I look forward to speaking with you!"
            },
            
            # Day 2
            "good_morning": {
                "body": "Good Morning {first_name}, Do you have a few minutes today to connect and go through your goals?"
            },
            "texting_or_call": {
                "body": "Hey it's Phil, just seeing when a good time is to connect for you. Do you want to continue texting or it would be most efficient and quickest if I can call you when your ideal time is. Let me know what day/time works best for you."
            },
            "5star_reviews": {
                "body": "BTW, just wanted to make sure you knew we are a 5 star lender with over 14,000 reviews for the company and I personally have over 200 5 star reviews and have over 17 years experience in this industry. Just want you to know you are in good hands!\n\nWest Cap Reviews: {wc_reviews}\nPhil Gustin Reviews: {phil_reviews}"
            },
            "know_who_working_with": {
                "subject": "Know who your working with",
                "body": "Learn more about Phil Gustin and West Capital Lending..."
            },
            "gentle_reminder": {
                "body": "Gentle reminder ☝️of messages above.. Is this email correct? {email}",
                "attachment": "did_you_get_it"
            },
            "shopping_best_deal": {
                "body": "👋 {first_name} I understand you're shopping for the best deal. What is important to you to make your decision and decide on who you want to go with?"
            },
            
            # Day 3
            "easy_dob_income": {
                "body": "I'll make it easy… want to text just your DOB and household income? I can send you an official offer with JUST that.",
                "attachment": "easy_button"
            },
            "day3_quote": {
                "body": "Day 3 Quote - Hi {first_name}, I just wanted to see if any of these options might suit you best. Not an automated system, this is me. As a broker, we are wholesale priced. It's worth at least having the conversation. Are you still interested?"
            },
            "vm_999_time": {
                "script": "VM - 99.9% of time we can help..."
            },
            "verify_details": {
                "body": "Since I'm sure you are busy. Can you do me a favor and verify a couple things so I can verify your options:\n\nWhat is your home worth?\nWhat is first loan balance?\nWhat is your current Interest rate?\nHow much cash are you requesting?\nWhat is your estimated credit score (if you know)?"
            },
            "skip_2_payments": {
                "body": "I wanted to make sure you knew that we can skip 2 months payments with refinancing, and consolidate all your debt. OR if you want a 2nd, we have a 5 day very quick HELOC option with no appraisal and automated income approval. Incredible options! Just let me know what you prefer. Here's a little more about me too.",
                "attachment": "about_me"
            },
            "couple_questions": {
                "subject": "{first_name} - Couple of Questions for Your Best Options"
            },
            "evening_available": {
                "body": "{first_name}, easier to talk in the evening? I am available until 11pm EST. Is this for debt consolidation or renovations?"
            },
            
            # Day 4
            "day4_quote": {
                "body": "Day 4 Quote - {first_name}, I don't want you to miss this opportunity to improve your financial future. Imagine the freedom of lower payments or extra cash for things that truly matter. Let's connect today and make sure you don't leave any money on the table."
            },
            "not_be_bother": {
                "body": "I don't want to be a bother, {first_name}. Still weighing your options?"
            },
            "vm_short_sweet": {
                "script": "VM Drop - Short & Sweet"
            },
            "told_no_elsewhere": {
                "body": "{first_name}, were you told NO elsewhere? This usually happens when I don't hear back from someone. We 99.9% of time can help... lets talk"
            },
            "heloc_1day_close": {
                "subject": "Introducing 1 day close Fixed HELOC - 30/20/15 year options"
            },
            "heloc_fast_close": {
                "body": "Did you see we have a HELOC that can close in less than a week? We can go up to $400k with rates as low as 6%. No income docs or appraisal needed and can close in a week. Happy to explain more on the phone when you have time, but if you send me your DOB and annual household income, I can get started and send a few options your way. OR you can go to www.philthemortgagepro.com/HELOC and get started and receive offers in 1 minute!"
            },
            
            # Day 5
            "day5_quote": {
                "body": "Day 5 quote - {first_name}, here is a reminder of our starting options. Let's get you setup with a perfect loan by aligning this cash out with your exact goals so your mortgage works for you and not the other way around. Please let me know when you have time or you can schedule an appointment here: {calendly_link}"
            },
            "vm_followup_proposal": {
                "script": "Random follow up on vm proposal"
            },
            "defer_payment": {
                "body": "Good Morning, I wanted to let you know that we can help you defer at least 1 payment, possibly 2 with this cash out. Are you available for a 5 min call today?"
            },
            "payoff_high_interest": {
                "body": "Also a lot of my clients are paying off high interest debt. If you have any I would love to show you how much we can save you monthly. 💸"
            },
            "ensure_saw_texts": {
                "body": "Hi {first_name}, did you see my texts above. Want to ensure you saw them. Do you have any questions?"
            },
            "figure_intro_video": {
                "subject": "Email - figure intro with video"
            },
            "rates_went_down": {
                "body": "I wanted to update you on today's rates. They went down! Would love to discuss your loan when you have a minute. Do you have time tonight or tomorrow?"
            },
            
            # Day 6+
            "confirm_name": {
                "body": "Is this {first_name}?"
            },
            "vm_didnt_hear": {
                "script": "VM drop - I didn't hear from you"
            },
            "rates_down_half_percent": {
                "subject": "Rates are down .5%!!!"
            },
            "updated_numbers_offer": {
                "body": "Hi, it's Phil again with West Capital Lending. Are you interested in getting updated numbers? Or if you have an offer from someone else, I can show you how much I can save you compared to others?"
            },
            "vm_beat_anyone": {
                "script": "WCL VM 5 - we'll beat anyone"
            },
            "cashout_great_idea": {
                "subject": "Cash out is a great idea now"
            },
            "equity_purpose": {
                "body": "Hi {first_name}, if you were thinking about cash out... Pulling out equity can help with paying off debt to decrease expenses, remodeling your home, or even investing, what did you want to tap into your equity for? And how much do you need?"
            },
            "told_dont_qualify": {
                "body": "Hi {first_name}, I hope you are doing well. Most of the time if I don't hear from someone, it means they were told they don't qualify. The good news with us, is that we can go as low as 500 on credit scores and have many unique products that can get you a home including bank statement, stated, and others. Also I have some HELOC's that go off only 1 person's credit score and still use other peoples income to qualify. When do you have a few mins to talk?"
            },
            "low_credit_no_problem": {
                "subject": "Low Credit? No Problem!"
            },
            "started_elsewhere": {
                "body": "You may have started the process elsewhere… I promise you're going to want to see what I can offer before you finalize. Do you have 5 mins?"
            },
            "already_in_process": {
                "subject": "Already in process?"
            },
            "rates_dropped": {
                "body": "{first_name}, Rates dropped. Are you still interested? Y or N"
            },
            "updated_quote_question": {
                "body": "Hey {first_name}, do you want to see an updated quote based off today's rates?"
            },
            "ghost_me": {
                "body": "{first_name}, did you ghost me? 👻"
            },
            "rates_3_percent_joke": {
                "body": "OMG, did you see rates are in the 3% range? J/k but they are getting better. Do you want to discuss your scenario?"
            },
            "last_ditch_effort": {
                "body": "Last ditch effort! Hope all is well! 🙏 Are you still looking into options for your home loan? I know it's been a while, but let me know what you owe on the home now and how much cash if any you're looking for. I can get some new numbers out to you in a few minutes. A lot has changed in the last month or so."
            },
            "rates_getting_better": {
                "subject": "{first_name} - Rates are getting Better!"
            },
            
            # Responded campaign
            "numbers_sent_confirm": {
                "body": "Numbers sent. See how easy that was with me. Can you confirm you got my proposal? When is a good time to hop on a call to review options? 5 min max!"
            },
            "review_proposal_which_option": {
                "body": "Hi {first_name}, did you have a chance to review the proposal we sent? Which option looks best?"
            },
            "saw_texts_above": {
                "subject": "{first_name}, Did you see my texts above? ☝️"
            },
            "not_automated_reviews": {
                "body": "FYI I'm not an automated system. I run my own branch here. See my reviews: {review_link}",
                "attachment": "about_me"
            },
            "saw_numbers_yesterday": {
                "body": "Good Morning {first_name}, did you see the numbers I sent you yesterday?"
            },
            "day2_quote_manual": {
                "body": "Day 2 Quote - Hi {first_name}, here is the proposal again for your review. My goal is to get an understanding of what you are looking to do and validate these numbers. Can you talk today? 5 min max!"
            },
            "hope_reviewed_proposal": {
                "body": "Hey it's Phil again, I hope you had a chance to review my proposal. Which option are you leaning towards? If anything needs updated please let me know. Lots of times the details are not entirely accurate.\n\nAlso to give you a better idea of who I am and what's important to me, I've included a photo of my family :), thank you very much and I look forward to serving you and exceeding your expectations",
                "attachment": "family_photo"
            },
            "vm_150_lenders": {
                "script": "VM 2 - 150 lenders"
            },
            "gentle_reminder_email": {
                "body": "Gentle reminder ☝️of messages above.. Is this email correct? {email}",
                "attachment": "did_you_get_it"
            },
            "what_think_numbers": {
                "body": "👋 {first_name} I understand you're shopping for the best deal. What did you think of the numbers I sent over?"
            },
        }
    
    def create_campaign(self, lead_id, campaign_type, lead_data):
        """
        Create a new campaign for a lead
        
        Args:
            lead_id: Unique identifier for the lead
            campaign_type: Type of campaign ("new_lead_cashout", "responded")
            lead_data: Lead information for personalization
        """
        campaign = {
            "lead_id": lead_id,
            "campaign_type": campaign_type,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "lead_data": lead_data,
            "scheduled_touchpoints": self._schedule_touchpoints(campaign_type, lead_data),
            "completed_touchpoints": [],
            "tags": [campaign_type]
        }
        
        # Save to file
        self._save_campaign(campaign)
        
        return campaign
    
    def _schedule_touchpoints(self, campaign_type, lead_data):
        """Calculate exact send times for all touchpoints based on lead's timezone"""
        template = self.campaign_templates.get(campaign_type, [])
        scheduled = []
        
        # Get lead's timezone (default to EST if not specified)
        timezone_str = lead_data.get("timezone", "America/New_York")
        lead_tz = pytz.timezone(timezone_str)
        
        # Campaign start time (now in lead's timezone)
        start_time = datetime.now(lead_tz)
        
        for touchpoint in template:
            scheduled_time = None
            
            if "delay_minutes" in touchpoint:
                # Delay-based (from campaign start or previous touchpoint)
                scheduled_time = start_time + timedelta(minutes=touchpoint["delay_minutes"])
            elif "time" in touchpoint:
                # Specific time of day
                day_offset = touchpoint["day"] - 1
                target_date = start_time.date() + timedelta(days=day_offset)
                
                # Parse time (e.g., "9:02am")
                time_str = touchpoint["time"]
                time_obj = datetime.strptime(time_str, "%I:%M%p" if ":" in time_str else "%I%p").time()
                
                scheduled_time = lead_tz.localize(datetime.combine(target_date, time_obj))
            
            # Only schedule if during allowed hours (8am - 8pm local time)
            if scheduled_time:
                hour = scheduled_time.hour
                if hour < 8:
                    scheduled_time = scheduled_time.replace(hour=8, minute=0)
                elif hour >= 20:
                    scheduled_time = scheduled_time + timedelta(days=1)
                    scheduled_time = scheduled_time.replace(hour=8, minute=0)
                
                scheduled.append({
                    **touchpoint,
                    "scheduled_time": scheduled_time.isoformat(),
                    "status": "pending",
                    "sent_at": None
                })
        
        return scheduled
    
    def _save_campaign(self, campaign):
        """Save campaign to JSON file"""
        campaigns = self._load_all_campaigns()
        campaigns[campaign["lead_id"]] = campaign
        
        with open(self.campaigns_file, 'w') as f:
            json.dump(campaigns, f, indent=2)
    
    def _load_all_campaigns(self):
        """Load all campaigns from file"""
        if not self.campaigns_file.exists():
            return {}
        
        try:
            with open(self.campaigns_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def get_campaign(self, lead_id):
        """Get campaign for a specific lead"""
        campaigns = self._load_all_campaigns()
        return campaigns.get(lead_id)
    
    def update_campaign_status(self, lead_id, new_status, new_tags=None):
        """Update campaign status (active, paused, stopped)"""
        campaigns = self._load_all_campaigns()
        
        if lead_id in campaigns:
            campaigns[lead_id]["status"] = new_status
            
            if new_tags:
                if "tags" not in campaigns[lead_id]:
                    campaigns[lead_id]["tags"] = []
                campaigns[lead_id]["tags"].extend(new_tags)
                campaigns[lead_id]["tags"] = list(set(campaigns[lead_id]["tags"]))  # Remove duplicates
            
            with open(self.campaigns_file, 'w') as f:
                json.dump(campaigns, f, indent=2)
    
    def mark_touchpoint_sent(self, lead_id, touchpoint_index):
        """Mark a touchpoint as sent"""
        campaigns = self._load_all_campaigns()
        
        if lead_id in campaigns:
            if touchpoint_index < len(campaigns[lead_id]["scheduled_touchpoints"]):
                touchpoint = campaigns[lead_id]["scheduled_touchpoints"][touchpoint_index]
                touchpoint["status"] = "sent"
                touchpoint["sent_at"] = datetime.now().isoformat()
                
                campaigns[lead_id]["completed_touchpoints"].append(touchpoint)
            
            with open(self.campaigns_file, 'w') as f:
                json.dump(campaigns, f, indent=2)
    
    def get_pending_touchpoints(self, lead_id):
        """Get all pending touchpoints that should be sent now"""
        campaign = self.get_campaign(lead_id)
        
        if not campaign or campaign["status"] != "active":
            return []
        
        now = datetime.now()
        pending = []
        
        for i, touchpoint in enumerate(campaign["scheduled_touchpoints"]):
            if touchpoint["status"] == "pending":
                scheduled_time = datetime.fromisoformat(touchpoint["scheduled_time"])
                
                if scheduled_time <= now:
                    pending.append({"index": i, "touchpoint": touchpoint})
        
        return pending
    
    def stop_campaign_on_response(self, lead_id):
        """
        Stop current campaign when lead responds
        Optionally start a new "responded" campaign
        """
        self.update_campaign_status(lead_id, "stopped", ["responded"])
        
        # Could automatically start "responded" campaign here if needed
        # self.create_campaign(lead_id, "responded", lead_data)
    
    def personalize_message(self, template_key, lead_data):
        """
        Personalize a message template with lead data
        
        Args:
            template_key: Key for the message template
            lead_data: Lead information for personalization
        """
        templates = self.get_message_templates()
        template = templates.get(template_key, {})
        
        # Personalization tokens
        tokens = {
            "first_name": lead_data.get("name", "").split()[0] if lead_data.get("name") else "there",
            "last_name": " ".join(lead_data.get("name", "").split()[1:]) if lead_data.get("name") else "",
            "email": lead_data.get("email", "[email]"),
            "property_value": f"${lead_data.get('property_value', 0):,}",
            "cash_out": f"${lead_data.get('cash_out_amount', 0):,}",
            "wc_reviews": "https://westcapitallending.com/reviews",
            "phil_reviews": "https://www.philthemortgagepro.com/reviews",
            "review_link": "https://www.philthemortgagepro.com/reviews",
            "calendly_link": "https://calendly.com/philgustin",
        }
        
        # Replace tokens in body and subject
        result = {}
        for key, value in template.items():
            if isinstance(value, str):
                result[key] = value.format(**tokens)
            else:
                result[key] = value
        
        return result
