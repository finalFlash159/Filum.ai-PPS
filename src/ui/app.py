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
    from agent.engine import get_filum_agent
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

# Clean, modern CSS
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Input section */
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e6ed;
        margin-bottom: 2rem;
    }
    
    .input-title {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Solution cards */
    .solution-card {
        background: white;
        border: 1px solid #e0e6ed;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .solution-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-color: #667eea;
    }
    
    .solution-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .solution-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0;
        flex: 1;
    }
    
    .confidence-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
        min-width: 90px;
        margin-left: 1rem;
    }
    
    .confidence-high {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
    }
    
    .confidence-medium {
        background: linear-gradient(135deg, #FF9800, #f57c00);
        color: white;
    }
    
    .confidence-low {
        background: linear-gradient(135deg, #9E9E9E, #757575);
        color: white;
    }
    
    .category-tags {
        margin: 0.5rem 0;
    }
    
    .category-tag {
        background: #f8f9fa;
        color: #495057;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        display: inline-block;
        border: 1px solid #dee2e6;
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
    """Display clean, modern header"""
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🎯 Filum.ai Solution Finder</h1>
        <p class="header-subtitle">Find the right technology solutions for your business challenges</p>
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

def display_solution_card(solution: Dict[str, Any], index: int):
    """Display clean solution card"""
    feature = solution.get("feature", {})
    confidence = solution.get("confidence_score", 0.0)
    
    # Get solution name
    solution_name = (solution.get('solution_name') or 
                    feature.get('name') or 
                    'Unknown Solution')
    
    # Get confidence info
    confidence_class, confidence_label, confidence_icon = get_confidence_info(confidence)
    
    # Categories
    category = solution.get("category") or feature.get("category", "")
    subcategory = solution.get("subcategory") or feature.get("subcategory", "")
    
    # Card HTML
    st.markdown(f"""
    <div class="solution-card">
        <div class="solution-header">
            <h3 class="solution-title">{confidence_icon} {solution_name}</h3>
            <div class="confidence-badge {confidence_class}">
                {confidence_label}<br>
                <small>{confidence:.0%}</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display category tags using simple text
    if category or subcategory:
        tags = []
        if category:
            tags.append(f"📂 {category}")
        if subcategory:
            tags.append(f"📋 {subcategory}")
        st.caption(" • ".join(tags))
    
    # Content in expandable sections
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # How it helps
        how_it_helps = solution.get("how_it_helps", "")
        if how_it_helps:
            st.markdown(f"""
            <div class="help-section">
                <div class="help-title">💡 How this helps</div>
                <p>{how_it_helps}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Debug: show what data we have
            st.write("**Available data:**")
            st.json({k: v for k, v in solution.items() if k not in ['feature']})
        
        # Description
        description = feature.get("description", "")
        if description:
            with st.expander("📖 Feature Details"):
                st.write(description)
    
    with col2:
        # Implementation suggestion
        implementation = solution.get("implementation_suggestion", "")
        if implementation:
            st.markdown(f"""
            <div class="help-section">
                <div class="help-title">🚀 Implementation</div>
                <p><small>{implementation}</small></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Benefits
        benefits = feature.get("benefits", [])
        if benefits:
            with st.expander("✅ Benefits"):
                for benefit in benefits[:4]:
                    st.write(f"• {benefit}")
    
    # Close the solution card
    st.markdown("</div>", unsafe_allow_html=True)

def display_examples_sidebar():
    """Display example pain points in sidebar"""
    st.sidebar.markdown("### 💡 Common Business Challenges")
    
    examples = [
        "Customers complain frequently but we don't know how to collect feedback",
        "Customer service team is overwhelmed, need automation",
        "Want to better understand customer behavior and needs",
        "Need detailed customer data reports and analytics",
        "Manual complaint handling process is slow and inefficient"
    ]
    
    for example in examples:
        if st.sidebar.button(
            example, 
            key=f"example_{hash(example)}", 
            help="Click to try this example"
        ):
            st.session_state.pain_point_input = example
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
    
    # Input section
    st.markdown("""
    <div class="input-section">
        <div class="input-title">
            📝 Describe your business challenge
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input
    pain_point = st.text_area(
        "Challenge description:",
        value=st.session_state.pain_point_input,
        placeholder="Example: We are struggling to collect and analyze customer feedback after purchases...",
        height=100,
        key="pain_point_main",
        label_visibility="collapsed"
    )
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analyze_button = st.button(
            "🔍 Find Solutions", 
            type="primary",
            use_container_width=True
        )
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
        
    with col3:
        if st.button("📞 Consult", use_container_width=True):
            st.info("📞 Contact: 1900-XXX-XXX or email: contact@filum.ai")
    
    if clear_button:
        st.session_state.pain_point_input = ""
        st.rerun()
    
    # Analysis
    if analyze_button and pain_point.strip():
        with st.spinner(""):
            display_loading()
            time.sleep(1)  # Simulate processing time
            
            result = analyze_pain_point(pain_point.strip())
            
            if result.get("status") == "success":
                solutions = result.get("solutions", [])
                
                if solutions:
                    st.success(f"✅ Found {len(solutions)} suitable solutions!")
                    
                    # Display stats
                    display_stats(solutions)
                    
                    st.markdown("### 🎯 Recommended Solutions")
                    
                    # Display solutions
                    for i, solution in enumerate(solutions):
                        display_solution_card(solution, i)
                        
                        if i < len(solutions) - 1:  # Add separator except for last item
                            st.markdown("---")
                
                else:
                    st.warning("🤔 No suitable solutions found. Try describing in more detail or contact for consultation.")
            
            else:
                st.error(f"❌ {result.get('message', 'An error occurred')}")
    
    elif analyze_button:
        st.warning("⚠️ Please enter a challenge description before finding solutions.")

if __name__ == "__main__":
    main()
