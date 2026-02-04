#!/usr/bin/env python3
"""
Australia Data Source - PBS (Pharmaceutical Benefits Scheme) - REAL DATA
Implements DataSource interface for Australian prescribing data

Data Source: PBS via AIHW + Department of Health
Real Data: July 2024 - June 2025 (updated monthly)
Coverage: ~90% of all Australian prescriptions
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from pharma_intelligence_engine import (
    DataSource, PrescribingData, Prescriber
)


class AustraliaDataSource(DataSource):
    """
    Australian PBS prescribing data - REAL DATA with state distribution
    
    Uses real national PBS data (9.79M metformin prescriptions, $320M AUD)
    distributed by state using demographic factors
    
    8 States/Territories: NSW, VIC, QLD, WA, SA, TAS, ACT, NT
    """
    
    def __init__(self, data_file='pbs_data/pbs_metformin_real_data.json'):
        self.data_file = data_file
        self.pbs_data = None
        self.cache = {}
        
        # Load real PBS data
        self._load_pbs_data()
        
        # State/Territory configuration (from PBS data)
        self.states = self.pbs_data['state_model'] if self.pbs_data else {}
        self.total_population = sum(s['population'] for s in self.states.values())
    
    def _load_pbs_data(self):
        """Load real PBS data from JSON file"""
        data_path = os.path.join(os.path.dirname(__file__), self.data_file)
        
        try:
            with open(data_path, 'r') as f:
                self.pbs_data = json.load(f)
            
            print(f"✓ Loaded real PBS data from {data_path}")
            print(f"  Period: {self.pbs_data['metadata']['period_start']} to {self.pbs_data['metadata']['period_end']}")
            print(f"  States: {len(self.pbs_data['state_model'])}")
            print(f"  Months: {len(list(self.pbs_data['monthly_data'].values())[0])}")
            
        except FileNotFoundError:
            print(f"⚠️  PBS data file not found: {data_path}")
            print(f"   Run: python3 prepare_pbs_real_data.py")
            self.pbs_data = None
        except Exception as e:
            print(f"⚠️  Error loading PBS data: {e}")
            self.pbs_data = None
    
    def search_drug(self, name: str) -> List[Dict]:
        """
        Search for drug codes by name
        
        Australia uses ATC codes (WHO standard) + PBS codes
        """
        # Common ATC codes for major drugs
        atc_lookup = {
            'metformin': [
                {'id': 'A10BA02', 'name': 'Metformin', 'type': 'atc', 'pbs_code': '2338B'},
            ],
            'atorvastatin': [
                {'id': 'C10AA05', 'name': 'Atorvastatin', 'type': 'atc', 'pbs_code': '8275K'},
            ],
            'inclisiran': [
                {'id': 'C10AX16', 'name': 'Inclisiran', 'type': 'atc', 'pbs_code': 'NEW'},
            ],
            'rosuvastatin': [
                {'id': 'C10AA07', 'name': 'Rosuvastatin', 'type': 'atc', 'pbs_code': '8913L'},
            ],
            'apixaban': [
                {'id': 'B01AF02', 'name': 'Apixaban', 'type': 'atc', 'pbs_code': '10447W'},
            ],
            'empagliflozin': [
                {'id': 'A10BK03', 'name': 'Empagliflozin', 'type': 'atc', 'pbs_code': '11082T'},
            ]
        }
        
        name_lower = name.lower()
        if name_lower in atc_lookup:
            return atc_lookup[name_lower]
        
        # Fuzzy match
        for drug, codes in atc_lookup.items():
            if name_lower in drug or drug in name_lower:
                return codes
        
        return []
    
    def get_prescribing_data(self, drug_code: str, period: str,
                           region: Optional[str] = None) -> List[PrescribingData]:
        """
        Get PBS prescribing data by State/Territory - REAL DATA
        
        Args:
            drug_code: ATC code or drug name
            period: Year-Month (e.g., "2024-10") or Year (e.g., "2024")
            region: Optional state code (NSW, VIC, etc.)
            
        Returns:
            List of PrescribingData objects (one per state/territory)
        """
        if not self.pbs_data:
            print(f"⚠️  No PBS data loaded - using fallback")
            return self._fallback_data(drug_code, period, region)
        
        # Check if drug is metformin (we only have real data for metformin currently)
        if drug_code.upper() not in ['METFORMIN', 'A10BA02']:
            print(f"ℹ️  Real data only available for metformin, using estimation for {drug_code}")
            return self._estimate_for_other_drugs(drug_code, period, region)
        
        # Parse period (support YYYY or YYYY-MM format)
        if '-' in period:
            year, month = period.split('-')
            month_key = f"{year}{month}"
        else:
            # If just year, use most recent month in that year
            year = period
            month_key = None
        
        # Get data from PBS dataset
        monthly_data = self.pbs_data['monthly_data']
        
        # If specific month requested
        if month_key:
            if month_key not in list(monthly_data.values())[0]:
                print(f"⚠️  Month {month_key} not in dataset, using latest")
                month_key = sorted(list(monthly_data.values())[0].keys())[-1]
        else:
            # Use latest month in year or overall latest
            available_months = sorted(list(monthly_data.values())[0].keys())
            year_months = [m for m in available_months if m.startswith(year)]
            month_key = year_months[-1] if year_months else available_months[-1]
        
        print(f"ℹ️  Using REAL PBS data for month: {month_key}")
        
        result = []
        for state_code, state_info in self.states.items():
            if region and region.upper() != state_code:
                continue
            
            # Get real data for this state and month
            state_data = monthly_data[state_code][month_key]
            
            prescriber = Prescriber(
                id=f"AU-{state_code}",
                name=f"State: {state_info['name']}",
                type="State/Territory",
                location=f"{state_info['name']}, Australia"
            )
            
            prescribing = PrescribingData(
                prescriber=prescriber,
                drug_code=drug_code,
                period=f"{month_key[:4]}-{month_key[4:]}",
                prescriptions=state_data['prescriptions'],
                quantity=state_data['prescriptions'] * 60,  # Assume 60 tablets per script
                cost=state_data['cost']  # Cost in AUD (real from PBS)
            )
            
            result.append(prescribing)
        
        return result
    
    def _estimate_for_other_drugs(self, drug_code: str, period: str, region: Optional[str]) -> List[PrescribingData]:
        """Estimate data for other drugs based on metformin patterns"""
        # Use metformin as baseline, scale by typical drug usage
        scaling_factors = {
            'atorvastatin': 1.2,  # More common than metformin
            'rosuvastatin': 0.8,  # Less common
            'apixaban': 0.3,      # Much less common
            'empagliflozin': 0.2, # Newer drug
        }
        
        # Get metformin data
        metformin_data = self.get_prescribing_data('metformin', period, region)
        
        # Find scaling factor
        drug_lower = drug_code.lower()
        scale = 1.0
        for drug, factor in scaling_factors.items():
            if drug in drug_lower:
                scale = factor
                break
        
        # Scale metformin data
        result = []
        for met_data in metformin_data:
            scaled = PrescribingData(
                prescriber=met_data.prescriber,
                drug_code=drug_code,
                period=met_data.period,
                prescriptions=int(met_data.prescriptions * scale),
                quantity=int(met_data.quantity * scale),
                cost=met_data.cost * scale
            )
            result.append(scaled)
        
        return result
    
    def _fallback_data(self, drug_code: str, period: str, region: Optional[str]) -> List[PrescribingData]:
        """Fallback to generated data if real PBS data not available"""
        print(f"⚠️  Using fallback generated data")
        
        # Basic population-based generation
        base_rate = 25  # prescriptions per 1,000 population per year
        
        regional_factors = {
            'NSW': 1.05, 'VIC': 1.02, 'QLD': 1.10, 'WA': 0.95,
            'SA': 1.08, 'TAS': 1.15, 'ACT': 0.85, 'NT': 0.90
        }
        
        cost_per_rx = 42.50
        quantity_per_rx = 60
        
        result = []
        for state_code, factor in regional_factors.items():
            if region and region.upper() != state_code:
                continue
            
            population = {
                'NSW': 8166000, 'VIC': 6613000, 'QLD': 5185000, 'WA': 2667000,
                'SA': 1771000, 'TAS': 541000, 'ACT': 431000, 'NT': 246000
            }[state_code]
            
            annual_prescriptions = int((population / 1000) * base_rate * factor)
            
            prescriber = Prescriber(
                id=f"AU-{state_code}",
                name=f"State: {state_code}",
                type="State/Territory",
                location=f"{state_code}, Australia"
            )
            
            prescribing = PrescribingData(
                prescriber=prescriber,
                drug_code=drug_code,
                period=period,
                prescriptions=annual_prescriptions,
                quantity=annual_prescriptions * quantity_per_rx,
                cost=annual_prescriptions * cost_per_rx
            )
            
            result.append(prescribing)
        
        return result
    
    def get_prescriber_details(self, prescriber_ids: List[str]) -> List[Prescriber]:
        """Get state/territory details"""
        result = []
        for state_id in prescriber_ids:
            state_code = state_id.replace('AU-', '')
            if state_code in self.states:
                state_info = self.states[state_code]
                prescriber = Prescriber(
                    id=state_id,
                    name=f"State: {state_info['name']}",
                    type="State/Territory",
                    location=f"{state_info['name']}, Australia"
                )
                result.append(prescriber)
        return result
    
    def get_latest_period(self) -> str:
        """
        Get most recent data period
        
        PBS data published monthly with ~2 month lag
        """
        if self.pbs_data:
            # Get latest month from data
            sample_state = list(self.pbs_data['monthly_data'].keys())[0]
            latest_month = sorted(self.pbs_data['monthly_data'][sample_state].keys())[-1]
            return f"{latest_month[:4]}-{latest_month[4:]}"
        
        return "2025-06"  # Fallback
    
    def find_drug_code(self, name: str, prefer_generic: bool = True) -> Optional[str]:
        """
        Find ATC code for drug name
        
        Returns ATC code for querying
        """
        results = self.search_drug(name)
        if results:
            return results[0]['id']
        return name  # Use name as-is if no ATC found


# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_australia_real_data():
    """Test Australia PBS data source with REAL DATA"""
    print("="*80)
    print("Testing Australia PBS Data Source - REAL DATA")
    print("="*80)
    
    ds = AustraliaDataSource()
    
    if not ds.pbs_data:
        print(f"\n❌ PBS data not loaded")
        print(f"Run: python3 prepare_pbs_real_data.py")
        return False
    
    print(f"\n✓ PBS data loaded successfully")
    print(f"  Period: {ds.pbs_data['metadata']['period_start']} to {ds.pbs_data['metadata']['period_end']}")
    
    # Test metformin (real data)
    print(f"\n1. Testing metformin (REAL PBS DATA):")
    data = ds.get_prescribing_data('metformin', '2024-10')
    
    if data:
        total_rx = sum(d.prescriptions for d in data)
        total_cost = sum(d.cost for d in data)
        
        print(f"   States: {len(data)}")
        print(f"   Total prescriptions: {total_rx:,}")
        print(f"   Total cost: ${total_cost:,.2f} AUD")
        print(f"\n   Top 3 states:")
        sorted_data = sorted(data, key=lambda d: d.prescriptions, reverse=True)
        for i, d in enumerate(sorted_data[:3], 1):
            print(f"   {i}. {d.prescriber.name}: {d.prescriptions:,} Rx, ${d.cost:,.2f} AUD")
    
    # Test monthly progression
    print(f"\n2. Testing monthly progression (Jul-Dec 2024):")
    months = ['2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
    for month in months:
        month_data = ds.get_prescribing_data('metformin', month)
        total = sum(d.prescriptions for d in month_data)
        print(f"   {month}: {total:,} prescriptions")
    
    # Test state filter
    print(f"\n3. Testing state filter (NSW only):")
    nsw_data = ds.get_prescribing_data('metformin', '2024-10', region='NSW')
    if nsw_data:
        print(f"   ✓ {nsw_data[0].prescriber.name}")
        print(f"   Prescriptions: {nsw_data[0].prescriptions:,}")
        print(f"   Cost: ${nsw_data[0].cost:,.2f} AUD")
    
    print("\n" + "="*80)
    print("✅ Real PBS Data Test Complete")
    print("="*80)
    return True


if __name__ == "__main__":
    test_australia_real_data()
