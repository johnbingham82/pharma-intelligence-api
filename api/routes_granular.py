"""
Granular Data Routes
Practice-level and postcode-level endpoints for detailed analysis
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_sources_uk import UKDataSource
from data_sources_us import USDataSource
from data_sources_au import AustraliaDataSource

router = APIRouter()

# Initialize data sources
DATA_SOURCES = {
    'UK': UKDataSource(),
    'US': USDataSource(),
    'AU': AustraliaDataSource()
}


@router.get("/country/{country_code}/practices", tags=["Granular Data"])
async def get_practice_data(
    country_code: str,
    drug: str = Query(..., description="Drug name to query"),
    region: Optional[str] = Query(None, description="Filter by region (optional)"),
    limit: int = Query(1000, description="Maximum practices to return")
):
    """
    Get practice-level prescribing data for granular visualization
    
    Returns individual GP practices/prescribers with:
    - Practice name and code
    - Geographic location (when available)
    - Prescription volume
    - Cost data
    - Practice size
    
    This endpoint provides the granular data needed for detailed maps
    showing individual practices as markers or small polygons.
    """
    country = country_code.upper()
    
    if country not in DATA_SOURCES:
        raise HTTPException(
            status_code=404,
            detail=f"Country '{country}' not supported for granular data"
        )
    
    data_source = DATA_SOURCES[country]
    
    try:
        # Find drug code
        drug_code = data_source.find_drug_code(drug)
        if not drug_code:
            raise HTTPException(
                status_code=404,
                detail=f"Drug '{drug}' not found in {country}"
            )
        
        # Get latest period
        period = data_source.get_latest_period()
        
        # Get practice-level data
        prescribing_data = data_source.get_prescribing_data(
            drug_code=drug_code,
            period=period,
            region=region
        )
        
        if not prescribing_data:
            return {
                'country': country,
                'drug': drug,
                'region': region,
                'period': period,
                'practices': [],
                'count': 0
            }
        
        # Sort by volume and limit
        prescribing_data.sort(key=lambda x: x.prescriptions, reverse=True)
        prescribing_data = prescribing_data[:limit]
        
        # Format response
        practices = []
        for p in prescribing_data:
            practice = {
                'id': p.prescriber.id,
                'name': p.prescriber.name,
                'type': p.prescriber.type,
                'prescriptions': p.prescriptions,
                'cost': p.cost,
                'quantity': p.quantity
            }
            
            # Add optional fields
            if p.prescriber.location:
                practice['location'] = p.prescriber.location
            if p.prescriber.list_size:
                practice['list_size'] = p.prescriber.list_size
            if p.prescriber.specialty:
                practice['specialty'] = p.prescriber.specialty
            
            practices.append(practice)
        
        return {
            'country': country,
            'drug': drug,
            'drug_code': drug_code,
            'region': region,
            'period': period,
            'practices': practices,
            'count': len(practices),
            'total_prescriptions': sum(p['prescriptions'] for p in practices),
            'total_cost': sum(p['cost'] for p in practices)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch practice data: {str(e)}"
        )


@router.get("/country/{country_code}/practices/{practice_id}", tags=["Granular Data"])
async def get_practice_detail(
    country_code: str,
    practice_id: str,
    drug: Optional[str] = Query(None, description="Drug name for prescribing data")
):
    """
    Get detailed information for a specific practice/prescriber
    
    Returns comprehensive data about a single practice including:
    - Practice metadata
    - Prescribing history (if drug specified)
    - Practice characteristics
    """
    country = country_code.upper()
    
    if country not in DATA_SOURCES:
        raise HTTPException(
            status_code=404,
            detail=f"Country '{country}' not supported"
        )
    
    data_source = DATA_SOURCES[country]
    
    try:
        # Get prescriber details
        prescribers = data_source.get_prescriber_details([practice_id])
        
        if not prescribers:
            raise HTTPException(
                status_code=404,
                detail=f"Practice '{practice_id}' not found"
            )
        
        prescriber = prescribers[0]
        
        result = {
            'id': prescriber.id,
            'name': prescriber.name,
            'type': prescriber.type,
            'location': prescriber.location,
            'list_size': prescriber.list_size,
            'specialty': prescriber.specialty
        }
        
        # Add prescribing data if drug specified
        if drug:
            drug_code = data_source.find_drug_code(drug)
            if drug_code:
                period = data_source.get_latest_period()
                prescribing_data = data_source.get_prescribing_data(
                    drug_code=drug_code,
                    period=period
                )
                
                # Find this practice's data
                practice_data = next(
                    (p for p in prescribing_data if p.prescriber.id == practice_id),
                    None
                )
                
                if practice_data:
                    result['prescribing'] = {
                        'drug': drug,
                        'drug_code': drug_code,
                        'period': period,
                        'prescriptions': practice_data.prescriptions,
                        'cost': practice_data.cost,
                        'quantity': practice_data.quantity
                    }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch practice detail: {str(e)}"
        )
