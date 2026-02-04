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
    
    # More Cardiovascular
    'bisoprolol': {
        'generic_name': 'Bisoprolol',
        'brand_names': ['Zebeta', 'Cardicor'],
        'class': 'Beta Blocker',
        'indications': 'Hypertension, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 1300000, 'cost': 22000000},
            'US': {'prescriptions': 3800000, 'cost': 480000000},
            'AU': {'prescriptions': 520000, 'cost': 18000000},
            'FR': {'prescriptions': 410000, 'cost': 14000000},
            'DE': {'prescriptions': 680000, 'cost': 19000000},
        }
    },
    'atenolol': {
        'generic_name': 'Atenolol',
        'brand_names': ['Tenormin'],
        'class': 'Beta Blocker',
        'indications': 'Hypertension, Angina',
        'typical_volumes': {
            'UK': {'prescriptions': 1100000, 'cost': 18000000},
            'US': {'prescriptions': 3200000, 'cost': 380000000},
            'AU': {'prescriptions': 450000, 'cost': 15000000},
            'FR': {'prescriptions': 350000, 'cost': 12000000},
            'DE': {'prescriptions': 480000, 'cost': 14000000},
        }
    },
    'metoprolol': {
        'generic_name': 'Metoprolol',
        'brand_names': ['Lopressor', 'Toprol-XL'],
        'class': 'Beta Blocker',
        'indications': 'Hypertension, Angina, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 980000, 'cost': 17000000},
            'US': {'prescriptions': 5800000, 'cost': 720000000},
            'AU': {'prescriptions': 420000, 'cost': 14000000},
            'FR': {'prescriptions': 320000, 'cost': 11000000},
            'DE': {'prescriptions': 540000, 'cost': 15000000},
        }
    },
    'carvedilol': {
        'generic_name': 'Carvedilol',
        'brand_names': ['Coreg'],
        'class': 'Beta Blocker',
        'indications': 'Heart Failure, Hypertension',
        'typical_volumes': {
            'UK': {'prescriptions': 680000, 'cost': 28000000},
            'US': {'prescriptions': 2800000, 'cost': 580000000},
            'AU': {'prescriptions': 290000, 'cost': 19000000},
            'FR': {'prescriptions': 220000, 'cost': 15000000},
            'DE': {'prescriptions': 350000, 'cost': 18000000},
        }
    },
    'furosemide': {
        'generic_name': 'Furosemide',
        'brand_names': ['Lasix'],
        'class': 'Loop Diuretic',
        'indications': 'Edema, Heart Failure, Hypertension',
        'typical_volumes': {
            'UK': {'prescriptions': 1200000, 'cost': 12000000},
            'US': {'prescriptions': 4200000, 'cost': 320000000},
            'AU': {'prescriptions': 480000, 'cost': 9000000},
            'FR': {'prescriptions': 380000, 'cost': 7000000},
            'DE': {'prescriptions': 520000, 'cost': 8000000},
        }
    },
    'spironolactone': {
        'generic_name': 'Spironolactone',
        'brand_names': ['Aldactone'],
        'class': 'Potassium-Sparing Diuretic',
        'indications': 'Heart Failure, Edema, Hypertension',
        'typical_volumes': {
            'UK': {'prescriptions': 720000, 'cost': 18000000},
            'US': {'prescriptions': 2800000, 'cost': 420000000},
            'AU': {'prescriptions': 320000, 'cost': 14000000},
            'FR': {'prescriptions': 250000, 'cost': 11000000},
            'DE': {'prescriptions': 380000, 'cost': 13000000},
        }
    },
    'diltiazem': {
        'generic_name': 'Diltiazem',
        'brand_names': ['Cardizem', 'Tiazac'],
        'class': 'Calcium Channel Blocker',
        'indications': 'Hypertension, Angina, Arrhythmia',
        'typical_volumes': {
            'UK': {'prescriptions': 620000, 'cost': 22000000},
            'US': {'prescriptions': 2400000, 'cost': 480000000},
            'AU': {'prescriptions': 280000, 'cost': 15000000},
            'FR': {'prescriptions': 220000, 'cost': 12000000},
            'DE': {'prescriptions': 320000, 'cost': 14000000},
        }
    },
    'valsartan': {
        'generic_name': 'Valsartan',
        'brand_names': ['Diovan'],
        'class': 'ARB',
        'indications': 'Hypertension, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 38000000},
            'US': {'prescriptions': 3800000, 'cost': 680000000},
            'AU': {'prescriptions': 420000, 'cost': 25000000},
            'FR': {'prescriptions': 320000, 'cost': 19000000},
            'DE': {'prescriptions': 480000, 'cost': 22000000},
        }
    },
    'candesartan': {
        'generic_name': 'Candesartan',
        'brand_names': ['Atacand'],
        'class': 'ARB',
        'indications': 'Hypertension, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 780000, 'cost': 32000000},
            'US': {'prescriptions': 2200000, 'cost': 420000000},
            'AU': {'prescriptions': 350000, 'cost': 21000000},
            'FR': {'prescriptions': 270000, 'cost': 16000000},
            'DE': {'prescriptions': 410000, 'cost': 19000000},
        }
    },
    'perindopril': {
        'generic_name': 'Perindopril',
        'brand_names': ['Coversyl', 'Aceon'],
        'class': 'ACE Inhibitor',
        'indications': 'Hypertension, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 880000, 'cost': 28000000},
            'US': {'prescriptions': 1800000, 'cost': 280000000},
            'AU': {'prescriptions': 520000, 'cost': 19000000},
            'FR': {'prescriptions': 680000, 'cost': 22000000},
            'DE': {'prescriptions': 420000, 'cost': 15000000},
        }
    },
    'enalapril': {
        'generic_name': 'Enalapril',
        'brand_names': ['Vasotec'],
        'class': 'ACE Inhibitor',
        'indications': 'Hypertension, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 18000000},
            'US': {'prescriptions': 2800000, 'cost': 320000000},
            'AU': {'prescriptions': 420000, 'cost': 12000000},
            'FR': {'prescriptions': 340000, 'cost': 9000000},
            'DE': {'prescriptions': 480000, 'cost': 11000000},
        }
    },
    'clopidogrel': {
        'generic_name': 'Clopidogrel',
        'brand_names': ['Plavix'],
        'class': 'Antiplatelet',
        'indications': 'Acute Coronary Syndrome, Stroke Prevention',
        'typical_volumes': {
            'UK': {'prescriptions': 820000, 'cost': 45000000},
            'US': {'prescriptions': 3800000, 'cost': 920000000},
            'AU': {'prescriptions': 380000, 'cost': 32000000},
            'FR': {'prescriptions': 290000, 'cost': 25000000},
            'DE': {'prescriptions': 420000, 'cost': 28000000},
        }
    },
    'rivaroxaban': {
        'generic_name': 'Rivaroxaban',
        'brand_names': ['Xarelto'],
        'class': 'DOAC',
        'indications': 'Atrial Fibrillation, DVT/PE',
        'typical_volumes': {
            'UK': {'prescriptions': 620000, 'cost': 88000000},
            'US': {'prescriptions': 3200000, 'cost': 2200000000},
            'AU': {'prescriptions': 290000, 'cost': 48000000},
            'FR': {'prescriptions': 220000, 'cost': 35000000},
            'DE': {'prescriptions': 320000, 'cost': 42000000},
        }
    },
    'dabigatran': {
        'generic_name': 'Dabigatran',
        'brand_names': ['Pradaxa'],
        'class': 'DOAC',
        'indications': 'Atrial Fibrillation, DVT/PE',
        'typical_volumes': {
            'UK': {'prescriptions': 480000, 'cost': 72000000},
            'US': {'prescriptions': 2200000, 'cost': 1600000000},
            'AU': {'prescriptions': 220000, 'cost': 38000000},
            'FR': {'prescriptions': 170000, 'cost': 28000000},
            'DE': {'prescriptions': 250000, 'cost': 35000000},
        }
    },
    
    # More Statins
    'pravastatin': {
        'generic_name': 'Pravastatin',
        'brand_names': ['Pravachol'],
        'class': 'Statin',
        'indications': 'Hyperlipidemia',
        'typical_volumes': {
            'UK': {'prescriptions': 1100000, 'cost': 28000000},
            'US': {'prescriptions': 3200000, 'cost': 420000000},
            'AU': {'prescriptions': 480000, 'cost': 18000000},
            'FR': {'prescriptions': 380000, 'cost': 15000000},
            'DE': {'prescriptions': 520000, 'cost': 17000000},
        }
    },
    'fluvastatin': {
        'generic_name': 'Fluvastatin',
        'brand_names': ['Lescol'],
        'class': 'Statin',
        'indications': 'Hyperlipidemia',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 15000000},
            'US': {'prescriptions': 1200000, 'cost': 180000000},
            'AU': {'prescriptions': 180000, 'cost': 8000000},
            'FR': {'prescriptions': 140000, 'cost': 6000000},
            'DE': {'prescriptions': 210000, 'cost': 7000000},
        }
    },
    'ezetimibe': {
        'generic_name': 'Ezetimibe',
        'brand_names': ['Zetia', 'Ezetrol'],
        'class': 'Cholesterol Absorption Inhibitor',
        'indications': 'Hyperlipidemia',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 38000000},
            'US': {'prescriptions': 2800000, 'cost': 820000000},
            'AU': {'prescriptions': 280000, 'cost': 28000000},
            'FR': {'prescriptions': 210000, 'cost': 22000000},
            'DE': {'prescriptions': 320000, 'cost': 25000000},
        }
    },
    
    # More Diabetes
    'gliclazide': {
        'generic_name': 'Gliclazide',
        'brand_names': ['Diamicron'],
        'class': 'Sulfonylurea',
        'indications': 'Type 2 Diabetes',
        'typical_volumes': {
            'UK': {'prescriptions': 880000, 'cost': 18000000},
            'US': {'prescriptions': 980000, 'cost': 120000000},
            'AU': {'prescriptions': 420000, 'cost': 12000000},
            'FR': {'prescriptions': 620000, 'cost': 15000000},
            'DE': {'prescriptions': 380000, 'cost': 11000000},
        }
    },
    'glimepiride': {
        'generic_name': 'Glimepiride',
        'brand_names': ['Amaryl'],
        'class': 'Sulfonylurea',
        'indications': 'Type 2 Diabetes',
        'typical_volumes': {
            'UK': {'prescriptions': 620000, 'cost': 14000000},
            'US': {'prescriptions': 2200000, 'cost': 280000000},
            'AU': {'prescriptions': 280000, 'cost': 9000000},
            'FR': {'prescriptions': 220000, 'cost': 7000000},
            'DE': {'prescriptions': 420000, 'cost': 11000000},
        }
    },
    'pioglitazone': {
        'generic_name': 'Pioglitazone',
        'brand_names': ['Actos'],
        'class': 'Thiazolidinedione',
        'indications': 'Type 2 Diabetes',
        'typical_volumes': {
            'UK': {'prescriptions': 320000, 'cost': 18000000},
            'US': {'prescriptions': 1400000, 'cost': 380000000},
            'AU': {'prescriptions': 150000, 'cost': 12000000},
            'FR': {'prescriptions': 120000, 'cost': 9000000},
            'DE': {'prescriptions': 180000, 'cost': 11000000},
        }
    },
    'dapagliflozin': {
        'generic_name': 'Dapagliflozin',
        'brand_names': ['Forxiga', 'Farxiga'],
        'class': 'SGLT2 Inhibitor',
        'indications': 'Type 2 Diabetes, Heart Failure',
        'typical_volumes': {
            'UK': {'prescriptions': 380000, 'cost': 35000000},
            'US': {'prescriptions': 2400000, 'cost': 1300000000},
            'AU': {'prescriptions': 240000, 'cost': 22000000},
            'FR': {'prescriptions': 160000, 'cost': 14000000},
            'DE': {'prescriptions': 280000, 'cost': 25000000},
        }
    },
    'liraglutide': {
        'generic_name': 'Liraglutide',
        'brand_names': ['Victoza', 'Saxenda'],
        'class': 'GLP-1 Agonist',
        'indications': 'Type 2 Diabetes, Weight Management',
        'typical_volumes': {
            'UK': {'prescriptions': 280000, 'cost': 68000000},
            'US': {'prescriptions': 1800000, 'cost': 2200000000},
            'AU': {'prescriptions': 180000, 'cost': 42000000},
            'FR': {'prescriptions': 120000, 'cost': 28000000},
            'DE': {'prescriptions': 220000, 'cost': 48000000},
        }
    },
    'dulaglutide': {
        'generic_name': 'Dulaglutide',
        'brand_names': ['Trulicity'],
        'class': 'GLP-1 Agonist',
        'indications': 'Type 2 Diabetes',
        'typical_volumes': {
            'UK': {'prescriptions': 220000, 'cost': 52000000},
            'US': {'prescriptions': 2200000, 'cost': 2800000000},
            'AU': {'prescriptions': 150000, 'cost': 35000000},
            'FR': {'prescriptions': 100000, 'cost': 22000000},
            'DE': {'prescriptions': 180000, 'cost': 38000000},
        }
    },
    
    # More Antidepressants/Antianxiety
    'escitalopram': {
        'generic_name': 'Escitalopram',
        'brand_names': ['Lexapro', 'Cipralex'],
        'class': 'SSRI',
        'indications': 'Depression, Anxiety',
        'typical_volumes': {
            'UK': {'prescriptions': 780000, 'cost': 18000000},
            'US': {'prescriptions': 3800000, 'cost': 520000000},
            'AU': {'prescriptions': 350000, 'cost': 14000000},
            'FR': {'prescriptions': 280000, 'cost': 11000000},
            'DE': {'prescriptions': 380000, 'cost': 13000000},
        }
    },
    'fluoxetine': {
        'generic_name': 'Fluoxetine',
        'brand_names': ['Prozac'],
        'class': 'SSRI',
        'indications': 'Depression, OCD, Bulimia',
        'typical_volumes': {
            'UK': {'prescriptions': 1200000, 'cost': 22000000},
            'US': {'prescriptions': 4200000, 'cost': 580000000},
            'AU': {'prescriptions': 520000, 'cost': 18000000},
            'FR': {'prescriptions': 420000, 'cost': 15000000},
            'DE': {'prescriptions': 580000, 'cost': 17000000},
        }
    },
    'paroxetine': {
        'generic_name': 'Paroxetine',
        'brand_names': ['Paxil', 'Seroxat'],
        'class': 'SSRI',
        'indications': 'Depression, Anxiety, PTSD',
        'typical_volumes': {
            'UK': {'prescriptions': 620000, 'cost': 15000000},
            'US': {'prescriptions': 2800000, 'cost': 420000000},
            'AU': {'prescriptions': 280000, 'cost': 11000000},
            'FR': {'prescriptions': 220000, 'cost': 9000000},
            'DE': {'prescriptions': 320000, 'cost': 11000000},
        }
    },
    'venlafaxine': {
        'generic_name': 'Venlafaxine',
        'brand_names': ['Effexor'],
        'class': 'SNRI',
        'indications': 'Depression, Anxiety',
        'typical_volumes': {
            'UK': {'prescriptions': 680000, 'cost': 22000000},
            'US': {'prescriptions': 3200000, 'cost': 580000000},
            'AU': {'prescriptions': 320000, 'cost': 18000000},
            'FR': {'prescriptions': 250000, 'cost': 14000000},
            'DE': {'prescriptions': 380000, 'cost': 16000000},
        }
    },
    'duloxetine': {
        'generic_name': 'Duloxetine',
        'brand_names': ['Cymbalta'],
        'class': 'SNRI',
        'indications': 'Depression, Anxiety, Neuropathic Pain',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 28000000},
            'US': {'prescriptions': 2800000, 'cost': 720000000},
            'AU': {'prescriptions': 280000, 'cost': 22000000},
            'FR': {'prescriptions': 210000, 'cost': 17000000},
            'DE': {'prescriptions': 320000, 'cost': 20000000},
        }
    },
    'mirtazapine': {
        'generic_name': 'Mirtazapine',
        'brand_names': ['Remeron'],
        'class': 'Tetracyclic Antidepressant',
        'indications': 'Depression',
        'typical_volumes': {
            'UK': {'prescriptions': 820000, 'cost': 18000000},
            'US': {'prescriptions': 2400000, 'cost': 380000000},
            'AU': {'prescriptions': 350000, 'cost': 12000000},
            'FR': {'prescriptions': 280000, 'cost': 9000000},
            'DE': {'prescriptions': 420000, 'cost': 11000000},
        }
    },
    'amitriptyline': {
        'generic_name': 'Amitriptyline',
        'brand_names': ['Elavil'],
        'class': 'Tricyclic Antidepressant',
        'indications': 'Depression, Neuropathic Pain, Migraine',
        'typical_volumes': {
            'UK': {'prescriptions': 1400000, 'cost': 15000000},
            'US': {'prescriptions': 3800000, 'cost': 320000000},
            'AU': {'prescriptions': 620000, 'cost': 11000000},
            'FR': {'prescriptions': 480000, 'cost': 9000000},
            'DE': {'prescriptions': 680000, 'cost': 10000000},
        }
    },
    'trazodone': {
        'generic_name': 'Trazodone',
        'brand_names': ['Desyrel'],
        'class': 'Serotonin Antagonist',
        'indications': 'Depression, Insomnia',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 12000000},
            'US': {'prescriptions': 3200000, 'cost': 480000000},
            'AU': {'prescriptions': 220000, 'cost': 9000000},
            'FR': {'prescriptions': 170000, 'cost': 7000000},
            'DE': {'prescriptions': 280000, 'cost': 8000000},
        }
    },
    'lorazepam': {
        'generic_name': 'Lorazepam',
        'brand_names': ['Ativan'],
        'class': 'Benzodiazepine',
        'indications': 'Anxiety, Insomnia, Seizures',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 8000000},
            'US': {'prescriptions': 2800000, 'cost': 280000000},
            'AU': {'prescriptions': 280000, 'cost': 7000000},
            'FR': {'prescriptions': 620000, 'cost': 9000000},
            'DE': {'prescriptions': 320000, 'cost': 6000000},
        }
    },
    'diazepam': {
        'generic_name': 'Diazepam',
        'brand_names': ['Valium'],
        'class': 'Benzodiazepine',
        'indications': 'Anxiety, Muscle Spasm, Seizures',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 11000000},
            'US': {'prescriptions': 2400000, 'cost': 320000000},
            'AU': {'prescriptions': 420000, 'cost': 8000000},
            'FR': {'prescriptions': 780000, 'cost': 10000000},
            'DE': {'prescriptions': 480000, 'cost': 7000000},
        }
    },
    'alprazolam': {
        'generic_name': 'Alprazolam',
        'brand_names': ['Xanax'],
        'class': 'Benzodiazepine',
        'indications': 'Anxiety, Panic Disorder',
        'typical_volumes': {
            'UK': {'prescriptions': 180000, 'cost': 5000000},
            'US': {'prescriptions': 4200000, 'cost': 520000000},
            'AU': {'prescriptions': 120000, 'cost': 4000000},
            'FR': {'prescriptions': 220000, 'cost': 6000000},
            'DE': {'prescriptions': 150000, 'cost': 4000000},
        }
    },
    'zolpidem': {
        'generic_name': 'Zolpidem',
        'brand_names': ['Ambien', 'Stilnoct'],
        'class': 'Sedative-Hypnotic',
        'indications': 'Insomnia',
        'typical_volumes': {
            'UK': {'prescriptions': 380000, 'cost': 8000000},
            'US': {'prescriptions': 3800000, 'cost': 480000000},
            'AU': {'prescriptions': 220000, 'cost': 6000000},
            'FR': {'prescriptions': 520000, 'cost': 9000000},
            'DE': {'prescriptions': 280000, 'cost': 5000000},
        }
    },
    'zopiclone': {
        'generic_name': 'Zopiclone',
        'brand_names': ['Imovane', 'Zimovane'],
        'class': 'Sedative-Hypnotic',
        'indications': 'Insomnia',
        'typical_volumes': {
            'UK': {'prescriptions': 1200000, 'cost': 18000000},
            'US': {'prescriptions': 0, 'cost': 0},  # Not approved in US
            'AU': {'prescriptions': 520000, 'cost': 12000000},
            'FR': {'prescriptions': 780000, 'cost': 15000000},
            'DE': {'prescriptions': 420000, 'cost': 8000000},
        }
    },
    
    # Anticonvulsants/Mood Stabilizers
    'gabapentin': {
        'generic_name': 'Gabapentin',
        'brand_names': ['Neurontin'],
        'class': 'Anticonvulsant',
        'indications': 'Neuropathic Pain, Seizures',
        'typical_volumes': {
            'UK': {'prescriptions': 1800000, 'cost': 28000000},
            'US': {'prescriptions': 6800000, 'cost': 820000000},
            'AU': {'prescriptions': 780000, 'cost': 22000000},
            'FR': {'prescriptions': 620000, 'cost': 18000000},
            'DE': {'prescriptions': 880000, 'cost': 20000000},
        }
    },
    'pregabalin': {
        'generic_name': 'Pregabalin',
        'brand_names': ['Lyrica'],
        'class': 'Anticonvulsant',
        'indications': 'Neuropathic Pain, Fibromyalgia, Seizures',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 52000000},
            'US': {'prescriptions': 3800000, 'cost': 1200000000},
            'AU': {'prescriptions': 420000, 'cost': 38000000},
            'FR': {'prescriptions': 320000, 'cost': 28000000},
            'DE': {'prescriptions': 480000, 'cost': 35000000},
        }
    },
    'lamotrigine': {
        'generic_name': 'Lamotrigine',
        'brand_names': ['Lamictal'],
        'class': 'Anticonvulsant',
        'indications': 'Epilepsy, Bipolar Disorder',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 22000000},
            'US': {'prescriptions': 2400000, 'cost': 480000000},
            'AU': {'prescriptions': 280000, 'cost': 18000000},
            'FR': {'prescriptions': 210000, 'cost': 14000000},
            'DE': {'prescriptions': 320000, 'cost': 16000000},
        }
    },
    'levetiracetam': {
        'generic_name': 'Levetiracetam',
        'brand_names': ['Keppra'],
        'class': 'Anticonvulsant',
        'indications': 'Epilepsy',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 28000000},
            'US': {'prescriptions': 2200000, 'cost': 620000000},
            'AU': {'prescriptions': 220000, 'cost': 22000000},
            'FR': {'prescriptions': 170000, 'cost': 18000000},
            'DE': {'prescriptions': 280000, 'cost': 20000000},
        }
    },
    'sodium_valproate': {
        'generic_name': 'Sodium Valproate',
        'brand_names': ['Depakote', 'Epilim'],
        'class': 'Anticonvulsant',
        'indications': 'Epilepsy, Bipolar Disorder, Migraine',
        'typical_volumes': {
            'UK': {'prescriptions': 620000, 'cost': 18000000},
            'US': {'prescriptions': 1800000, 'cost': 380000000},
            'AU': {'prescriptions': 280000, 'cost': 12000000},
            'FR': {'prescriptions': 420000, 'cost': 15000000},
            'DE': {'prescriptions': 320000, 'cost': 11000000},
        }
    },
    'carbamazepine': {
        'generic_name': 'Carbamazepine',
        'brand_names': ['Tegretol'],
        'class': 'Anticonvulsant',
        'indications': 'Epilepsy, Trigeminal Neuralgia, Bipolar',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 12000000},
            'US': {'prescriptions': 1400000, 'cost': 280000000},
            'AU': {'prescriptions': 220000, 'cost': 8000000},
            'FR': {'prescriptions': 180000, 'cost': 7000000},
            'DE': {'prescriptions': 280000, 'cost': 9000000},
        }
    },
    'lithium': {
        'generic_name': 'Lithium',
        'brand_names': ['Priadel', 'Lithobid'],
        'class': 'Mood Stabilizer',
        'indications': 'Bipolar Disorder',
        'typical_volumes': {
            'UK': {'prescriptions': 280000, 'cost': 5000000},
            'US': {'prescriptions': 1200000, 'cost': 180000000},
            'AU': {'prescriptions': 120000, 'cost': 4000000},
            'FR': {'prescriptions': 95000, 'cost': 3000000},
            'DE': {'prescriptions': 150000, 'cost': 4000000},
        }
    },
    
    # Antipsychotics
    'quetiapine': {
        'generic_name': 'Quetiapine',
        'brand_names': ['Seroquel'],
        'class': 'Atypical Antipsychotic',
        'indications': 'Schizophrenia, Bipolar, Depression',
        'typical_volumes': {
            'UK': {'prescriptions': 680000, 'cost': 48000000},
            'US': {'prescriptions': 3800000, 'cost': 1200000000},
            'AU': {'prescriptions': 350000, 'cost': 38000000},
            'FR': {'prescriptions': 280000, 'cost': 32000000},
            'DE': {'prescriptions': 420000, 'cost': 35000000},
        }
    },
    'olanzapine': {
        'generic_name': 'Olanzapine',
        'brand_names': ['Zyprexa'],
        'class': 'Atypical Antipsychotic',
        'indications': 'Schizophrenia, Bipolar',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 28000000},
            'US': {'prescriptions': 2200000, 'cost': 680000000},
            'AU': {'prescriptions': 220000, 'cost': 22000000},
            'FR': {'prescriptions': 170000, 'cost': 18000000},
            'DE': {'prescriptions': 280000, 'cost': 20000000},
        }
    },
    'risperidone': {
        'generic_name': 'Risperidone',
        'brand_names': ['Risperdal'],
        'class': 'Atypical Antipsychotic',
        'indications': 'Schizophrenia, Bipolar, Autism Irritability',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 22000000},
            'US': {'prescriptions': 2800000, 'cost': 580000000},
            'AU': {'prescriptions': 280000, 'cost': 18000000},
            'FR': {'prescriptions': 220000, 'cost': 15000000},
            'DE': {'prescriptions': 320000, 'cost': 17000000},
        }
    },
    'aripiprazole': {
        'generic_name': 'Aripiprazole',
        'brand_names': ['Abilify'],
        'class': 'Atypical Antipsychotic',
        'indications': 'Schizophrenia, Bipolar, Depression',
        'typical_volumes': {
            'UK': {'prescriptions': 320000, 'cost': 42000000},
            'US': {'prescriptions': 2400000, 'cost': 1100000000},
            'AU': {'prescriptions': 180000, 'cost': 28000000},
            'FR': {'prescriptions': 140000, 'cost': 22000000},
            'DE': {'prescriptions': 220000, 'cost': 25000000},
        }
    },
    
    # More Respiratory
    'beclometasone': {
        'generic_name': 'Beclometasone',
        'brand_names': ['Qvar', 'Clenil'],
        'class': 'Inhaled Corticosteroid',
        'indications': 'Asthma',
        'typical_volumes': {
            'UK': {'prescriptions': 1100000, 'cost': 38000000},
            'US': {'prescriptions': 1800000, 'cost': 520000000},
            'AU': {'prescriptions': 480000, 'cost': 28000000},
            'FR': {'prescriptions': 380000, 'cost': 22000000},
            'DE': {'prescriptions': 520000, 'cost': 25000000},
        }
    },
    'budesonide': {
        'generic_name': 'Budesonide',
        'brand_names': ['Pulmicort', 'Symbicort'],
        'class': 'Inhaled Corticosteroid',
        'indications': 'Asthma, COPD',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 35000000},
            'US': {'prescriptions': 3200000, 'cost': 920000000},
            'AU': {'prescriptions': 420000, 'cost': 28000000},
            'FR': {'prescriptions': 320000, 'cost': 22000000},
            'DE': {'prescriptions': 480000, 'cost': 25000000},
        }
    },
    'tiotropium': {
        'generic_name': 'Tiotropium',
        'brand_names': ['Spiriva'],
        'class': 'Anticholinergic',
        'indications': 'COPD',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 52000000},
            'US': {'prescriptions': 2200000, 'cost': 1200000000},
            'AU': {'prescriptions': 280000, 'cost': 42000000},
            'FR': {'prescriptions': 210000, 'cost': 32000000},
            'DE': {'prescriptions': 320000, 'cost': 38000000},
        }
    },
    'montelukast': {
        'generic_name': 'Montelukast',
        'brand_names': ['Singulair'],
        'class': 'Leukotriene Receptor Antagonist',
        'indications': 'Asthma, Allergies',
        'typical_volumes': {
            'UK': {'prescriptions': 720000, 'cost': 28000000},
            'US': {'prescriptions': 3800000, 'cost': 680000000},
            'AU': {'prescriptions': 350000, 'cost': 22000000},
            'FR': {'prescriptions': 280000, 'cost': 18000000},
            'DE': {'prescriptions': 420000, 'cost': 20000000},
        }
    },
    
    # More GI
    'esomeprazole': {
        'generic_name': 'Esomeprazole',
        'brand_names': ['Nexium'],
        'class': 'Proton Pump Inhibitor',
        'indications': 'GERD, Peptic Ulcer',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 38000000},
            'US': {'prescriptions': 4200000, 'cost': 1100000000},
            'AU': {'prescriptions': 420000, 'cost': 32000000},
            'FR': {'prescriptions': 320000, 'cost': 25000000},
            'DE': {'prescriptions': 480000, 'cost': 28000000},
        }
    },
    'pantoprazole': {
        'generic_name': 'Pantoprazole',
        'brand_names': ['Protonix'],
        'class': 'Proton Pump Inhibitor',
        'indications': 'GERD, Peptic Ulcer',
        'typical_volumes': {
            'UK': {'prescriptions': 820000, 'cost': 32000000},
            'US': {'prescriptions': 3800000, 'cost': 720000000},
            'AU': {'prescriptions': 380000, 'cost': 25000000},
            'FR': {'prescriptions': 620000, 'cost': 28000000},
            'DE': {'prescriptions': 880000, 'cost': 32000000},
        }
    },
    'ranitidine': {
        'generic_name': 'Ranitidine',
        'brand_names': ['Zantac'],
        'class': 'H2 Blocker',
        'indications': 'GERD, Peptic Ulcer',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 8000000},
            'US': {'prescriptions': 1200000, 'cost': 180000000},
            'AU': {'prescriptions': 180000, 'cost': 5000000},
            'FR': {'prescriptions': 280000, 'cost': 6000000},
            'DE': {'prescriptions': 220000, 'cost': 5000000},
        }
    },
    'domperidone': {
        'generic_name': 'Domperidone',
        'brand_names': ['Motilium'],
        'class': 'Prokinetic',
        'indications': 'Nausea, Gastroparesis',
        'typical_volumes': {
            'UK': {'prescriptions': 680000, 'cost': 12000000},
            'US': {'prescriptions': 0, 'cost': 0},  # Not approved in US
            'AU': {'prescriptions': 420000, 'cost': 9000000},
            'FR': {'prescriptions': 520000, 'cost': 11000000},
            'DE': {'prescriptions': 320000, 'cost': 7000000},
        }
    },
    'loperamide': {
        'generic_name': 'Loperamide',
        'brand_names': ['Imodium'],
        'class': 'Antidiarrheal',
        'indications': 'Diarrhea',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 5000000},
            'US': {'prescriptions': 2200000, 'cost': 120000000},
            'AU': {'prescriptions': 280000, 'cost': 4000000},
            'FR': {'prescriptions': 420000, 'cost': 5000000},
            'DE': {'prescriptions': 320000, 'cost': 4000000},
        }
    },
    
    # Antibiotics (Commonly Prescribed)
    'amoxicillin': {
        'generic_name': 'Amoxicillin',
        'brand_names': ['Amoxil'],
        'class': 'Penicillin Antibiotic',
        'indications': 'Bacterial Infections',
        'typical_volumes': {
            'UK': {'prescriptions': 3200000, 'cost': 22000000},
            'US': {'prescriptions': 8800000, 'cost': 520000000},
            'AU': {'prescriptions': 1400000, 'cost': 18000000},
            'FR': {'prescriptions': 2800000, 'cost': 25000000},
            'DE': {'prescriptions': 1800000, 'cost': 16000000},
        }
    },
    'azithromycin': {
        'generic_name': 'Azithromycin',
        'brand_names': ['Zithromax', 'Z-Pak'],
        'class': 'Macrolide Antibiotic',
        'indications': 'Bacterial Infections',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 18000000},
            'US': {'prescriptions': 4200000, 'cost': 580000000},
            'AU': {'prescriptions': 520000, 'cost': 15000000},
            'FR': {'prescriptions': 680000, 'cost': 16000000},
            'DE': {'prescriptions': 480000, 'cost': 12000000},
        }
    },
    'doxycycline': {
        'generic_name': 'Doxycycline',
        'brand_names': ['Vibramycin'],
        'class': 'Tetracycline Antibiotic',
        'indications': 'Bacterial Infections, Acne',
        'typical_volumes': {
            'UK': {'prescriptions': 820000, 'cost': 15000000},
            'US': {'prescriptions': 3800000, 'cost': 480000000},
            'AU': {'prescriptions': 420000, 'cost': 12000000},
            'FR': {'prescriptions': 520000, 'cost': 14000000},
            'DE': {'prescriptions': 380000, 'cost': 11000000},
        }
    },
    'ciprofloxacin': {
        'generic_name': 'Ciprofloxacin',
        'brand_names': ['Cipro'],
        'class': 'Fluoroquinolone Antibiotic',
        'indications': 'Bacterial Infections, UTI',
        'typical_volumes': {
            'UK': {'prescriptions': 680000, 'cost': 14000000},
            'US': {'prescriptions': 2800000, 'cost': 420000000},
            'AU': {'prescriptions': 320000, 'cost': 11000000},
            'FR': {'prescriptions': 420000, 'cost': 12000000},
            'DE': {'prescriptions': 520000, 'cost': 13000000},
        }
    },
    'trimethoprim': {
        'generic_name': 'Trimethoprim',
        'brand_names': ['Primsol'],
        'class': 'Antibiotic',
        'indications': 'UTI',
        'typical_volumes': {
            'UK': {'prescriptions': 1200000, 'cost': 9000000},
            'US': {'prescriptions': 1800000, 'cost': 180000000},
            'AU': {'prescriptions': 520000, 'cost': 7000000},
            'FR': {'prescriptions': 420000, 'cost': 6000000},
            'DE': {'prescriptions': 620000, 'cost': 7000000},
        }
    },
    
    # More Pain/Inflammation
    'naproxen': {
        'generic_name': 'Naproxen',
        'brand_names': ['Aleve', 'Naprosyn'],
        'class': 'NSAID',
        'indications': 'Pain, Inflammation',
        'typical_volumes': {
            'UK': {'prescriptions': 820000, 'cost': 12000000},
            'US': {'prescriptions': 3200000, 'cost': 380000000},
            'AU': {'prescriptions': 380000, 'cost': 9000000},
            'FR': {'prescriptions': 420000, 'cost': 10000000},
            'DE': {'prescriptions': 320000, 'cost': 8000000},
        }
    },
    'diclofenac': {
        'generic_name': 'Diclofenac',
        'brand_names': ['Voltaren'],
        'class': 'NSAID',
        'indications': 'Pain, Inflammation, Arthritis',
        'typical_volumes': {
            'UK': {'prescriptions': 1100000, 'cost': 18000000},
            'US': {'prescriptions': 2800000, 'cost': 420000000},
            'AU': {'prescriptions': 520000, 'cost': 14000000},
            'FR': {'prescriptions': 680000, 'cost': 16000000},
            'DE': {'prescriptions': 880000, 'cost': 17000000},
        }
    },
    'celecoxib': {
        'generic_name': 'Celecoxib',
        'brand_names': ['Celebrex'],
        'class': 'COX-2 Inhibitor',
        'indications': 'Arthritis, Pain',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 28000000},
            'US': {'prescriptions': 2200000, 'cost': 820000000},
            'AU': {'prescriptions': 220000, 'cost': 22000000},
            'FR': {'prescriptions': 170000, 'cost': 18000000},
            'DE': {'prescriptions': 280000, 'cost': 20000000},
        }
    },
    'tramadol': {
        'generic_name': 'Tramadol',
        'brand_names': ['Ultram', 'Tramal'],
        'class': 'Opioid Analgesic',
        'indications': 'Moderate Pain',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 18000000},
            'US': {'prescriptions': 3800000, 'cost': 520000000},
            'AU': {'prescriptions': 420000, 'cost': 14000000},
            'FR': {'prescriptions': 620000, 'cost': 16000000},
            'DE': {'prescriptions': 520000, 'cost': 15000000},
        }
    },
    'codeine': {
        'generic_name': 'Codeine',
        'brand_names': ['Co-codamol (with paracetamol)'],
        'class': 'Opioid Analgesic',
        'indications': 'Mild to Moderate Pain',
        'typical_volumes': {
            'UK': {'prescriptions': 1800000, 'cost': 15000000},
            'US': {'prescriptions': 2400000, 'cost': 280000000},
            'AU': {'prescriptions': 820000, 'cost': 11000000},
            'FR': {'prescriptions': 1200000, 'cost': 14000000},
            'DE': {'prescriptions': 680000, 'cost': 9000000},
        }
    },
    
    # Steroids
    'prednisolone': {
        'generic_name': 'Prednisolone',
        'brand_names': ['Prelone'],
        'class': 'Corticosteroid',
        'indications': 'Inflammation, Autoimmune, Asthma',
        'typical_volumes': {
            'UK': {'prescriptions': 1400000, 'cost': 15000000},
            'US': {'prescriptions': 3200000, 'cost': 380000000},
            'AU': {'prescriptions': 620000, 'cost': 12000000},
            'FR': {'prescriptions': 520000, 'cost': 11000000},
            'DE': {'prescriptions': 680000, 'cost': 13000000},
        }
    },
    'prednisone': {
        'generic_name': 'Prednisone',
        'brand_names': ['Deltasone'],
        'class': 'Corticosteroid',
        'indications': 'Inflammation, Autoimmune',
        'typical_volumes': {
            'UK': {'prescriptions': 820000, 'cost': 12000000},
            'US': {'prescriptions': 4200000, 'cost': 480000000},
            'AU': {'prescriptions': 420000, 'cost': 10000000},
            'FR': {'prescriptions': 320000, 'cost': 9000000},
            'DE': {'prescriptions': 480000, 'cost': 11000000},
        }
    },
    'hydrocortisone': {
        'generic_name': 'Hydrocortisone',
        'brand_names': ['Cortef', 'Solu-Cortef'],
        'class': 'Corticosteroid',
        'indications': 'Adrenal Insufficiency, Inflammation',
        'typical_volumes': {
            'UK': {'prescriptions': 620000, 'cost': 8000000},
            'US': {'prescriptions': 2200000, 'cost': 280000000},
            'AU': {'prescriptions': 280000, 'cost': 7000000},
            'FR': {'prescriptions': 220000, 'cost': 6000000},
            'DE': {'prescriptions': 320000, 'cost': 7000000},
        }
    },
    
    # Antihistamines
    'cetirizine': {
        'generic_name': 'Cetirizine',
        'brand_names': ['Zyrtec'],
        'class': 'Antihistamine',
        'indications': 'Allergies, Urticaria',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 8000000},
            'US': {'prescriptions': 4200000, 'cost': 320000000},
            'AU': {'prescriptions': 520000, 'cost': 7000000},
            'FR': {'prescriptions': 680000, 'cost': 9000000},
            'DE': {'prescriptions': 420000, 'cost': 6000000},
        }
    },
    'loratadine': {
        'generic_name': 'Loratadine',
        'brand_names': ['Claritin'],
        'class': 'Antihistamine',
        'indications': 'Allergies',
        'typical_volumes': {
            'UK': {'prescriptions': 820000, 'cost': 7000000},
            'US': {'prescriptions': 3800000, 'cost': 280000000},
            'AU': {'prescriptions': 420000, 'cost': 6000000},
            'FR': {'prescriptions': 520000, 'cost': 8000000},
            'DE': {'prescriptions': 380000, 'cost': 5000000},
        }
    },
    'fexofenadine': {
        'generic_name': 'Fexofenadine',
        'brand_names': ['Allegra'],
        'class': 'Antihistamine',
        'indications': 'Allergies',
        'typical_volumes': {
            'UK': {'prescriptions': 620000, 'cost': 12000000},
            'US': {'prescriptions': 2800000, 'cost': 380000000},
            'AU': {'prescriptions': 320000, 'cost': 9000000},
            'FR': {'prescriptions': 280000, 'cost': 10000000},
            'DE': {'prescriptions': 380000, 'cost': 11000000},
        }
    },
    
    # Osteoporosis
    'alendronate': {
        'generic_name': 'Alendronate',
        'brand_names': ['Fosamax'],
        'class': 'Bisphosphonate',
        'indications': 'Osteoporosis',
        'typical_volumes': {
            'UK': {'prescriptions': 680000, 'cost': 18000000},
            'US': {'prescriptions': 2800000, 'cost': 480000000},
            'AU': {'prescriptions': 320000, 'cost': 14000000},
            'FR': {'prescriptions': 420000, 'cost': 16000000},
            'DE': {'prescriptions': 520000, 'cost': 17000000},
        }
    },
    'risedronate': {
        'generic_name': 'Risedronate',
        'brand_names': ['Actonel'],
        'class': 'Bisphosphonate',
        'indications': 'Osteoporosis',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 22000000},
            'US': {'prescriptions': 1400000, 'cost': 380000000},
            'AU': {'prescriptions': 180000, 'cost': 15000000},
            'FR': {'prescriptions': 220000, 'cost': 16000000},
            'DE': {'prescriptions': 280000, 'cost': 18000000},
        }
    },
    
    # Urological
    'tamsulosin': {
        'generic_name': 'Tamsulosin',
        'brand_names': ['Flomax'],
        'class': 'Alpha Blocker',
        'indications': 'Benign Prostatic Hyperplasia',
        'typical_volumes': {
            'UK': {'prescriptions': 920000, 'cost': 22000000},
            'US': {'prescriptions': 3800000, 'cost': 580000000},
            'AU': {'prescriptions': 420000, 'cost': 18000000},
            'FR': {'prescriptions': 520000, 'cost': 20000000},
            'DE': {'prescriptions': 680000, 'cost': 21000000},
        }
    },
    'finasteride': {
        'generic_name': 'Finasteride',
        'brand_names': ['Proscar', 'Propecia'],
        'class': '5-Alpha Reductase Inhibitor',
        'indications': 'BPH, Hair Loss',
        'typical_volumes': {
            'UK': {'prescriptions': 520000, 'cost': 18000000},
            'US': {'prescriptions': 2800000, 'cost': 520000000},
            'AU': {'prescriptions': 280000, 'cost': 15000000},
            'FR': {'prescriptions': 220000, 'cost': 12000000},
            'DE': {'prescriptions': 380000, 'cost': 14000000},
        }
    },
    'solifenacin': {
        'generic_name': 'Solifenacin',
        'brand_names': ['Vesicare'],
        'class': 'Antimuscarinic',
        'indications': 'Overactive Bladder',
        'typical_volumes': {
            'UK': {'prescriptions': 420000, 'cost': 28000000},
            'US': {'prescriptions': 1800000, 'cost': 680000000},
            'AU': {'prescriptions': 180000, 'cost': 22000000},
            'FR': {'prescriptions': 140000, 'cost': 18000000},
            'DE': {'prescriptions': 220000, 'cost': 20000000},
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
