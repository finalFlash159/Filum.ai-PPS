"""
Advanced Text Processor for Filum.ai Pain Point Matching
Handles preprocessing, embedding, and multi-layer text analysis
"""

import re
import json
import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from fuzzywuzzy import fuzz
import nltk

# Download required NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

@dataclass
class ProcessedQuery:
    """Processed query with extracted components"""
    original: str
    cleaned: str
    tokens: List[str]
    keywords: List[str]
    business_intent: Dict[str, float]
    embedding: Optional[np.ndarray] = None

@dataclass
class LayeredScore:
    """Multi-layer matching score breakdown"""
    exact_match: float
    fuzzy_match: float
    semantic_match: float
    domain_match: float
    intent_match: float
    final_score: float
    reasoning: List[str]

class AdvancedTextProcessor:
    """Advanced text processing with multi-layer analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize NLTK components
        self.stop_words = set(stopwords.words('english'))
        
        # Business domain synonyms for Filum.ai
        self.business_synonyms = {
            'customer': ['client', 'user', 'consumer', 'buyer', 'patron', 'clientele'],
            'feedback': ['review', 'comment', 'opinion', 'suggestion', 'input', 'response'],
            'support': ['help', 'assistance', 'service', 'aid', 'care', 'helpdesk'],
            'analysis': ['analytics', 'examination', 'evaluation', 'assessment', 'insights'],
            'insight': ['understanding', 'knowledge', 'intelligence', 'perception', 'wisdom'],
            'automation': ['automatic', 'automated', 'ai', 'machine', 'bot', 'smart'],
            'integration': ['connection', 'linking', 'combining', 'merging', 'sync'],
            'dashboard': ['interface', 'panel', 'view', 'display', 'screen', 'console'],
            'survey': ['poll', 'questionnaire', 'form', 'quiz', 'inquiry'],
            'engagement': ['interaction', 'participation', 'involvement', 'activity'],
            'personalization': ['customization', 'tailoring', 'individualization', 'custom'],
            'workflow': ['process', 'procedure', 'flow', 'operation', 'pipeline'],
            'real-time': ['live', 'instant', 'immediate', 'current', 'realtime'],
            'tracking': ['monitoring', 'following', 'observing', 'watching', 'surveillance']
        }
        
        # Create reverse mapping
        self.reverse_synonyms = {}
        for main_word, synonyms in self.business_synonyms.items():
            for synonym in synonyms:
                self.reverse_synonyms[synonym] = main_word
                
        # Business intent patterns
        self.intent_patterns = {
            'feedback_collection': [
                'collect feedback', 'gather opinion', 'survey', 'review collection',
                'customer input', 'feedback gathering', 'opinion mining'
            ],
            'customer_service': [
                'support customer', 'help desk', 'customer care', 'service quality',
                'resolve issue', 'customer assistance', 'support ticket'
            ],
            'data_analysis': [
                'analyze data', 'insights', 'analytics', 'reporting', 'dashboard',
                'metrics', 'kpi', 'business intelligence', 'data visualization'
            ],
            'automation': [
                'automate process', 'workflow automation', 'ai powered', 'automatic',
                'streamline', 'efficiency', 'reduce manual work'
            ],
            'integration': [
                'integrate system', 'connect platform', 'sync data', 'api integration',
                'third party', 'external system', 'data flow'
            ]
        }
        
        self.logger.info("AdvancedTextProcessor initialized successfully")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace and special characters
        text = re.sub(r'[^\w\s-]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        if not text:
            return []
            
        # Tokenize
        tokens = word_tokenize(self.clean_text(text))
        
        # Filter meaningful keywords
        keywords = [
            token for token in tokens 
            if (len(token) > 2 and 
                token not in self.stop_words and 
                not token.isdigit())
        ]
        
        return list(set(keywords))  # Remove duplicates
    
    def expand_with_synonyms(self, keywords: List[str]) -> List[str]:
        """Expand keywords with business synonyms"""
        expanded = set(keywords)
        
        for keyword in keywords:
            # Check if keyword has synonyms
            if keyword in self.business_synonyms:
                expanded.update(self.business_synonyms[keyword])
            
            # Check reverse mapping
            if keyword in self.reverse_synonyms:
                main_word = self.reverse_synonyms[keyword]
                expanded.add(main_word)
                expanded.update(self.business_synonyms.get(main_word, []))
        
        return list(expanded)
    
    def detect_business_intent(self, text: str) -> Dict[str, float]:
        """Detect business intent from text"""
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            
            for pattern in patterns:
                # Check for exact phrase match
                if pattern in text_lower:
                    score += 1.0
                
                # Check for fuzzy match
                pattern_words = pattern.split()
                text_words = text_lower.split()
                
                for p_word in pattern_words:
                    for t_word in text_words:
                        if fuzz.ratio(p_word, t_word) > 80:
                            score += 0.5
            
            # Normalize score
            intent_scores[intent] = min(score / len(patterns), 1.0)
        
        return intent_scores
    
    def process_query(self, query: str) -> ProcessedQuery:
        """Process user query into structured format"""
        cleaned = self.clean_text(query)
        tokens = word_tokenize(cleaned)
        keywords = self.extract_keywords(query)
        expanded_keywords = self.expand_with_synonyms(keywords)
        business_intent = self.detect_business_intent(query)
        
        return ProcessedQuery(
            original=query,
            cleaned=cleaned,
            tokens=tokens,
            keywords=expanded_keywords,
            business_intent=business_intent
        )
    
    def calculate_exact_match_score(self, query_keywords: List[str], target_keywords: List[str]) -> float:
        """Calculate exact keyword match score"""
        if not query_keywords or not target_keywords:
            return 0.0
        
        # Convert to sets for intersection
        query_set = set(query_keywords)
        target_set = set(target_keywords)
        
        intersection = query_set & target_set
        union = query_set | target_set
        
        # Jaccard similarity
        return len(intersection) / len(union) if union else 0.0
    
    def calculate_fuzzy_match_score(self, query_keywords: List[str], target_keywords: List[str]) -> float:
        """Calculate fuzzy keyword match score"""
        if not query_keywords or not target_keywords:
            return 0.0
        
        total_score = 0.0
        match_count = 0
        
        for q_keyword in query_keywords:
            best_match = 0.0
            for t_keyword in target_keywords:
                similarity = fuzz.ratio(q_keyword, t_keyword) / 100.0
                best_match = max(best_match, similarity)
            
            if best_match > 0.7:  # Only count significant matches
                total_score += best_match
                match_count += 1
        
        return total_score / len(query_keywords) if query_keywords else 0.0
    
    def calculate_semantic_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between embeddings"""
        if embedding1 is None or embedding2 is None:
            return 0.0
            
        # Cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return float(dot_product / (norm1 * norm2))
    
    def calculate_domain_relevance(self, query_intent: Dict[str, float], feature_category: str) -> float:
        """Calculate domain relevance score"""
        # Map categories to intents
        category_intent_mapping = {
            'voice of customer': ['feedback_collection', 'data_analysis'],
            'ai customer service': ['customer_service', 'automation'],
            'insights': ['data_analysis'],
            'customer 360': ['customer_service', 'data_analysis'],
            'ai & automation': ['automation', 'integration']
        }
        
        category_lower = feature_category.lower()
        relevant_intents = category_intent_mapping.get(category_lower, [])
        
        if not relevant_intents:
            return 0.0
        
        # Calculate weighted intent match
        total_score = sum(query_intent.get(intent, 0.0) for intent in relevant_intents)
        return min(total_score / len(relevant_intents), 1.0)
    
    def explain_score(self, score: LayeredScore) -> str:
        """Generate human-readable explanation for the score"""
        explanations = []
        
        if score.exact_match > 0.3:
            explanations.append(f"Strong keyword match ({score.exact_match:.1%})")
        elif score.exact_match > 0.1:
            explanations.append(f"Moderate keyword match ({score.exact_match:.1%})")
            
        if score.fuzzy_match > 0.5:
            explanations.append(f"Good fuzzy similarity ({score.fuzzy_match:.1%})")
            
        if score.semantic_match > 0.7:
            explanations.append(f"High semantic relevance ({score.semantic_match:.1%})")
        elif score.semantic_match > 0.5:
            explanations.append(f"Moderate semantic relevance ({score.semantic_match:.1%})")
            
        if score.domain_match > 0.5:
            explanations.append(f"Domain relevant ({score.domain_match:.1%})")
            
        if score.intent_match > 0.3:
            explanations.append(f"Intent alignment ({score.intent_match:.1%})")
        
        if not explanations:
            explanations.append("Basic text similarity")
            
        return " • ".join(explanations)
