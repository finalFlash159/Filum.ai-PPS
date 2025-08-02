# Enhanced Filum.ai Matching System

## 🚀 Overview

Enhanced 5-layer matching system với semantic embeddings cho Filum.ai Pain Point Solution Agent.

## 🏗️ Architecture

### 5-Layer Matching System:
1. **Exact Match (20%)** - Exact keyword overlap
2. **Fuzzy Match (25%)** - Fuzzy keyword similarity  
3. **Semantic Match (35%)** - AI-based semantic similarity ⭐
4. **Domain Match (15%)** - Business domain relevance
5. **Intent Match (5%)** - Pain point intent alignment

### Pre-computed Embeddings:
- **4 trường được embedding**: `description`, `pain_points_addressed`, `keywords`, `use_cases`
- **Model**: `all-MiniLM-L6-v2` (384 dimensions)
- **Cache**: Pre-computed embeddings lưu trong `data/filum_embeddings.pkl`

## 📦 Installation

### 1. Install dependencies:
```bash
pip install -r requirements_enhanced.txt
```

### 2. Build embeddings cache:
```bash
python scripts/build.py
```

### 3. Test system:
```bash
python scripts/test.py
```

## 🔧 Usage

### Basic Usage:
```python
from src.agent import FilumAgent

# Initialize with enhanced matching
agent = FilumAgent(use_enhanced_matching=True)

# Analyze pain point
result = agent.analyze_pain_point(
    "We struggle with collecting customer feedback after purchases"
)

print(f"Found {len(result['solutions'])} solutions")
for solution in result['solutions']:
    print(f"- {solution['solution_name']} ({solution['confidence_score']:.3f})")
```

### Advanced Usage:
```python
from src.matching import EnhancedFilumMatcher

# Direct matcher usage
matcher = EnhancedFilumMatcher("data/filum_knowledge_base.json")

# Get detailed match results
matches = matcher.find_matches("customer feedback collection", max_results=3)

for match in matches:
    print(f"Feature: {match.feature_name}")
    print(f"Confidence: {match.confidence_score:.3f}")
    print(f"Layer Breakdown: {match.layer_scores}")
    print(f"Reasoning: {match.reasoning}")
```

## 📁 File Structure

```
src/
├── agent/                  # Main business logic
│   ├── agent.py           # Main FilumAgent
│   └── engine.py          # Solution engine
├── matching/              # Matching algorithms  
│   ├── enhanced.py        # 5-layer matching
│   └── basic.py           # Basic fallback
├── processing/            # Text processing
│   └── processor.py       # Text analysis & NLP
├── embeddings/            # Semantic embeddings
│   └── manager.py         # Embedding management
├── api/                   # REST API
│   └── main.py           # FastAPI server
└── ui/                    # User interface
    └── app.py            # Streamlit app

scripts/
├── build.py              # Build embeddings
└── test.py               # Test system

data/
├── filum_knowledge_base.json
├── filum_embeddings.pkl
└── filum_embeddings.json
```

## 🎯 Performance

### Accuracy Improvements:
- **Semantic Understanding**: 35% weight - handles synonyms, context
- **Intent Recognition**: Better pain point matching
- **Multi-layer Validation**: Reduces false positives
- **Business Context**: Domain-aware matching

### Speed:
- **Cold start**: ~2-3 seconds (model loading)
- **Query processing**: ~50-100ms
- **Pre-computed embeddings**: No embedding calculation during inference

## 🔄 Workflow

### 1. Pre-processing (One-time):
```bash
# Build embeddings for all features
python scripts/build.py
```

### 2. Runtime (Per query):
```
User Query → Process Query → Create Query Embedding → 
5-Layer Scoring → Weighted Combination → Ranked Results
```

### 3. Maintenance:
```bash
# Update embeddings when knowledge base changes
python scripts/build.py --force
```

## 🎛️ Configuration

### Layer Weights (in matching/enhanced.py):
```python
layer_weights = {
    'exact_match': 0.20,
    'fuzzy_match': 0.25,
    'semantic_match': 0.35,  # Highest weight
    'domain_match': 0.15,
    'intent_match': 0.05
}
```

### Confidence Thresholds:
```python
confidence_thresholds = {
    'high': 0.65,    # Strong match
    'medium': 0.40,  # Moderate match  
    'low': 0.20      # Weak but relevant
}
```

## 🐛 Troubleshooting

### Common Issues:

1. **ImportError: sentence_transformers**
   ```bash
   pip install sentence-transformers
   ```

2. **No embeddings found**
   ```bash
   python scripts/build.py
   ```

3. **Slow first query**
   - Normal behavior (model loading)
   - Subsequent queries will be fast

4. **Low quality matches**
   - Check if embeddings cache exists
   - Try rebuilding embeddings
   - Adjust layer weights if needed

## 🔍 Debugging

### Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check system stats:
```python
from src.matching import EnhancedFilumMatcher
matcher = EnhancedFilumMatcher("data/filum_knowledge_base.json")
stats = matcher.get_matching_stats()
print(stats)
```

### Explain match results:
```python
matches = matcher.find_matches("your query")
explanation = matcher.explain_match(matches[0])
print(explanation)
```

## 🔄 Migration from Basic Matcher

The system is backward compatible:

```python
# Automatic fallback if enhanced matching fails
from src.agent import FilumAgent
agent = FilumAgent(use_enhanced_matching=True)

# Force basic matching
agent = FilumAgent(use_enhanced_matching=False)
```

## 📊 Monitoring

### Track matching performance:
- Confidence score distributions
- Layer score breakdowns  
- User feedback on results
- Response time metrics

### Key metrics to monitor:
- Average confidence scores
- Distribution of confidence levels
- Most matched features
- Query processing time
