"""
Enhanced Multi-Layer Matching Engine for Filum.ai
5-layer scoring system with pre-computed embeddings
"""

import json
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from ..processing import AdvancedTextProcessor, ProcessedQuery, LayeredScore
from ..embeddings import EmbeddingManager, FeatureEmbedding

@dataclass
class MatchResult:
    """Enhanced match result with detailed scoring breakdown"""
    feature_id: str
    feature_name: str
    confidence_score: float
    layer_scores: LayeredScore
    reasoning: str
    match_details: Dict[str, Any]
    feature_data: Dict[str, Any]

class EnhancedFilumMatcher:
    """5-Layer matching engine with semantic embeddings"""
    
    def __init__(self, knowledge_base_path: str, embeddings_cache_path: str = None):
        """Initialize enhanced matcher"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.text_processor = AdvancedTextProcessor()
        self.embedding_manager = EmbeddingManager(knowledge_base_path, embeddings_cache_path)
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.features = self.knowledge_base.get('filum_features', [])
        
        # Load or create embeddings
        self.feature_embeddings = self.embedding_manager.load_embeddings()
        if not self.feature_embeddings:
            self.logger.warning("No embeddings cache found. Building embeddings...")
            self.feature_embeddings = self.embedding_manager.build_embeddings_from_knowledge_base()
            self.embedding_manager.save_embeddings()
        
        # Layer weights (must sum to 1.0)
        self.layer_weights = {
            'exact_match': 0.20,      # Exact keyword matches
            'fuzzy_match': 0.25,      # Fuzzy keyword similarity  
            'semantic_match': 0.35,   # AI semantic similarity (highest weight)
            'domain_match': 0.15,     # Business domain relevance
            'intent_match': 0.05      # Specific pain point intent
        }
        
        # Confidence thresholds
        self.confidence_thresholds = {
            'high': 0.65,    # Strong match
            'medium': 0.40,  # Moderate match
            'low': 0.20      # Weak but relevant match
        }
        
        self.logger.info(f"Enhanced matcher initialized with {len(self.features)} features")
        self.logger.info(f"Loaded embeddings for {len(self.feature_embeddings)} features")
    
    def _load_knowledge_base(self, file_path: str) -> Dict:
        """Load knowledge base from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading knowledge base: {e}")
            return {'filum_features': []}
    
    def _calculate_layer_scores(self, processed_query: ProcessedQuery, feature: Dict[str, Any], 
                               feature_embedding: FeatureEmbedding) -> LayeredScore:
        """Calculate scores for all 5 layers"""
        
        # Extract feature text components
        feature_keywords = feature.get('keywords', [])
        feature_description = feature.get('description', '')
        feature_pain_points = feature.get('pain_points_addressed', [])
        feature_category = feature.get('category', '')
        
        # Layer 1: Exact Match Score
        exact_score = self.text_processor.calculate_exact_match_score(
            processed_query.keywords, 
            feature_keywords
        )
        
        # Layer 2: Fuzzy Match Score  
        fuzzy_score = self.text_processor.calculate_fuzzy_match_score(
            processed_query.keywords,
            feature_keywords + feature_description.split() + feature_pain_points
        )
        
        # Layer 3: Semantic Match Score (using embeddings)
        semantic_score = 0.0
        if processed_query.embedding is not None and feature_embedding:
            semantic_score = self.text_processor.calculate_semantic_similarity(
                processed_query.embedding,
                feature_embedding.combined_embedding
            )
        
        # Layer 4: Domain Match Score
        domain_score = self.text_processor.calculate_domain_relevance(
            processed_query.business_intent,
            feature_category
        )
        
        # Layer 5: Intent Match Score (pain points addressed)
        intent_score = 0.0
        if feature_pain_points:
            intent_matches = []
            for pain_point in feature_pain_points:
                pain_keywords = self.text_processor.extract_keywords(pain_point)
                intent_match = self.text_processor.calculate_fuzzy_match_score(
                    processed_query.keywords,
                    pain_keywords
                )
                intent_matches.append(intent_match)
            intent_score = max(intent_matches) if intent_matches else 0.0
        
        # Generate reasoning
        reasoning_parts = []
        
        if exact_score > 0.3:
            reasoning_parts.append(f"Strong keyword match ({exact_score:.1%})")
        if fuzzy_score > 0.5:
            reasoning_parts.append(f"Good fuzzy similarity ({fuzzy_score:.1%})")
        if semantic_score > 0.7:
            reasoning_parts.append(f"High semantic relevance ({semantic_score:.1%})")
        if domain_score > 0.5:
            reasoning_parts.append(f"Domain relevant ({domain_score:.1%})")
        if intent_score > 0.3:
            reasoning_parts.append(f"Pain point alignment ({intent_score:.1%})")
        
        return LayeredScore(
            exact_match=exact_score,
            fuzzy_match=fuzzy_score,
            semantic_match=semantic_score,
            domain_match=domain_score,
            intent_match=intent_score,
            final_score=0.0,  # Will be calculated next
            reasoning=reasoning_parts
        )
    
    def _calculate_final_score(self, layer_scores: LayeredScore) -> float:
        """Calculate weighted final score from layer scores"""
        final_score = (
            layer_scores.exact_match * self.layer_weights['exact_match'] +
            layer_scores.fuzzy_match * self.layer_weights['fuzzy_match'] +
            layer_scores.semantic_match * self.layer_weights['semantic_match'] +
            layer_scores.domain_match * self.layer_weights['domain_match'] +
            layer_scores.intent_match * self.layer_weights['intent_match']
        )
        
        # Update the layer_scores object
        layer_scores.final_score = min(final_score, 1.0)  # Cap at 1.0
        
        return layer_scores.final_score
    
    def _determine_confidence_level(self, score: float) -> str:
        """Determine confidence level from score"""
        if score >= self.confidence_thresholds['high']:
            return 'high'
        elif score >= self.confidence_thresholds['medium']:
            return 'medium'
        elif score >= self.confidence_thresholds['low']:
            return 'low'
        else:
            return 'very_low'
    
    def find_matches(self, pain_point_description: str, max_results: int = 5) -> List[MatchResult]:
        """
        Find best matching Filum.ai features using 5-layer analysis
        
        Args:
            pain_point_description: User's business challenge description
            max_results: Maximum number of results to return
            
        Returns:
            List of MatchResult objects sorted by confidence
        """
        if not pain_point_description or not pain_point_description.strip():
            return []
        
        if not self.features:
            self.logger.warning("No features loaded for matching")
            return []
        
        # Process user query
        processed_query = self.text_processor.process_query(pain_point_description)
        
        # Create embedding for user query
        try:
            processed_query.embedding = self.embedding_manager.create_text_embedding(
                pain_point_description
            )
        except Exception as e:
            self.logger.warning(f"Failed to create query embedding: {e}")
            processed_query.embedding = None
        
        results = []
        
        # Process each feature
        for feature in self.features:
            feature_id = feature.get('id', '')
            feature_embedding = self.feature_embeddings.get(feature_id)
            
            if not feature_embedding:
                self.logger.warning(f"No embedding found for feature: {feature_id}")
                continue
            
            # Calculate layer scores
            layer_scores = self._calculate_layer_scores(
                processed_query, 
                feature, 
                feature_embedding
            )
            
            # Calculate final weighted score
            final_score = self._calculate_final_score(layer_scores)
            
            # Only include results above minimum threshold
            if final_score >= self.confidence_thresholds['low']:
                
                # Generate explanation
                reasoning = self.text_processor.explain_score(layer_scores)
                
                # Create match details
                match_details = {
                    'confidence_level': self._determine_confidence_level(final_score),
                    'layer_breakdown': {
                        'exact_match': layer_scores.exact_match,
                        'fuzzy_match': layer_scores.fuzzy_match,
                        'semantic_match': layer_scores.semantic_match,
                        'domain_match': layer_scores.domain_match,
                        'intent_match': layer_scores.intent_match
                    },
                    'weights_used': self.layer_weights,
                    'matched_keywords': list(set(processed_query.keywords) & set(feature.get('keywords', []))),
                    'business_intent': processed_query.business_intent,
                    'category': feature.get('category', ''),
                    'subcategory': feature.get('subcategory', '')
                }
                
                result = MatchResult(
                    feature_id=feature_id,
                    feature_name=feature.get('name', ''),
                    confidence_score=final_score,
                    layer_scores=layer_scores,
                    reasoning=reasoning,
                    match_details=match_details,
                    feature_data=feature
                )
                
                results.append(result)
        
        # Sort by confidence score and return top matches
        results.sort(key=lambda x: x.confidence_score, reverse=True)
        return results[:max_results]
    
    def explain_match(self, result: MatchResult) -> Dict[str, Any]:
        """Generate detailed explanation for a match result"""
        return {
            'feature_name': result.feature_name,
            'confidence_score': result.confidence_score,
            'confidence_level': result.match_details['confidence_level'],
            'reasoning': result.reasoning,
            'layer_breakdown': result.match_details['layer_breakdown'],
            'weights_used': result.match_details['weights_used'],
            'matched_keywords': result.match_details['matched_keywords'],
            'business_intent_detected': result.match_details['business_intent'],
            'feature_category': result.match_details['category']
        }
    
    def get_matching_stats(self) -> Dict[str, Any]:
        """Get statistics about the matching system"""
        return {
            'total_features': len(self.features),
            'features_with_embeddings': len(self.feature_embeddings),
            'layer_weights': self.layer_weights,
            'confidence_thresholds': self.confidence_thresholds,
            'embedding_cache_path': self.embedding_manager.embeddings_cache_path
        }
