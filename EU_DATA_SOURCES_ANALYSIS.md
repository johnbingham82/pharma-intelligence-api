# EU Pharmaceutical Data Sources Analysis
**Date:** 2026-02-05  
**Purpose:** Identify FREE real data sources for EU countries (proof-of-concept demo)  
**Focus:** Spain + other EU countries with accessible prescription/pharmaceutical data

---

## 🎯 Executive Summary

**BEST OPTION FOUND: France 🇫🇷**

France has **"Open Medic"** - an excellent FREE open data platform with:
- ✅ **2014-2024 data** (updated annually)
- ✅ **ATC classification** (same as your platform!)
- ✅ **Regional breakdowns** (13 régions)
- ✅ **Age/sex demographics**
- ✅ **Prescriber specialty data**
- ✅ **Completely FREE** - No API key required
- ✅ **CSV downloads** - Easy to integrate

**Second Option: Netherlands 🇳🇱**
- GIP database has open data but older (2011-2015 publicly available)

**Spain 🇪🇸 & Germany 🇩🇪:**
- Government portals exist but harder to access/limited open APIs

---

## 1️⃣ FRANCE 🇫🇷 - Open Medic (⭐ RECOMMENDED)

### Overview
- **Platform:** Open Medic via data.gouv.fr (French government open data portal)
- **Provider:** CNAM (Caisse Nationale d'Assurance Maladie)
- **Data Source:** SNDS (Système National des Données de Santé)
- **URL:** https://www.data.gouv.fr/datasets/open-medic-base-complete-sur-les-depenses-de-medicaments-interregimes

### Key Features
✅ **Comprehensive coverage** - All reimbursed medicines 2014-2024  
✅ **ATC Classification** - Uses standard ATC hierarchy (perfect match!)  
✅ **Regional data** - 13 French régions + département level  
✅ **Demographics** - Age groups, sex breakdowns  
✅ **Prescriber data** - By medical specialty  
✅ **Cost & volume** - Reimbursed amounts + boxes delivered  
✅ **FREE download** - CSV files, no API key required  

### Data Available

#### Base Complete Dataset (Open_Medic_YYYY)
- **Years:** 2014 - 2024 (annual releases)
- **Metrics:**
  - Montants remboursés (reimbursed amounts)
  - Montants remboursables (reimbursable amounts)
  - Nombre de boîtes délivrées (boxes delivered)
- **Dimensions:**
  - Age groups (tranches d'âge)
  - Sex (sexe)
  - Region (région de résidence - 13 régions)
  - Prescriber specialty (spécialité du prescripteur)

#### Enriched Datasets (NB_YYYY_*)
- **Additional metric:** Number of consumers (consommants)
- **ATC levels:** ATC1, ATC2, ATC3, ATC4, ATC5, CIP13 (most detailed)
- **48 different files** covering various combinations

### ATC Classification Structure
```
ATC1: Anatomical main group (e.g., A = Alimentary tract)
ATC2: Therapeutic subgroup
ATC3: Pharmacological subgroup
ATC4: Chemical subgroup
ATC5: Chemical substance (e.g., A10BA02 = Metformin)
```

### Geographic Coverage
**13 French Régions:**
1. Île-de-France (Paris)
2. Centre-Val de Loire
3. Bourgogne-Franche-Comté
4. Normandie
5. Hauts-de-France
6. Grand Est
7. Pays de la Loire
8. Bretagne
9. Nouvelle-Aquitaine
10. Occitanie
11. Auvergne-Rhône-Alpes
12. Provence-Alpes-Côte d'Azur
13. Corse

### Data Format
- **Format:** CSV files
- **Encoding:** UTF-8
- **Delimiter:** Semicolon (;)
- **Size:** Varies (largest ~500MB for complete datasets)

### Example Data Structure
```csv
L_ATC;L_ATC_SUBSTANCE;AGE;SEX;REGION;SPECIALITE_PRESCRIPTEUR;BOITES;REMB;BASE_REMB
A10BA02;Metformine;40-44;F;11 (Île-de-France);Médecin généraliste;123456;€456789;€500000
```

### Access Method
1. Visit: https://www.data.gouv.fr/datasets/open-medic-base-complete-sur-les-depenses-de-medicaments-interregimes
2. Select year (e.g., "Open_Medic_2024")
3. Download CSV files directly
4. No registration required

### Integration Approach
```python
import pandas as pd

# Download file from data.gouv.fr
url = "https://www.data.gouv.fr/fr/datasets/r/[RESOURCE_ID]"  # Get from website
df = pd.read_csv(url, sep=';', encoding='utf-8')

# Filter by ATC code (e.g., Metformin)
metformin = df[df['L_ATC'].str.startswith('A10BA02')]

# Aggregate by region
regional_summary = metformin.groupby('REGION').agg({
    'BOITES': 'sum',
    'REMB': 'sum'
})
```

### Limitations
❌ **Annual updates only** - Not monthly (vs UK which is monthly)  
❌ **1-year lag** - 2024 data published in 2025  
❌ **No API** - Must download CSV files manually  
❌ **French language** - Field names in French  
❌ **Excludes hospital** - Only community pharmacy  

### Citation
> "Open Medic, Caisse Nationale d'Assurance Maladie (CNAM), 2024"

---

## 2️⃣ NETHERLANDS 🇳🇱 - GIP Database

### Overview
- **Platform:** GIPdatabank.nl
- **Provider:** Zorginstituut Nederland (National Health Care Institute)
- **Open Data:** Available via data.openstate.eu
- **URL:** https://www.gipdatabank.nl/

### Key Features
✅ **ATC Classification** - Uses standard ATC codes  
✅ **Cost & volume data** - Deliveries, DDD, costs  
✅ **User statistics** - Number of unique users  
✅ **Free access** - CSV downloads  

### Data Available
- **Pharmaceutical care:**
  - Total deliveries (aantal leveringen)
  - Standard daily doses (DDD)
  - Reimbursement amounts
  - Number of unique users
  - Average DDD per user

- **Medical devices:**
  - Total deliveries
  - Total costs
  - Number of unique users

### Current Status
⚠️ **Limited open data availability:**
- **Open State dataset:** 2011-2015 (outdated)
- **GIPdatabank.nl:** Interactive portal (not easily downloadable)
- **No recent open CSV files** publicly available

### Access Method
1. **Interactive portal:** https://www.gipdatabank.nl/databank.asp
2. **Old CSV files:** https://data.openstate.eu/dataset/gip-databank
3. Manual queries through web interface

### Limitations
❌ **Outdated open data** - 2011-2015 only publicly available  
❌ **Limited API** - Mainly interactive web portal  
❌ **Requires navigation** - Not straightforward downloads  

---

## 3️⃣ SPAIN 🇪🇸 - Limited Open Data

### Overview
- **Portals:**
  - Ministerio de Sanidad: https://www.sanidad.gob.es/
  - datos.gob.es: Spanish open data portal
  - AEMPS (Agencia Española de Medicamentos)

### Current Status
⚠️ **Prescription data NOT easily accessible:**
- **Electronic prescription system** exists (Receta Electrónica SNS)
- **No public API** for prescription volumes
- **Limited open datasets** on pharmaceutical usage

### What IS Available
- ✅ **Medicine database** - Authorized medicines, financing status
- ✅ **Administrative data** - Drug approvals, registrations
- ❌ **Prescription volumes** - NOT publicly available
- ❌ **Regional statistics** - Limited access

### Why It's Difficult
- **Privacy regulations** - Stricter than UK/France
- **Decentralized system** - 17 Autonomous Communities manage separately
- **No unified portal** - Data fragmented across regions

### Verdict
❌ **NOT RECOMMENDED** for proof-of-concept (too difficult to access real data)

---

## 4️⃣ GERMANY 🇩🇪 - GKV Data

### Overview
- **System:** GKV (Gesetzliche Krankenversicherung - statutory health insurance)
- **Potential sources:**
  - GKV-Spitzenverband
  - DIMDI (Deutsches Institut für Medizinische Dokumentation)
  - Wissenschaftliches Institut der AOK (WIdO)

### Current Status
⚠️ **Limited public access:**
- **Research databases exist** but require applications
- **Arzneiverordnungsreport** - Annual report (summary only, not raw data)
- **No open API** for public use

### Limitations
❌ **Primarily for researchers** - Not open to public  
❌ **Application required** - Data access controlled  
❌ **Not suitable** for proof-of-concept demo  

---

## 5️⃣ ITALY 🇮🇹 - AIFA Data

### Overview
- **Agency:** AIFA (Agenzia Italiana del Farmaco)
- **Portal:** https://www.aifa.gov.it/

### Current Status
⚠️ **Limited open prescription data:**
- **L'uso dei Farmaci in Italia** - Annual report (PDF)
- **No open datasets** readily available
- **Regional variations** - Data managed locally

### Limitations
❌ **Reports only** - No raw datasets  
❌ **No API** - Must parse PDFs  
❌ **Not practical** for proof-of-concept  

---

## 🔄 Country Comparison

| Country | Data Availability | Format | Coverage | Update Freq | Ease of Use | Verdict |
|---------|------------------|--------|----------|-------------|-------------|---------|
| **France 🇫🇷** | ⭐⭐⭐⭐⭐ Excellent | CSV | 2014-2024 | Annual | ⭐⭐⭐⭐⭐ Easy | ✅ **USE THIS** |
| **Netherlands 🇳🇱** | ⭐⭐⭐ Moderate | CSV | 2011-2015 | Unknown | ⭐⭐⭐ Moderate | ⚠️ Outdated |
| **Spain 🇪🇸** | ⭐ Poor | N/A | N/A | N/A | ⭐ Difficult | ❌ Skip |
| **Germany 🇩🇪** | ⭐⭐ Limited | Research | Various | Annual | ⭐ Difficult | ❌ Skip |
| **Italy 🇮🇹** | ⭐ Poor | PDF | Annual | Annual | ⭐ Difficult | ❌ Skip |

---

## 📋 Recommendation for Your Platform

### ✅ Use France (Open Medic) for EU Demonstration

**Why France:**
1. **Best data quality** - Comprehensive, validated, official
2. **ATC codes** - Already using same classification as your platform
3. **Regional data** - 13 régions for geographic analysis
4. **Easy access** - Direct CSV download, no barriers
5. **Up-to-date** - 2024 data available now
6. **FREE** - No costs, no registration

**Implementation Strategy:**

### Step 1: Download Sample Data
```bash
# Visit: https://www.data.gouv.fr/datasets/open-medic-base-complete-sur-les-depenses-de-medicaments-interregimes
# Download: Open_Medic_2024.csv (or most recent year)
```

### Step 2: Create `data_sources_france.py`
```python
class FranceDataSource(PharmaceuticalDataSource):
    """Real data from France Open Medic (SNDS)"""
    
    def __init__(self):
        super().__init__()
        self.country_code = "FR"
        self.country_name = "France"
        self.data_type = "REAL"  # Not mock!
        self.regions = [
            "Île-de-France", "Centre-Val de Loire", 
            "Bourgogne-Franche-Comté", "Normandie",
            "Hauts-de-France", "Grand Est",
            "Pays de la Loire", "Bretagne",
            "Nouvelle-Aquitaine", "Occitanie",
            "Auvergne-Rhône-Alpes", "Provence-Alpes-Côte d'Azur",
            "Corse"
        ]
        self.population = 67_000_000
        self.data_source = "Open Medic / CNAM"
        
    def get_prescription_data(self, drug_code, region=None):
        """Query Open Medic data by ATC code"""
        # Load cached CSV or query on-demand
        df = self._load_open_medic_data()
        
        # Filter by ATC code
        drug_data = df[df['L_ATC'].str.startswith(drug_code)]
        
        if region:
            drug_data = drug_data[drug_data['REGION'] == region]
            
        return self._aggregate_results(drug_data)
```

### Step 3: Update Platform Status
```python
COUNTRIES = {
    'FR': {
        'name': 'France',
        'regions': 13,
        'population': 67_000_000,
        'data_type': 'REAL',
        'source': 'Open Medic (CNAM)',
        'badge': '🎯 REAL DATA'
    }
}
```

### Step 4: Test with Metformin
```python
# Query for Metformin (A10BA02)
results = france_source.get_prescription_data('A10BA02')
print(f"Metformin in France:")
print(f"  - Boxes delivered: {results['boxes']:,}")
print(f"  - Cost: €{results['cost']:,.2f}")
print(f"  - Regions: {len(results['regions'])}")
```

---

## 🚀 Next Steps

1. **Download French Open Medic data** (2024 or 2023)
2. **Create data loader** for CSV files
3. **Map ATC codes** to your existing drug database
4. **Update frontend** with France 🇫🇷 as "REAL DATA" country
5. **Add region selector** for 13 French régions
6. **Demo ready!** Show live French pharmaceutical data

---

## 💡 Alternative Approach: If You Want Spain

**Option A: Use EuroStat Aggregate Data**
- EU-wide statistics (not country-specific)
- High-level only, no regional detail

**Option B: Contact Spanish Health Authorities**
- Request access for research purposes
- May take weeks/months
- Not suitable for quick demo

**Option C: Continue with Mock Data**
- Keep Spain with realistic sample data
- Clearly label as "SAMPLE DATA"
- Focus France as your "REAL DATA" showcase

---

## 📊 Data Comparison: France vs UK

| Feature | France (Open Medic) | UK (OpenPrescribing) |
|---------|-------------------|---------------------|
| **Update Frequency** | Annual | Monthly |
| **Latest Data** | 2024 | December 2025 |
| **Geographic Detail** | 13 régions | 6,500+ GP practices |
| **Classification** | ATC | BNF codes |
| **API** | ❌ CSV downloads | ✅ REST API |
| **Ease of Access** | ⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐⭐ Very easy |
| **Data Quality** | Official government | Processed by Oxford |
| **Cost** | FREE | FREE |

**Both are excellent options!** UK has better API, France has ATC codes (your standard).

---

## ✅ Final Recommendation

**For your proof-of-concept demo:**

1. **Keep existing countries** (UK, US, AU, JP) with their current data sources
2. **Upgrade FRANCE** from mock → real Open Medic data
3. **Keep SPAIN** with sample data (but label clearly)
4. **Result:** 5 out of 9 countries with REAL DATA (UK, US, AU, JP, FR)

**This gives you:**
- ✅ Real European data (France)
- ✅ Easy to implement (CSV download)
- ✅ ATC classification (native)
- ✅ Regional breakdowns
- ✅ Completely free

**Time to implement:** ~2-3 hours for France integration

---

*Analysis completed: 2026-02-05*  
*Data sources verified: France (excellent), Netherlands (limited), Spain/Germany/Italy (difficult)*
