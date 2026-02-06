#!/usr/bin/env python3
"""
US Data Source - CMS Medicare Part D Prescriber Data Adapter
Implements DataSource interface for US prescribing data

API Documentation: https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers
Coverage: Medicare Part D prescriptions (40M+ beneficiaries, seniors 65+)
"""
import requests
import os
import json
from typing import List, Dict, Optional
from pharma_intelligence_engine import (
    DataSource, PrescribingData, Prescriber
)

class USDataSource(DataSource):
    """US Medicare Part D prescribing data via CMS API"""
    
    def __init__(self):
        # CMS new API base URL
        self.base_url = "https://data.cms.gov/data-api/v1/dataset"
        
        # Main dataset: Medicare Part D Prescribers by Provider and Drug
        # Dataset ID: 9552739e-3d05-4c1b-8eff-ecabf391e2e5
        self.dataset_id = "9552739e-3d05-4c1b-8eff-ecabf391e2e5"
        self.prescriber_drug_endpoint = f"{self.base_url}/{self.dataset_id}/data"
        
        # Drug lookup: Use FDA NDC directory
        self.fda_ndc_url = "https://api.fda.gov/drug/ndc.json"
        
        self.cache = {}
        
        # Load available drugs from cache directory
        self._load_available_drugs()
    
    def _load_available_drugs(self):
        """Load list of available drugs from cache directory"""
        self.available_drugs = {}
        
        try:
            cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
            if not os.path.exists(cache_dir):
                print("⚠️  No cache directory found for US data")
                return
            
            # Scan for drug cache files (us_{drug}_data.json)
            for filename in os.listdir(cache_dir):
                if filename.startswith('us_') and filename.endswith('_data.json') and filename != 'us_state_data.json':
                    # Extract drug name from filename (e.g., us_gabapentin_data.json -> gabapentin)
                    drug_name = filename[3:-10].replace('_', ' ')
                    
                    # Also store the cleaned filename version for exact matching
                    self.available_drugs[drug_name.lower()] = drug_name
                    
            print(f"✓ Loaded {len(self.available_drugs)} drugs from US cache")
            
        except Exception as e:
            print(f"⚠️  Error loading available drugs: {e}")
            self.available_drugs = {}
    
    def search_drug(self, name: str) -> List[Dict]:
        """
        Search for NDC codes by drug name using FDA API
        
        Args:
            name: Drug name (brand or generic)
            
        Returns:
            List of matching drugs with NDC codes
        """
        try:
            # FDA openFDA API
            params = {
                'search': f'generic_name:"{name}" OR brand_name:"{name}"',
                'limit': 50
            }
            
            response = requests.get(self.fda_ndc_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for drug in data.get('results', []):
                    # Extract relevant info
                    generic_name = drug.get('generic_name', 'Unknown')
                    brand_name = drug.get('brand_name', '')
                    ndc = drug.get('product_ndc', 'Unknown')
                    
                    results.append({
                        'id': ndc,
                        'name': f"{brand_name} ({generic_name})" if brand_name else generic_name,
                        'type': 'ndc',
                        'generic_name': generic_name,
                        'brand_name': brand_name
                    })
                
                return results
            else:
                print(f"FDA API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error searching drug: {e}")
            return []
    
    def get_prescribing_data(self, drug_code: str, period: str, 
                           region: Optional[str] = None) -> List[PrescribingData]:
        """
        Get prescribing data for a drug from CMS Medicare Part D
        
        Args:
            drug_code: Generic drug name (CMS uses names, not NDC codes in main API)
            period: Year (e.g., "2022")
            region: Optional state code (e.g., "CA", "NY")
            
        Returns:
            List of PrescribingData objects
        """
        try:
            # CMS new API: fetch data in batches and filter client-side
            # Note: CMS API doesn't support complex server-side filtering yet
            
            all_data = []
            offset = 0
            batch_size = 1000
            max_records = 10000  # Limit total fetch
            
            print(f"Fetching Medicare data for '{drug_code}'...")
            
            # Fetch in batches
            while offset < max_records:
                params = {
                    'size': batch_size,
                    'offset': offset
                }
                
                response = requests.get(
                    self.prescriber_drug_endpoint,
                    params=params,
                    timeout=60
                )
                
                if response.status_code != 200:
                    print(f"CMS API error: {response.status_code}")
                    break
                
                batch_data = response.json()
                if not batch_data:
                    break
                
                # Filter for our drug (case-insensitive)
                matching = [
                    r for r in batch_data 
                    if drug_code.lower() in r.get('Gnrc_Name', '').lower()
                ]
                
                # Apply region filter if specified
                if region:
                    matching = [
                        r for r in matching 
                        if r.get('Prscrbr_State_Abrvtn', '').upper() == region.upper()
                    ]
                
                all_data.extend(matching)
                
                # If we found enough matches, stop
                if len(all_data) >= 1000:
                    print(f"Found {len(all_data)} matching prescribers")
                    break
                
                offset += batch_size
                
                # If batch was less than batch_size, we've reached the end
                if len(batch_data) < batch_size:
                    break
            
            if not all_data:
                print(f"No Medicare data found for '{drug_code}'")
                return []
            
            # Sort by total claims (descending)
            all_data.sort(key=lambda x: int(x.get('Tot_Clms', 0) or 0), reverse=True)
            
            raw_data = all_data
            
            print(f"✅ Found {len(raw_data)} Medicare prescribers for {drug_code}")
            
            # Convert to PrescribingData objects
            result = []
            for item in raw_data:
                # Create prescriber object
                prescriber = Prescriber(
                    id=item.get('Prscrbr_NPI', 'unknown'),
                    name=f"{item.get('Prscrbr_Last_Org_Name', '')} {item.get('Prscrbr_First_Name', '')}".strip(),
                    type=item.get('Prscrbr_Type', 'Prescriber'),
                    location=f"{item.get('Prscrbr_City', '')}, {item.get('Prscrbr_State_Abrvtn', '')}",
                    specialty=item.get('Prscrbr_Type')
                )
                
                # Extract prescribing metrics
                # Handle empty strings and missing values
                total_claims = int(item.get('Tot_Clms') or 0)
                total_drug_cost = float(item.get('Tot_Drug_Cst') or 0)
                beneficiary_count = int(item.get('Tot_Benes') or 0)
                
                # Create prescribing data object
                data = PrescribingData(
                    prescriber=prescriber,
                    drug_code=drug_code,
                    period=period,
                    prescriptions=total_claims,
                    quantity=total_claims,  # CMS doesn't separate quantity
                    cost=total_drug_cost,
                    patients=beneficiary_count
                )
                
                result.append(data)
            
            return result
            
        except Exception as e:
            print(f"Error fetching prescribing data: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_prescriber_details(self, prescriber_ids: List[str]) -> List[Prescriber]:
        """
        Get detailed prescriber information by NPI
        
        Args:
            prescriber_ids: List of NPI numbers
            
        Returns:
            List of Prescriber objects
        """
        # CMS Medicare Part D data already includes prescriber details
        # This would be used for enrichment if needed
        
        result = []
        for npi in prescriber_ids:
            # Could fetch from NPI Registry API if needed
            # For now, return basic info (enriched during get_prescribing_data)
            prescriber = Prescriber(
                id=npi,
                name="Unknown",
                type="Prescriber"
            )
            result.append(prescriber)
        
        return result
    
    def get_latest_period(self) -> str:
        """
        Get the most recent data period available
        
        Returns:
            Year as string (e.g., "2022")
        """
        # CMS Part D data is typically 2 years behind
        # Check their data catalog for latest year
        # For now, return 2022 (most recent as of 2024)
        return "2022"
    
    def find_drug_code(self, name: str, prefer_generic: bool = True) -> Optional[str]:
        """
        Helper: Find the best drug name for CMS queries (from cache files)
        
        Args:
            name: Drug name to search
            prefer_generic: Return generic name if True, brand if False
            
        Returns:
            Drug name that matches a cache file, or None if not found
        """
        # Clean the name for querying
        clean_name = name.lower().strip().replace('_', ' ')
        
        # Check if drug exists in our cache
        if clean_name in self.available_drugs:
            return self.available_drugs[clean_name]
        
        # Try partial matching for common abbreviations/variations
        for cached_drug in self.available_drugs:
            if clean_name in cached_drug or cached_drug in clean_name:
                print(f"✓ Matched '{name}' to cached drug '{cached_drug}'")
                return self.available_drugs[cached_drug]
        
        # Not found in cache
        print(f"⚠️  Drug '{name}' not found in US cache (available: {len(self.available_drugs)} drugs)")
        return None
    
    def get_state_summary(self, drug_name: str, year: str = "2022") -> Dict:
        """
        Get state-level summary for a drug
        
        Useful for geographic analysis
        
        Args:
            drug_name: Generic drug name
            year: Year to analyze
            
        Returns:
            Dict with state-level aggregates
        """
        try:
            params = {
                '$where': f"LOWER(gnrc_name) LIKE '%{drug_name.lower()}%' AND year = {year}",
                '$select': 'prscrbr_state_abrvtn, SUM(tot_clms) as total_claims, SUM(tot_drug_cst) as total_cost, COUNT(*) as prescriber_count',
                '$group': 'prscrbr_state_abrvtn',
                '$order': 'total_claims DESC',
                '$limit': 100
            }
            
            response = requests.get(
                self.prescriber_drug_endpoint,
                params=params,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"Error fetching state summary: {e}")
            return {}
    
    def get_specialty_breakdown(self, drug_name: str, year: str = "2022") -> Dict:
        """
        Get prescriber specialty breakdown for a drug
        
        Useful for understanding prescriber types
        
        Args:
            drug_name: Generic drug name
            year: Year to analyze
            
        Returns:
            Dict with specialty-level aggregates
        """
        try:
            params = {
                '$where': f"LOWER(gnrc_name) LIKE '%{drug_name.lower()}%' AND year = {year}",
                '$select': 'prscrbr_type, SUM(tot_clms) as total_claims, COUNT(*) as prescriber_count',
                '$group': 'prscrbr_type',
                '$order': 'total_claims DESC',
                '$limit': 50
            }
            
            response = requests.get(
                self.prescriber_drug_endpoint,
                params=params,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            print(f"Error fetching specialty breakdown: {e}")
            return {}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def test_us_data_source():
    """Quick test of US data source"""
    print("Testing US Data Source (CMS Medicare Part D)\n")
    
    us_data = USDataSource()
    
    # Test 1: Drug search (FDA API)
    print("="*80)
    print("TEST 1: Search for drugs")
    print("="*80)
    results = us_data.search_drug("metformin")
    print(f"Found {len(results)} results for 'metformin'")
    if results:
        print(f"First result: {results[0]['name']} (NDC: {results[0]['id']})")
    
    # Test 2: Get prescribing data
    print("\n" + "="*80)
    print("TEST 2: Get prescribing data for metformin")
    print("="*80)
    drug_code = us_data.find_drug_code("metformin")
    print(f"Using drug code: {drug_code}")
    
    prescribing = us_data.get_prescribing_data(
        drug_code=drug_code,
        period="2022",
        region=None  # All states
    )
    
    if prescribing:
        print(f"\n✅ Found prescribing data for {len(prescribing)} prescribers")
        print(f"\nTop 5 prescribers:")
        for i, p in enumerate(prescribing[:5], 1):
            print(f"{i}. {p.prescriber.name} ({p.prescriber.location})")
            print(f"   Claims: {p.prescriptions:,} | Cost: ${p.cost:,.0f} | Patients: {p.patients}")
    else:
        print("❌ No prescribing data found")
    
    # Test 3: State summary
    print("\n" + "="*80)
    print("TEST 3: State-level summary")
    print("="*80)
    state_summary = us_data.get_state_summary("metformin", "2022")
    if state_summary:
        print(f"Found data for {len(state_summary)} states")
        print("\nTop 5 states by volume:")
        for i, state in enumerate(state_summary[:5], 1):
            print(f"{i}. {state.get('prscrbr_state_abrvtn', 'Unknown')}: "
                  f"{int(state.get('total_claims', 0)):,} claims, "
                  f"{int(state.get('prescriber_count', 0)):,} prescribers")


if __name__ == "__main__":
    test_us_data_source()
