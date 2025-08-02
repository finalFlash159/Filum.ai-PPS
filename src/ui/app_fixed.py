"""
Filum.ai Pain Point Solution Agent - Improved UI
Clean, intuitive interface for business problem solving
"""

import streamlit as st
import requests
import json
import time
from typing import Dict, Any, List
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Filum.ai agent directly for fallback
try:
    from src.agent import get_filum_agent
    agent = get_filum_agent()
    USE_AGENT = True
except ImportError:
    USE_AGENT = False

# Configure Streamlit page
st.set_page_config(
    page_title="Filum.ai - Business Solution Finder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple, clean CSS (NO COMPLEX HTML)
st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .stApp { background-color: #f8fafc; }
    .css-1d391kg { padding-top: 1rem; }
    
    /* Simple header styling */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def display_header():
    """Display clean header"""
    st.markdown("""
    <div class="header">
        <h1>🎯 Filum.ai - Business Solution Finder</h1>
        <p>Intelligent matching of business challenges to Filum.ai solutions</p>
    </div>
    """, unsafe_allow_html=True)

def get_confidence_info(confidence):
    """Get confidence display info (SIMPLE VERSION)"""
    if confidence >= 0.8:
        return "high", "High Confidence", "🟢"
    elif confidence >= 0.6:
        return "medium", "Medium Confidence", "🟡"  
    else:
        return "low", "Low Confidence", "🔴"

def render_score_visualization(solution):
    """Render score breakdown (SIMPLE VERSION)"""
    scores = solution.get("scores", {})
    if not scores:
        st.write("Score breakdown not available")
        return
    
    for score_type, score_value in scores.items():
        if isinstance(score_value, (int, float)):
            st.write(f"**{score_type.replace('_', ' ').title()}:** {score_value:.1%}")

def display_solution_card(solution, index):
    """Display solution card - COMPLETELY SAFE VERSION"""
    
    # Get data with fallbacks
    feature = solution.get("feature", {})
    confidence = solution.get("confidence_score", 0.0)
    
    solution_name = feature.get('name', f"Solution #{index + 1}")
    category = feature.get("category", "Uncategorized")
    subcategory = feature.get("subcategory", "")
    description = feature.get("description", "")
    
    # 🎯 SECTION 1: Solution Header (SAFE)
    st.success(f"🎯 **{solution_name}**")
    
    confidence_color = "🟢" if confidence > 0.8 else "🟡" if confidence > 0.6 else "🔴"
    st.markdown(f"{confidence_color} **Confidence:** {confidence:.0%}")
    
    # 🏷️ SECTION 2: Category Information (SAFE)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info(f"📂 **Category:** {category}")
        if subcategory:
            st.info(f"📋 **Subcategory:** {subcategory}")
    
    with col2:
        if description:
            st.markdown("**📝 Description:**")
            st.write(description)
        else:
            st.warning("Description not available")
    
    # 🎯 SECTION 3: Pain Points & Solution (SAFE)
    pain_points = feature.get("pain_points_addressed", [])
    if pain_points:
        st.markdown("### 🎯 Pain Points This Solves")
        
        # Simple info display
        pain_point_text = "**🔴 Pain Points:**\n" + "\n".join([f"• {pain_point}" for pain_point in pain_points])
        pain_point_text += f"\n\n**✅ Filum.ai Solution:** {solution_name}"
        pain_point_text += f"\n**Category:** {category}"
        if subcategory:
            pain_point_text += f" - {subcategory}"
        
        st.info(pain_point_text)
    
    # 📊 SECTION 4: Additional Details (EXPANDABLE)
    with st.expander("📊 View Details", expanded=False):
        render_score_visualization(solution)
        
        # Benefits
        benefits = feature.get("benefits", [])
        if benefits:
            st.markdown("**✅ Benefits:**")
            for benefit in benefits[:3]:
                st.write(f"• {benefit}")
        
        # Use cases
        use_cases = feature.get("use_cases", [])
        if use_cases:
            st.markdown("**🔧 Use Cases:**")
            for use_case in use_cases[:3]:
                st.write(f"• {use_case}")

def display_examples_sidebar():
    """Display example pain points in sidebar"""
    st.sidebar.markdown("### 💡 Example Business Challenges")
    
    examples = [
        {
            "title": "📊 Customer Feedback",
            "pain_point": "It's difficult to collect customer feedback consistently after purchases across multiple channels like web, mobile, and in-store.",
        },
        {
            "title": "👥 Customer Profile",
            "pain_point": "It's difficult to get a single view of a customer's interaction history when they contact us.",
        },
        {
            "title": "🔍 Survey Analysis", 
            "pain_point": "Manually analyzing thousands of open-ended survey responses for common themes is too time-consuming.",
        }
    ]
    
    for example in examples:
        if st.sidebar.button(f"{example['title']}", key=f"example_{example['title']}"):
            st.session_state.input_text = example["pain_point"]
            st.experimental_rerun()

def analyze_pain_point_agent(pain_point_text: str) -> Dict[str, Any]:
    """Analyze using Filum.ai agent directly"""
    if not USE_AGENT:
        return {"error": "Agent not available"}
    
    try:
        result = agent.analyze_pain_point(pain_point_text)
        return result
    except Exception as e:
        return {"error": f"Agent error: {str(e)}"}

def analyze_pain_point_api(pain_point_text: str) -> Dict[str, Any]:
    """Analyze using API endpoint"""
    try:
        response = requests.post(
            "http://localhost:8000/analyze-pain-point",
            json={"pain_point": pain_point_text},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}

def main():
    """Main application"""
    
    # Display header
    display_header()
    
    # Sidebar examples
    display_examples_sidebar()
    
    # Main input area
    st.markdown("## 📝 Describe Your Business Challenge")
    
    # Initialize session state
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""
    
    # Input area
    pain_point_input = st.text_area(
        "What business challenge are you facing?",
        value=st.session_state.input_text,
        height=120,
        placeholder="Describe your business problem, operational challenge, or area where you need improvement...",
        help="Be specific about your challenge. The more details you provide, the better we can match you with the right Filum.ai solution."
    )
    
    # Analysis button
    if st.button("🔍 Find Filum.ai Solutions", type="primary"):
        if pain_point_input.strip():
            
            with st.spinner("🧠 AI is analyzing your challenge..."):
                
                # Try agent first, then API
                result = analyze_pain_point_agent(pain_point_input)
                
                if "error" in result and USE_AGENT:
                    # Fallback to API
                    result = analyze_pain_point_api(pain_point_input)
                
                if "error" in result:
                    st.error(f"❌ Analysis failed: {result['error']}")
                    st.info("💡 Make sure the backend server is running or try a different description.")
                else:
                    # Display results
                    st.markdown("## 🎯 Recommended Filum.ai Solutions")
                    
                    solutions = result.get("solutions", [])
                    if solutions:
                        for i, solution in enumerate(solutions):
                            with st.container():
                                display_solution_card(solution, i)
                                if i < len(solutions) - 1:
                                    st.markdown("---")
                    else:
                        st.warning("No matching solutions found. Try rephrasing your challenge.")
        else:
            st.warning("⚠️ Please describe your business challenge first.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 1rem;">
        🎯 <strong>Filum.ai</strong> - Intelligent Business Solution Finder<br>
        Powered by Advanced AI Matching • Built for Business Excellence
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
