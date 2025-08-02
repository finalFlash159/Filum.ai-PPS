"""
Filum.ai Agent Package
Main package for Filum.ai Pain Point Solution Agent
"""

from .agent import FilumAgent
from .engine import FilumSolutionEngine, get_filum_agent, PainPointAgent

__version__ = "1.0.0"

__all__ = ['FilumAgent', 'FilumSolutionEngine', 'get_filum_agent', 'PainPointAgent']
__author__ = "Filum.ai Team"

def create_agent() -> FilumAgent:
    """
    Factory function to create a configured Filum.ai agent
    
    Returns:
        FilumAgent: Configured agent ready for pain point analysis
    """
    return FilumAgent()

# Legacy compatibility
def get_filum_agent() -> FilumAgent:
    """Legacy function for backward compatibility"""
    return create_agent()

__all__ = [
    'FilumAgent',
    'FilumTextMatcher', 
    'FilumSolutionEngine',
    'create_agent',
    'get_filum_agent'
]
