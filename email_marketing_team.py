import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def run_email_marketing_team(task, progress_callback=None):
    if progress_callback:
        progress_callback("🤔 Analyzing campaign requirements...")
    
    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-pro')
    
    if progress_callback:
        progress_callback("📊 Generating campaign strategy...")
    
    # Generate campaign strategy
    strategy_prompt = f"""
    As an email marketing strategist, create a detailed campaign strategy for the following task:
    {task}
    
    Include:
    1. Campaign objectives
    2. Key messaging points
    3. Email sequence plan
    4. Success metrics
    """
    
    strategy_response = model.generate_content(strategy_prompt)
    strategy = strategy_response.text
    
    # Extract number of emails from task
    num_emails_match = re.search(r'Number of Emails: (\d+)', task)
    num_emails = int(num_emails_match.group(1)) if num_emails_match else 1
    
    if progress_callback:
        progress_callback("✍️ Crafting email drafts...")
    
    # Generate multiple email drafts
    email_drafts = []
    for i in range(num_emails):
        email_prompt = f"""
        Based on this strategy:
        {strategy}
        
        Write email {i+1} of {num_emails} for this campaign. Make each email unique but connected.
        The email should have:
        1. An attention-grabbing subject line
        2. Persuasive body copy that builds on previous emails
        3. A clear call-to-action
        
        Format the response as:
        Subject: [Your subject line]
        
        [Email body]
        
        CTA: [Your call-to-action]
        """
        
        email_response = model.generate_content(email_prompt)
        email_drafts.append(email_response.text)
        if progress_callback:
            progress_callback(f"✍️ Crafting email draft {i+1} of {num_emails}...")
    
    if progress_callback:
        progress_callback("✅ Finalizing campaign materials...")
    
    # Generate HTML preview if requested
    html_preview = None
    if "Generate HTML Preview: True" in task:
        html_preview = generate_html_preview(email_drafts[0])  # Preview first email
    
    return {
        "strategy": strategy,
        "email_drafts": email_drafts,
        "html_preview": html_preview
    }

def generate_html_preview(email_text):
    # Simple HTML template for email preview
    html_template = f"""
    <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; padding: 20px;">
        {email_text.replace('\n', '<br>')}
    </div>
    """
    return html_template