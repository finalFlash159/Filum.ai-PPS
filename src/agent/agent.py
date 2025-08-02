"""
Main Filum.ai Agent
Central coordinator for pain point analysis and solution recommendations
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from ..matching import EnhancedFilumMatcher

class FilumAgent:
    """
    Main Filum.ai Pain Point Solution Agent
    
    This is the primary interface for analyzing business pain points
    and recommending relevant Filum.ai platform features.
    Uses enhanced 5-layer matching with semantic embeddings.
    """
    
    def __init__(self, knowledge_base_path: Optional[str] = None, use_enhanced_matching: bool = True):
        """
        Initialize the Filum.ai agent
        
        Args:
            knowledge_base_path: Path to Filum.ai knowledge base JSON file
            use_enhanced_matching: Whether to use enhanced 5-layer matching
        """
        self.logger = logging.getLogger(__name__)
        self.use_enhanced_matching = use_enhanced_matching
        
        # Default knowledge base path
        if not knowledge_base_path:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            knowledge_base_path = os.path.join(current_dir, "../../data/filum_knowledge_base.json")
        
        # Initialize enhanced or basic matcher
        if use_enhanced_matching:
            try:
                self.enhanced_matcher = EnhancedFilumMatcher(knowledge_base_path)
                self.logger.info("Enhanced 5-layer matching enabled")
            except Exception as e:
                self.logger.warning(f"Failed to initialize enhanced matcher: {e}")
                self.logger.info("Falling back to basic text matcher")
                use_enhanced_matching = False
        
        if not use_enhanced_matching:
            # Use basic fallback matcher
            from .fallback import BasicMatcher
            self.basic_matcher = BasicMatcher(knowledge_base_path)
        
        self.logger.info(f"Filum.ai Agent initialized with enhanced matching: {use_enhanced_matching}")
    
    def analyze_pain_point(self, 
                          pain_point_description: str, 
                          max_solutions: int = 5) -> Dict[str, Any]:
        """
        Analyze a business pain point and recommend Filum.ai solutions
        
        Args:
            pain_point_description: Description of the business challenge
            max_solutions: Maximum number of solutions to return
            
        Returns:
            Dict containing status, solutions, and analysis
        """
        try:
            if not pain_point_description or not pain_point_description.strip():
                return {
                    "status": "error",
                    "message": "Pain point description cannot be empty",
                    "pain_point": "",
                    "solutions": [],
                    "analysis": {}
                }
            
            if self.use_enhanced_matching and hasattr(self, 'enhanced_matcher'):
                return self._analyze_with_enhanced_matching(
                    pain_point_description, max_solutions
                )
            elif hasattr(self, 'basic_matcher'):
                # Use basic matcher directly
                return self._analyze_with_basic_matching(
                    pain_point_description, max_solutions
                )
            else:
                return {
                    "status": "error",
                    "message": "No matching system available",
                    "pain_point": pain_point_description,
                    "solutions": [],
                    "analysis": {}
                }
            
        except Exception as e:
            self.logger.error(f"Error in analyze_pain_point: {e}")
            return {
                "status": "error",
                "message": f"Analysis failed: {str(e)}",
                "pain_point": pain_point_description,
                "solutions": [],
                "analysis": {}
            }
    
    def _analyze_with_enhanced_matching(self, pain_point_description: str, max_solutions: int) -> Dict[str, Any]:
        """Analyze using enhanced 5-layer matching"""
        try:
            # Get matches using enhanced matcher
            matches = self.enhanced_matcher.find_matches(pain_point_description, max_solutions)
            
            if not matches:
                return {
                    "status": "success",
                    "message": "No relevant solutions found for this pain point",
                    "pain_point": pain_point_description,
                    "solutions": [],
                    "analysis": {
                        "total_features_analyzed": len(self.enhanced_matcher.features),
                        "matching_method": "enhanced_5_layer",
                        "layer_weights": self.enhanced_matcher.layer_weights
                    }
                }
            
            # Convert matches to solution format
            solutions = []
            for match in matches:
                solution = {
                    "solution_name": match.feature_name,
                    "confidence_score": match.confidence_score,
                    "confidence_level": match.match_details['confidence_level'],
                    "reasoning": match.reasoning,
                    "feature": match.feature_data,
                    "layer_breakdown": match.match_details['layer_breakdown'],
                    "matched_keywords": match.match_details['matched_keywords']
                }
                solutions.append(solution)
            
            # Generate analysis summary
            best_match = matches[0]
            analysis = {
                "total_features_analyzed": len(self.enhanced_matcher.features),
                "matching_method": "enhanced_5_layer",
                "layer_weights": self.enhanced_matcher.layer_weights,
                "best_match_confidence": best_match.confidence_score,
                "best_match_reasoning": best_match.reasoning,
                "business_intent_detected": best_match.match_details['business_intent'],
                "confidence_distribution": {
                    "high": len([m for m in matches if m.match_details['confidence_level'] == 'high']),
                    "medium": len([m for m in matches if m.match_details['confidence_level'] == 'medium']),
                    "low": len([m for m in matches if m.match_details['confidence_level'] == 'low'])
                }
            }
            
            return {
                "status": "success",
                "message": f"Found {len(solutions)} relevant solutions",
                "pain_point": pain_point_description,
                "solutions": solutions,
                "analysis": analysis
            }
            
        except Exception as e:
            self.logger.error(f"Enhanced matching failed: {e}")
            # Fallback to basic matching
            if hasattr(self, 'solution_engine'):
                return self.solution_engine.analyze_pain_point(pain_point_description, max_solutions)
            else:
                raise
    
    def _analyze_with_basic_matching(self, pain_point_description: str, max_solutions: int) -> Dict[str, Any]:
        """Analyze using basic matching"""
        try:
            # Get matches using basic matcher
            matches = self.basic_matcher.find_matches(pain_point_description, max_solutions)
            
            if not matches:
                return {
                    "status": "success",
                    "message": "No relevant solutions found for this pain point",
                    "pain_point": pain_point_description,
                    "solutions": [],
                    "analysis": {
                        "matching_method": "basic",
                        "total_features_analyzed": len(self.basic_matcher.features) if self.basic_matcher.features else 0
                    }
                }
            
            # Convert matches to solution format
            solutions = []
            for match in matches:
                solution = {
                    "solution_name": match['feature'].get('name', 'Unknown'),
                    "confidence_score": match['confidence_score'],
                    "confidence_level": self._determine_basic_confidence_level(match['confidence_score']),
                    "reasoning": match['match_explanation'],
                    "feature": match['feature']
                }
                solutions.append(solution)
            
            # Generate analysis summary
            analysis = {
                "matching_method": "basic",
                "total_features_analyzed": len(self.basic_matcher.features) if self.basic_matcher.features else 0,
                "best_match_confidence": matches[0]['confidence_score'] if matches else 0.0
            }
            
            return {
                "status": "success",
                "message": f"Found {len(solutions)} relevant solutions (basic matching)",
                "pain_point": pain_point_description,
                "solutions": solutions,
                "analysis": analysis
            }
            
        except Exception as e:
            self.logger.error(f"Basic matching failed: {e}")
            return {
                "status": "error",
                "message": f"Basic matching failed: {str(e)}",
                "pain_point": pain_point_description,
                "solutions": [],
                "analysis": {}
            }
    
    def _determine_basic_confidence_level(self, score: float) -> str:
        """Determine confidence level for basic matching"""
        if score >= 0.6:
            return 'high'
        elif score >= 0.3:
            return 'medium'
        else:
            return 'low'
    
    def get_feature_details(self, feature_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific Filum.ai feature
        
        Args:
            feature_id: Unique identifier for the feature
            
        Returns:
            Feature details or None if not found
        """
        return self.solution_engine.get_feature_details(feature_id)
    
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """
        Get all available Filum.ai feature categories
        
        Returns:
            List of categories with feature counts
        """
        return self.solution_engine.get_all_categories()
    
    def get_features_by_category(self, category_name: str) -> List[Dict[str, Any]]:
        """
        Get all features in a specific category
        
        Args:
            category_name: Name of the category
            
        Returns:
            List of features in the category
        """
        return self.solution_engine.get_features_by_category(category_name)
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about the agent and its capabilities
        
        Returns:
            Agent information and statistics
        """
        feature_count = len(self.text_matcher.features)
        categories = self.get_all_categories()
        
        return {
            "agent_version": "1.0.0",
            "platform": "Filum.ai",
            "features_loaded": feature_count,
            "categories_available": len(categories),
            "matching_algorithm": "Fuzzy + Keyword + Category",
            "status": "operational" if feature_count > 0 else "no_features_loaded",
            "capabilities": [
                "Pain point analysis",
                "Feature matching", 
                "Confidence scoring",
                "Implementation suggestions",
                "Category classification"
            ]
        }
    
    def search_features(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search features by query string
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of matching features with scores
        """
        matches = self.text_matcher.find_matches(query, max_results)
        return [
            {
                "feature": match["feature"],
                "confidence_score": match["confidence_score"],
                "match_explanation": match.get("match_explanation", "")
            }
            for match in matches
        ]
    
    def validate_setup(self) -> Dict[str, Any]:
        """
        Validate that the agent is properly set up
        
        Returns:
            Validation results
        """
        issues = []
        
        if not self.text_matcher.features:
            issues.append("No features loaded from knowledge base")
        
        if len(self.text_matcher.features) < 5:
            issues.append(f"Only {len(self.text_matcher.features)} features loaded, expected more")
        
        # Test basic functionality
        try:
            test_result = self.analyze_pain_point("test pain point", max_solutions=1)
            if test_result["status"] != "success":
                issues.append("Pain point analysis test failed")
        except Exception as e:
            issues.append(f"Pain point analysis test error: {e}")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "features_count": len(self.text_matcher.features),
            "test_status": "passed" if len(issues) == 0 else "failed"
        }
