"""
CardWise - AI-Powered Credit Card Recommendation System
======================================================

A professional Streamlit web application that provides personalized credit card 
recommendations based on user's financial profile using AI analysis.
"""

import streamlit as st
import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from googlesearch import search
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import base64


@dataclass
class UserProfile:
    """Data class to store essential user financial profile information."""
    monthly_spending: float
    credit_score_range: str
    primary_goals: List[str]
    spending_categories: Dict[str, float]


class CardWiseApp:
    """Main application class for CardWise credit card recommendation system."""
    
    def __init__(self):
        """Initialize the CardWise application."""
        self.setup_page_config()
        self.setup_session_state()
        
    def setup_page_config(self):
        """Configure Streamlit page settings with dark theme."""
        st.set_page_config(
            page_title="CardWise - AI Credit Card Advisor",
            page_icon="💳",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Set dark theme using Streamlit's native dark mode
        st.markdown("""
        <style>
        /* Force dark theme */
        .stApp {
            background-color: #000000;
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)
        
    def setup_session_state(self):
        """Initialize session state variables."""
        if 'recommendation_generated' not in st.session_state:
            st.session_state.recommendation_generated = False
        if 'recommendation_data' not in st.session_state:
            st.session_state.recommendation_data = None
        if 'search_results' not in st.session_state:
            st.session_state.search_results = []
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = None
            
    def apply_custom_css(self):
        """Apply custom CSS styling for professional dark theme appearance."""
        st.markdown("""
        <style>
        /* Main app background */
        .main .block-container {
            background-color: #000000;
            color: #ffffff;
        }
        
        /* Overall app background */
        .stApp {
            background-color: #000000;
            color: #ffffff;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1a1a1a;
        }
        
        .css-1lcbmhc {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        
        /* Headers */
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
            color: #cccccc;
            text-align: center;
            margin-bottom: 3rem;
            font-style: italic;
        }
        
        /* Recommendation card with dark theme */
        .recommendation-card {
            background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
            padding: 2rem;
            border-radius: 15px;
            color: #ffffff;
            margin: 1rem 0;
            border: 1px solid #4a5568;
        }
        
        /* Step items with dark theme */
        .step-item {
            background-color: #2d3748;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            border-left: 4px solid #68d391;
            color: #ffffff;
        }
        
        /* Success box with dark theme */
        .success-box {
            background-color: #1a202c;
            border: 1px solid #38a169;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            color: #ffffff;
        }
        
        /* All text elements */
        .stMarkdown, .stText, .stCaption {
            color: #ffffff;
        }
        
        /* Input labels and text */
        .stSelectbox label, .stNumberInput label, .stMultiSelect label, .stSlider label {
            color: #ffffff !important;
        }
        
        /* Sidebar text */
        .css-1lcbmhc .stMarkdown {
            color: #ffffff;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #4299e1;
            color: #ffffff;
            border: none;
        }
        
        .stButton button:hover {
            background-color: #3182ce;
            color: #ffffff;
        }
        
        /* Expandable sections */
        .streamlit-expanderHeader {
            background-color: #2d3748;
            color: #ffffff;
        }
        
        /* Metrics and other components */
        .metric-container {
            background-color: #2d3748;
            color: #ffffff;
        }
        
        /* Fix any remaining white backgrounds */
        div[data-testid="stSidebar"] {
            background-color: #1a1a1a;
        }
        
        div[data-testid="stSidebar"] .stMarkdown {
            color: #ffffff;
        }
        
        /* Error and warning messages */
        .stAlert {
            background-color: #2d3748;
            color: #ffffff;
            border: 1px solid #e53e3e;
        }
        
        /* Success messages */
        .stSuccess {
            background-color: #1a202c;
            color: #ffffff;
            border: 1px solid #38a169;
        }
        
        /* Spinner and loading */
        .stSpinner {
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

    def render_header(self):
        """Render the main application header with dark theme."""
        st.markdown('<h1 class="main-header">💳 CardWise</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-Powered Credit Card Recommendations</p>', unsafe_allow_html=True)
        
    def render_sidebar(self) -> Optional[UserProfile]:
        """Render the simplified sidebar with essential inputs only."""
        st.sidebar.header("📊 Essential Profile")
        
        # Monthly Spending - Most critical for reward calculations
        st.sidebar.markdown("### 💰 Monthly Spending")
        monthly_spending = st.sidebar.number_input(
            "Total Monthly Spending ($)",
            min_value=500,
            max_value=20000,
            value=3000,
            step=100,
            help="Your total monthly credit card spending across all categories"
        )
        
        # Credit Score - Determines card eligibility
        st.sidebar.markdown("### 📈 Credit Score")
        credit_score_range = st.sidebar.selectbox(
            "Credit Score Range",
            ["Excellent (750+)", "Good (700-749)", "Fair (650-699)", "Poor (600-649)"],
            index=1,
            help="Your current credit score range determines which cards you qualify for"
        )
        
        # Primary Goals - Core recommendation driver
        st.sidebar.markdown("### 🎯 Primary Goals")
        primary_goals = st.sidebar.multiselect(
            "What do you want to maximize?",
            ["Maximize cashback", "Earn travel rewards", "Build credit", "No annual fees", 
             "Sign-up bonuses", "Low interest rates"],
            default=["Maximize cashback"],
            help="Select your main financial objectives for credit card usage"
        )
        
        # Simplified Spending Categories - Top 3 categories only
        st.sidebar.markdown("### 🛍️ Top Spending Categories")
        st.sidebar.markdown("*Allocate your spending across these main categories:*")
        
        dining_travel = st.sidebar.slider(
            "Dining & Travel (%)", 
            0, 100, 30,
            help="Restaurants, bars, hotels, flights, etc."
        )
        groceries_gas = st.sidebar.slider(
            "Groceries & Gas (%)", 
            0, 100, 35,
            help="Supermarkets, gas stations, everyday essentials"
        )
        other = max(0, 100 - (dining_travel + groceries_gas))
        
        st.sidebar.markdown(f"**Other purchases: {other}%**")
        
        spending_categories = {
            "dining_travel": dining_travel,
            "groceries_gas": groceries_gas,
            "other": other
        }
        
        # Generate recommendations button
        generate_button = st.sidebar.button(
            "🔍 Get AI Recommendations",
            type="primary",
            use_container_width=True
        )
        
        if generate_button:
            if not primary_goals:
                st.sidebar.error("Please select at least one financial goal.")
                return None
                
            return UserProfile(
                monthly_spending=monthly_spending,
                credit_score_range=credit_score_range,
                primary_goals=primary_goals,
                spending_categories=spending_categories
            )
        
        return None
    
    def search_credit_cards(self, user_profile: UserProfile) -> List[str]:
        """Search for relevant credit cards using Google search - real-time data only."""
        search_terms = []
        
        # Build search terms based on user goals
        if "Maximize cashback" in user_profile.primary_goals:
            search_terms.append("best cashback credit cards 2024 current offers")
        if "Earn travel rewards" in user_profile.primary_goals:
            search_terms.append("best travel rewards credit cards 2024 current bonuses")
        if "No annual fees" in user_profile.primary_goals:
            search_terms.append("best no annual fee credit cards 2024")
        if "Build credit" in user_profile.primary_goals:
            search_terms.append("best credit building cards 2024")
        if "Sign-up bonuses" in user_profile.primary_goals:
            search_terms.append("credit cards best signup bonuses 2024")
        
        # Add credit score specific searches
        if "Excellent" in user_profile.credit_score_range:
            search_terms.append("premium credit cards excellent credit 2024")
        elif "Good" in user_profile.credit_score_range:
            search_terms.append("best credit cards good credit score 2024")
        elif "Fair" in user_profile.credit_score_range:
            search_terms.append("credit cards fair credit 2024")
        
        search_results = []
        
        try:
            for term in search_terms[:4]:  # Get more comprehensive results
                try:
                    results = list(search(term, num_results=4, sleep_interval=2))
                    search_results.extend(results)
                    time.sleep(2)  # Be respectful to search engines
                except Exception as e:
                    st.warning(f"Search for '{term}' failed: {str(e)}")
                    continue
            
            if not search_results:
                st.error("⚠️ Unable to fetch real-time credit card data. Search service unavailable.")
                st.error("This app requires real-time market data to function properly.")
                st.stop()
            
            return search_results[:12]  # Return more comprehensive results
            
        except Exception as e:
            st.error(f"⚠️ Real-time search failed: {str(e)}")
            st.error("Unable to fetch current credit card offers. Please try again later.")
            st.stop()
    
    def generate_ai_recommendation(self, user_profile: UserProfile, search_results: List[str]) -> Dict:
        """Generate AI-powered recommendations using OpenRouter API."""
        prompt = self._create_recommendation_prompt(user_profile, search_results)
        
        # Get API key from secrets - required for operation
        api_key = st.secrets.get("OPENROUTER_API_KEY", "")
        if not api_key:
            st.error("⚠️ OpenRouter API key not found. Please configure OPENROUTER_API_KEY in secrets.")
            st.stop()
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a financial advisor specializing in credit card recommendations. Analyze real-time market data and provide personalized recommendations based on current credit card offers."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                st.success("✅ AI recommendations generated successfully")
                return self._parse_ai_response(ai_response)
            else:
                st.error(f"⚠️ API request failed with status {response.status_code}: {response.text}")
                st.error("Unable to generate recommendations without AI service.")
                st.stop()
                
        except requests.exceptions.Timeout:
            st.error("⚠️ Request timed out. Please try again.")
            st.stop()
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Network error: {str(e)}")
            st.stop()
        except Exception as e:
            st.error(f"⚠️ Unexpected error: {str(e)}")
            st.stop()
    
    def _create_recommendation_prompt(self, user_profile: UserProfile, search_results: List[str]) -> str:
        """Create a detailed prompt for AI recommendation generation using essential user data."""
        return f"""
        You are a professional financial advisor. Analyze this user's essential financial profile and current real-time credit card market data to provide the most suitable credit card recommendations.

        USER ESSENTIAL PROFILE:
        - Monthly Spending: ${user_profile.monthly_spending:,}
        - Credit Score Range: {user_profile.credit_score_range}
        - Primary Goals: {', '.join(user_profile.primary_goals)}
        - Top Spending Categories: {user_profile.spending_categories}

        CURRENT REAL-TIME MARKET DATA:
        {chr(10).join([f"- {result}" for result in search_results[:8]])}

        ANALYSIS INSTRUCTIONS:
        1. Focus on the user's monthly spending amount of ${user_profile.monthly_spending:,} to calculate actual reward values
        2. Ensure recommended cards match their {user_profile.credit_score_range} credit score range
        3. Prioritize cards that align with their goals: {', '.join(user_profile.primary_goals)}
        4. Consider their spending pattern: {user_profile.spending_categories}
        5. Use only current market data to ensure recommendations reflect today's offers

        Please provide your response in the following JSON format:
        {{
            "primary_recommendation": {{
                "card_name": "Exact card name from market data",
                "issuer": "Card issuer",
                "key_benefits": ["benefit1", "benefit2", "benefit3"],
                "annual_fee": "Specific fee amount or 'No annual fee'",
                "reward_rate": "Detailed reward structure for their spending",
                "why_recommended": "Specific explanation based on their ${user_profile.monthly_spending:,} monthly spending and {user_profile.credit_score_range} credit score",
                "current_signup_bonus": "Current signup bonus if available"
            }},
            "action_plan": [
                "Specific step 1 based on current offers",
                "Specific step 2 for maximizing their monthly ${user_profile.monthly_spending:,} spending",
                "Specific step 3 for their credit score range",
                "Specific step 4 for long-term strategy"
            ],
            "optimization_tips": [
                "Tip 1 for their spending categories",
                "Tip 2 for maximizing rewards on ${user_profile.monthly_spending:,}/month",
                "Tip 3 for their credit score range"
            ],
            "estimated_annual_value": "Calculated based on ${user_profile.monthly_spending:,} monthly spending",
            "alternative_options": [
                {{
                    "card_name": "Alternative card name",
                    "reason": "Why this could work for their profile"
                }}
            ]
        }}
        """
    
    def _parse_ai_response(self, ai_response: str) -> Dict:
        """Parse AI response and extract structured data."""
        try:
            # Find JSON in the response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = ai_response[json_start:json_end]
                parsed_data = json.loads(json_str)
                
                # Validate required fields
                required_fields = ['primary_recommendation', 'action_plan', 'optimization_tips']
                for field in required_fields:
                    if field not in parsed_data:
                        st.error(f"⚠️ Invalid AI response: missing {field}")
                        st.stop()
                
                return parsed_data
            else:
                st.error("⚠️ AI response format error: No valid JSON found")
                st.stop()
                
        except json.JSONDecodeError as e:
            st.error(f"⚠️ AI response parsing error: {str(e)}")
            st.error("Unable to process AI recommendations.")
            st.stop()
        except Exception as e:
            st.error(f"⚠️ Unexpected parsing error: {str(e)}")
            st.stop()


    
    def render_recommendations(self, recommendation_data: Dict, search_results: List[str]):
        """Render the AI-generated recommendations with dark theme."""
        st.markdown("## 🎯 Your Personalized Credit Card Strategy")
        st.markdown("*Based on real-time market data and AI analysis*")
        
        primary = recommendation_data["primary_recommendation"]
        
        # Enhanced primary recommendation display with explicit white text
        st.markdown(f"""
        <div class="recommendation-card">
            <h2 style="color: #ffffff;">🏆 Primary Recommendation</h2>
            <h3 style="color: #ffffff;">{primary['card_name']}</h3>
            <p style="color: #ffffff;"><strong>Issuer:</strong> {primary['issuer']}</p>
            <p style="color: #ffffff;"><strong>Annual Fee:</strong> {primary['annual_fee']}</p>
            <p style="color: #ffffff;"><strong>Reward Rate:</strong> {primary['reward_rate']}</p>
            {f"<p style='color: #ffffff;'><strong>Current Signup Bonus:</strong> {primary.get('current_signup_bonus', 'Check current offers')}</p>" if primary.get('current_signup_bonus') else ""}
        </div>
        """, unsafe_allow_html=True)
        
        # Key Benefits with white text
        st.markdown("### ✨ Key Benefits")
        for benefit in primary['key_benefits']:
            st.markdown(f"<p style='color: #ffffff;'>• {benefit}</p>", unsafe_allow_html=True)
        
        # Why recommended with white text
        st.markdown("### 💡 Why This Card is Perfect for You")
        st.markdown(f"<p style='color: #ffffff;'>{primary['why_recommended']}</p>", unsafe_allow_html=True)
        
        # Action Plan with dark theme
        st.markdown("### 📋 Your Action Plan")
        for i, step in enumerate(recommendation_data["action_plan"], 1):
            st.markdown(f"""
            <div class="step-item">
                <strong style="color: #ffffff;">Step {i}:</strong> <span style="color: #ffffff;">{step}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Optimization Tips with white text
        st.markdown("### 🚀 Optimization Tips")
        for tip in recommendation_data["optimization_tips"]:
            st.markdown(f"<p style='color: #ffffff;'>💡 {tip}</p>", unsafe_allow_html=True)
        
        # Estimated Annual Value
        if recommendation_data.get("estimated_annual_value"):
            st.markdown(f"""
            <div class="success-box">
                <h4 style="color: #ffffff;">💰 Estimated Annual Value: {recommendation_data['estimated_annual_value']}</h4>
            </div>
            """, unsafe_allow_html=True)
        
        # Alternative Options (if available)
        if recommendation_data.get("alternative_options"):
            st.markdown("### 🔄 Alternative Options to Consider")
            for alt in recommendation_data["alternative_options"]:
                st.markdown(f"<p style='color: #ffffff;'><strong>{alt['card_name']}:</strong> {alt['reason']}</p>", unsafe_allow_html=True)
        
        # Real-time market data summary with dark theme
        if search_results:
            with st.expander("📊 View Real-Time Market Data Used"):
                st.markdown("<p style='color: #ffffff;'><em>Current credit card offers analyzed for your recommendations:</em></p>", unsafe_allow_html=True)
                for i, result in enumerate(search_results[:8], 1):
                    st.markdown(f"<p style='color: #ffffff;'>{i}. {result}</p>", unsafe_allow_html=True)
    
    def generate_pdf_report(self, user_profile: UserProfile, recommendation_data: Dict) -> bytes:
        """Generate comprehensive PDF report of recommendations."""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            story = []
            
            # Title and Header
            title_style = styles['Title']
            title_style.textColor = colors.darkblue
            story.append(Paragraph("CardWise Credit Card Recommendation Report", title_style))
            story.append(Spacer(1, 20))
            
            # Generation info
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
            story.append(Paragraph(f"Report ID: CW-{datetime.now().strftime('%Y%m%d%H%M%S')}", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Financial Profile Section
            story.append(Paragraph("Your Financial Profile", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            profile_data = [
                ["Monthly Spending:", f"${user_profile.monthly_spending:,}"],
                ["Credit Score Range:", user_profile.credit_score_range],
                ["Primary Goals:", ", ".join(user_profile.primary_goals)],
                ["Spending Categories:", ""]
            ]
            
            # Add spending category breakdown
            for category, percentage in user_profile.spending_categories.items():
                formatted_category = category.replace('_', ' & ').title()
                profile_data.append(["", f"  • {formatted_category}: {percentage}%"])
            
            for label, value in profile_data:
                if label:
                    story.append(Paragraph(f"<b>{label}</b> {value}", styles['Normal']))
                else:
                    story.append(Paragraph(value, styles['Normal']))
            
            story.append(Spacer(1, 20))
            
            # Primary Recommendation Section
            primary = recommendation_data["primary_recommendation"]
            story.append(Paragraph("🏆 Primary Recommendation", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph(f"<b>Card:</b> {primary['card_name']}", styles['Normal']))
            story.append(Paragraph(f"<b>Issuer:</b> {primary['issuer']}", styles['Normal']))
            story.append(Paragraph(f"<b>Annual Fee:</b> {primary['annual_fee']}", styles['Normal']))
            story.append(Paragraph(f"<b>Reward Rate:</b> {primary['reward_rate']}", styles['Normal']))
            
            if primary.get('current_signup_bonus'):
                story.append(Paragraph(f"<b>Current Signup Bonus:</b> {primary['current_signup_bonus']}", styles['Normal']))
            
            story.append(Spacer(1, 12))
            story.append(Paragraph("<b>Why This Card is Perfect for You:</b>", styles['Normal']))
            story.append(Paragraph(primary['why_recommended'], styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Key Benefits
            story.append(Paragraph("Key Benefits:", styles['Heading2']))
            for benefit in primary['key_benefits']:
                story.append(Paragraph(f"• {benefit}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Action Plan
            story.append(Paragraph("Your Action Plan", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            for i, step in enumerate(recommendation_data["action_plan"], 1):
                story.append(Paragraph(f"<b>Step {i}:</b> {step}", styles['Normal']))
                story.append(Spacer(1, 6))
            
            # Optimization Tips
            story.append(Spacer(1, 12))
            story.append(Paragraph("Optimization Tips", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            for tip in recommendation_data["optimization_tips"]:
                story.append(Paragraph(f"💡 {tip}", styles['Normal']))
                story.append(Spacer(1, 6))
            
            # Estimated Value
            if recommendation_data.get("estimated_annual_value"):
                story.append(Spacer(1, 12))
                story.append(Paragraph(f"💰 Estimated Annual Value: {recommendation_data['estimated_annual_value']}", styles['Heading2']))
            
            # Alternative Options
            if recommendation_data.get("alternative_options"):
                story.append(Spacer(1, 12))
                story.append(Paragraph("Alternative Options to Consider", styles['Heading1']))
                story.append(Spacer(1, 12))
                
                for alt in recommendation_data["alternative_options"]:
                    story.append(Paragraph(f"<b>{alt['card_name']}:</b> {alt['reason']}", styles['Normal']))
                    story.append(Spacer(1, 6))
            
            # Footer
            story.append(Spacer(1, 30))
            story.append(Paragraph("Generated by CardWise - AI-Powered Credit Card Recommendations", styles['Normal']))
            story.append(Paragraph("This report is based on real-time market data and your personal financial profile.", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            # If PDF generation fails, raise with more context
            raise Exception(f"PDF generation error: {str(e)}. Please ensure ReportLab is installed and try again.")
    
    def render_pdf_download(self, user_profile: UserProfile, recommendation_data: Dict):
        """Render PDF download section with enhanced functionality."""
        st.markdown("### 📄 Download Your Recommendation Report")
        st.markdown("<p style='color: #ffffff;'>Generate a professional PDF report of your personalized credit card recommendations.</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            generate_pdf = st.button(
                "📄 Generate PDF",
                type="primary",
                use_container_width=True
            )
        
        if generate_pdf:
            try:
                with st.spinner("📄 Generating your PDF report..."):
                    pdf_data = self.generate_pdf_report(user_profile, recommendation_data)
                    
                # Create download link
                b64_pdf = base64.b64encode(pdf_data).decode()
                pdf_filename = f"CardWise_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                
                # Use download button (better than href)
                st.download_button(
                    label="💾 Download PDF Report",
                    data=pdf_data,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    type="secondary",
                    use_container_width=True
                )
                
                st.success("✅ PDF report generated successfully!")
                st.markdown(f"<p style='color: #ffffff;'>📁 File: <code>{pdf_filename}</code></p>", unsafe_allow_html=True)
                
            except ImportError as e:
                st.error("⚠️ PDF generation failed: ReportLab library not properly installed.")
                st.error("Please install ReportLab: pip install reportlab")
            except Exception as e:
                st.error(f"⚠️ PDF generation failed: {str(e)}")
                st.info("💡 Try refreshing the page and generating recommendations again.")
    
    def run(self):
        """Main application runner with real-time data emphasis."""
        self.apply_custom_css()
        self.render_header()
        
        # Add info about real-time data requirements
        if not st.session_state.recommendation_generated:
            st.markdown("""
            <div class="success-box">
                <h3 style="color: #ffffff;">👋 Welcome to CardWise!</h3>
                <p style="color: #ffffff;">Get AI-powered credit card recommendations based on <strong>real-time market data</strong>.</p>
                <p style="color: #ffffff;">🎯 <strong>Simple & Accurate:</strong> Just 4 essential inputs for precise recommendations:</p>
                <ul style="color: #ffffff;">
                    <li>💰 <strong>Monthly Spending</strong> - For reward calculations</li>
                    <li>📈 <strong>Credit Score</strong> - Determines card eligibility</li>
                    <li>🎯 <strong>Financial Goals</strong> - Drives recommendation logic</li>
                    <li>🛍️ <strong>Spending Categories</strong> - Maximizes category rewards</li>
                </ul>
                <p style="color: #ffffff;">⚠️ <strong>Requirements:</strong></p>
                <ul style="color: #ffffff;">
                    <li>OpenRouter API key must be configured</li>
                    <li>Internet connection for real-time credit card data</li>
                    <li>No fallback recommendations - only current market offers</li>
                </ul>
                <p style="color: #ffffff;">Fill out your essential profile in the sidebar to get started!</p>
            </div>
            """, unsafe_allow_html=True)
        
        user_profile = self.render_sidebar()
        
        if user_profile:
            # Store user profile in session state for PDF generation
            st.session_state.user_profile = user_profile
            
            # Real-time search with enhanced feedback
            with st.spinner("🔍 Fetching real-time credit card offers..."):
                search_results = self.search_credit_cards(user_profile)
                st.session_state.search_results = search_results
                st.success(f"✅ Found {len(search_results)} current credit card offers")
            
            # AI analysis with enhanced feedback
            with st.spinner("🤖 AI analyzing your profile with current market data..."):
                recommendation_data = self.generate_ai_recommendation(user_profile, search_results)
                st.session_state.recommendation_data = recommendation_data
                st.session_state.recommendation_generated = True
                st.success("✅ AI recommendations generated successfully")
        
        if st.session_state.recommendation_generated and st.session_state.recommendation_data:
            self.render_recommendations(
                st.session_state.recommendation_data, 
                st.session_state.search_results
            )
            
            # Always show PDF download if recommendations are available
            if st.session_state.user_profile:
                st.markdown("---")  # Add separator
                self.render_pdf_download(st.session_state.user_profile, st.session_state.recommendation_data)


# Main application entry point
if __name__ == "__main__":
    app = CardWiseApp()
    app.run()
