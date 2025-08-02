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

# Modern, professional CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Reset and base styling */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ffffff, #f8fafc);
        -webkit-background-clip: text;
        background-clip: text;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Input section */
    .input-section {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .input-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
    }
    
    .input-title {
        color: #1e293b;
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Solution cards */
    .solution-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .solution-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(79, 70, 229, 0.15);
        border-color: #4f46e5;
    }
    
    .solution-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.5rem;
    }
    
    .solution-title {
        color: #1e293b;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0;
        flex: 1;
        line-height: 1.4;
    }
    
    .confidence-badge {
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        text-align: center;
        min-width: 100px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-left: 1rem;
    }
    
    .confidence-high {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
    }
    
    .confidence-medium {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
    }
    
    .confidence-low {
        background: linear-gradient(135deg, #6b7280, #4b5563);
        color: white;
    }
    
    /* Score visualization */
    .score-section {
        margin: 1.5rem 0;
        padding: 1.5rem;
        background: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .score-title {
        color: #374151;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .score-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.8rem;
    }
    
    .score-label {
        font-size: 0.9rem;
        color: #4b5563;
        font-weight: 500;
        min-width: 120px;
    }
    
    .score-bar-container {
        flex: 1;
        margin: 0 1rem;
        background: #e5e7eb;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
    }
    
    .score-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.6s ease-in-out;
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }
    
    .score-value {
        font-size: 0.85rem;
        color: #374151;
        font-weight: 600;
        min-width: 45px;
        text-align: right;
    }
    
    /* Keywords section */
    .keywords-section {
        margin: 1rem 0;
    }
    
    .keyword-tag {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem 0.3rem 0.2rem 0;
        display: inline-block;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(79, 70, 229, 0.3);
    }
    
    .category-tags {
        margin: 0.8rem 0;
    }
    
    .category-tag {
        background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
        color: #374151;
        padding: 0.4rem 0.9rem;
        border-radius: 25px;
        font-size: 0.8rem;
        margin-right: 0.6rem;
        display: inline-block;
        border: 1px solid #d1d5db;
        font-weight: 500;
    }
    
    .solution-content {
        line-height: 1.6;
    }
    
    .help-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .help-title {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    .example-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196F3;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .example-box:hover {
        background: #bbdefb;
        transform: translateX(5px);
    }
    
    .example-text {
        margin: 0;
        color: #1565C0;
        font-weight: 500;
    }
    
    /* Stats styling */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        flex: 1;
        border: 1px solid #e0e6ed;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin: 0;
    }
    
    /* Loading animation */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .solution-header {
            flex-direction: column;
            gap: 1rem;
        }
        
        .confidence-badge {
            margin-left: 0;
            align-self: flex-start;
        }
        
        .stats-container {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

def display_header():
    """Display beautiful, modern header"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🎯 Filum.ai Solution Finder</h1>
        <p class="header-subtitle">Powered by AI • Find the perfect technology solutions for your business challenges</p>
    </div>
    """, unsafe_allow_html=True)

def get_confidence_info(confidence: float) -> tuple:
    """Get confidence badge info"""
    if confidence >= 0.7:
        return "confidence-high", "High Match", ""
    elif confidence >= 0.4:
        return "confidence-medium", "Medium Match", "" 
    else:
        return "confidence-low", "Possible Match", ""

def render_score_visualization(solution: Dict[str, Any]):
    """Render beautiful score breakdown visualization"""
    layer_breakdown = solution.get("layer_breakdown", {})
    matched_keywords = solution.get("matched_keywords", [])
    
    if not layer_breakdown:
        return
    
    # Score mapping with icons and colors
    score_config = {
        "exact_match": {"label": "🎯 Exact Match", "color": "#10b981"},
        "fuzzy_match": {"label": "🔍 Fuzzy Match", "color": "#3b82f6"}, 
        "semantic_match": {"label": "🧠 Semantic Match", "color": "#8b5cf6"},
        "domain_match": {"label": "🏢 Domain Match", "color": "#f59e0b"},
        "intent_match": {"label": "💭 Intent Match", "color": "#ef4444"}
    }
    
    st.markdown("""
    <div class="score-section">
        <div class="score-title">📊 Matching Score Breakdown</div>
    """, unsafe_allow_html=True)
    
    # Render each score
    for score_key, config in score_config.items():
        score_value = layer_breakdown.get(score_key, 0.0)
        percentage = score_value * 100
        
        st.markdown(f"""
        <div class="score-item">
            <div class="score-label">{config['label']}</div>
            <div class="score-bar-container">
                <div class="score-bar" style="width: {percentage}%; background: {config['color']};"></div>
            </div>
            <div class="score-value">{percentage:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Keywords section
    if matched_keywords:
        st.markdown('<div class="keywords-section">', unsafe_allow_html=True)
        st.markdown("**🔑 Matched Keywords:**")
        for keyword in matched_keywords:
            st.markdown(f'<span class="keyword-tag">{keyword}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_solution_card(solution: Dict[str, Any], index: int):
    """Display solution card with clear info hierarchy"""
    
    # Debug: Check what data we have
    feature = solution.get("feature", {})
    confidence = solution.get("confidence_score", 0.0)
    
    # Get clear solution info with fallbacks
    solution_name = feature.get('name') or solution.get('solution_name') or f"Solution #{index + 1}"
    category = feature.get("category") or solution.get("category") or "Uncategorized"
    subcategory = feature.get("subcategory") or solution.get("subcategory") or ""
    description = feature.get("description") or solution.get("description") or ""
    
    # Get confidence info
    confidence_class, confidence_label, confidence_icon = get_confidence_info(confidence)
    
    # 🎯 SECTION 1: Solution Header & Basic Info (HTML STYLED)
    st.markdown(f"""
    <div class="solution-card">
        <div class="solution-header">
            <h2 style="color: #1e293b; font-size: 1.8rem; font-weight: 700; margin: 0; line-height: 1.3;">
                {confidence_icon} {solution_name}
            </h2>
            <div class="confidence-badge {confidence_class}">
                {confidence_label}<br>
                <small>{confidence:.0%}</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🏷️ SECTION 2: Category Information (HTML STYLED)
    st.markdown("### 📂 Solution Category")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; padding: 1rem; border-radius: 15px; text-align: center; margin: 0.5rem 0;">
            <div style="font-size: 1.1rem; font-weight: 600;">📂 {category}</div>
            {f'<div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">📋 {subcategory}</div>' if subcategory else ''}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if description:
            st.markdown("**📝 Description:**")
            st.write(description)
        else:
            st.warning("Description not available")
    
    # 🎯 SECTION 3: Pain Points & Solution (SIMPLE & CLEAR VERSION)
    pain_points = feature.get("pain_points_addressed", [])
    if pain_points:
        st.markdown("### 🎯 Pain Points This Solves")
        
        # Create formatted pain points with better spacing
        pain_points_formatted = []
        for pain_point in pain_points:
            pain_points_formatted.append(f"• **{pain_point.capitalize()}**")
        
        pain_points_text = "\n\n".join(pain_points_formatted)  # Double line break for better spacing
        
        # Use info box with markdown formatting for white background
        st.info(f"""**🔴 Pain Points:**

{pain_points_text}

---

**✅ Filum.ai Solution:**  
**{solution_name}**

**📂 Category:** {category}{f" - {subcategory}" if subcategory else ""}

**💡 How it helps:**  
{description if description else "Provides comprehensive solution for these business challenges"}
        """)
    
    # 📊 SECTION 4: Matching Score Breakdown (MOVED TO BOTTOM)
    st.markdown("### 📊 AI Matching Analysis")
    with st.expander("🔍 View Detailed Matching Scores", expanded=False):
        render_score_visualization(solution)
    
    # Implementation info (KEEP ONLY THIS)
    how_it_helps = solution.get("how_it_helps", "")
    implementation = solution.get("implementation_suggestion", "")
    
    if how_it_helps or implementation:
        with st.expander("🚀 Implementation Details"):
            if how_it_helps:
                st.markdown(f"**💡 How this helps:** {how_it_helps}")
            if implementation:
                st.markdown(f"**🛠️ Implementation suggestion:** {implementation}")

def display_examples_sidebar():
    """Display example pain points in sidebar"""
    st.sidebar.markdown("### 💡 Example Business Challenges")
    st.sidebar.markdown("*Click any example to try it*")
    
    examples = [
        {
            "title": "📊 Customer Feedback Collection", 
            "pain_point": "It's difficult to collect customer feedback consistently after purchases across multiple channels like web, mobile, and in-store.",
            "expected": "→ Automated Post-Purchase Surveys (Voice of Customer - Surveys)"
        },
        {
            "title": "👥 Customer Profile Management",
            "pain_point": "It's difficult to get a single view of a customer's interaction history when they contact us.",
            "expected": "→ Customer Profile with Interaction History (Customer 360 - Customers)"
        },
        {
            "title": "🔍 Survey Analysis",
            "pain_point": "Manually analyzing thousands of open-ended survey responses for common themes is too time-consuming.",
            "expected": "→ AI-Powered Topic & Sentiment Analysis (VoC - Insights)"
        },
        {
            "title": "📞 Customer Service Automation",
            "pain_point": "Customer service team is overwhelmed with repetitive questions and needs automation to handle common inquiries.",
            "expected": "→ AI Inbox FAQ Management (AI Inbox - FAQ)"
        },
        {
            "title": "📈 Business Performance Tracking",
            "pain_point": "We need better insights into our operational performance and customer satisfaction metrics.",
            "expected": "→ Operational Performance Analytics (Insights - Performance)"
        }
    ]
    
    for example in examples:
        with st.sidebar.container():
            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; cursor: pointer; transition: all 0.2s ease;">
                <div style="font-weight: 600; color: #4f46e5; margin-bottom: 0.5rem; font-size: 0.9rem;">{example['title']}</div>
                <div style="font-size: 0.8rem; color: #64748b; line-height: 1.4; margin-bottom: 0.5rem;">{example['pain_point'][:80]}...</div>
                <div style="font-size: 0.75rem; color: #059669; font-style: italic;">{example['expected']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.sidebar.button(
                "Try This Example", 
                key=f"example_{hash(example['pain_point'])}", 
                use_container_width=True
            ):
                st.session_state.pain_point_input = example['pain_point']
                st.rerun()

def display_loading():
    """Display loading animation"""
    st.markdown("""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <p>🔍 Analyzing and finding suitable solutions...</p>
    </div>
    """, unsafe_allow_html=True)

def display_stats(solutions: List[Dict[str, Any]]):
    """Display analysis stats"""
    if not solutions:
        return
    
    # Calculate stats
    total_solutions = len(solutions)
    avg_confidence = sum(s.get("confidence_score", 0) for s in solutions) / total_solutions
    categories = set(s.get("category", "") for s in solutions if s.get("category"))
    high_confidence = sum(1 for s in solutions if s.get("confidence_score", 0) >= 0.7)
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box">
            <p class="stat-number">{total_solutions}</p>
            <p class="stat-label">Solutions Found</p>
        </div>
        <div class="stat-box">
            <p class="stat-number">{avg_confidence:.0%}</p>
            <p class="stat-label">Average Match</p>
        </div>
        <div class="stat-box">
            <p class="stat-number">{len(categories)}</p>
            <p class="stat-label">Product Categories</p>
        </div>
        <div class="stat-box">
            <p class="stat-number">{high_confidence}</p>
            <p class="stat-label">High Confidence</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def analyze_pain_point(pain_point: str) -> Dict[str, Any]:
    """Analyze pain point using agent or API"""
    if USE_AGENT:
        return agent.analyze_pain_point(pain_point)
    else:
        # Fallback to API
        try:
            response = requests.post(
                "http://localhost:8000/analyze-pain-point",
                json={"description": pain_point},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "status": "error",
                "message": f"API Connection Error: {str(e)}",
                "solutions": []
            }

def main():
    """Main app function"""
    display_header()
    
    # Sidebar
    display_examples_sidebar()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ How to Use")
    st.sidebar.markdown("""
    1. **Describe Challenge**: Enter your business problem
    2. **Get Solutions**: System will find matching Filum.ai features  
    3. **View Details**: Click on each solution to learn more
    4. **Contact**: Click button for specific consultation
    """)
    
    # Initialize session state
    if 'pain_point_input' not in st.session_state:
        st.session_state.pain_point_input = ""
    
    # Input section with beautiful styling
    st.markdown("""
    <div class="input-section">
        <div class="input-title">
            📝 Describe Your Business Challenge
        </div>
        <p style="color: #64748b; margin-bottom: 1.5rem; font-size: 0.95rem;">
            Tell us about your business problem and we'll find the perfect Filum.ai solution for you.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input with better styling
    pain_point = st.text_area(
        "Challenge description:",
        value=st.session_state.pain_point_input,
        placeholder="Example: We are struggling to collect and analyze customer feedback efficiently. Our current process is manual and takes too much time...",
        height=120,
        key="pain_point_main",
        label_visibility="collapsed",
        help="Be specific about your challenge - the more detail you provide, the better our recommendations will be!"
    )
    
    # Action buttons with better layout
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        analyze_button = st.button(
            "🔍 Find Perfect Solutions", 
            type="primary",
            use_container_width=True,
            help="Analyze your challenge and find matching solutions"
        )
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
        
    with col3:
        if st.button("� Examples", use_container_width=True):
            st.info("Check the sidebar for example challenges you can try!")
            
    with col4:
        if st.button("�📞 Consult", use_container_width=True):
            st.success("📞 **Contact Us:**\n\n📧 Email: contact@filum.ai\n📱 Phone: 1900-XXX-XXX")
    
    if clear_button:
        st.session_state.pain_point_input = ""
        st.rerun()
    
    # Analysis with improved UX
    if analyze_button and pain_point.strip():
        with st.spinner("🔍 Analyzing your challenge and finding the best solutions..."):
            display_loading()
            time.sleep(1.5)  # Simulate processing time
            
            result = analyze_pain_point(pain_point.strip())
            
            if result.get("status") == "success":
                solutions = result.get("solutions", [])
                
                if solutions:
                    st.success(f"✅ **Great news!** Found {len(solutions)} perfect solution{'' if len(solutions) == 1 else 's'} for your challenge!")
                    
                    # Display stats
                    display_stats(solutions)
                    
                    st.markdown("### 🎯 Recommended Solutions")
                    st.markdown("*Solutions are ranked by relevance to your specific challenge*")
                    
                    # Display solutions
                    for i, solution in enumerate(solutions):
                        display_solution_card(solution, i)
                        
                        if i < len(solutions) - 1:  # Add separator except for last item
                            st.markdown("---")
                
                else:
                    st.warning("🤔 **No exact matches found.** Try describing your challenge in more detail or contact our team for personalized consultation.")
                    
                    # Suggest what to do next
                    st.markdown("""
                    **💡 Tips for better results:**
                    - Be more specific about your industry or use case
                    - Mention the scale of your problem (small team vs enterprise)
                    - Include what you've tried before
                    - Describe the impact on your business
                    """)
            
            else:
                st.error(f"❌ {result.get('message', 'An error occurred')}")
    
    elif analyze_button:
        st.warning("⚠️ Please enter a challenge description before finding solutions.")

if __name__ == "__main__":
    main()
