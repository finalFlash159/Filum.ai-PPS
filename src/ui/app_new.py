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
        <p class="header-subtitle">Tìm giải pháp công nghệ phù hợp cho thách thức kinh doanh của bạn</p>
    </div>
    """, unsafe_allow_html=True)

def get_confidence_info(confidence: float) -> tuple:
    """Get confidence badge info"""
    if confidence >= 0.7:
        return "confidence-high", "Khớp cao", "🎯"
    elif confidence >= 0.4:
        return "confidence-medium", "Khớp vừa", "🎲" 
    else:
        return "confidence-low", "Có thể khớp", "🤔"

def display_solution_card(solution: Dict[str, Any], index: int):
    """Display clean solution card"""
    feature = solution.get("feature", {})
    confidence = solution.get("confidence_score", 0.0)
    
    # Get solution name
    solution_name = (solution.get('solution_name') or 
                    feature.get('name') or 
                    'Giải pháp chưa xác định')
    
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
        
        <div class="category-tags">
            {f'<span class="category-tag">📂 {category}</span>' if category else ''}
            {f'<span class="category-tag">📋 {subcategory}</span>' if subcategory else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Content in expandable sections
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # How it helps
        how_it_helps = solution.get("how_it_helps", "")
        if how_it_helps:
            st.markdown(f"""
            <div class="help-section">
                <div class="help-title">💡 Giải pháp này giúp gì?</div>
                <p>{how_it_helps}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Description
        description = feature.get("description", "")
        if description:
            with st.expander("📖 Chi tiết tính năng"):
                st.write(description)
    
    with col2:
        # Implementation suggestion
        implementation = solution.get("implementation_suggestion", "")
        if implementation:
            st.markdown(f"""
            <div class="help-section">
                <div class="help-title">🚀 Triển khai</div>
                <p><small>{implementation}</small></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Benefits
        benefits = feature.get("benefits", [])
        if benefits:
            with st.expander("✅ Lợi ích"):
                for benefit in benefits[:4]:
                    st.write(f"• {benefit}")

def display_examples_sidebar():
    """Display example pain points in sidebar"""
    st.sidebar.markdown("### 💡 Ví dụ thách thức phổ biến")
    
    examples = [
        "Khách hàng phàn nàn nhiều nhưng không biết cách thu thập phản hồi",
        "Đội ngũ chăm sóc khách hàng quá tải, cần tự động hóa",
        "Muốn hiểu rõ hơn về hành vi và nhu cầu khách hàng",
        "Cần báo cáo và phân tích dữ liệu khách hàng chi tiết",
        "Quy trình xử lý khiếu nại còn thủ công, chậm chạp"
    ]
    
    for example in examples:
        if st.sidebar.button(
            example, 
            key=f"example_{hash(example)}", 
            help="Click để thử ví dụ này"
        ):
            st.session_state.pain_point_input = example
            st.rerun()

def display_loading():
    """Display loading animation"""
    st.markdown("""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <p>🔍 Đang phân tích và tìm giải pháp phù hợp...</p>
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
            <p class="stat-label">Giải pháp tìm thấy</p>
        </div>
        <div class="stat-box">
            <p class="stat-number">{avg_confidence:.0%}</p>
            <p class="stat-label">Độ khớp trung bình</p>
        </div>
        <div class="stat-box">
            <p class="stat-number">{len(categories)}</p>
            <p class="stat-label">Danh mục sản phẩm</p>
        </div>
        <div class="stat-box">
            <p class="stat-number">{high_confidence}</p>
            <p class="stat-label">Khớp độ cao</p>
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
                "message": f"Lỗi kết nối API: {str(e)}",
                "solutions": []
            }

def main():
    """Main app function"""
    display_header()
    
    # Sidebar
    display_examples_sidebar()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Hướng dẫn sử dụng")
    st.sidebar.markdown("""
    1. **Mô tả thách thức**: Nhập vấn đề kinh doanh bạn đang gặp
    2. **Nhận giải pháp**: Hệ thống sẽ tìm tính năng Filum.ai phù hợp  
    3. **Xem chi tiết**: Click vào từng giải pháp để hiểu rõ hơn
    4. **Liên hệ**: Nhấn nút để được tư vấn cụ thể
    """)
    
    # Initialize session state
    if 'pain_point_input' not in st.session_state:
        st.session_state.pain_point_input = ""
    
    # Input section
    st.markdown("""
    <div class="input-section">
        <div class="input-title">
            📝 Mô tả thách thức kinh doanh của bạn
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input
    pain_point = st.text_area(
        "",
        value=st.session_state.pain_point_input,
        placeholder="Ví dụ: Chúng tôi đang gặp khó khăn trong việc thu thập và phân tích phản hồi từ khách hàng sau khi mua hàng...",
        height=100,
        key="pain_point_main"
    )
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        analyze_button = st.button(
            "🔍 Tìm giải pháp", 
            type="primary",
            use_container_width=True
        )
    
    with col2:
        clear_button = st.button("🗑️ Xóa", use_container_width=True)
        
    with col3:
        if st.button("📞 Tư vấn", use_container_width=True):
            st.info("📞 Liên hệ: 1900-XXX-XXX hoặc email: contact@filum.ai")
    
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
                    st.success(f"✅ Tìm thấy {len(solutions)} giải pháp phù hợp!")
                    
                    # Display stats
                    display_stats(solutions)
                    
                    st.markdown("### 🎯 Giải pháp được đề xuất")
                    
                    # Display solutions
                    for i, solution in enumerate(solutions):
                        display_solution_card(solution, i)
                        
                        if i < len(solutions) - 1:  # Add separator except for last item
                            st.markdown("---")
                
                else:
                    st.warning("🤔 Không tìm thấy giải pháp phù hợp. Hãy thử mô tả chi tiết hơn hoặc liên hệ tư vấn.")
            
            else:
                st.error(f"❌ {result.get('message', 'Có lỗi xảy ra')}")
    
    elif analyze_button:
        st.warning("⚠️ Vui lòng nhập mô tả thách thức trước khi tìm giải pháp.")

if __name__ == "__main__":
    main()
