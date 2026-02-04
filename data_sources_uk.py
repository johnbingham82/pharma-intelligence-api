#!/usr/bin/env python3
"""
UK Data Source - NHS OpenPrescribing API Adapter
Implements DataSource interface for UK prescribing data
"""
import requests
from typing import List, Dict, Optional
from pharma_intelligence_engine import (
    DataSource, PrescribingData, Prescriber
)

class UKDataSource(DataSource):
    """UK NHS prescribing data via OpenPrescribing API"""
    
    def __init__(self):
        self.base_url = "https://openprescribing.net/api/1.0"
        self.cache = {}
    
    def search_drug(self, name: str) -> List[Dict]:
        """Search for BNF codes by drug name"""
        url = f"{self.base_url}/bnf_code/"
        params = {'q': name, 'format': 'json'}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error searching drug: {e}")
        
        return []
    
    def get_prescribing_data(self, drug_code: str, period: str, 
                           region: Optional[str] = None) -> List[PrescribingData]:
        """Get prescribing data for a drug"""
        url = f"{self.base_url}/spending_by_org/"
        params = {
            'org_type': 'practice',
            'code': drug_code,
            'date': period,
            'format': 'json'
        }
        
        if region:
            params['org'] = region
        
        try:
            response = requests.get(url, params=params, timeout=60)
            if response.status_code != 200:
                print(f"API error: {response.status_code}")
                return []
            
            raw_data = response.json()
            
            # Get practice details for list sizes
            practice_details = self._get_practice_details_batch(
                [p['row_id'] for p in raw_data]
            )
            
            # Convert to PrescribingData objects
            result = []
            for item in raw_data:
                practice_code = item.get('row_id')
                details = practice_details.get(practice_code, {})
                
                prescriber = Prescriber(
                    id=practice_code,
                    name=item.get('row_name', 'Unknown'),
                    type='GP Practice',
                    list_size=details.get('total_list_size')
                )
                
                data = PrescribingData(
                    prescriber=prescriber,
                    drug_code=drug_code,
                    period=period,
                    prescriptions=int(item.get('items', 0)),
                    quantity=float(item.get('quantity', 0)),
                    cost=float(item.get('actual_cost', 0))
                )
                
                result.append(data)
            
            return result
            
        except Exception as e:
            print(f"Error fetching prescribing data: {e}")
            return []
    
    def get_prescriber_details(self, prescriber_ids: List[str]) -> List[Prescriber]:
        """Get detailed prescriber information"""
        # Note: OpenPrescribing doesn't have a batch API, so we fetch all practices
        # and filter. For production, implement caching.
        details = self._get_practice_details_batch(prescriber_ids)
        
        result = []
        for pid, data in details.items():
            prescriber = Prescriber(
                id=pid,
                name=data.get('name', 'Unknown'),
                type='GP Practice',
                list_size=data.get('total_list_size'),
                location=data.get('setting', 'Unknown')
            )
            result.append(prescriber)
        
        return result
    
    def get_latest_period(self) -> str:
        """Get the most recent data period available"""
        # NHS data typically has 2-3 month lag
        # For production, fetch this dynamically from the API
        return "2025-10-01"
    
    def _get_practice_details_batch(self, practice_codes: List[str]) -> Dict[str, Dict]:
        """Internal: Fetch practice details in batch"""
        # Check cache first
        cache_key = 'all_practices'
        if cache_key in self.cache:
            all_practices = self.cache[cache_key]
        else:
            url = f"{self.base_url}/org_details/"
            params = {
                'org_type': 'practice',
                'keys': 'total_list_size,setting',
                'format': 'json'
            }
            
            try:
                response = requests.get(url, params=params, timeout=60)
                if response.status_code == 200:
                    all_practices = response.json()
                    self.cache[cache_key] = all_practices
                else:
                    all_practices = []
            except Exception as e:
                print(f"Error fetching practice details: {e}")
                all_practices = []
        
        # Build lookup dict
        details = {}
        for practice in all_practices:
            code = practice.get('row_id')
            if code in practice_codes:
                details[code] = {
                    'name': practice.get('row_name', 'Unknown'),
                    'total_list_size': practice.get('total_list_size'),
                    'setting': practice.get('setting')
                }
        
        return details
    
    def find_drug_code(self, name: str, prefer_generic: bool = True) -> Optional[str]:
        """
        Helper: Find the best BNF code for a drug name
        
        Args:
            name: Drug name to search
            prefer_generic: Prefer chemical substance codes over branded presentations
            
        Returns:
            BNF code or None
        """
        results = self.search_drug(name)
        
        if not results:
            return None
        
        # Strategy: Prefer 9-character chemical codes (e.g., 0212000AA)
        # over 15-character presentation codes (e.g., 0212000AAAAAAA)
        
        if prefer_generic:
            # Look for chemical codes first (9 chars)
            for result in results:
                code = result.get('id', '')
                result_name = result.get('name', '').lower()
                if len(code) == 9 and '/' not in result_name:
                    return code
        
        # Fallback: any 9-character code
        for result in results:
            code = result.get('id', '')
            if len(code) == 9:
                return code
        
        # Last resort: first result
        return results[0].get('id')
