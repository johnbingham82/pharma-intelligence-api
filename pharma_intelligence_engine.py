#!/usr/bin/env python3
"""
Pharma Intelligence Engine - Generalized Analysis Platform
Analyzes prescribing data for any drug in any supported country
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
import json

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Drug:
    """Represents a pharmaceutical product"""
    name: str
    generic_name: str
    therapeutic_area: str
    company: str
    country_codes: Dict[str, str]  # {country: drug_code}
    indication: Optional[str] = None
    launch_date: Optional[str] = None

@dataclass
class Prescriber:
    """Represents a prescriber/practice"""
    id: str
    name: str
    location: Optional[str] = None
    type: str = "unknown"  # GP, hospital, specialist
    list_size: Optional[int] = None
    specialty: Optional[str] = None

@dataclass
class PrescribingData:
    """Prescribing metrics for a prescriber"""
    prescriber: Prescriber
    drug_code: str
    period: str
    prescriptions: int
    quantity: float
    cost: float
    patients: Optional[int] = None

@dataclass
class OpportunityProfile:
    """Opportunity assessment for a prescriber"""
    prescriber: Prescriber
    opportunity_score: float
    current_volume: int
    potential_volume: int
    market_share: Optional[float] = None
    competitive_position: Dict[str, Any] = None
    recommendations: List[str] = None
    segment: Optional[str] = None

# ============================================================================
# ABSTRACT DATA SOURCE
# ============================================================================

class DataSource(ABC):
    """Abstract base class for country-specific data sources"""
    
    @abstractmethod
    def search_drug(self, name: str) -> List[Dict]:
        """Search for drug codes by name"""
        pass
    
    @abstractmethod
    def get_prescribing_data(self, drug_code: str, period: str, 
                           region: Optional[str] = None) -> List[PrescribingData]:
        """Get prescribing data for a drug"""
        pass
    
    @abstractmethod
    def get_prescriber_details(self, prescriber_ids: List[str]) -> List[Prescriber]:
        """Get detailed prescriber information"""
        pass
    
    @abstractmethod
    def get_latest_period(self) -> str:
        """Get the most recent data period available"""
        pass

# ============================================================================
# SCORING MODELS
# ============================================================================

class OpportunityScorer(ABC):
    """Abstract base class for opportunity scoring algorithms"""
    
    @abstractmethod
    def calculate_score(self, data: PrescribingData, context: Dict) -> float:
        """Calculate opportunity score for a prescriber"""
        pass

class SimpleVolumeScorer(OpportunityScorer):
    """Simple scorer based on prescription volume"""
    
    def calculate_score(self, data: PrescribingData, context: Dict) -> float:
        return float(data.prescriptions)

class MarketShareScorer(OpportunityScorer):
    """Advanced scorer incorporating market share and growth potential"""
    
    def calculate_score(self, data: PrescribingData, context: Dict) -> float:
        base_score = data.prescriptions
        
        # Adjust for market share (low share = high opportunity)
        if 'market_share' in context:
            share = context['market_share']
            if share < 0.1:  # <10% share = 3x multiplier
                base_score *= 3.0
            elif share < 0.25:  # <25% share = 2x multiplier
                base_score *= 2.0
        
        # Adjust for practice size
        if 'list_size' in context and context['list_size']:
            # Normalize by practice size for fair comparison
            base_score = (base_score / context['list_size']) * 10000
        
        # Adjust for cost (higher cost drugs = higher value)
        if data.cost > 0:
            cost_per_script = data.cost / data.prescriptions
            if cost_per_script > 100:  # High-cost drug
                base_score *= 1.5
        
        return base_score

# ============================================================================
# SEGMENTATION ENGINE
# ============================================================================

class Segmenter:
    """Segments prescribers into actionable groups"""
    
    @staticmethod
    def segment_by_volume(opportunities: List[OpportunityProfile]) -> Dict[str, List[OpportunityProfile]]:
        """Segment by current prescribing volume"""
        segments = {
            'High Prescribers': [],
            'Medium Prescribers': [],
            'Low Prescribers': [],
            'Non-Prescribers': []
        }
        
        volumes = [o.current_volume for o in opportunities if o.current_volume > 0]
        if not volumes:
            return segments
        
        avg = sum(volumes) / len(volumes)
        
        for opp in opportunities:
            if opp.current_volume == 0:
                segments['Non-Prescribers'].append(opp)
            elif opp.current_volume > avg * 2:
                segments['High Prescribers'].append(opp)
            elif opp.current_volume > avg * 0.5:
                segments['Medium Prescribers'].append(opp)
            else:
                segments['Low Prescribers'].append(opp)
        
        return segments
    
    @staticmethod
    def segment_by_opportunity(opportunities: List[OpportunityProfile]) -> Dict[str, List[OpportunityProfile]]:
        """Segment by opportunity type"""
        segments = {
            'Quick Wins': [],        # High volume, low effort
            'Strategic Growth': [],  # High potential, medium effort
            'New Business': [],      # Zero share, need conversion
            'Defend': []            # High share, risk of loss
        }
        
        for opp in opportunities:
            if opp.current_volume == 0:
                segments['New Business'].append(opp)
            elif opp.market_share and opp.market_share > 0.5:
                segments['Defend'].append(opp)
            elif opp.current_volume > 50:
                segments['Quick Wins'].append(opp)
            else:
                segments['Strategic Growth'].append(opp)
        
        return segments

# ============================================================================
# RECOMMENDATION ENGINE
# ============================================================================

class RecommendationEngine:
    """Generates actionable recommendations"""
    
    @staticmethod
    def generate_recommendations(profile: OpportunityProfile, 
                                therapeutic_area: str) -> List[str]:
        """Generate tailored recommendations based on profile"""
        recs = []
        
        # Volume-based recommendations
        if profile.current_volume == 0:
            recs.append("🎯 NEW PRESCRIBER: Schedule introductory MSL visit")
            recs.append("📧 Send product monograph and clinical trial data")
        elif profile.current_volume < 10:
            recs.append("📈 GROWTH OPPORTUNITY: Low volume, high potential")
            recs.append("🤝 Arrange peer-to-peer meeting with high prescriber")
        elif profile.current_volume > 100:
            recs.append("⭐ KEY ACCOUNT: Maintain strong relationship")
            recs.append("🎓 Invite to advisory board or speaker program")
        
        # Market share recommendations
        if profile.market_share:
            if profile.market_share < 0.1:
                recs.append(f"⚠️ LOW SHARE ({profile.market_share*100:.1f}%): Address access barriers")
            elif profile.market_share > 0.5:
                recs.append(f"✅ STRONG POSITION ({profile.market_share*100:.1f}%): Focus on retention")
        
        # Competitive recommendations
        if profile.competitive_position:
            main_competitor = profile.competitive_position.get('main_competitor')
            if main_competitor:
                recs.append(f"🥊 COMPETITIVE INTEL: Track {main_competitor} activity")
        
        return recs

# ============================================================================
# MAIN INTELLIGENCE ENGINE
# ============================================================================

class PharmaIntelligenceEngine:
    """Core analysis engine - drug and country agnostic"""
    
    def __init__(self, data_source: DataSource, scorer: Optional[OpportunityScorer] = None):
        self.data_source = data_source
        self.scorer = scorer or MarketShareScorer()
        self.segmenter = Segmenter()
        self.recommender = RecommendationEngine()
    
    def analyze_drug(self, 
                    drug: Drug,
                    country: str,
                    competitor_drugs: Optional[List[Drug]] = None,
                    region: Optional[str] = None,
                    top_n: int = 50) -> Dict[str, Any]:
        """
        Complete analysis for a drug in a country
        
        Args:
            drug: Target drug to analyze
            country: Country code (e.g., 'UK', 'US')
            competitor_drugs: List of competing drugs
            region: Optional region filter
            top_n: Number of top opportunities to return
            
        Returns:
            Comprehensive analysis report
        """
        print(f"\n{'='*80}")
        print(f"PHARMA INTELLIGENCE ENGINE")
        print(f"Drug: {drug.name} ({drug.generic_name})")
        print(f"Company: {drug.company}")
        print(f"Therapeutic Area: {drug.therapeutic_area}")
        print(f"Country: {country}")
        print(f"{'='*80}\n")
        
        # Get drug code for this country
        if country not in drug.country_codes:
            raise ValueError(f"Drug code not available for country: {country}")
        
        drug_code = drug.country_codes[country]
        print(f"📋 Drug Code: {drug_code}")
        
        # Get latest data period
        period = self.data_source.get_latest_period()
        print(f"📅 Data Period: {period}\n")
        
        # Fetch prescribing data
        print("⏳ Fetching prescribing data...")
        prescribing_data = self.data_source.get_prescribing_data(
            drug_code, period, region
        )
        
        if not prescribing_data:
            print("❌ No prescribing data found")
            return {}
        
        print(f"✅ Found data for {len(prescribing_data)} prescribers\n")
        
        # Calculate market context
        total_volume = sum(p.prescriptions for p in prescribing_data)
        total_cost = sum(p.cost for p in prescribing_data)
        
        print(f"📊 Market Overview:")
        print(f"   Total Prescribers: {len(prescribing_data):,}")
        print(f"   Total Prescriptions: {total_volume:,}")
        print(f"   Total Cost: £{total_cost:,.0f}\n")
        
        # Score opportunities
        print("🎯 Scoring opportunities...")
        opportunities = []
        
        for data in prescribing_data:
            context = {
                'total_market_volume': total_volume,
                'list_size': data.prescriber.list_size
            }
            
            score = self.scorer.calculate_score(data, context)
            
            profile = OpportunityProfile(
                prescriber=data.prescriber,
                opportunity_score=score,
                current_volume=data.prescriptions,
                potential_volume=int(data.prescriptions * 1.5),  # Simple estimate
                segment=None
            )
            
            # Generate recommendations
            profile.recommendations = self.recommender.generate_recommendations(
                profile, drug.therapeutic_area
            )
            
            opportunities.append(profile)
        
        # Sort by score
        opportunities.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        # Segment opportunities
        print("📑 Segmenting prescribers...")
        volume_segments = self.segmenter.segment_by_volume(opportunities)
        opportunity_segments = self.segmenter.segment_by_opportunity(opportunities)
        
        # Display results
        self._display_results(opportunities[:top_n], volume_segments, drug, country)
        
        # Prepare output
        report = {
            'drug': {
                'name': drug.name,
                'generic_name': drug.generic_name,
                'therapeutic_area': drug.therapeutic_area,
                'company': drug.company
            },
            'analysis_date': datetime.now().isoformat(),
            'country': country,
            'region': region,
            'period': period,
            'market_summary': {
                'total_prescribers': len(prescribing_data),
                'total_prescriptions': total_volume,
                'total_cost': total_cost,
                'avg_prescriptions_per_prescriber': total_volume / len(prescribing_data)
            },
            'top_opportunities': [
                {
                    'rank': i+1,
                    'prescriber_id': opp.prescriber.id,
                    'prescriber_name': opp.prescriber.name,
                    'location': opp.prescriber.location,
                    'current_volume': opp.current_volume,
                    'opportunity_score': round(opp.opportunity_score, 2),
                    'recommendations': opp.recommendations
                }
                for i, opp in enumerate(opportunities[:top_n])
            ],
            'segments': {
                'by_volume': {k: len(v) for k, v in volume_segments.items()},
                'by_opportunity': {k: len(v) for k, v in opportunity_segments.items()}
            }
        }
        
        # Save report
        filename = f"analysis_{drug.name.replace(' ', '_')}_{country}_{period}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Full report saved to: {filename}\n")
        
        return report
    
    def _display_results(self, top_opportunities: List[OpportunityProfile],
                        segments: Dict, drug: Drug, country: str):
        """Display formatted results"""
        print(f"\n{'='*80}")
        print(f"🎯 TOP {len(top_opportunities)} OPPORTUNITIES")
        print(f"{'='*80}\n")
        
        print(f"{'Rank':<6} {'ID':<12} {'Current Vol':<13} {'Score':<10} {'Prescriber Name'}")
        print("-" * 80)
        
        for i, opp in enumerate(top_opportunities, 1):
            print(f"{i:<6} {opp.prescriber.id:<12} {opp.current_volume:<13} "
                  f"{opp.opportunity_score:<10.1f} {opp.prescriber.name[:40]}")
        
        print(f"\n{'='*80}")
        print("📊 PRESCRIBER SEGMENTATION")
        print(f"{'='*80}\n")
        
        for segment, prescribers in segments.items():
            print(f"{segment}: {len(prescribers)} prescribers")
        
        print(f"\n{'='*80}")
        print("💡 KEY INSIGHTS")
        print(f"{'='*80}\n")
        
        total = sum(len(v) for v in segments.values())
        high_pct = (len(segments.get('High Prescribers', [])) / total) * 100
        
        print(f"✓ Top 20% of prescribers (High) = {high_pct:.1f}% of total")
        print(f"✓ Focus sales resources on top {len(top_opportunities)} targets")
        print(f"✓ Estimated addressable market: {sum(o.current_volume for o in top_opportunities):,} prescriptions")
        print()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_drug(name: str, generic_name: str, therapeutic_area: str,
                company: str, country_codes: Dict[str, str]) -> Drug:
    """Convenience function to create a Drug object"""
    return Drug(
        name=name,
        generic_name=generic_name,
        therapeutic_area=therapeutic_area,
        company=company,
        country_codes=country_codes
    )
