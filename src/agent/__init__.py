"""
Filum.ai Agent Package
Main package for Filum.ai Pain Point Solution Agent
"""

from .agent import FilumAgent

__version__ = "1.0.0"
__author__ = "Filum.ai Team"

def get_filum_agent(use_enhanced_matching: bool = True) -> FilumAgent:
    """
    Factory function to create a configured Filum.ai agent
    
    Args:
        use_enhanced_matching: Whether to use enhanced 5-layer matching
        
    Returns:
        FilumAgent: Configured agent ready for pain point analysis
    """
    return FilumAgent(use_enhanced_matching=use_enhanced_matching)

# Legacy compatibility - keep for backward compatibility
def create_agent() -> FilumAgent:
    """Legacy function for backward compatibility"""
    return get_filum_agent()

__all__ = [
    'FilumAgent',
    'get_filum_agent', 
    'create_agent'
]
