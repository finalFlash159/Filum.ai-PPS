"""
Simple fallback matcher for when enhanced matching fails
"""

import json
import os
import logging
import re
from typing import List, Dict, Any
from fuzzywuzzy import fuzz

class BasicMatcher:
    """
    Simple text matching fallback
    """
    
    def __init__(self, knowledge_base_path: str = None):
        """Initialize basic matcher"""
        self.logger = logging.getLogger(__name__)
        self.features = []
        
        # Default path if not provided
        if not knowledge_base_path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            knowledge_base_path = os.path.join(current_dir, "../../data/filum_knowledge_base.json")
        
        self.load_knowledge_base(knowledge_base_path)
    
    def load_knowledge_base(self, file_path: str):
        """Load knowledge base from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if 'filum_features' in data:
                    self.features = data.get('filum_features', [])
                else:
                    self.features = data
            
            self.logger.info(f"Loaded {len(self.features)} features for basic matching")
            
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base: {e}")
            self.features = []
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        words = text.split()
        
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'we', 'our', 'us', 'are', 'is', 'have', 'has', 'need', 'want', 'can', 'should', 'would'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    def find_matches(self, pain_point_description: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Find basic matches"""
        if not pain_point_description or not pain_point_description.strip():
            return []
        
        if not self.features:
            self.logger.warning("No features loaded for matching")
            return []
        
        pain_keywords = self.extract_keywords(pain_point_description.lower())
        matches = []
        
        for feature in self.features:
            feature_keywords = feature.get('keywords', [])
            feature_description = feature.get('description', '').lower()
            
            # Simple fuzzy matching
            desc_similarity = fuzz.partial_ratio(pain_point_description.lower(), feature_description) / 100.0
            
            # Keyword overlap
            keyword_score = 0.0
            if feature_keywords and pain_keywords:
                overlap_count = 0
                for pain_kw in pain_keywords:
                    for feature_kw in feature_keywords:
                        if fuzz.partial_ratio(pain_kw, feature_kw.lower()) > 70:
                            overlap_count += 1
                keyword_score = min(overlap_count / len(pain_keywords), 1.0)
            
            # Combined score
            final_score = (desc_similarity * 0.6 + keyword_score * 0.4)
            
            if final_score > 0.1:  # Minimum threshold
                match = {
                    "feature": feature,
                    "confidence_score": final_score,
                    "match_explanation": f"Basic similarity match ({final_score:.3f})"
                }
                matches.append(match)
        
        # Sort by confidence and return top matches
        matches.sort(key=lambda x: x["confidence_score"], reverse=True)
        return matches[:max_results]
