#!/usr/bin/env python3
"""
Leqvio Opportunity Finder
Identify specific practice-level switching & conversion opportunities
"""
import json

# Load the saved results
with open('gp_targets_inclisiran_2025-10-01.json') as f:
    leqvio_data = json.load(f)

with open('gp_targets_evolocumab_2025-10-01.json') as f:
    repatha_data = json.load(f)

with open('gp_targets_alirocumab_2025-10-01.json') as f:
    praluent_data = json.load(f)
    
with open('gp_targets_atorvastatin_2025-10-01.json') as f:
    statin_data = json.load(f)

# Create practice sets
leqvio_practices = {p['code']: p for p in leqvio_data['top_targets']}
repatha_practices = {p['code']: p for p in repatha_data['top_targets']}
praluent_practices = {p['code']: p for p in praluent_data['top_targets']}
statin_practices = {p['code']: p for p in statin_data['top_targets']}

print("\n" + "="*80)
print("LEQVIO MARKET OPPORTUNITIES - ACTIONABLE PRACTICE TARGETS")
print("="*80)

# OPPORTUNITY 1: Competitor Switch Targets
print("\n🔄 OPPORTUNITY 1: COMPETITOR SWITCH TARGETS")
print("="*80)
print("High-volume Repatha/Praluent practices NOT using Leqvio\n")

switch_targets = []
for code, practice in repatha_practices.items():
    if code not in leqvio_practices:
        switch_targets.append({
            'code': code,
            'name': practice['name'],
            'competitor': 'Repatha',
            'items': practice['items']
        })

for code, practice in praluent_practices.items():
    if code not in leqvio_practices:
        switch_targets.append({
            'code': code,
            'name': practice['name'],
            'competitor': 'Praluent',
            'items': practice['items']
        })

switch_targets.sort(key=lambda x: x['items'], reverse=True)

if switch_targets:
    print(f"Found {len(switch_targets)} switching opportunities:\n")
    print(f"{'Code':<12} {'Competitor':<12} {'Rx':<8} {'Practice Name'}")
    print("-" * 80)
    for target in switch_targets[:15]:
        print(f"{target['code']:<12} {target['competitor']:<12} {target['items']:<8} {target['name'][:45]}")
else:
    print("✅ Excellent! Most competitor practices already using Leqvio")

# OPPORTUNITY 2: High-Volume Statin Practices (Conversion)
print("\n\n💊 OPPORTUNITY 2: HIGH-VOLUME STATIN CONVERSION TARGETS")
print("="*80)
print("Top statin practices with NO PCSK9i usage (prime conversion targets)\n")

conversion_targets = []
all_pcsk9i = set(leqvio_practices.keys()) | set(repatha_practices.keys()) | set(praluent_practices.keys())

for code, practice in statin_practices.items():
    if code not in all_pcsk9i and practice['items'] > 3000:  # High volume threshold
        conversion_targets.append({
            'code': code,
            'name': practice['name'],
            'statin_rx': practice['items'],
            'statin_cost': practice['cost'],
            'potential': practice['items'] * 0.05  # Assume 5% could be PCSK9i candidates
        })

conversion_targets.sort(key=lambda x: x['potential'], reverse=True)

print(f"Found {len(conversion_targets)} high-value conversion opportunities:\n")
print(f"{'Code':<12} {'Statin Rx':<12} {'Est. PCSK9i Potential':<22} {'Practice Name'}")
print("-" * 80)
for target in conversion_targets[:20]:
    print(f"{target['code']:<12} {target['statin_rx']:<12,} {target['potential']:<22.0f} {target['name'][:35]}")

# OPPORTUNITY 3: Leqvio Growth Opportunities  
print("\n\n📈 OPPORTUNITY 3: LEQVIO GROWTH OPPORTUNITIES")
print("="*80)
print("Practices already using Leqvio but with low volume (grow existing users)\n")

growth_targets = []
for code, practice in leqvio_practices.items():
    if code in statin_practices:
        statin_rx = statin_practices[code]['items']
        leqvio_rx = practice['items']
        penetration = (leqvio_rx / statin_rx * 100) if statin_rx > 0 else 0
        
        # Low penetration = growth opportunity
        if penetration < 2 and statin_rx > 2000:
            growth_targets.append({
                'code': code,
                'name': practice['name'],
                'leqvio_rx': leqvio_rx,
                'statin_rx': statin_rx,
                'penetration': penetration,
                'potential_growth': statin_rx * 0.03 - leqvio_rx  # Target 3% penetration
            })

growth_targets.sort(key=lambda x: x['potential_growth'], reverse=True)

print(f"Found {len(growth_targets)} growth opportunities:\n")
print(f"{'Code':<12} {'Current Leqvio':<15} {'Statin Rx':<12} {'Penetration':<12} {'Practice Name'}")
print("-" * 80)
for target in growth_targets[:20]:
    print(f"{target['code']:<12} {target['leqvio_rx']:<15.0f} {target['statin_rx']:<12,} {target['penetration']:<12.2f}% {target['name'][:30]}")

# Summary recommendations
print("\n\n" + "="*80)
print("📋 ACTIONABLE RECOMMENDATIONS")
print("="*80)
print(f"""
Priority 1: COMPETITOR SWITCHING ({len(switch_targets)} practices)
→ Rep visits to practices using Repatha/Praluent
→ Key message: Leqvio's twice-yearly dosing advantage
→ Estimated quick wins: {min(len(switch_targets), 10)} practices

Priority 2: HIGH-VOLUME CONVERSIONS ({len(conversion_targets)} practices)  
→ Target practices with 3,000+ statin prescriptions
→ Key message: Identify patients who've failed statins
→ Estimated potential: {sum(t['potential'] for t in conversion_targets[:20]):.0f} new Leqvio Rx

Priority 3: GROW EXISTING USERS ({len(growth_targets)} practices)
→ Low-penetration Leqvio practices with high statin volume
→ Key message: Educational support to identify more candidates
→ Estimated potential: {sum(t['potential_growth'] for t in growth_targets[:20]):.0f} incremental Rx

Total addressable opportunity in top targets: ~{
    sum(t.get('items', 0) for t in switch_targets[:10]) +
    sum(t.get('potential', 0) for t in conversion_targets[:20]) +
    sum(t.get('potential_growth', 0) for t in growth_targets[:20])
:.0f} prescriptions
""")

print("="*80)
print("💾 Next step: Export these lists to CRM for rep assignment")
print("="*80 + "\n")
