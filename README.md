# 🎯 Filum.ai Pain Point Solution Agent

Hệ thống AI chuyên biệt để phân tích business pain points và gợi ý giải pháp từ nền tảng Filum.ai. Agent này sử dụng thuật toán text matching tiên tiến để kết nối các vấn đề kinh doanh với các tính năng của Filum.ai platform.

### **🎯 Core Objectives:**
- **🧠 Smart Pain Point Analysis**: Deep understanding using NLP and semantic AI
- **🔍 Advanced Matching**: Fuzzy logic + semantic similarity + business domain knowledge
- **💡 Intelligent Recommendations**: High-confidence suggestions with detailed reasoning
- **📊 Implementation Guidance**: Comprehensive insights and next steps

### **🏢 About Filum.ai**
Filum.ai is a Generative AI-powered Customer Experience and Service Platform with 5 core product categories:

- **🎤 Voice of Customer (VoC)**: Customer feedback collection and analysis
- **🤖 AI Customer Service**: AI-powered support and automation  
- **📊 Insights**: Customer data analytics and intelligence
- **👤 Customer 360**: Comprehensive customer management and engagement
- **⚡ AI & Automation**: AI model configuration and workflow automation

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.9+
- pip or conda
- Git

### **Installation & Setup**

1. **Clone repository**
```bash
git clone https://github.com/finalFlash159/pain-point-solution.git
cd pain-point-solution
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn streamlit plotly pandas
pip install fuzzywuzzy python-levenshtein sentence-transformers nltk
```

4. **Run the Advanced System**
```bash
# Start API Server (Terminal 1)
python -m uvicorn src.api.main:app --reload --port 8000

# Start Streamlit Interface (Terminal 2)  
streamlit run streamlit_app_advanced.py --server.port 8501
```

5. **Access the Application**
- **API**: http://localhost:8000 (with auto-docs at /docs)
- **UI**: http://localhost:8501 (Interactive interface)
- **Health**: http://localhost:8000/health (System status)

---

## 🧠 **Advanced Features**

### **🔍 Multi-Layer Matching Engine**
- **Fuzzy Matching**: 70% threshold for typo tolerance using FuzzyWuzzy
- **Semantic Similarity**: AI understanding via Sentence Transformers
- **Business Synonyms**: 20+ domain-specific expansions (customer→client, etc.)
- **Token Overlap**: Smart keyword matching with NLTK processing
- **Weighted Scoring**: Optimal combination of all similarity metrics

### **📊 Intelligence & Analytics**
- **Confidence Levels**: High/Medium/Low with detailed reasoning
- **Visual Breakdowns**: Plotly radar charts for similarity analysis
- **Processing Stats**: Real-time keyword extraction and expansion
- **Performance Monitoring**: Response time and accuracy tracking

### **🌐 API Capabilities**
- **7 REST Endpoints**: Complete CRUD + advanced search
- **Auto-Documentation**: Swagger/OpenAPI integration
- **CORS Enabled**: Cross-origin support for web integration
- **Error Handling**: Comprehensive error messages and logging

---

## 📁 **Project Structure**

```
pain-point-solution/
├── 📄 README.md                           # Project documentation
├── 📄 streamlit_app_advanced.py           # Advanced UI interface
├── � src/
│   ├── 📂 agent/                          # Core AI Engine
│   │   ├── core_engine.py                # Main orchestration
│   │   ├── advanced_matching_engine.py   # Multi-layer matching
│   │   ├── advanced_text_processing.py   # NLP & semantic processing
│   │   ├── matcher.py                    # Legacy matching (backup)
│   │   └── text_processing.py           # Basic processing (backup)
│   ├── � api/                           # FastAPI REST API
│   │   └── main.py                       # API endpoints & middleware
│   ├── 📂 models/                        # Data & Knowledge Base
│   │   ├── filum_knowledge_base.json     # 15 Filum.ai features
│   │   ├── knowledge_base_config.json    # Configuration
│   │   └── schemas.py                    # Pydantic models
│   └── 📂 utils/                         # Utilities
│       └── logger.py                     # Logging configuration
│   │   ├── scorer.py                # Tính điểm relevance
│   │   ├── response_generator.py    # Tạo response
│   │   └── processor.py             # Xử lý input
│   ├── 📂 models/                    # Data models & Knowledge Base
│   │   ├── filum_knowledge_base.json # Knowledge base chính
│   │   ├── knowledge_base_config.json # Configuration
│   │   ├── schemas.py               # Pydantic models
│   │   └── knowledge_loader.py      # Load knowledge base
│   ├── 📂 utils/                     # Utilities
│   │   ├── text_processing.py       # Text processing
│   │   ├── similarity.py            # Similarity calculations
│   │   ├── validation.py            # Input validation
│   │   └── logger.py                # Logging
│   ├── 📂 api/                       # REST API
│   │   ├── main.py                  # FastAPI app
│   │   ├── endpoints.py             # API endpoints
│   │   └── middleware.py            # Middleware
│   └── 📂 demo/                      # Demo interface
│       └── streamlit_app.py         # Streamlit demo
├── 📂 tests/                         # Test suite
├── 📂 data/                          # Sample data
└── 📂 docs/                          # Documentation
```

---

## 🔧 **Core Features**

### **1. Multi-Dimensional Matching**
- **Keyword Matching**: Exact + fuzzy keyword matching với synonym expansion
- **Semantic Similarity**: Sử dụng sentence transformers cho deep understanding
- **Category Classification**: AI-powered pain point categorization
- **Use Case Matching**: So sánh với documented use cases
- **Business Value Alignment**: Đánh giá alignment với business objectives

### **2. Intelligent Scoring**
- **Weighted Scoring**: Multi-factor scoring với configurable weights
- **Confidence Calculation**: Độ tin cậy dựa trên score distribution
- **Threshold-based Classification**: High/Medium/Low confidence levels
- **Ranking Algorithm**: Smart ranking based on relevance và context

### **3. Rich Knowledge Base**
- **15 Filum.ai Features**: Comprehensive coverage của tất cả capabilities
- **Detailed Metadata**: Implementation complexity, pricing, integrations
- **Use Case Examples**: Real-world scenarios và applications
- **Business Context**: Industry-specific information và considerations

### **4. Professional API**
- **RESTful Design**: Clean, well-documented API endpoints
- **Input Validation**: Comprehensive validation và sanitization
- **Error Handling**: Proper error responses và status codes
- **Rate Limiting**: Protection against abuse
- **Monitoring**: Performance metrics và logging

---

## 🔍 **Usage Examples**

### **API Usage**

```python
import requests

# Example pain point
pain_point = {
    "description": "We're struggling to collect customer feedback consistently after a purchase",
    "context": {
        "industry": "retail",
        "company_size": "medium"
    },
    "urgency": "high"
}

# Get recommendations
response = requests.post(
    "http://localhost:8000/api/v1/solutions/recommend",
    json=pain_point
)

recommendations = response.json()
print(f"Found {len(recommendations['recommendations'])} solutions")

for rec in recommendations['recommendations']:
    print(f"- {rec['feature_name']}: {rec['confidence_score']:.2f}")
```

### **Expected Output**
```json
{
  "recommendations": [
    {
      "feature_id": "voc_surveys",
      "feature_name": "Multi-Channel Survey Platform",
      "confidence_score": 0.92,
      "relevance_explanation": "Perfect match for post-purchase feedback collection with automated deployment across multiple channels",
      "key_capabilities": [
        "Multi-channel survey deployment",
        "Automated survey triggers",
        "Real-time response analytics"
      ],
      "business_value": "Increased feedback collection rates and better customer insights",
      "implementation_info": {
        "complexity": "low",
        "time_to_value": "1-2 weeks",
        "pricing_tier": "basic"
      },
      "next_steps": [
        "Schedule a demo of the survey platform",
        "Identify key post-purchase touchpoints",
        "Design your first automated survey"
      ]
    }
  ],
  "total_matches": 3,
  "processing_time_ms": 245,
  "confidence_summary": {
    "high": 1,
    "medium": 2,
    "low": 0
  }
}
```

---

## 🧪 **Testing**

### **Run Tests**
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test category
pytest tests/test_agent/
pytest tests/test_api/
```

### **Test Coverage Goals**
- **Unit Tests**: > 90% coverage
- **Integration Tests**: Core workflows
- **Performance Tests**: Response time < 2s
- **API Tests**: All endpoints

---

## 📊 **Performance Specifications**

| Metric | Target | Maximum |
|--------|--------|---------|
| Response Time | < 1.5s | < 3.0s |
| Throughput | 50 req/s | 25 req/s |
| Memory Usage | < 512MB | < 1GB |
| Accuracy | > 85% | > 75% |
| Uptime | > 99.5% | > 99% |

---

## 🚀 **Deployment**

### **Docker Deployment**
```bash
# Build image
docker build -t pain-point-agent .

# Run container
docker run -p 8000:8000 pain-point-agent

# Docker Compose (with Redis)
docker-compose up -d
```

### **Production Considerations**
- **Load Balancing**: Nginx hoặc HAProxy
- **Caching**: Redis cho performance optimization
- **Monitoring**: Prometheus + Grafana
- **Logging**: Centralized logging với ELK stack
- **Security**: HTTPS, input validation, rate limiting

---

## 📖 **Documentation**

### **Available Documentation**
- **[Development Plan](PROJECT_DEVELOPMENT_PLAN.md)**: Chi tiết kế hoạch phát triển 4-6 tuần
- **[Technical Specification](TECHNICAL_SPECIFICATION.md)**: Architecture và implementation details
- **API Documentation**: Swagger UI tại `/docs` khi chạy server
- **Usage Guide**: Examples và best practices (coming soon)

### **Knowledge Base**
- **[Filum Knowledge Base](src/models/filum_knowledge_base.json)**: 15 features với metadata chi tiết
- **[Configuration](src/models/knowledge_base_config.json)**: Matching rules và examples

---

## 🤝 **Contributing**

### **Development Workflow**
1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

### **Code Standards**
- **Formatting**: Black
- **Linting**: Flake8
- **Type Hints**: mypy
- **Testing**: pytest với > 90% coverage
- **Documentation**: Comprehensive docstrings

---

## 📝 **License**

Dự án này được phát triển cho Filum.ai assessment. Vui lòng tham khảo licensing terms trước khi sử dụng.

---

## 👥 **Contact & Support**

- **Developer**: [Your Name]
- **Email**: [your.email@example.com]
- **GitHub**: [@finalFlash159](https://github.com/finalFlash159)

### **Getting Help**
- **Issues**: Sử dụng GitHub Issues cho bug reports
- **Discussions**: GitHub Discussions cho questions
- **Documentation**: Check `/docs` endpoint khi server running

---

## 🎯 **Roadmap**

### **Phase 1: Core Implementation** ✅
- [x] Knowledge Base design
- [x] Project structure
- [x] Development plan
- [ ] Core matching engine
- [ ] API development
- [ ] Basic testing

### **Phase 2: Advanced Features** 🚧
- [ ] Machine learning improvements
- [ ] Advanced analytics
- [ ] Performance optimization
- [ ] Comprehensive testing

### **Phase 3: Production Ready** 📋
- [ ] Security hardening
- [ ] Monitoring & alerting
- [ ] Documentation completion
- [ ] Deployment automation

---

**🚀 Ready to transform customer pain points into actionable solutions with AI-powered intelligence!**