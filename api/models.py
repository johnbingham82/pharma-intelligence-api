"""
API Request/Response Models
Pydantic models for type-safe API contracts
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============================================================================
# REQUEST MODELS
# ============================================================================

class AnalysisRequest(BaseModel):
    """Request model for drug analysis"""
    company: str = Field(..., min_length=1, max_length=200, 
                        description="Pharmaceutical company name")
    drug_name: str = Field(..., min_length=1, max_length=200,
                          description="Drug name (brand or generic)")
    country: str = Field(..., pattern="^[A-Z]{2}$",
                        description="ISO 3166-1 alpha-2 country code (e.g., UK, US)")
    region: Optional[str] = Field(None, max_length=50,
                                 description="Optional region filter (e.g., ICB code for UK)")
    top_n: int = Field(50, ge=1, le=500,
                      description="Number of top opportunities to return (1-500)")
    scorer: Optional[str] = Field("market_share", 
                                 description="Scoring algorithm: simple_volume or market_share")
    
    class Config:
        schema_extra = {
            "example": {
                "company": "Novartis",
                "drug_name": "Inclisiran",
                "country": "UK",
                "region": None,
                "top_n": 50,
                "scorer": "market_share"
            }
        }


class DrugSearchRequest(BaseModel):
    """Request model for drug search"""
    query: str = Field(..., min_length=2, max_length=200,
                      description="Search query (drug name)")
    country: str = Field(..., pattern="^[A-Z]{2}$",
                        description="Country code for drug lookup")
    limit: int = Field(10, ge=1, le=50,
                      description="Maximum results to return")
    
    class Config:
        schema_extra = {
            "example": {
                "query": "metformin",
                "country": "UK",
                "limit": 10
            }
        }


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class OpportunityResponse(BaseModel):
    """Single opportunity/prescriber response"""
    rank: int
    prescriber_id: str
    prescriber_name: str
    location: Optional[str]
    current_volume: int
    opportunity_score: float
    recommendations: List[str]


class MarketSummaryResponse(BaseModel):
    """Market summary statistics"""
    total_prescribers: int
    total_prescriptions: int
    total_cost: float
    avg_prescriptions_per_prescriber: float


class SegmentationResponse(BaseModel):
    """Prescriber segmentation breakdown"""
    by_volume: Dict[str, int]
    by_opportunity: Optional[Dict[str, int]] = None


class DrugInfoResponse(BaseModel):
    """Drug metadata"""
    name: str
    generic_name: str
    therapeutic_area: str
    company: str


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    drug: DrugInfoResponse
    analysis_date: datetime
    country: str
    region: Optional[str]
    period: str
    market_summary: MarketSummaryResponse
    top_opportunities: List[OpportunityResponse]
    segments: SegmentationResponse
    
    class Config:
        schema_extra = {
            "example": {
                "drug": {
                    "name": "Inclisiran",
                    "generic_name": "inclisiran",
                    "therapeutic_area": "Cardiovascular - Lipid Management",
                    "company": "Novartis"
                },
                "analysis_date": "2026-02-04T10:30:00",
                "country": "UK",
                "region": None,
                "period": "2025-10-01",
                "market_summary": {
                    "total_prescribers": 4520,
                    "total_prescriptions": 45230,
                    "total_cost": 12500000.0,
                    "avg_prescriptions_per_prescriber": 10.01
                },
                "top_opportunities": [
                    {
                        "rank": 1,
                        "prescriber_id": "Y12345",
                        "prescriber_name": "High Street Medical",
                        "location": "Greater Manchester",
                        "current_volume": 450,
                        "opportunity_score": 1523.5,
                        "recommendations": [
                            "⭐ KEY ACCOUNT: Maintain strong relationship",
                            "🎓 Invite to advisory board or speaker program"
                        ]
                    }
                ],
                "segments": {
                    "by_volume": {
                        "High Prescribers": 120,
                        "Medium Prescribers": 580,
                        "Low Prescribers": 1200,
                        "Non-Prescribers": 2620
                    }
                }
            }
        }


class DrugSearchResultResponse(BaseModel):
    """Single drug search result"""
    id: str
    name: str
    type: str  # chemical, presentation, etc.


class DrugSearchResponse(BaseModel):
    """Drug search results"""
    query: str
    country: str
    results: List[DrugSearchResultResponse]
    count: int


class CountryResponse(BaseModel):
    """Supported country information"""
    code: str
    name: str
    data_source: str
    available: bool


class HealthResponse(BaseModel):
    """API health check response"""
    status: str
    version: str
    timestamp: datetime
    data_sources: Dict[str, str]


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Drug not found",
                "detail": "No drug code found for 'invalid_drug' in UK",
                "timestamp": "2026-02-04T10:30:00"
            }
        }
