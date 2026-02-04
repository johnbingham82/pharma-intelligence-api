#!/usr/bin/env python3
"""
Leqvio ICB Formulary Intelligence
Identify geographic opportunities and potential formulary barriers
"""
import requests
import json
from collections import defaultdict

class ICBIntelligence:
    def __init__(self):
        self.base_url = "https://openprescribing.net/api/1.0"
        
    def get_icb_prescribing(self, bnf_code, date="2025-10-01"):
        """Get prescribing by ICB"""
        url = f"{self.base_url}/spending_by_org/"
        params = {
            'org_type': 'icb',
            'code': bnf_code,
            'date': date,
            'format': 'json'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_practice_prescribing_by_icb(self, bnf_code, date="2025-10-01"):
        """Get all practice-level data to aggregate by ICB"""
        url = f"{self.base_url}/spending_by_org/"
        params = {
            'org_type': 'practice',
            'code': bnf_code,
            'date': date,
            'format': 'json'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_icb_details(self):
        """Get list of all ICBs"""
        url = f"{self.base_url}/org_code/"
        params = {
            'org_type': 'icb',
            'format': 'json'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def analyze_icb_opportunities(self):
        """Compare Leqvio vs statin prescribing by ICB"""
        
        print("\n" + "="*80)
        print("LEQVIO ICB FORMULARY INTELLIGENCE")
        print("Geographic Market Access Analysis")
        print("="*80)
        
        # Get BNF codes
        leqvio_code = "0601023AF"  # inclisiran
        statin_code = "0212000B0"   # atorvastatin as reference
        
        print("\n⏳ Fetching ICB data for Leqvio...")
        leqvio_icb_data = self.get_icb_prescribing(leqvio_code)
        
        print("⏳ Fetching ICB data for statins (reference)...")
        statin_icb_data = self.get_icb_prescribing(statin_code)
        
        # Create lookup dictionaries
        leqvio_by_icb = {d['row_id']: d for d in leqvio_icb_data}
        statin_by_icb = {d['row_id']: d for d in statin_icb_data}
        
        # Get all ICB codes
        all_icbs = set(leqvio_by_icb.keys()) | set(statin_by_icb.keys())
        
        # Calculate metrics per ICB
        icb_analysis = []
        
        for icb_code in all_icbs:
            leqvio_items = int(leqvio_by_icb.get(icb_code, {}).get('items', 0))
            statin_items = int(statin_by_icb.get(icb_code, {}).get('items', 0))
            
            leqvio_cost = float(leqvio_by_icb.get(icb_code, {}).get('actual_cost', 0))
            
            # Get ICB name
            icb_name = leqvio_by_icb.get(icb_code, {}).get('row_name', 
                       statin_by_icb.get(icb_code, {}).get('row_name', 'Unknown'))
            
            # Calculate penetration
            penetration = (leqvio_items / statin_items * 100) if statin_items > 0 else 0
            
            # Opportunity score: high statin volume + low Leqvio penetration = opportunity
            opportunity_score = statin_items * (1 - min(penetration/5, 1))  # Target 5% penetration
            
            icb_analysis.append({
                'code': icb_code,
                'name': icb_name,
                'leqvio_items': leqvio_items,
                'statin_items': statin_items,
                'leqvio_cost': leqvio_cost,
                'penetration': penetration,
                'opportunity_score': opportunity_score,
                'status': self.classify_icb_status(leqvio_items, penetration)
            })
        
        # Sort by opportunity score
        icb_analysis.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        # Display results by category
        self.display_formulary_intelligence(icb_analysis)
        
        # Save results
        with open('leqvio_icb_analysis.json', 'w') as f:
            json.dump(icb_analysis, f, indent=2)
        
        print("\n💾 Full ICB analysis saved to: leqvio_icb_analysis.json\n")
        
        return icb_analysis
    
    def classify_icb_status(self, leqvio_items, penetration):
        """Classify ICB based on Leqvio adoption"""
        if leqvio_items == 0:
            return "NO_USAGE"
        elif penetration < 0.5:
            return "RESTRICTED"
        elif penetration < 2.0:
            return "LIMITED_ACCESS"
        elif penetration < 5.0:
            return "MODERATE_ACCESS"
        else:
            return "GOOD_ACCESS"
    
    def display_formulary_intelligence(self, icb_analysis):
        """Display categorized ICB intelligence"""
        
        # Group by status
        by_status = defaultdict(list)
        for icb in icb_analysis:
            by_status[icb['status']].append(icb)
        
        print("\n" + "="*80)
        print("🚨 PRIORITY 1: NO USAGE ICBs (Potential Formulary Blocks)")
        print("="*80)
        
        no_usage = by_status.get('NO_USAGE', [])
        if no_usage:
            print(f"\nFound {len(no_usage)} ICBs with ZERO Leqvio prescribing:\n")
            print(f"{'ICB Code':<10} {'Statin Rx':<12} {'ICB Name'}")
            print("-" * 80)
            for icb in sorted(no_usage, key=lambda x: x['statin_items'], reverse=True)[:10]:
                print(f"{icb['code']:<10} {icb['statin_items']:<12,} {icb['name'][:55]}")
            print(f"\n💡 Action: Contact these ICBs to understand formulary barriers")
        else:
            print("\n✅ All ICBs have at least some Leqvio usage")
        
        print("\n" + "="*80)
        print("⚠️  PRIORITY 2: RESTRICTED ACCESS ICBs (<0.5% penetration)")
        print("="*80)
        
        restricted = by_status.get('RESTRICTED', [])
        if restricted:
            print(f"\nFound {len(restricted)} ICBs with very low Leqvio usage:\n")
            print(f"{'ICB Code':<10} {'Leqvio Rx':<12} {'Statin Rx':<12} {'Penetration':<12} {'ICB Name'}")
            print("-" * 80)
            for icb in sorted(restricted, key=lambda x: x['opportunity_score'], reverse=True)[:15]:
                print(f"{icb['code']:<10} {icb['leqvio_items']:<12,} {icb['statin_items']:<12,} "
                      f"{icb['penetration']:<12.2f}% {icb['name'][:40]}")
            print(f"\n💡 Action: Likely formulary restrictions - engage payer relations team")
        
        print("\n" + "="*80)
        print("📈 PRIORITY 3: GROWTH OPPORTUNITY ICBs (0.5-2% penetration)")
        print("="*80)
        
        limited = by_status.get('LIMITED_ACCESS', [])
        if limited:
            print(f"\nFound {len(limited)} ICBs with room for growth:\n")
            print(f"{'ICB Code':<10} {'Leqvio Rx':<12} {'Penetration':<12} {'Opportunity':<12} {'ICB Name'}")
            print("-" * 80)
            for icb in sorted(limited, key=lambda x: x['opportunity_score'], reverse=True)[:15]:
                print(f"{icb['code']:<10} {icb['leqvio_items']:<12,} {icb['penetration']:<12.2f}% "
                      f"{int(icb['opportunity_score']):<12,} {icb['name'][:40]}")
            print(f"\n💡 Action: On formulary but underutilized - focus sales resources here")
        
        print("\n" + "="*80)
        print("✅ STRONG PERFORMANCE ICBs (>2% penetration)")
        print("="*80)
        
        good_access = by_status.get('MODERATE_ACCESS', []) + by_status.get('GOOD_ACCESS', [])
        if good_access:
            print(f"\nFound {len(good_access)} ICBs with healthy Leqvio adoption:\n")
            print(f"{'ICB Code':<10} {'Leqvio Rx':<12} {'Penetration':<12} {'Cost (£)':<15} {'ICB Name'}")
            print("-" * 80)
            for icb in sorted(good_access, key=lambda x: x['penetration'], reverse=True)[:10]:
                print(f"{icb['code']:<10} {icb['leqvio_items']:<12,} {icb['penetration']:<12.2f}% "
                      f"£{icb['leqvio_cost']:<14,.0f} {icb['name'][:35]}")
            print(f"\n💡 Action: Best practices to replicate - what's working here?")
        
        # Summary recommendations
        print("\n" + "="*80)
        print("🎯 STRATEGIC RECOMMENDATIONS")
        print("="*80)
        
        total_no_usage = len(no_usage)
        total_restricted = len(restricted)
        total_opportunity = sum(icb['opportunity_score'] for icb in restricted[:10])
        
        print(f"""
IMMEDIATE ACTIONS:

1. FORMULARY ACCESS ({total_no_usage + total_restricted} ICBs need attention)
   → {total_no_usage} ICBs with zero usage - likely not on formulary
   → {total_restricted} ICBs with restricted access - prior authorization barriers?
   → Engage payer relations team for formulary negotiations

2. SALES RESOURCE ALLOCATION
   → Focus field teams on "GROWTH OPPORTUNITY" ICBs (on formulary, low uptake)
   → Estimated potential: {int(total_opportunity):,} incremental prescriptions
   → ROI will be higher than fighting formulary battles

3. BEST PRACTICE SHARING
   → Study top-performing ICBs ({good_access[0]['name'] if good_access else 'N/A'}{': ' + str(round(good_access[0]['penetration'], 2)) + '%' if good_access else ''})
   → What's their formulary status? Reimbursement? HCP education approach?
   → Replicate success factors in similar ICBs

4. COMPETITIVE POSITIONING
   → Contrast Leqvio ICB access vs Repatha/Praluent
   → Highlight twice-yearly dosing in formulary submissions
   → Build business case: adherence = better outcomes = cost savings
        """)

if __name__ == "__main__":
    intel = ICBIntelligence()
    intel.analyze_icb_opportunities()
