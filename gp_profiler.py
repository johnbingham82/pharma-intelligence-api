#!/usr/bin/env python3
"""
GP Practice Profiler MVP
Analyzes NHS prescribing data to identify high-value practice targets
"""
import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

class GPProfiler:
    def __init__(self):
        self.base_url = "https://openprescribing.net/api/1.0"
        
    def get_latest_month(self):
        """Get the most recent data month (typically 2-3 months ago)"""
        # NHS data has ~2-3 month lag, try October 2025
        return "2025-10-01"
    
    def search_drug(self, drug_name):
        """Search for BNF codes by drug name"""
        url = f"{self.base_url}/bnf_code/"
        params = {'q': drug_name, 'format': 'json'}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_practice_prescribing(self, bnf_code, date, region_code=None):
        """Get prescribing by all practices for a drug"""
        url = f"{self.base_url}/spending_by_org/"
        params = {
            'org_type': 'practice',
            'code': bnf_code,
            'date': date,
            'format': 'json'
        }
        
        if region_code:
            params['org'] = region_code
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_practice_details(self, region_code=None):
        """Get practice list sizes"""
        url = f"{self.base_url}/org_details/"
        params = {
            'org_type': 'practice',
            'keys': 'total_list_size',
            'format': 'json'
        }
        
        if region_code:
            params['org'] = region_code
            
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def analyze_therapeutic_area(self, drug_name, competitor_drugs=None, region_code=None):
        """
        Analyze prescribing patterns and identify opportunities
        
        Args:
            drug_name: Your product (e.g., "metformin")
            competitor_drugs: List of competitor names
            region_code: ICB code to filter (e.g., "15N" for NHS Devon)
        """
        print(f"\n{'='*70}")
        print(f"GP PRACTICE PROFILER - {drug_name.upper()}")
        print(f"{'='*70}\n")
        
        # Get latest data month
        latest_month = self.get_latest_month()
        print(f"📅 Analyzing data from: {latest_month}")
        
        # Search for drug codes
        print(f"\n🔍 Searching for '{drug_name}'...")
        drug_results = self.search_drug(drug_name)
        
        if not drug_results:
            print(f"❌ No results found for '{drug_name}'")
            return
        
        print(f"✅ Found {len(drug_results)} matching codes:")
        for result in drug_results[:5]:
            print(f"   - {result.get('name', 'Unknown')} ({result.get('id', 'N/A')})")
        
        # Use the first chemical code (not presentation)
        # Prefer codes ending in specific patterns for pure substances
        target_code = None
        for result in drug_results:
            code = result.get('id', '')
            name = result.get('name', '').lower()
            # Chemical codes are typically 9 characters (e.g., 0212000AA)
            # Prefer exact matches without combinations
            if len(code) == 9 and '/' not in name and drug_name.lower() in name:
                target_code = code
                break
        
        # Fallback to any 9-character code
        if not target_code:
            for result in drug_results:
                code = result.get('id', '')
                if len(code) == 9:
                    target_code = code
                    break
        
        if not target_code:
            print("❌ Could not find suitable BNF code")
            return
        
        print(f"\n📊 Analyzing prescribing for code: {target_code}")
        
        # Get practice prescribing data
        print(f"⏳ Fetching practice data...")
        practice_data = self.get_practice_prescribing(target_code, latest_month, region_code)
        
        if not practice_data:
            print("❌ No practice data found")
            return
        
        print(f"✅ Found data for {len(practice_data)} practices\n")
        
        # Calculate opportunity scores
        opportunities = []
        
        for practice in practice_data:
            practice_code = practice.get('row_id')
            practice_name = practice.get('row_name', 'Unknown')
            items = int(practice.get('items', 0))
            quantity = float(practice.get('quantity', 0))
            actual_cost = float(practice.get('actual_cost', 0))
            
            # Simple opportunity score: high volume = high value
            # In production, add: market share, trends, peer comparison
            opportunity_score = items * 1.0  # Weight by prescription count
            
            opportunities.append({
                'code': practice_code,
                'name': practice_name,
                'items': items,
                'quantity': quantity,
                'cost': actual_cost,
                'score': opportunity_score
            })
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x['score'], reverse=True)
        
        # Display top 20 targets
        print(f"\n{'='*70}")
        print("🎯 TOP 20 HIGH-VALUE TARGET PRACTICES")
        print(f"{'='*70}\n")
        print(f"{'Rank':<6} {'Practice Code':<12} {'Prescriptions':<15} {'Cost (£)':<12} {'Practice Name'}")
        print("-" * 70)
        
        for i, opp in enumerate(opportunities[:20], 1):
            print(f"{i:<6} {opp['code']:<12} {opp['items']:<15} £{opp['cost']:<11,.0f} {opp['name'][:40]}")
        
        # Summary stats
        print(f"\n{'='*70}")
        print("📈 SUMMARY")
        print(f"{'='*70}")
        
        total_practices = len(opportunities)
        total_items = sum(p['items'] for p in opportunities)
        total_cost = sum(p['cost'] for p in opportunities)
        
        top_20_items = sum(p['items'] for p in opportunities[:20])
        top_20_cost = sum(p['cost'] for p in opportunities[:20])
        
        print(f"Total Practices Prescribing: {total_practices:,}")
        print(f"Total Prescriptions: {total_items:,}")
        print(f"Total Cost: £{total_cost:,.0f}")
        print(f"\nTop 20 Practices:")
        print(f"  - Prescriptions: {top_20_items:,} ({top_20_items/total_items*100:.1f}% of total)")
        print(f"  - Cost: £{top_20_cost:,.0f} ({top_20_cost/total_cost*100:.1f}% of total)")
        print(f"\n💡 Insight: Focus on these 20 practices for maximum ROI\n")
        
        # Save results
        output_file = f"gp_targets_{drug_name}_{latest_month}.json"
        with open(output_file, 'w') as f:
            json.dump({
                'drug': drug_name,
                'bnf_code': target_code,
                'date': latest_month,
                'region': region_code,
                'top_targets': opportunities[:50],
                'summary': {
                    'total_practices': total_practices,
                    'total_items': total_items,
                    'total_cost': total_cost
                }
            }, f, indent=2)
        
        print(f"💾 Full results saved to: {output_file}\n")
        
        return opportunities

if __name__ == "__main__":
    profiler = GPProfiler()
    
    # Example: Analyze metformin prescribing (Type 2 diabetes)
    # You can change this to any drug name
    profiler.analyze_therapeutic_area(
        drug_name="metformin",
        region_code=None  # Set to ICB code like "15N" to filter by region
    )
