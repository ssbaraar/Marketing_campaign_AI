import streamlit as st
import os
from dotenv import load_dotenv
from email_marketing_team import run_email_marketing_team
from email_utils import EmailMarketingUtils
from auth import login_page, check_auth, login_user
from campaign_manager import (
    save_campaign,
    save_strategy,
    save_approved_email,
    get_user_campaigns,
    get_campaign_details,
    update_campaign_status,
    verify_database_connection
)
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize session state variables
session_vars = [
    'authenticated', 'user_id', 'user_name', 'user_token',
    'current_page', 'campaign_data', 'strategy_approved',
    'email_approved', 'current_step', 'progress_message',
    'pending_review', 'approved_emails', 'email_drafts',
    'email_feedback', 'current_campaign_id', 'form_submitted',
    'current_view', 'last_action', 'authentication_status'
]

for var in session_vars:
    if var not in st.session_state:
        st.session_state[var] = None if 'id' in var or 'campaign' in var else False

# Cache campaign data
@st.cache_data(ttl=300, experimental_allow_widgets=True)
def fetch_campaign_details(campaign_id):
    return get_campaign_details(campaign_id)

@st.cache_data(ttl=300)
def fetch_user_campaigns_cached(user_id):
    """Cached wrapper for getting user campaigns"""
    return get_user_campaigns(user_id)

def handle_strategy_approval(campaign_id):
    key = f"strategy_approved_{campaign_id}"
    if key not in st.session_state:
        st.session_state[key] = False
    
    if st.checkbox("Approve Strategy", key=f"strategy_checkbox_{campaign_id}"):
        st.session_state[key] = True
    return st.session_state[key]

def handle_email_approval(campaign_id, email_number):
    key = f"email_approved_{campaign_id}_{email_number}"
    if key not in st.session_state:
        st.session_state[key] = False
    return st.session_state[key]

def handle_campaign_approval(campaign_id, email_number=None):
    # Keys for tracking approval state
    strategy_key = f"strategy_approved_{campaign_id}"
    email_key = f"email_approved_{campaign_id}_{email_number}" if email_number else None
    
    # Initialize in session state if not exists
    if strategy_key not in st.session_state:
        st.session_state[strategy_key] = False
    if email_key and email_key not in st.session_state:
        st.session_state[email_key] = False
    
    return st.session_state[strategy_key], st.session_state[email_key] if email_key else None

def maintain_campaign_state():
    """Initialize and maintain campaign state"""
    if 'campaign_states' not in st.session_state:
        st.session_state.campaign_states = {}
    
    if 'current_campaign_id' in st.session_state:
        campaign_id = st.session_state.current_campaign_id
        if campaign_id not in st.session_state.campaign_states:
            st.session_state.campaign_states[campaign_id] = {
                'approved_emails': [],
                'feedback': {},
                'strategy_approved': False
            }

# Page config
st.set_page_config(
    page_title="Email Marketing Team AI",
    page_icon="📧",
    layout="wide"
)

# Initialize page
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Main app flow
if not st.session_state.get('authenticated'):
    login_page()
else:
    try:
        user_id = check_auth()
        if user_id:
            # Your main app code here
            pass
        else:
            st.session_state.clear()
            st.rerun()
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.session_state.clear()
        st.rerun()

# Title and navigation
st.title("📧 AI Email Marketing Team")
    
# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["New Campaign", "My Campaigns"])

if page == "New Campaign":
    st.markdown("## Create New Campaign")
        
    # Campaign details form
    campaign_name = st.text_input("Campaign Name", "", key="campaign_name_input")
    product_name = st.text_input("Product Name", "", key="product_name_input")
    target_audience = st.text_input("Target Audience", "", key="target_audience_input")
    campaign_goal = st.text_input("Campaign Goal", "", key="campaign_goal_input")
    timeline = st.number_input("Timeline (weeks)", min_value=1, max_value=52, value=4, key="timeline_input")
        
    col1, col2 = st.columns(2)
    with col1:
        num_emails = st.number_input("Number of Emails", 1, 10, 3, key="num_emails_input")
        frequency = st.selectbox(
            "Email Frequency",
            ["Daily", "Weekly", "Bi-weekly", "Monthly"],
            key="frequency_input"
        )
        
    with col2:
        email_tone = st.select_slider(
            "Email Tone",
            options=["Very Formal", "Professional", "Neutral", "Casual", "Friendly"],
            value="Professional",
            key="email_tone_input"
        )
            
        template_style = st.selectbox(
            "Email Template Style",
            ["Professional", "Casual", "Minimalist"],
            key="template_style_input"
        )
        
    # Advanced options
    with st.expander("Advanced Options"):
        include_metrics = st.checkbox("Include Success Metrics", True, key="include_metrics_checkbox")
        preview_html = st.checkbox("Generate HTML Preview", False, key="preview_html_checkbox")
            
        st.subheader("Content Preferences")
        include_images = st.checkbox("Include Image Placeholders", True, key="include_images_checkbox")
        cta_style = st.selectbox(
            "Call-to-Action Style",
            ["Button", "Text Link", "Both"],
            key="cta_style_input"
        )
        max_email_length = st.number_input(
            "Maximum Email Length (words)",
            min_value=100,
            max_value=500,
            value=250,
            step=50,
            key="max_email_length_input"
        )

    if st.button("Generate Campaign", key="generate_campaign_button"):
        if campaign_name and product_name and target_audience and campaign_goal and timeline:
            # Save campaign details
            campaign_data = {
                "campaign_name": campaign_name,
                "product_name": product_name,
                "target_audience": target_audience,
                "campaign_goal": campaign_goal,
                "timeline": timeline,
                "num_emails": num_emails,
                "frequency": frequency,
                "email_tone": email_tone,
                "template_style": template_style
            }
            
            campaign_id = save_campaign(st.session_state.user_id, campaign_data)
            st.session_state.current_campaign_id = campaign_id
            
            # Create task prompt
            task = f"""
            We need to create an email campaign for our new product launch:
            - Campaign: {campaign_name}
            - Product: {product_name}
            - Target audience: {target_audience}
            - Goal: {campaign_goal}
            - Timeline: {timeline} weeks
            - Number of Emails: {num_emails}
            - Frequency: {frequency}
            - Email Tone: {email_tone}
        
            - Content Preferences:
              * Maximum Length: {max_email_length} words
              * Include Images: {include_images}
              * CTA Style: {cta_style}
            """
            
            try:
                # Run the email marketing team with progress updates
                results = run_email_marketing_team(task, lambda x: st.write(x))
                
                # Save strategy
                save_strategy(campaign_id, results["strategy"])
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs(["Strategy", "Email Drafts", "Preview", "Review & Approve"])
                
                with tab1:
                    st.header("Campaign Strategy")
                    st.write(results["strategy"])
                    strategy_approved = st.checkbox("Approve Strategy", key="approve_strategy_checkbox")
                
                with tab2:
                    st.header("Email Drafts")
                    st.session_state.email_drafts = results["email_drafts"]
                    for i, email in enumerate(st.session_state.email_drafts, 1):
                        with st.expander(f"Email {i}"):
                            st.markdown("### Draft Content")
                            email_content = st.text_area("Email Content", email, height=300, key=f"email_content_{i}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                feedback = st.text_area(
                                    "Feedback",
                                    key=f"feedback_{i}",
                                    value=st.session_state.email_feedback.get(i, "")
                                )
                                if feedback:
                                    st.session_state.email_feedback[i] = feedback
                            
                            with col2:
                                if i in st.session_state.approved_emails:
                                    st.success("✅ Approved")
                                else:
                                    col_a, col_b = st.columns([3, 1])
                                    with col_a:
                                        feedback_extra = st.text_area(
                                            "Additional Feedback",
                                            key=f"additional_feedback_{i}",
                                            value=st.session_state.email_feedback.get(i, "")
                                        )
                                    with col_b:
                                        if st.button(f"Approve Email {i}", key=f"approve_email_{campaign_id}_{i}"):
                                            st.session_state.approved_emails.append(i)
                                            if feedback_extra:
                                                st.session_state.email_feedback[i] = feedback_extra
                                                
                                                # Save approved email without triggering refresh
                                                email_data = {
                                                    "email_number": i,
                                                    "subject": email.split('\n')[0],
                                                    "content": email_content,
                                                    "feedback": feedback_extra
                                                }
                                                save_approved_email(campaign_id, email_data)
                                                
                                                # Update session state
                                                st.session_state[f"email_approved_{campaign_id}_{i}"] = True
                                                # Prevent refresh
                                                st.experimental_rerun()
                
                with tab3:
                    st.header("Preview")
                    if preview_html and results.get("html_preview"):
                        st.components.v1.html(results["html_preview"], height=600)
                    else:
                        st.info("Enable HTML Preview in Advanced Options to see the email preview")
                
                with tab4:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Approval Status")
                        st.write("Approved Emails:", sorted(st.session_state.approved_emails))
                        st.write(f"Progress: {len(st.session_state.approved_emails)}/{num_emails} emails approved")
                        
                    with col2:
                        st.subheader("Launch Campaign")
                        if len(st.session_state.approved_emails) == num_emails and strategy_approved:
                            if st.button("🚀 Launch Campaign", key=f"launch_campaign_{campaign_id}", type="primary"):
                                update_campaign_status(campaign_id, "launched")
                                st.balloons()
                                st.success("Campaign is ready for launch! 🎉")
                        else:
                            remaining = num_emails - len(st.session_state.approved_emails)
                            if not strategy_approved:
                                st.warning("⚠️ Please approve the strategy")
                            if remaining > 0:
                                st.warning(f"⚠️ Please approve {remaining} more email{'s' if remaining > 1 else ''}")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("Please fill in all required fields")

else:  # My Campaigns page
    st.markdown("## My Campaigns")
        
    # Debug information
    st.write("Current user ID:", st.session_state.user_id)
        
    try:
        # Clear the cache for testing
        fetch_user_campaigns_cached.clear()
            
        # Fetch campaigns
        user_campaigns = fetch_user_campaigns_cached(st.session_state.user_id)
            
        # Debug information
        st.write(f"Found {len(user_campaigns)} campaigns")
            
        if user_campaigns:
            for campaign in user_campaigns:
                with st.expander(f"📧 {campaign.get('campaign_name', 'Unnamed Campaign')} "
                                f"({campaign.get('status', 'Draft')})"):
                    
                    # Display campaign details
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Product:**", campaign.get('product_name', 'N/A'))
                        st.write("**Target Audience:**", campaign.get('target_audience', 'N/A'))
                        st.write("**Goal:**", campaign.get('campaign_goal', 'N/A'))
                    
                    with col2:
                        st.write("**Timeline:**", campaign.get('timeline', 'N/A'), "weeks")
                        st.write("**Number of Emails:**", campaign.get('num_emails', 'N/A'))
                        st.write("**Approved Emails:**", len(campaign.get('emails', [])))
                            
                        created_at = campaign.get('created_at')
                        if created_at:
                            if isinstance(created_at, str):
                                st.write("**Created:**", created_at)
                            else:
                                st.write("**Created:**", created_at.strftime("%Y-%m-%d %H:%M"))
                    
                    # Campaign actions
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("View Details", key=f"view_{campaign['_id']}"):
                            st.session_state.current_campaign_id = campaign['_id']
                            st.session_state.current_view = 'campaign_details'
                            st.experimental_rerun()
                    
                    with col_b:
                        if st.button("Delete Campaign", key=f"delete_{campaign['_id']}"):
                            # Add delete functionality here
                            # Example:
                            update_campaign_status(campaign['_id'], "deleted")
                            st.success(f"Campaign '{campaign.get('campaign_name', 'Unnamed')}' deleted successfully.")
                            st.experimental_rerun()
        else:
            # Check the database directly
            from database import campaigns
            direct_count = campaigns.count_documents({"user_id": st.session_state.user_id})
            st.write(f"Direct database count: {direct_count} campaigns")
                
            if direct_count > 0:
                st.error("Campaigns exist but couldn't be loaded properly. Please contact support.")
            else:
                st.info("You haven't created any campaigns yet. Go to 'New Campaign' to create one!")

    except Exception as e:
        st.error(f"Error loading campaigns: {str(e)}")
        st.write("Debug info:")
        st.write(f"User ID: {st.session_state.user_id}")
        st.write(f"Error details: {str(e)}")