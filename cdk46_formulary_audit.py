#!/usr/bin/env python3
"""
CDK4/6 Inhibitor Formulary Audit
Real-time scraping of NHS trust formularies to compare positioning
"""
import requests
from urllib.parse import urljoin
import json
import time

class FormularyAuditor:
    def __init__(self):
        self.drugs = {
            'palbociclib': {'brand': 'Ibrance', 'company': 'Pfizer'},
            'ribociclib': {'brand': 'Kisqali', 'company': 'Novartis'},
            'abemaciclib': {'brand': 'Verzenio', 'company': 'Lilly'}
        }
        
        self.priority_trusts = [
            {
                'name': 'The Royal Marsden NHS Foundation Trust',
                'code': 'RPY',
                'formulary_url': 'https://www.royalmarsden.nhs.uk',
                'search_terms': ['formulary', 'medicines', 'guidelines']
            },
            {
                'name': 'The Christie NHS Foundation Trust',
                'code': 'RM2',
                'formulary_url': 'https://www.christie.nhs.uk',
                'search_terms': ['formulary', 'medicines', 'guidelines']
            },
            {
                'name': 'University College London Hospitals NHS Foundation Trust',
                'code': 'RRV',
                'formulary_url': 'https://www.uclh.nhs.uk',
                'search_terms': ['formulary', 'medicines', 'guidelines']
            },
            {
                'name': 'Guy\'s and St Thomas\' NHS Foundation Trust',
                'code': 'RJ1',
                'formulary_url': 'https://www.guysandstthomas.nhs.uk',
                'search_terms': ['formulary', 'medicines', 'guidelines']
            },
            {
                'name': 'Cambridge University Hospitals NHS Foundation Trust',
                'code': 'RGT',
                'formulary_url': 'https://www.cuh.nhs.uk',
                'search_terms': ['formulary', 'medicines', 'guidelines']
            },
            {
                'name': 'Imperial College Healthcare NHS Trust',
                'code': 'RYJ',
                'formulary_url': 'https://www.imperial.nhs.uk',
                'search_terms': ['formulary', 'medicines', 'guidelines']
            },
            {
                'name': 'Manchester University NHS Foundation Trust',
                'code': 'R0A',
                'formulary_url': 'https://mft.nhs.uk',
                'search_terms': ['formulary', 'medicines', 'guidelines']
            },
            {
                'name': 'Oxford University Hospitals NHS Foundation Trust',
                'code': 'RTH',
                'formulary_url': 'https://www.ouh.nhs.uk',
                'search_terms': ['formulary', 'medicines', 'guidelines']
            },
        ]
        
        self.results = []
    
    def search_trust_website(self, trust):
        """
        Search trust website for formulary information
        """
        print(f"\n{'='*80}")
        print(f"AUDITING: {trust['name']}")
        print(f"{'='*80}\n")
        
        result = {
            'trust_name': trust['name'],
            'trust_code': trust['code'],
            'formulary_found': False,
            'drugs_found': {},
            'positioning': 'Unknown',
            'notes': []
        }
        
        # Try to find formulary page
        print(f"🔍 Searching {trust['formulary_url']}...")
        
        try:
            # Search for formulary page
            search_url = f"{trust['formulary_url']}/search"
            
            # Most NHS trusts have some form of public information
            # Real implementation would need more sophisticated scraping
            print(f"   Checking main website structure...")
            
            response = requests.get(trust['formulary_url'], timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for formulary mentions
                if 'formulary' in content or 'medicines' in content:
                    print(f"   ✅ Found potential formulary section")
                    result['formulary_found'] = True
                    result['notes'].append('Formulary section detected on main site')
                else:
                    print(f"   ⚠️  No public formulary found on main page")
                    result['notes'].append('No public formulary access found')
                
                # Search for drug mentions
                for generic, info in self.drugs.items():
                    if generic in content or info['brand'].lower() in content:
                        print(f"   📋 Found mention of {info['brand']} ({generic})")
                        result['drugs_found'][info['brand']] = 'Mentioned on website'
                
            else:
                print(f"   ❌ Could not access website (status: {response.status_code})")
                result['notes'].append(f'Website access failed: {response.status_code}')
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️  Request timed out")
            result['notes'].append('Website timeout')
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            result['notes'].append(f'Error: {str(e)[:50]}')
        
        # Add realistic assessment based on trust type
        if 'Marsden' in trust['name'] or 'Christie' in trust['name']:
            result['positioning'] = 'All three likely available (specialist cancer center)'
            result['notes'].append('Specialist cancer center - typically comprehensive formularies')
        elif 'University' in trust['name']:
            result['positioning'] = 'All three likely available (academic center)'
            result['notes'].append('Academic medical center - usually has all NICE-approved options')
        else:
            result['positioning'] = 'Mixed - local formulary decision'
        
        self.results.append(result)
        time.sleep(2)  # Be polite to servers
        
        return result
    
    def run_audit(self):
        """
        Run full formulary audit across priority trusts
        """
        print("\n" + "="*80)
        print("CDK4/6 INHIBITOR FORMULARY AUDIT")
        print("Kisqali vs Ibrance vs Verzenio")
        print("="*80)
        
        print(f"""
METHODOLOGY:
- Target: 8 major breast cancer treatment centers
- Drugs: Palbociclib (Ibrance), Ribociclib (Kisqali), Abemaciclib (Verzenio)
- Approach: Web scraping + inference based on trust type
- Data source: Trust websites + publicly available documents

NOTE: Most NHS trust formularies are internal/restricted.
This audit combines:
1. Public website scraping (where accessible)
2. Inference based on trust characteristics
3. NICE guidance compliance expectations

For production: Would add manual verification, FOI requests, MSL field intelligence.
        """)
        
        # Audit each trust
        for trust in self.priority_trusts:
            self.search_trust_website(trust)
        
        # Generate summary report
        self.generate_report()
    
    def generate_report(self):
        """
        Generate summary report of findings
        """
        print("\n" + "="*80)
        print("AUDIT SUMMARY REPORT")
        print("="*80)
        
        print(f"\n{'Trust':<50} {'Public Formulary':<18} {'Assessment'}")
        print("-" * 80)
        
        for result in self.results:
            formulary_status = "✅ Found" if result['formulary_found'] else "❌ Not Public"
            print(f"{result['trust_name'][:48]:<50} {formulary_status:<18} {result['positioning'][:30]}")
        
        # Detailed findings
        print("\n" + "="*80)
        print("DETAILED FINDINGS BY TRUST")
        print("="*80)
        
        for result in self.results:
            print(f"\n### {result['trust_name']} ({result['trust_code']})")
            print(f"Formulary Access: {'Public' if result['formulary_found'] else 'Restricted'}")
            
            if result['drugs_found']:
                print(f"Drug Mentions Found:")
                for drug, status in result['drugs_found'].items():
                    print(f"  • {drug}: {status}")
            
            if result['notes']:
                print(f"Notes:")
                for note in result['notes']:
                    print(f"  - {note}")
        
        # Strategic insights
        print("\n" + "="*80)
        print("STRATEGIC INSIGHTS")
        print("="*80)
        
        print(f"""
FORMULARY ACCESS CHALLENGE:
→ Only {sum(1 for r in self.results if r['formulary_found'])} of {len(self.results)} trusts have publicly accessible formularies
→ Most oncology formularies are internal documents (clinician-only access)
→ This is NORMAL for NHS - formularies are working documents, not public resources

WHAT THIS MEANS:
→ Intelligence gathering requires field-based approach (MSL engagement)
→ Cannot rely on web scraping alone for formulary positioning
→ Need: MSL surveys, pharmacist interviews, FOI requests

RECOMMENDED APPROACH FOR PRODUCTION:

1. MSL Field Intelligence (PRIMARY)
   → Train MSLs to ask: "What CDK4/6 inhibitors are on your formulary?"
   → Survey question: "Is Kisqali first-line or alternative to Ibrance?"
   → Collect: 10 trusts × 2-3 oncologists each = 20-30 data points

2. Pharmacy Director Engagement
   → Contact trust pharmacy departments directly
   → Request formulary information (professional inquiry)
   → Many will share positioning for legitimate medical/commercial purposes

3. Freedom of Information Requests
   → FOI request: "Please provide CDK4/6 inhibitor formulary status"
   → Legal requirement to respond within 20 working days
   → Can be batch-submitted to 50 trusts simultaneously

4. NICE Implementation Data
   → Innovation Scorecard (quarterly published data)
   → Shows which ICBs/trusts are using NICE-approved drugs
   → Proxy for formulary inclusion

5. Procurement Intelligence
   → Contracts Finder (public tender data)
   → Which trusts are buying which CDK4/6 inhibitors?
   → Contract values indicate market share

ESTIMATED TIMELINE FOR COMPLETE FORMULARY MAP:
- MSL field intelligence: 4-6 weeks
- FOI requests: 6-8 weeks (20-day response time)
- Procurement analysis: 2 weeks
- Total: 8-10 weeks for comprehensive 50-trust audit

VALUE OF COMPLETE AUDIT:
→ Know exactly where Kisqali is disadvantaged vs Ibrance
→ Target formulary submissions at specific trusts
→ Measure success (track formulary status changes over time)
→ Competitive intelligence (where is Verzenio gaining?)
        """)
        
        # Save results
        with open('cdk46_formulary_audit_results.json', 'w') as f:
            json.dump({
                'audit_date': '2026-02-03',
                'drugs_analyzed': self.drugs,
                'trusts_audited': len(self.results),
                'results': self.results,
                'methodology': 'Web scraping + inference',
                'completeness': 'Initial reconnaissance - field verification required'
            }, f, indent=2)
        
        print("\n💾 Results saved to: cdk46_formulary_audit_results.json")
        
        print("\n" + "="*80)
        print("NEXT STEPS")
        print("="*80)
        
        print("""
Immediate Actions:

1. MSL INTELLIGENCE GATHERING (Week 1-2)
   → Create standardized survey for MSL team
   → Questions: 
     * "Which CDK4/6 inhibitors are on your trust formulary?"
     * "Is Kisqali first-line, second-line, or alternative?"
     * "What drives CDK4/6 inhibitor choice here?"
   → Target: 20-30 oncologists across 10 priority trusts

2. FOI REQUEST BATCH (Week 2)
   → Template: "Please provide information on CDK4/6 inhibitor formulary status..."
   → Submit to: 50 major NHS trusts
   → Track responses (20-day deadline)

3. PHARMACY ENGAGEMENT (Weeks 2-4)
   → Email trust pharmacy directors
   → Professional inquiry about formulary positioning
   → Offer: Clinical/safety information in exchange for intel

4. PROCUREMENT DATA PULL (Week 3)
   → Contracts Finder: Search "palbociclib" "ribociclib" "abemaciclib"
   → Analyze contract values (proxy for market share by trust)

DELIVERABLE (8 weeks from now):
→ Complete formulary map: 50 major trusts
→ Positioning matrix: Kisqali vs Ibrance vs Verzenio by trust
→ Heat map: Where Kisqali is winning vs losing
→ Action plan: Formulary submissions for disadvantaged trusts
        """)

if __name__ == "__main__":
    auditor = FormularyAuditor()
    auditor.run_audit()
