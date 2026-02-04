"""
Common Drug Database
Comprehensive list of top-prescribed drugs globally with realistic data
"""

COMMON_DRUGS = {
    # Cardiovascular / Antihypertensives
    'amlodipine': {
        'generic_name': 'Amlodipine',
        'brand_names': ['Norvasc', 'Istin'],
        'class': 'Calcium Channel Blocker',
        'indications': 'Hypertension, Angina',
        'typical_volumes': {
            'UK': {'prescriptions': 2100000, 'cost': 35000000},
            'US': {'prescriptions': 7500000, 'cost': 850000000},
            'AU': {'prescriptions': 850000, 'cost': 28000000},
            'FR': {'prescriptions': 650000, 'cost': 19000000},
            'DE': {'prescriptions': 780000, 'cost': 22000000},
        }
    },
    'lisinopril': {
        'generic_name': 'Lisinopril',
        'brand_names': ['Zestril', 'Prinivil'],
        'class': 'ACE Inhibitor',
        'indications': 'Hypertension, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 1800000, 'cost': 32000000},
            'US': {'prescriptions': 8500000, 'cost': 950000000},
            'AU': {'prescriptions': 720000, 'cost': 24000000},
            'FR': {'prescriptions': 580000, 'cost': 17000000},
            'DE': {'prescriptions': 690000, 'cost': 20000000},
        }
    },
    'ramipril': {
        'generic_name': 'Ramipril',
        'brand_names': ['Tritace', 'Altace'],
        'class': 'ACE Inhibitor',
        'indications': 'Hypertension, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 1600000, 'cost': 28000000},
            'US': {'prescriptions': 3200000, 'cost': 420000000},
            'AU': {'prescriptions': 680000, 'cost': 22000000},
            'FR': {'prescriptions': 520000, 'cost': 15000000},
            'DE': {'prescriptions': 890000, 'cost': 26000000},
        }
    },
    'losartan': {
        'generic_name': 'Losartan',
        'brand_names': ['Cozaar'],
        'class': 'ARB (Angiotensin Receptor Blocker)',
        'indications': 'Hypertension, Diabetic Nephropathy',
        'typical_volumes': {
            'UK': {'prescriptions': 1400000, 'cost': 45000000},
            'US': {'prescriptions': 6800000, 'cost': 780000000},
            'AU': {'prescriptions': 620000, 'cost': 28000000},
            'FR': {'prescriptions': 480000, 'cost': 18000000},
            'DE': {'prescriptions': 710000, 'cost': 25000000},
        }
    },
    
    # Statins
    'atorvastatin': {
        'generic_name': 'Atorvastatin',
        'brand_names': ['Lipitor'],
        'class': 'Statin',
        'indications': 'Hyperlipidemia, Cardiovascular Prevention',
        'typical_volumes': {
            'UK': {'prescriptions': 2500000, 'cost': 45000000},
            'US': {'prescriptions': 7200000, 'cost': 1100000000},
            'AU': {'prescriptions': 950000, 'cost': 32000000},
            'FR': {'prescriptions': 720000, 'cost': 28000000},
            'DE': {'prescriptions': 850000, 'cost': 35000000},
        }
    },
    'simvastatin': {
        'generic_name': 'Simvastatin',
        'brand_names': ['Zocor'],
        'class': 'Statin',
        'indications': 'Hyperlipidemia',
        'typical_volumes': {
            'UK': {'prescriptions': 1900000, 'cost': 38000000},
            'US': {'prescriptions': 5800000, 'cost': 680000000},
            'AU': {'prescriptions': 780000, 'cost': 25000000},
            'FR': {'prescriptions': 610000, 'cost': 21000000},
            'DE': {'prescriptions': 730000, 'cost': 26000000},
        }
    },
    'rosuvastatin': {
        'generic_name': 'Rosuvastatin',
        'brand_names': ['Crestor'],
        'class': 'Statin',
        'indications': 'Hyperlipidemia',
        'typical_volumes': {
            'UK': {'prescriptions': 1700000, 'cost': 52000000},
            'US': {'prescriptions': 5200000, 'cost': 820000000},
            'AU': {'prescriptions': 720000, 'cost': 30000000},
            'FR': {'prescriptions': 560000, 'cost': 22000000},
            'DE': {'prescriptions': 680000, 'cost': 28000000},
        }
    },
    
    # Diabetes
    'metformin': {
        'generic_name': 'Metformin',
        'brand_names': ['Glucophage', 'Riomet'],
        'class': 'Biguanide',
        'indications': 'Type 2 Diabetes',
        'typical_volumes': {
            'UK': {'prescriptions': 2200000, 'cost': 38000000},
            'US': {'prescriptions': 7800000, 'cost': 880000000},
            'AU': {'prescriptions': 980000, 'cost': 32000000},
            'FR': {'prescriptions': 750000, 'cost': 25000000},
            'DE': {'prescriptions': 890000, 'cost': 30000000},
        }
    },
    'insulin': {
        'generic_name': 'Insulin (various)',
        'brand_names': ['Humalog', 'Lantus', 'NovoRapid'],
        'class': 'Hormone',
        'indications': 'Diabetes (Type 1 & 2)',
        'typical_volumes': {
            'UK': {'prescriptions': 1200000, 'cost': 180000000},
            'US': {'prescriptions': 4500000, 'cost': 3200000000},
            'AU': {'prescriptions': 520000, 'cost': 95000000},
            'FR': {'prescriptions': 410000, 'cost': 72000000},
            'DE': {'prescriptions': 490000, 'cost': 85000000},
        }
    },
    'sitagliptin': {
        'generic_name': 'Sitagliptin',
        'brand_names': ['Januvia'],
        'class': 'DPP-4 Inhibitor',
        'indications': 'Type 2 Diabetes',
        'typical_volumes': {
            'UK': {'prescriptions': 680000, 'cost': 48000000},
            'US': {'prescriptions': 3200000, 'cost': 1800000000},
            'AU': {'prescriptions': 320000, 'cost': 28000000},
            'FR': {'prescriptions': 240000, 'cost': 18000000},
            'DE': {'prescriptions': 290000, 'cost': 22000000},
        }
    },
    'empagliflozin': {
        'generic_name': 'Empagliflozin',
        'brand_names': ['Jardiance'],
        'class': 'SGLT2 Inhibitor',
        'indications': 'Type 2 Diabetes, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 38000000},
            'US': {'prescriptions': 2800000, 'cost': 1500000000},
            'AU': {'prescriptions': 280000, 'cost': 25000000},
            'FR': {'prescriptions': 180000, 'cost': 15000000},
            'DE': {'prescriptions': 320000, 'cost': 28000000},
        }
    },
    
    # Gastrointestinal
    'omeprazole': {
        'generic_name': 'Omeprazole',
        'brand_names': ['Prilosec', 'Losec'],
        'class': 'Proton Pump Inhibitor',
        'indications': 'GERD, Peptic Ulcer',
        'typical_volumes': {
            'UK': {'prescriptions': 1800000, 'cost': 32000000},
            'US': {'prescriptions': 6500000, 'cost': 720000000},
            'AU': {'prescriptions': 780000, 'cost': 26000000},
            'FR': {'prescriptions': 620000, 'cost': 22000000},
            'DE': {'prescriptions': 740000, 'cost': 28000000},
        }
    },
    'lansoprazole': {
        'generic_name': 'Lansoprazole',
        'brand_names': ['Prevacid'],
        'class': 'Proton Pump Inhibitor',
        'indications': 'GERD, Peptic Ulcer',
        'typical_volumes': {
            'UK': {'prescriptions': 1500000, 'cost': 28000000},
            'US': {'prescriptions': 4200000, 'cost': 580000000},
            'AU': {'prescriptions': 620000, 'cost': 22000000},
            'FR': {'prescriptions': 480000, 'cost': 18000000},
            'DE': {'prescriptions': 580000, 'cost': 21000000},
        }
    },
    
    # Respiratory
    'salbutamol': {
        'generic_name': 'Salbutamol',
        'brand_names': ['Ventolin', 'Albuterol (US)'],
        'class': 'Short-acting Beta Agonist',
        'indications': 'Asthma, COPD',
        'typical_volumes': {
            'UK': {'prescriptions': 1600000, 'cost': 35000000},
            'US': {'prescriptions': 5800000, 'cost': 950000000},
            'AU': {'prescriptions': 680000, 'cost': 28000000},
            'FR': {'prescriptions': 520000, 'cost': 22000000},
            'DE': {'prescriptions': 620000, 'cost': 25000000},
        }
    },
    'fluticasone': {
        'generic_name': 'Fluticasone',
        'brand_names': ['Flonase', 'Flovent'],
        'class': 'Inhaled Corticosteroid',
        'indications': 'Asthma, Allergic Rhinitis',
        'typical_volumes': {
            'UK': {'prescriptions': 1200000, 'cost': 42000000},
            'US': {'prescriptions': 4800000, 'cost': 1200000000},
            'AU': {'prescriptions': 520000, 'cost': 32000000},
            'FR': {'prescriptions': 390000, 'cost': 25000000},
            'DE': {'prescriptions': 470000, 'cost': 28000000},
        }
    },
    
    # Thyroid
    'levothyroxine': {
        'generic_name': 'Levothyroxine',
        'brand_names': ['Synthroid', 'Levoxyl'],
        'class': 'Thyroid Hormone',
        'indications': 'Hypothyroidism',
        'typical_volumes': {
            'UK': {'prescriptions': 1400000, 'cost': 18000000},
            'US': {'prescriptions': 7200000, 'cost': 580000000},
            'AU': {'prescriptions': 620000, 'cost': 15000000},
            'FR': {'prescriptions': 480000, 'cost': 12000000},
            'DE': {'prescriptions': 580000, 'cost': 14000000},
        }
    },
    
    # Antidepressants
    'sertraline': {
        'generic_name': 'Sertraline',
        'brand_names': ['Zoloft'],
        'class': 'SSRI',
        'indications': 'Depression, Anxiety, PTSD',
        'typical_volumes': {
            'UK': {'prescriptions': 1100000, 'cost': 22000000},
            'US': {'prescriptions': 5200000, 'cost': 680000000},
            'AU': {'prescriptions': 480000, 'cost': 18000000},
            'FR': {'prescriptions': 380000, 'cost': 15000000},
            'DE': {'prescriptions': 450000, 'cost': 17000000},
        }
    },
    'citalopram': {
        'generic_name': 'Citalopram',
        'brand_names': ['Celexa', 'Cipramil'],
        'class': 'SSRI',
        'indications': 'Depression, Anxiety',
        'typical_volumes': {
            'UK': {'prescriptions': 980000, 'cost': 19000000},
            'US': {'prescriptions': 4500000, 'cost': 620000000},
            'AU': {'prescriptions': 420000, 'cost': 16000000},
            'FR': {'prescriptions': 340000, 'cost': 13000000},
            'DE': {'prescriptions': 410000, 'cost': 15000000},
        }
    },
    
    # Anticoagulants
    'warfarin': {
        'generic_name': 'Warfarin',
        'brand_names': ['Coumadin', 'Jantoven'],
        'class': 'Vitamin K Antagonist',
        'indications': 'Thromboembolism, Atrial Fibrillation',
        'typical_volumes': {
            'UK': {'prescriptions': 780000, 'cost': 12000000},
            'US': {'prescriptions': 3200000, 'cost': 280000000},
            'AU': {'prescriptions': 320000, 'cost': 9000000},
            'FR': {'prescriptions': 250000, 'cost': 7000000},
            'DE': {'prescriptions': 300000, 'cost': 8000000},
        }
    },
    'apixaban': {
        'generic_name': 'Apixaban',
        'brand_names': ['Eliquis'],
        'class': 'DOAC (Direct Oral Anticoagulant)',
        'indications': 'Atrial Fibrillation, DVT/PE',
        'typical_volumes': {
            'UK': {'prescriptions': 680000, 'cost': 95000000},
            'US': {'prescriptions': 4200000, 'cost': 2800000000},
            'AU': {'prescriptions': 320000, 'cost': 52000000},
            'FR': {'prescriptions': 240000, 'cost': 38000000},
            'DE': {'prescriptions': 290000, 'cost': 45000000},
        }
    },
    
    # Pain/Anti-inflammatory
    'paracetamol': {
        'generic_name': 'Paracetamol/Acetaminophen',
        'brand_names': ['Tylenol', 'Panadol'],
        'class': 'Analgesic/Antipyretic',
        'indications': 'Pain, Fever',
        'typical_volumes': {
            'UK': {'prescriptions': 2800000, 'cost': 15000000},
            'US': {'prescriptions': 8500000, 'cost': 380000000},
            'AU': {'prescriptions': 1200000, 'cost': 12000000},
            'FR': {'prescriptions': 920000, 'cost': 9000000},
            'DE': {'prescriptions': 1100000, 'cost': 11000000},
        }
    },
    'ibuprofen': {
        'generic_name': 'Ibuprofen',
        'brand_names': ['Advil', 'Motrin', 'Nurofen'],
        'class': 'NSAID',
        'indications': 'Pain, Inflammation, Fever',
        'typical_volumes': {
            'UK': {'prescriptions': 1400000, 'cost': 18000000},
            'US': {'prescriptions': 5200000, 'cost': 420000000},
            'AU': {'prescriptions': 620000, 'cost': 15000000},
            'FR': {'prescriptions': 480000, 'cost': 12000000},
            'DE': {'prescriptions': 580000, 'cost': 14000000},
        }
    },
}


def get_drug_info(drug_name: str):
    """Get drug information by name (case-insensitive)"""
    drug_key = drug_name.lower().strip()
    return COMMON_DRUGS.get(drug_key)


def get_all_drug_names():
    """Get list of all available drug names"""
    return [drug['generic_name'] for drug in COMMON_DRUGS.values()]


def search_drugs(query: str, limit: int = 10):
    """Search for drugs by name (generic or brand)"""
    query_lower = query.lower().strip()
    results = []
    
    for key, drug in COMMON_DRUGS.items():
        # Check generic name
        if query_lower in drug['generic_name'].lower():
            results.append({
                'id': key,
                'name': drug['generic_name'],
                'type': 'generic',
                'class': drug['class'],
                'indications': drug['indications']
            })
            continue
        
        # Check brand names
        for brand in drug['brand_names']:
            if query_lower in brand.lower():
                results.append({
                    'id': key,
                    'name': f"{brand} ({drug['generic_name']})",
                    'type': 'brand',
                    'class': drug['class'],
                    'indications': drug['indications']
                })
                break
    
    return results[:limit]
