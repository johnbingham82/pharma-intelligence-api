#!/usr/bin/env python3
"""
EU Data Source - Aggregated Regional Data Adapter
Implements DataSource interface for EU prescribing data

NOTE: Due to GDPR/privacy laws, most EU countries don't publish prescriber-level data.
This adapter provides REGIONAL/AGGREGATED analysis instead.

Supported Countries:
- France (FR): Open Data Assurance Maladie
- Germany (DE): GKV Reports (aggregated)
- Netherlands (NL): GIP Databank (aggregated)
- Italy (IT): AIFA Open Data (aggregated)
- Spain (ES): Ministry of Health - BIFAP (aggregated)

Coverage: Regional analysis, not individual prescriber targeting
"""
import requests
from typing import List, Dict, Optional
from pharma_intelligence_engine import (
    DataSource, PrescribingData, Prescriber
)


class EUDataSource(DataSource):
    """
    EU prescribing data - Regional/Aggregated
    
    IMPORTANT: Returns regional data, not individual prescribers
    Each "prescriber" represents a region/department
    """
    
    def __init__(self, country: str = "FR"):
        """
        Initialize EU data source
        
        Args:
            country: ISO country code (FR, DE, NL)
        """
        self.country = country.upper()
        self.cache = {}
        
        # Country-specific configuration
        self.config = {
            'FR': {
                'name': 'France',
                'data_source': 'Open Data Assurance Maladie',
                'base_url': 'https://data.ameli.fr/api/records/1.0/search/',
                'dataset_id': 'pha_2_med_fra',  # Example dataset
                'level': 'Département',  # Regional level
                'population': 67_000_000
            },
            'DE': {
                'name': 'Germany', 
                'data_source': 'GKV Reports',
                'base_url': None,  # No public API, would use scraped/manual data
                'level': 'Bundesland',  # State level
                'population': 83_000_000
            },
            'NL': {
                'name': 'Netherlands',
                'data_source': 'GIP Databank',
                'base_url': None,  # Requires registration
                'level': 'Province',
                'population': 17_500_000
            },
            'IT': {
                'name': 'Italy',
                'data_source': 'AIFA Open Data',
                'base_url': 'https://www.aifa.gov.it/en/open-data',
                'dataset_id': 'osmed',  # OsMed dataset
                'level': 'Regione',  # Regional level (20 regions)
                'population': 60_000_000
            },
            'ES': {
                'name': 'Spain',
                'data_source': 'Ministry of Health - BIFAP',
                'base_url': 'https://www.sanidad.gob.es/estadEstudios/estadisticas/estadisticas/home.htm',
                'dataset_id': 'bifap',  # BIFAP database
                'level': 'Comunidad Autónoma',  # Autonomous community level (17 regions)
                'population': 47_400_000
            }
        }
        
        if self.country not in self.config:
            raise ValueError(f"Country {country} not supported. Available: FR, DE, NL, IT, ES")
    
    def search_drug(self, name: str) -> List[Dict]:
        """
        Search for drug codes by name
        
        EU uses ATC codes (Anatomical Therapeutic Chemical Classification)
        """
        # For France, could use Open Medic API
        # For now, return mock data showing ATC structure
        
        # Common ATC codes (would fetch from API in production)
        atc_lookup = {
            'metformin': [
                {'id': 'A10BA02', 'name': 'Metformin', 'type': 'atc'},
            ],
            'atorvastatin': [
                {'id': 'C10AA05', 'name': 'Atorvastatin', 'type': 'atc'},
            ],
            'inclisiran': [
                {'id': 'C10AX16', 'name': 'Inclisiran', 'type': 'atc'},
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
        Get REGIONAL prescribing data (not individual prescribers)
        
        Args:
            drug_code: ATC code or drug name
            period: Year (e.g., "2022")
            region: Optional region filter (département code for FR)
            
        Returns:
            List of PrescribingData objects (one per region)
        """
        if self.country == 'FR':
            return self._get_france_data(drug_code, period, region)
        elif self.country == 'DE':
            return self._get_germany_data(drug_code, period, region)
        elif self.country == 'NL':
            return self._get_netherlands_data(drug_code, period, region)
        elif self.country == 'IT':
            return self._get_italy_data(drug_code, period, region)
        elif self.country == 'ES':
            return self._get_spain_data(drug_code, period, region)
        else:
            return []
    
    def _get_france_data(self, drug_code: str, period: str, 
                        region: Optional[str] = None) -> List[PrescribingData]:
        """Get France regional data from Open Data Assurance Maladie"""
        
        # NOTE: This is a MOCK implementation
        # In production, would fetch from data.ameli.fr API
        
        print(f"⚠️  MOCK DATA: France regional analysis for {drug_code}")
        print(f"   Real implementation requires data.ameli.fr dataset configuration")
        
        # Mock regional data for demonstration
        mock_regions = [
            {'code': '75', 'name': 'Paris', 'prescriptions': 125000, 'cost': 5200000},
            {'code': '13', 'name': 'Bouches-du-Rhône', 'prescriptions': 98000, 'cost': 4100000},
            {'code': '69', 'name': 'Rhône', 'prescriptions': 87000, 'cost': 3600000},
            {'code': '59', 'name': 'Nord', 'prescriptions': 82000, 'cost': 3400000},
            {'code': '33', 'name': 'Gironde', 'prescriptions': 76000, 'cost': 3200000},
        ]
        
        result = []
        for region_data in mock_regions:
            if region and region != region_data['code']:
                continue
            
            prescriber = Prescriber(
                id=f"FR-{region_data['code']}",
                name=f"Département {region_data['name']}",
                type="Region",
                location=f"{region_data['name']}, France"
            )
            
            data = PrescribingData(
                prescriber=prescriber,
                drug_code=drug_code,
                period=period,
                prescriptions=region_data['prescriptions'],
                quantity=region_data['prescriptions'],
                cost=region_data['cost']
            )
            
            result.append(data)
        
        return result
    
    def _get_germany_data(self, drug_code: str, period: str,
                         region: Optional[str] = None) -> List[PrescribingData]:
        """Get Germany regional data from GKV reports"""
        
        print(f"⚠️  MOCK DATA: Germany state-level analysis for {drug_code}")
        print(f"   Real implementation requires GKV report parsing")
        
        # Mock state-level data
        mock_states = [
            {'code': 'NW', 'name': 'Nordrhein-Westfalen', 'prescriptions': 320000, 'cost': 13500000},
            {'code': 'BY', 'name': 'Bayern', 'prescriptions': 285000, 'cost': 12000000},
            {'code': 'BW', 'name': 'Baden-Württemberg', 'prescriptions': 240000, 'cost': 10100000},
        ]
        
        result = []
        for state in mock_states:
            prescriber = Prescriber(
                id=f"DE-{state['code']}",
                name=f"Bundesland {state['name']}",
                type="State",
                location=f"{state['name']}, Germany"
            )
            
            data = PrescribingData(
                prescriber=prescriber,
                drug_code=drug_code,
                period=period,
                prescriptions=state['prescriptions'],
                quantity=state['prescriptions'],
                cost=state['cost']
            )
            
            result.append(data)
        
        return result
    
    def _get_netherlands_data(self, drug_code: str, period: str,
                            region: Optional[str] = None) -> List[PrescribingData]:
        """Get Netherlands regional data from GIP Databank"""
        
        print(f"⚠️  MOCK DATA: Netherlands province-level analysis for {drug_code}")
        print(f"   Real implementation requires GIP Databank API integration")
        
        # Mock province data
        mock_provinces = [
            {'code': 'ZH', 'name': 'Zuid-Holland', 'prescriptions': 78000, 'cost': 3300000},
            {'code': 'NH', 'name': 'Noord-Holland', 'prescriptions': 65000, 'cost': 2750000},
            {'code': 'NB', 'name': 'Noord-Brabant', 'prescriptions': 54000, 'cost': 2280000},
        ]
        
        result = []
        for province in mock_provinces:
            prescriber = Prescriber(
                id=f"NL-{province['code']}",
                name=f"Province {province['name']}",
                type="Province",
                location=f"{province['name']}, Netherlands"
            )
            
            data = PrescribingData(
                prescriber=prescriber,
                drug_code=drug_code,
                period=period,
                prescriptions=province['prescriptions'],
                quantity=province['prescriptions'],
                cost=province['cost']
            )
            
            result.append(data)
        
        return result
    
    def _get_italy_data(self, drug_code: str, period: str,
                       region: Optional[str] = None) -> List[PrescribingData]:
        """Get Italy regional data from AIFA Open Data"""
        
        print(f"⚠️  MOCK DATA: Italy regional analysis for {drug_code}")
        print(f"   Real implementation requires AIFA Open Data CSV/API integration")
        
        # Mock regional data for Italy's 20 regions
        # Based on population density and healthcare spending
        mock_regions = [
            {'code': 'LOM', 'name': 'Lombardia', 'prescriptions': 185000, 'cost': 7800000},
            {'code': 'LAZ', 'name': 'Lazio', 'prescriptions': 142000, 'cost': 6000000},
            {'code': 'CAM', 'name': 'Campania', 'prescriptions': 135000, 'cost': 5700000},
            {'code': 'SIC', 'name': 'Sicilia', 'prescriptions': 118000, 'cost': 4950000},
            {'code': 'VEN', 'name': 'Veneto', 'prescriptions': 112000, 'cost': 4720000},
            {'code': 'EMR', 'name': 'Emilia-Romagna', 'prescriptions': 105000, 'cost': 4420000},
            {'code': 'PIE', 'name': 'Piemonte', 'prescriptions': 98000, 'cost': 4130000},
            {'code': 'PUG', 'name': 'Puglia', 'prescriptions': 92000, 'cost': 3870000},
            {'code': 'TOS', 'name': 'Toscana', 'prescriptions': 87000, 'cost': 3660000},
            {'code': 'CAL', 'name': 'Calabria', 'prescriptions': 45000, 'cost': 1890000},
        ]
        
        result = []
        for region_data in mock_regions:
            if region and region != region_data['code']:
                continue
            
            prescriber = Prescriber(
                id=f"IT-{region_data['code']}",
                name=f"Regione {region_data['name']}",
                type="Region",
                location=f"{region_data['name']}, Italy"
            )
            
            data = PrescribingData(
                prescriber=prescriber,
                drug_code=drug_code,
                period=period,
                prescriptions=region_data['prescriptions'],
                quantity=region_data['prescriptions'],
                cost=region_data['cost']
            )
            
            result.append(data)
        
        return result
    
    def _get_spain_data(self, drug_code: str, period: str,
                       region: Optional[str] = None) -> List[PrescribingData]:
        """Get Spain regional data from Ministry of Health"""
        
        print(f"⚠️  MOCK DATA: Spain regional analysis for {drug_code}")
        print(f"   Real implementation requires Ministry of Health BIFAP database integration")
        
        # Mock regional data for Spain's 17 Autonomous Communities
        # Based on population and healthcare spending patterns
        mock_regions = [
            {'code': 'AN', 'name': 'Andalucía', 'prescriptions': 165000, 'cost': 6950000},
            {'code': 'CT', 'name': 'Cataluña', 'prescriptions': 148000, 'cost': 6230000},
            {'code': 'MD', 'name': 'Comunidad de Madrid', 'prescriptions': 132000, 'cost': 5560000},
            {'code': 'VC', 'name': 'Comunidad Valenciana', 'prescriptions': 98000, 'cost': 4130000},
            {'code': 'GA', 'name': 'Galicia', 'prescriptions': 82000, 'cost': 3450000},
            {'code': 'CL', 'name': 'Castilla y León', 'prescriptions': 75000, 'cost': 3160000},
            {'code': 'PV', 'name': 'País Vasco', 'prescriptions': 68000, 'cost': 2860000},
            {'code': 'CM', 'name': 'Castilla-La Mancha', 'prescriptions': 62000, 'cost': 2610000},
            {'code': 'MU', 'name': 'Región de Murcia', 'prescriptions': 47000, 'cost': 1980000},
            {'code': 'AR', 'name': 'Aragón', 'prescriptions': 42000, 'cost': 1770000},
            {'code': 'IB', 'name': 'Islas Baleares', 'prescriptions': 38000, 'cost': 1600000},
            {'code': 'EX', 'name': 'Extremadura', 'prescriptions': 35000, 'cost': 1470000},
            {'code': 'AS', 'name': 'Principado de Asturias', 'prescriptions': 32000, 'cost': 1350000},
            {'code': 'NC', 'name': 'Comunidad Foral de Navarra', 'prescriptions': 21000, 'cost': 880000},
            {'code': 'CN', 'name': 'Islas Canarias', 'prescriptions': 28000, 'cost': 1180000},
            {'code': 'CB', 'name': 'Cantabria', 'prescriptions': 18000, 'cost': 760000},
            {'code': 'RI', 'name': 'La Rioja', 'prescriptions': 10000, 'cost': 420000},
        ]
        
        result = []
        for region_data in mock_regions:
            if region and region != region_data['code']:
                continue
            
            prescriber = Prescriber(
                id=f"ES-{region_data['code']}",
                name=f"Comunidad {region_data['name']}",
                type="Region",
                location=f"{region_data['name']}, Spain"
            )
            
            data = PrescribingData(
                prescriber=prescriber,
                drug_code=drug_code,
                period=period,
                prescriptions=region_data['prescriptions'],
                quantity=region_data['prescriptions'],
                cost=region_data['cost']
            )
            
            result.append(data)
        
        return result
    
    def get_prescriber_details(self, prescriber_ids: List[str]) -> List[Prescriber]:
        """Get region details (not individual prescribers)"""
        # EU data is regional, so "prescribers" are regions
        result = []
        for region_id in prescriber_ids:
            prescriber = Prescriber(
                id=region_id,
                name=f"Region {region_id}",
                type="Region"
            )
            result.append(prescriber)
        return result
    
    def get_latest_period(self) -> str:
        """Get most recent data period"""
        # EU data typically 1-2 years behind
        return "2022"
    
    def find_drug_code(self, name: str, prefer_generic: bool = True) -> Optional[str]:
        """
        Find ATC code for drug name
        
        Returns drug name for querying (EU uses names/ATC codes)
        """
        results = self.search_drug(name)
        if results:
            return results[0]['id']
        return name  # Use name as-is if no ATC found


# ============================================================================
# MULTI-COUNTRY DATA SOURCE (Wrapper)
# ============================================================================

class MultiCountryDataSource(DataSource):
    """
    Wrapper that routes to appropriate country-specific data source
    
    Usage:
        multi_ds = MultiCountryDataSource()
        data = multi_ds.get_prescribing_data('metformin', '2022', country='FR')
    """
    
    def __init__(self):
        self.sources = {
            'FR': EUDataSource('FR'),
            'DE': EUDataSource('DE'),
            'NL': EUDataSource('NL'),
            'IT': EUDataSource('IT'),
            'ES': EUDataSource('ES')
        }
        self.current_country = None
    
    def set_country(self, country: str):
        """Set active country"""
        self.current_country = country.upper()
        if self.current_country not in self.sources:
            raise ValueError(f"Country {country} not supported")
    
    def search_drug(self, name: str) -> List[Dict]:
        if not self.current_country:
            raise ValueError("Country not set. Call set_country() first")
        return self.sources[self.current_country].search_drug(name)
    
    def get_prescribing_data(self, drug_code: str, period: str,
                           region: Optional[str] = None) -> List[PrescribingData]:
        if not self.current_country:
            raise ValueError("Country not set. Call set_country() first")
        return self.sources[self.current_country].get_prescribing_data(
            drug_code, period, region
        )
    
    def get_prescriber_details(self, prescriber_ids: List[str]) -> List[Prescriber]:
        if not self.current_country:
            raise ValueError("Country not set. Call set_country() first")
        return self.sources[self.current_country].get_prescriber_details(prescriber_ids)
    
    def get_latest_period(self) -> str:
        if not self.current_country:
            raise ValueError("Country not set. Call set_country() first")
        return self.sources[self.current_country].get_latest_period()
    
    def find_drug_code(self, name: str, prefer_generic: bool = True) -> Optional[str]:
        if not self.current_country:
            raise ValueError("Country not set. Call set_country() first")
        return self.sources[self.current_country].find_drug_code(name, prefer_generic)


# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_eu_data_sources():
    """Test EU data sources"""
    print("="*80)
    print("Testing EU Data Sources (Regional/Aggregated)")
    print("="*80)
    
    countries = ['FR', 'DE', 'NL', 'IT', 'ES']
    
    for country in countries:
        print(f"\n{'='*80}")
        print(f"Testing {country}")
        print('='*80)
        
        ds = EUDataSource(country)
        
        # Test drug search
        print(f"\n1. Search for 'metformin':")
        results = ds.search_drug('metformin')
        if results:
            print(f"   Found: {results[0]['name']} (Code: {results[0]['id']})")
        
        # Test prescribing data
        print(f"\n2. Get regional prescribing data:")
        drug_code = ds.find_drug_code('metformin')
        data = ds.get_prescribing_data(drug_code, '2022')
        
        if data:
            print(f"   Found {len(data)} regions")
            print(f"\n   Top 3 regions by volume:")
            for i, d in enumerate(data[:3], 1):
                print(f"   {i}. {d.prescriber.name}: {d.prescriptions:,} prescriptions, €{d.cost:,.0f}")
        
        print()


if __name__ == "__main__":
    test_eu_data_sources()
