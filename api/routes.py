"""
API Routes
REST endpoints for pharma intelligence platform
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
import sys
import os

# Add parent directory to path to import engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models import (
    AnalysisRequest, AnalysisResponse, DrugSearchRequest, DrugSearchResponse,
    DrugSearchResultResponse, CountryResponse, HealthResponse, ErrorResponse,
    OpportunityResponse, MarketSummaryResponse, SegmentationResponse, DrugInfoResponse
)

from pharma_intelligence_engine import (
    PharmaIntelligenceEngine, create_drug, 
    MarketShareScorer, SimpleVolumeScorer
)
from data_sources_uk import UKDataSource
from data_sources_us import USDataSource
from data_sources_eu import EUDataSource
from data_sources_au import AustraliaDataSource

router = APIRouter()

# Initialize data sources (in production, use dependency injection)
DATA_SOURCES = {
    'UK': UKDataSource(),
    'US': USDataSource(),
    'FR': EUDataSource('FR'),
    'DE': EUDataSource('DE'),
    'NL': EUDataSource('NL'),
    'IT': EUDataSource('IT'),
    'ES': EUDataSource('ES'),
    'AU': AustraliaDataSource()
}


def get_data_source(country: str):
    """Get data source for country"""
    if country not in DATA_SOURCES:
        raise HTTPException(
            status_code=400,
            detail=f"Country '{country}' not supported. Available: {', '.join(DATA_SOURCES.keys())}"
        )
    return DATA_SOURCES[country]


def get_scorer(scorer_name: str):
    """Get scorer instance by name"""
    scorers = {
        'simple_volume': SimpleVolumeScorer(),
        'market_share': MarketShareScorer()
    }
    return scorers.get(scorer_name, MarketShareScorer())


@router.get("/", tags=["General"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Pharma Intelligence API",
        "version": "1.0.0",
        "description": "Drug analysis platform for pharmaceutical targeting",
        "docs": "/docs",
        "health": "/health"
    }


@router.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(),
        data_sources={
            country: "available" for country in DATA_SOURCES.keys()
        }
    )


@router.get("/countries", response_model=list[CountryResponse], tags=["Reference"])
async def list_countries():
    """List supported countries and data sources"""
    countries = [
        CountryResponse(
            code="UK",
            name="United Kingdom",
            data_source="NHS OpenPrescribing (Prescriber-level)",
            available=True
        ),
        CountryResponse(
            code="US",
            name="United States",
            data_source="CMS Medicare Part D (Prescriber-level)",
            available=True
        ),
        CountryResponse(
            code="FR",
            name="France",
            data_source="Open Data Assurance Maladie (Regional/Aggregate)",
            available=True
        ),
        CountryResponse(
            code="DE",
            name="Germany",
            data_source="GKV Reports (Regional/Aggregate)",
            available=True
        ),
        CountryResponse(
            code="NL",
            name="Netherlands",
            data_source="GIP Databank (Regional/Aggregate)",
            available=True
        ),
        CountryResponse(
            code="IT",
            name="Italy",
            data_source="AIFA Open Data (Regional/Aggregate)",
            available=True
        ),
        CountryResponse(
            code="ES",
            name="Spain",
            data_source="Ministry of Health - BIFAP (Regional/Aggregate)",
            available=True
        ),
        CountryResponse(
            code="AU",
            name="Australia",
            data_source="PBS - AIHW Monthly Data (State/Territory level)",
            available=True
        )
    ]
    return countries


@router.post("/drugs/search", response_model=DrugSearchResponse, tags=["Drugs"])
async def search_drugs(request: DrugSearchRequest):
    """
    Search for drugs by name in a specific country
    
    Returns matching drug codes and names that can be used for analysis
    """
    try:
        data_source = get_data_source(request.country)
        
        # Search for drugs
        results = data_source.search_drug(request.query)
        
        if not results:
            return DrugSearchResponse(
                query=request.query,
                country=request.country,
                results=[],
                count=0
            )
        
        # Limit results
        limited_results = results[:request.limit]
        
        # Format response
        formatted_results = [
            DrugSearchResultResponse(
                id=r.get('id', 'unknown'),
                name=r.get('name', 'Unknown'),
                type=r.get('type', 'unknown')
            )
            for r in limited_results
        ]
        
        return DrugSearchResponse(
            query=request.query,
            country=request.country,
            results=formatted_results,
            count=len(formatted_results)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/drugs/lookup", tags=["Drugs"])
async def lookup_drug(
    name: str = Query(..., description="Drug name to lookup"),
    country: str = Query(..., pattern="^[A-Z]{2}$", description="Country code")
):
    """
    Quick drug code lookup by name
    
    Returns the best matching drug code for analysis
    """
    try:
        data_source = get_data_source(country)
        
        # Find drug code
        drug_code = data_source.find_drug_code(name)
        
        if not drug_code:
            raise HTTPException(
                status_code=404,
                detail=f"No drug code found for '{name}' in {country}"
            )
        
        return {
            "name": name,
            "country": country,
            "drug_code": drug_code,
            "ready_for_analysis": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lookup failed: {str(e)}")


@router.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_drug(request: AnalysisRequest):
    """
    Analyze prescribing patterns for a drug
    
    This is the core endpoint - returns comprehensive targeting analysis
    including top opportunities, segmentation, and recommendations
    """
    try:
        # Get data source for country
        data_source = get_data_source(request.country)
        
        # Find drug code
        drug_code = data_source.find_drug_code(request.drug_name)
        
        if not drug_code:
            raise HTTPException(
                status_code=404,
                detail=f"Drug '{request.drug_name}' not found in {request.country}"
            )
        
        # Create drug object
        drug = create_drug(
            name=request.drug_name.title(),
            generic_name=request.drug_name.lower(),
            therapeutic_area="Auto-detected",  # TODO: Add therapeutic area detection
            company=request.company,
            country_codes={request.country: drug_code}
        )
        
        # Get scorer
        scorer = get_scorer(request.scorer)
        
        # Initialize engine
        engine = PharmaIntelligenceEngine(
            data_source=data_source,
            scorer=scorer
        )
        
        # Run analysis
        report = engine.analyze_drug(
            drug=drug,
            country=request.country,
            region=request.region,
            top_n=request.top_n
        )
        
        # Convert to response model
        response = AnalysisResponse(
            drug=DrugInfoResponse(**report['drug']),
            analysis_date=datetime.fromisoformat(report['analysis_date']),
            country=report['country'],
            region=report.get('region'),
            period=report['period'],
            market_summary=MarketSummaryResponse(**report['market_summary']),
            top_opportunities=[
                OpportunityResponse(**opp)
                for opp in report['top_opportunities']
            ],
            segments=SegmentationResponse(**report['segments'])
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/analyze/status/{analysis_id}", tags=["Analysis"])
async def get_analysis_status(analysis_id: str):
    """
    Get status of a long-running analysis (future feature)
    
    For now, all analyses are synchronous
    """
    # TODO: Implement async analysis with job queue
    raise HTTPException(
        status_code=501,
        detail="Async analysis not yet implemented. All analyses are currently synchronous."
    )


@router.get("/country/{country_code}", tags=["Reference"])
async def get_country_detail(country_code: str):
    """
    Get detailed country information and metadata
    
    Returns country metadata including:
    - Population and market size
    - Data source information
    - Currency and update frequency
    """
    country = country_code.upper()
    
    try:
        # Verify country is supported
        if country not in DATA_SOURCES:
            raise HTTPException(
                status_code=404,
                detail=f"Country '{country}' not supported"
            )
        
        # Country metadata
        country_info = {
            'UK': {
                'name': 'United Kingdom',
                'population': '67M',
                'market_value': '£20B',
                'has_real_data': True,
                'data_source': 'NHS OpenPrescribing',
                'update_frequency': 'Daily',
                'currency': 'GBP'
            },
            'US': {
                'name': 'United States',
                'population': '335M',
                'market_value': '$370B',
                'has_real_data': True,
                'data_source': 'CMS Medicare Part D',
                'update_frequency': 'Quarterly',
                'currency': 'USD'
            },
            'AU': {
                'name': 'Australia',
                'population': '26M',
                'market_value': 'A$16B',
                'has_real_data': True,
                'data_source': 'PBS - AIHW Monthly Data',
                'update_frequency': 'Monthly',
                'currency': 'AUD'
            },
            'FR': {
                'name': 'France',
                'population': '67M',
                'market_value': '€37B',
                'has_real_data': False,
                'data_source': 'Framework (Open Data Assurance Maladie planned)',
                'update_frequency': 'Annual',
                'currency': 'EUR'
            },
            'DE': {
                'name': 'Germany',
                'population': '83M',
                'market_value': '€48B',
                'has_real_data': False,
                'data_source': 'Framework (GKV Reports planned)',
                'update_frequency': 'Annual',
                'currency': 'EUR'
            },
            'IT': {
                'name': 'Italy',
                'population': '60M',
                'market_value': '€30B',
                'has_real_data': False,
                'data_source': 'Framework (AIFA Open Data planned)',
                'update_frequency': 'Annual',
                'currency': 'EUR'
            },
            'ES': {
                'name': 'Spain',
                'population': '47M',
                'market_value': '€23B',
                'has_real_data': False,
                'data_source': 'Framework (BIFAP planned)',
                'update_frequency': 'Annual',
                'currency': 'EUR'
            },
            'NL': {
                'name': 'Netherlands',
                'population': '17.5M',
                'market_value': '€6.5B',
                'has_real_data': False,
                'data_source': 'Framework (GIP Databank planned)',
                'update_frequency': 'Annual',
                'currency': 'EUR'
            }
        }
        
        info = country_info.get(country, {})
        
        return {
            'code': country,
            'name': info.get('name', country),
            'population': info.get('population', 'Unknown'),
            'market_value': info.get('market_value', 'Unknown'),
            'has_real_data': info.get('has_real_data', False),
            'data_source': info.get('data_source'),
            'update_frequency': info.get('update_frequency'),
            'currency': info.get('currency', 'USD'),
            'regions': [],  # TODO: Implement regional data fetching
            'monthly_data': None,
            'top_drugs': None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch country data: {str(e)}"
        )
