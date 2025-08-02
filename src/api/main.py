"""
FastAPI server for Filum.ai Pain Point Solution Agent
Specialized for matching business pain points to Filum.ai platform features
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Import the Filum.ai solution engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.agent.engine import get_filum_agent, PainPointAgent

app = FastAPI(
    title="Filum.ai Pain Point Solution Agent API",
    description="AI-powered system for matching business pain points to Filum.ai platform features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class PainPointRequest(BaseModel):
    description: str = Field(..., description="Business pain point description", min_length=10)
    max_solutions: Optional[int] = Field(5, description="Maximum number of solutions to return", ge=1, le=10)
    include_analysis: Optional[bool] = Field(True, description="Include detailed analysis in response")

class PainPointResponse(BaseModel):
    status: str
    message: str
    pain_point: str
    solutions: List[Dict[str, Any]]
    analysis: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    message: str
    features_loaded: int

class CategoryResponse(BaseModel):
    categories: List[Dict[str, Any]]
    total_categories: int

# Initialize Filum.ai agent
filum_agent = get_filum_agent()

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API health check and information"""
    feature_count = len(filum_agent.matcher.features) if filum_agent.matcher.features else 0
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="Filum.ai Pain Point Solution Agent API is running",
        features_loaded=feature_count
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint"""
    feature_count = len(filum_agent.matcher.features) if filum_agent.matcher.features else 0
    
    if feature_count == 0:
        return HealthResponse(
            status="warning",
            version="1.0.0",
            message="API is running but no Filum.ai features loaded",
            features_loaded=feature_count
        )
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="All systems operational",
        features_loaded=feature_count
    )

@app.post("/analyze-pain-point", response_model=PainPointResponse)
async def analyze_pain_point(request: PainPointRequest):
    """
    Analyze business pain point and recommend Filum.ai solutions
    
    This endpoint takes a business pain point description and returns
    relevant Filum.ai platform features that can address the challenge.
    """
    try:
        if not request.description.strip():
            raise HTTPException(
                status_code=400,
                detail="Pain point description cannot be empty"
            )
        
        # Analyze pain point using Filum.ai engine
        result = filum_agent.analyze_pain_point(
            pain_point_description=request.description,
            max_solutions=request.max_solutions
        )
        
        # Format response
        response_data = {
            "status": result["status"],
            "message": result["message"],
            "pain_point": result["pain_point"],
            "solutions": result["solutions"]
        }
        
        if request.include_analysis:
            response_data["analysis"] = result.get("analysis")
        
        return PainPointResponse(**response_data)
        
    except Exception as e:
        logging.error(f"Error in analyze_pain_point: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/feature/{feature_id}")
async def get_feature_details(feature_id: str):
    """
    Get detailed information about a specific Filum.ai feature
    
    Args:
        feature_id: Unique identifier for the Filum.ai feature
        
    Returns:
        Detailed feature information including description, benefits, use cases
    """
    try:
        feature = filum_agent.get_feature_details(feature_id)
        
        if not feature:
            raise HTTPException(
                status_code=404,
                detail=f"Feature with ID '{feature_id}' not found"
            )
        
        return {
            "feature": feature,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in get_feature_details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories", response_model=CategoryResponse)
async def get_categories():
    """
    Get all available Filum.ai feature categories
    
    Returns:
        List of categories with feature counts and subcategories
    """
    try:
        categories = filum_agent.get_all_categories()
        
        return CategoryResponse(
            categories=categories,
            total_categories=len(categories)
        )
        
    except Exception as e:
        logging.error(f"Error in get_categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/category/{category_name}")
async def get_features_by_category(category_name: str):
    """
    Get all Filum.ai features in a specific category
    
    Args:
        category_name: Name of the category (e.g., "Voice of Customer", "AI Customer Service")
        
    Returns:
        List of features in the specified category
    """
    try:
        features = filum_agent.get_features_by_category(category_name)
        
        return {
            "category": category_name,
            "features": features,
            "total_features": len(features),
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Error in get_features_by_category: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/examples")
async def get_example_pain_points():
    """
    Get example pain points and their potential Filum.ai solutions
    
    Returns:
        List of example pain points with suggested solutions
    """
    examples = [
        {
            "pain_point": "We're struggling to collect customer feedback consistently after a purchase.",
            "suggested_solution": "Automated Post-Purchase Surveys (VoC - Surveys)",
            "how_it_helps": "Trigger surveys automatically via email/SMS after a transaction"
        },
        {
            "pain_point": "Our support agents are overwhelmed by the high volume of repetitive questions.",
            "suggested_solution": "AI Agent for FAQ & First Response (AI Customer Service - AI Inbox)",
            "how_it_helps": "Deflects common queries and provides instant answers, freeing up human agents"
        },
        {
            "pain_point": "We have no clear idea which customer touchpoints are causing the most frustration.",
            "suggested_solution": "Customer Journey Experience Analysis (Insights - Experience)",
            "how_it_helps": "Identifies friction points by analyzing feedback and operational data across the journey"
        },
        {
            "pain_point": "It's difficult to get a single view of a customer's interaction history when they contact us.",
            "suggested_solution": "Customer Profile with Interaction History (Customer 360 - Customers & AI Inbox)",
            "how_it_helps": "Consolidates all touchpoints and past interactions for a comprehensive view"
        },
        {
            "pain_point": "Manually analyzing thousands of open-ended survey responses for common themes is too time-consuming.",
            "suggested_solution": "AI-Powered Topic & Sentiment Analysis for VoC (VoC - Conversations/Surveys, Insights - Experience)",
            "how_it_helps": "Automatically extracts key topics and sentiment from text feedback"
        }
    ]
    
    return {
        "examples": examples,
        "total_examples": len(examples),
        "status": "success"
    }

# Legacy endpoints for backward compatibility
@app.post("/recommend")
async def legacy_recommend(request: PainPointRequest):
    """Legacy endpoint for backward compatibility"""
    return await analyze_pain_point(request)

@app.get("/solution/{solution_id}")
async def legacy_get_solution(solution_id: str):
    """Legacy endpoint for backward compatibility"""
    return await get_feature_details(solution_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
