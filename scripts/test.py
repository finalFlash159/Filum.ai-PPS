#!/usr/bin/env python3
"""
Test Enhanced Matching System
Run this script to test the new 5-layer matching engine
"""

import os
import sys
import logging
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def setup_logging():
    """Setup logging for testing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_basic_functionality():
    """Test basic system functionality"""
    print("🧪 Testing Enhanced Matching System...")
    
    try:
        from src.agent import FilumAgent
        
        # Initialize agent with enhanced matching
        agent = FilumAgent(use_enhanced_matching=True)
        
        # Test queries
        test_queries = [
            "We struggle with collecting customer feedback after purchases",
            "Our support team is overwhelmed with repetitive questions",
            "We need better insights from our customer data",
            "Manual analysis of feedback takes too much time",
            "We want to automate our customer service workflows"
        ]
        
        print(f"\n📝 Testing {len(test_queries)} queries...\n")
        
        for i, query in enumerate(test_queries, 1):
            print(f"Query {i}: {query}")
            print("-" * 50)
            
            result = agent.analyze_pain_point(query, max_solutions=3)
            
            if result['status'] == 'success':
                print(f"✅ Found {len(result['solutions'])} solutions")
                
                for j, solution in enumerate(result['solutions'], 1):
                    print(f"  {j}. {solution['solution_name']}")
                    print(f"     Confidence: {solution['confidence_score']:.3f} ({solution['confidence_level']})")
                    print(f"     Reasoning: {solution['reasoning']}")
                    
                    if 'layer_breakdown' in solution:
                        breakdown = solution['layer_breakdown']
                        print(f"     Layer Scores: Exact={breakdown['exact_match']:.2f}, "
                              f"Fuzzy={breakdown['fuzzy_match']:.2f}, "
                              f"Semantic={breakdown['semantic_match']:.2f}, "
                              f"Domain={breakdown['domain_match']:.2f}, "
                              f"Intent={breakdown['intent_match']:.2f}")
                    print()
                
                if 'analysis' in result:
                    analysis = result['analysis']
                    print(f"📊 Analysis: {analysis.get('matching_method', 'unknown')} method")
                    if 'business_intent_detected' in analysis:
                        intents = analysis['business_intent_detected']
                        top_intents = {k: v for k, v in intents.items() if v > 0.1}
                        if top_intents:
                            print(f"🎯 Detected Intents: {top_intents}")
                    print()
            else:
                print(f"❌ Error: {result['message']}")
            
            print("=" * 60)
            print()
        
        print("✅ Basic functionality test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_embedding_system():
    """Test embedding system specifically"""
    print("\n🔍 Testing Embedding System...")
    
    try:
        from src.embeddings import EmbeddingManager
        
        # Test embedding manager
        knowledge_base_path = "data/filum_knowledge_base.json"
        manager = EmbeddingManager(knowledge_base_path)
        
        # Check if embeddings exist
        embeddings = manager.load_embeddings()
        
        if embeddings:
            print(f"✅ Loaded {len(embeddings)} pre-computed embeddings")
            
            # Test embedding creation
            test_text = "We need better customer feedback collection"
            embedding = manager.create_text_embedding(test_text)
            print(f"✅ Created embedding for test text: {embedding.shape}")
            
        else:
            print("⚠️  No embeddings cache found")
            print("💡 Run: python scripts/build_embeddings.py")
        
        stats = manager.get_embedding_stats()
        print(f"📊 Embedding Stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Embedding test failed: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are available"""
    print("🔍 Checking Dependencies...")
    
    required_packages = [
        ('numpy', 'numpy'),
        ('fuzzywuzzy', 'fuzzywuzzy'),
        ('nltk', 'nltk'),
        ('sentence_transformers', 'sentence-transformers')
    ]
    
    missing = []
    available = []
    
    for package, pip_name in required_packages:
        try:
            __import__(package)
            available.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(pip_name)
            print(f"❌ {package} (install: pip install {pip_name})")
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    else:
        print(f"\n✅ All dependencies available!")
        return True

def main():
    setup_logging()
    
    print("🚀 Enhanced Filum.ai Matching System Test")
    print("=" * 50)
    
    # Check dependencies first
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Cannot run tests without required dependencies")
        sys.exit(1)
    
    # Test embedding system
    embedding_ok = test_embedding_system()
    
    # Test basic functionality
    basic_ok = test_basic_functionality()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"Dependencies: {'✅' if deps_ok else '❌'}")
    print(f"Embeddings: {'✅' if embedding_ok else '❌'}")
    print(f"Basic Functionality: {'✅' if basic_ok else '❌'}")
    
    if deps_ok and basic_ok:
        print("\n🎉 All tests passed! System is ready.")
        
        if not embedding_ok:
            print("\n💡 To enable full semantic matching, run:")
            print("   python scripts/build_embeddings.py")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
