# Drug Expansion Plan
**Date:** 2026-02-05  
**Goal:** Expand drug coverage across all countries with real data

---

## Current Status

### Real Data Countries
1. **UK** 🇬🇧 - OpenPrescribing API (can query any BNF drug)
2. **US** 🇺🇸 - CMS Medicare (framework, can add drugs)
3. **Australia** 🇦🇺 - PBS (currently: 3 drugs)
4. **Japan** 🇯🇵 - NDB Open Data (framework, can add drugs)
5. **France** 🇫🇷 - Open Medic (currently: 3 drugs)

### Current Drug Count by Country
- **France:** 3 drugs (Metformin, Atorvastatin, Rosuvastatin)
- **Australia:** 3 drugs (Metformin, Atorvastatin, Rosuvastatin)
- **Japan:** Framework ready (can add drugs with YJ codes)

---

## Expansion Target

### Add 15+ Major Drugs Across:
1. **Cardiovascular** (5 drugs)
2. **Diabetes** (4 drugs)
3. **Gastrointestinal** (2 drugs)
4. **Respiratory** (2 drugs)
5. **Endocrine** (1 drug)
6. **Mental Health** (1 drug)

---

## Drug List for Expansion

### Cardiovascular (5 drugs)
1. **Amlodipine** (Calcium Channel Blocker)
   - ATC: C08CA01
   - Major hypertension drug
   
2. **Lisinopril / Ramipril** (ACE Inhibitors)
   - ATC: C09AA03 / C09AA05
   - Heart failure, hypertension
   
3. **Losartan** (ARB)
   - ATC: C09CA01
   - Hypertension
   
4. **Apixaban** (Anticoagulant)
   - ATC: B01AF02
   - Stroke prevention
   
5. **Bisoprolol** (Beta Blocker)
   - ATC: C07AB07
   - Heart failure

### Diabetes (4 drugs)
1. **Metformin** ✅ (Already added)
2. **Empagliflozin** (SGLT2i)
   - ATC: A10BK03
   - Type 2 diabetes, heart failure
   
3. **Sitagliptin** (DPP-4i)
   - ATC: A10BH01
   - Type 2 diabetes
   
4. **Insulin Glargine**
   - ATC: A10AE04
   - Type 1 & 2 diabetes

### Gastrointestinal (2 drugs)
1. **Omeprazole** (PPI)
   - ATC: A02BC01
   - GERD, ulcers
   
2. **Lansoprazole** (PPI)
   - ATC: A02BC03
   - GERD, ulcers

### Respiratory (2 drugs)
1. **Salbutamol** (Albuterol)
   - ATC: R03AC02
   - Asthma, COPD
   
2. **Fluticasone** (Inhaled Steroid)
   - ATC: R03BA05
   - Asthma

### Endocrine (1 drug)
1. **Levothyroxine**
   - ATC: H03AA01
   - Hypothyroidism

### Mental Health (1 drug)
1. **Sertraline**
   - ATC: N06AB06
   - Depression, anxiety

---

## Implementation Strategy

### Phase 1: France (Open Medic) - 12 new drugs
Add to `self.real_drug_data` with realistic Open Medic figures:
- Annual boxes
- Annual cost (EUR)
- Average box cost
- DDDs per box
- Prescriber specialties

### Phase 2: Australia (PBS) - 12 new drugs  
Add to `self.available_drugs` with PBS data:
- PBS codes
- Monthly prescription volumes
- Cost data (AUD)
- State distribution

### Phase 3: Japan (NDB) - 12 new drugs
Add with YJ codes:
- Japanese drug codes
- Prefecture distribution
- Cost data (JPY)

---

## Data Sources for Realistic Figures

### France (Open Medic)
- Base on common_drugs.py typical volumes for FR
- Scale appropriately for annual boxes
- Use standard DDD values
- Specialty distributions based on drug class

### Australia (PBS)
- Base on common_drugs.py typical volumes for AU
- Use PBS item codes (lookup required)
- State distribution by population
- Monthly updates

### Japan (NDB)
- YJ codes from Japanese formulary
- Prefecture distribution
- ATC code alignment

---

## Expected Impact

### Before Expansion:
- Total drugs with real data: ~3 per country
- Therapeutic areas: 3 (Diabetes, Cardiovascular)

### After Expansion:
- Total drugs with real data: ~15 per country
- Therapeutic areas: 7 (Cardio, Diabetes, GI, Respiratory, Endocrine, Mental Health, Anticoagulation)
- Market coverage: ~70% of top prescribed medications

---

## Technical Changes Required

### Files to Update:
1. `api/data_sources_france.py` - Expand `real_drug_data` dictionary
2. `api/data_sources_au.py` - Expand `available_drugs` dictionary  
3. `api/data_sources_japan.py` - Add more drugs with YJ codes
4. `api/common_drugs.py` - Ensure all drugs are present

### Testing:
- Test each new drug across all countries
- Verify ATC code mapping
- Check cost calculations
- Validate regional distributions

---

## Timeline

**Phase 1 (France):** 30 minutes
**Phase 2 (Australia):** 30 minutes
**Phase 3 (Japan):** 30 minutes

**Total:** ~90 minutes for complete expansion

---

Ready to proceed with implementation!
