"""
Filum.ai Solution Engine
Core business logic for analyzing pain points and generating solution recommendations
"""

import logging
from typing import Dict, Any, List, Optional
from ..matching import FilumTextMatcher

class FilumSolutionEngine:
    """
    Solution engine for processing pain points and generating recommendations
    """
    
    def __init__(self, text_matcher: FilumTextMatcher):
        """
        Initialize the solution engine
        
        Args:
            text_matcher: Configured FilumTextMatcher instance
        """
        self.matcher = text_matcher
        self.logger = logging.getLogger(__name__)
    
    def analyze_pain_point(self, 
                          pain_point_description: str, 
                          max_solutions: int = 5) -> Dict[str, Any]:
        """
        Analyze a pain point and generate solution recommendations
        
        Args:
            pain_point_description: The business pain point to analyze
            max_solutions: Maximum number of solutions to return
            
        Returns:
            Complete analysis result with solutions and metadata
        """
        try:
            # Find matching features
            matches = self.matcher.find_matches(pain_point_description, max_solutions)
            
            # Generate solutions with enhanced information
            solutions = []
            for match in matches:
                solution = self._create_solution_from_match(match, pain_point_description)
                solutions.append(solution)
            
            # Create analysis summary
            analysis = self._create_analysis_summary(pain_point_description, solutions)
            
            return {
                "status": "success",
                "message": f"Found {len(solutions)} relevant Filum.ai solutions",
                "pain_point": pain_point_description,
                "solutions": solutions,
                "analysis": analysis
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
    
    def _create_solution_from_match(self, match: Dict[str, Any], pain_point: str) -> Dict[str, Any]:
        """Create a complete solution object from a feature match"""
        feature = match["feature"]
        confidence = match["confidence_score"]
        
        return {
            "feature_id": feature["id"],
            "solution_name": feature["name"],
            "category": feature["category"],
            "subcategory": feature.get("subcategory", ""),
            "confidence_score": confidence,
            "confidence_level": self._get_confidence_level(confidence),
            "how_it_helps": self._generate_how_it_helps(feature, pain_point),
            "implementation_suggestion": self._generate_implementation_suggestion(feature),
            "feature_details": {
                "description": feature.get("description", ""),
                "benefits": feature.get("benefits", []),
                "use_cases": feature.get("use_cases", []),
                "keywords": feature.get("keywords", [])
            },
            "relevance_explanation": match.get("match_explanation", "")
        }
    
    def _generate_how_it_helps(self, feature: Dict[str, Any], pain_point: str) -> str:
        """Generate contextual explanation of how the feature helps with the specific pain point"""
        
        # Extract key concepts from pain point
        pain_keywords = self.matcher.extract_keywords(pain_point.lower())
        feature_keywords = feature.get("keywords", [])
        
        # Generate contextual explanation
        base_description = feature.get("description", "")
        
        if "feedback" in pain_keywords and feature["category"] == "Voice of Customer":
            return f"{base_description} This directly addresses your feedback collection challenges."
        elif "support" in pain_keywords and feature["category"] == "AI Customer Service":
            return f"{base_description} This can reduce the burden on your support team."
        elif "customer" in pain_keywords and "analysis" in pain_keywords:
            return f"{base_description} This provides the customer insights you need."
        else:
            return base_description
    
    def _generate_implementation_suggestion(self, feature: Dict[str, Any]) -> str:
        """Generate implementation suggestions based on feature type"""
        
        category = feature["category"]
        
        suggestions = {
            "Voice of Customer": "Start with a pilot program focusing on your most important customer touchpoints.",
            "AI Customer Service": "Begin with FAQ automation for your most common support queries.",
            "Insights": "Start by connecting your existing data sources for immediate visibility.",
            "Customer 360": "Begin with integrating your primary customer interaction channels.",
            "AI & Automation": "Start with automating your most repetitive customer service tasks."
        }
        
        return suggestions.get(category, "Consider implementing this feature as part of your customer experience improvement initiative.")
    
    def _get_confidence_level(self, score: float) -> str:
        """Convert confidence score to human-readable level"""
        if score >= 0.8:
            return "High"
        elif score >= 0.6:
            return "Medium"
        else:
            return "Low"
    
    def _create_analysis_summary(self, pain_point: str, solutions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create analysis summary with insights"""
        
        # Category distribution
        categories = {}
        for solution in solutions:
            cat = solution["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        # Confidence distribution
        confidence_levels = {}
        for solution in solutions:
            level = solution["confidence_level"]
            confidence_levels[level] = confidence_levels.get(level, 0) + 1
        
        # Pain point complexity analysis
        word_count = len(pain_point.split())
        complexity = "high" if word_count > 20 else "medium" if word_count > 10 else "low"
        
        return {
            "pain_point_complexity": complexity,
            "word_count": word_count,
            "solutions_found": len(solutions),
            "top_confidence": solutions[0]["confidence_score"] if solutions else 0,
            "category_distribution": categories,
            "confidence_distribution": confidence_levels,
            "primary_categories": list(categories.keys())[:3]
        }
    
    def get_feature_details(self, feature_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific feature"""
        for feature in self.matcher.features:
            if feature["id"] == feature_id:
                return feature
        return None
    
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all available categories with feature counts"""
        categories = {}
        
        for feature in self.matcher.features:
            cat = feature["category"]
            if cat not in categories:
                categories[cat] = {
                    "name": cat,
                    "feature_count": 0,
                    "features": [],
                    "subcategories": set()
                }
            
            categories[cat]["feature_count"] += 1
            categories[cat]["features"].append(feature["name"])
            
            if "subcategory" in feature:
                categories[cat]["subcategories"].add(feature["subcategory"])
        
        # Convert to list and clean up
        result = []
        for cat_info in categories.values():
            cat_info["subcategories"] = list(cat_info["subcategories"])
            result.append(cat_info)
        
        return sorted(result, key=lambda x: x["feature_count"], reverse=True)
    
    def get_features_by_category(self, category_name: str) -> List[Dict[str, Any]]:
        """Get all features in a specific category"""
        return [
            feature for feature in self.matcher.features 
            if feature["category"].lower() == category_name.lower()
        ]


# Legacy compatibility functions
def get_filum_agent():
    """Legacy function for backward compatibility"""
    from .agent import FilumAgent
    return FilumAgent()

class PainPointAgent:
    """Legacy class for backward compatibility"""
    
    def __init__(self):
        from .agent import FilumAgent
        self._agent = FilumAgent()
    
    def recommend_solutions(self, description: str, max_results: int = 5):
        """Legacy method"""
        return self._agent.analyze_pain_point(description, max_results)
    
    def get_solution_details(self, solution_id: str):
        """Legacy method"""
        return self._agent.get_feature_details(solution_id)
