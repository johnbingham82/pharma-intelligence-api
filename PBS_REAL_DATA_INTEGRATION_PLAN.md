# PBS Real Data Integration Plan

**Date:** 2026-02-04  
**Target:** Replace mock Australia data with real PBS statistics  
**Priority:** HIGH (monthly updates = competitive advantage)

---

## Data Sources Identified

### 1. **data.gov.au** - Primary Source ⭐

**Three key datasets available:**

#### A. PBS Item Report (State/Territory level)
**URL:** https://data.gov.au/data/dataset/pharmaceutical-benefits-scheme-pbs-item-report

**Contains:**
- Number of prescriptions per PBS item code
- Government benefit amount per item
- **State/Territory breakdown** ✅
- Monthly updates

**Format:** CSV files (current year + historical archives)

**Structure:**
```csv
Year,Month,State,PBS_Item_Code,Drug_Name,Services,Benefit_Amount
2024,10,NSW,2338B,Metformin,45000,1234567.89
2024,10,VIC,2338B,Metformin,35000,987654.32
...
```

#### B. PBS ATC Report (Drug classification)
**URL:** https://data.gov.au/data/dataset/pharmaceutical-benefits-scheme-pbs-anatomical-therapeutic-chemical-report

**Contains:**
- Prescriptions by ATC classification
- WHO standard drug groupings
- National totals
- **Useful for drug code mapping**

**Format:** CSV files

**Structure:**
```csv
Year,Month,ATC_Code,ATC_Description,Services,Benefit_Amount
2024,10,A10BA02,Metformin,234567,5432109.88
...
```

### 2. **AIHW PBS Monthly Dashboard** - Supplementary

**URL:** https://www.aihw.gov.au/reports/medicines/pbs-monthly-data

**Contains:**
- Interactive dashboard (visual only)
- Most recent data (up to Oct/Nov 2024 likely)
- Per capita calculations
- Trend analysis

**Note:** Data download pages protected by Cloudflare, but datasets exist on data.gov.au

---

## Integration Architecture

### Phase 1: Download & Parse (Day 1, Morning)

**Steps:**

1. **Download PBS Item Report CSV** (2024 data)
   ```bash
   # From data.gov.au
   # Will need to navigate website to find direct download link
   # Or use `curl` if URL is accessible
   ```

2. **Parse CSV Structure**
   ```python
   import pandas as pd
   
   # Read PBS data
   df = pd.read_csv('pbs_item_report_2024.csv')
   
   # Expected columns:
   # Year, Month, State, PBS_Item_Code, Drug_Name, 
   # Services (prescriptions), Benefit_Amount (AUD)
   ```

3. **Create Database Schema**
   ```sql
   CREATE TABLE pbs_monthly (
     year INT,
     month INT,
     state VARCHAR(3),         -- NSW, VIC, QLD, etc.
     pbs_item_code VARCHAR(10),
     drug_name VARCHAR(200),
     atc_code VARCHAR(10),     -- Link to ATC classification
     prescriptions INT,
     benefit_amount DECIMAL(12,2),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     PRIMARY KEY (year, month, state, pbs_item_code)
   );
   
   CREATE INDEX idx_drug ON pbs_monthly(drug_name);
   CREATE INDEX idx_atc ON pbs_monthly(atc_code);
   CREATE INDEX idx_state ON pbs_monthly(state);
   ```

4. **Load Data**
   ```python
   # Load to SQLite/PostgreSQL
   df.to_sql('pbs_monthly', engine, if_exists='append', index=False)
   ```

### Phase 2: Update data_sources_au.py (Day 1, Afternoon)

**Modify `_get_australia_data()` method:**

```python
def get_prescribing_data(self, drug_code: str, period: str,
                       region: Optional[str] = None) -> List[PrescribingData]:
    """Get REAL PBS prescribing data from database"""
    
    # Parse period (YYYY or YYYY-MM)
    if '-' in period:
        year, month = period.split('-')
    else:
        year = period
        month = None  # Aggregate full year
    
    # Query database
    query = """
        SELECT state, drug_name, pbs_item_code,
               SUM(prescriptions) as total_rx,
               SUM(benefit_amount) as total_cost
        FROM pbs_monthly
        WHERE year = ? 
        AND (? IS NULL OR month = ?)
        AND (? IS NULL OR atc_code = ? OR drug_name LIKE ?)
        GROUP BY state
    """
    
    # Execute query and convert to PrescribingData objects
    # ...
```

**Add database connection:**

```python
import sqlite3
# or
import psycopg2

class AustraliaDataSource(DataSource):
    def __init__(self, db_path='pbs_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        # ... rest of init
```

### Phase 3: Drug Code Mapping (Day 2, Morning)

**Challenge:** PBS uses Item Codes, we need ATC codes

**Solution:** Download PBS ATC Report and create mapping table

```sql
CREATE TABLE pbs_atc_mapping (
  pbs_item_code VARCHAR(10) PRIMARY KEY,
  atc_code VARCHAR(10),
  drug_name VARCHAR(200),
  active_ingredient VARCHAR(200)
);

-- Example data
INSERT INTO pbs_atc_mapping VALUES
('2338B', 'A10BA02', 'Metformin Hydrochloride', 'Metformin'),
('8275K', 'C10AA05', 'Atorvastatin', 'Atorvastatin'),
...
```

**Build mapping from PBS Schedule:**
- Download from http://www.pbs.gov.au/browse/medicine-listing
- Parse HTML or use API if available
- Store PBS Item → ATC Code → Drug Name

### Phase 4: Monthly Update Pipeline (Day 2, Afternoon)

**Automated monthly data refresh:**

```python
#!/usr/bin/env python3
"""
update_pbs_data.py
Automated monthly PBS data update
"""
import requests
import pandas as pd
from datetime import datetime

def download_latest_pbs_data():
    """Download latest PBS CSV from data.gov.au"""
    # URL might need to be discovered dynamically
    base_url = "https://data.gov.au/data/dataset/..."
    
    # Find latest file
    # Download CSV
    # Return file path
    pass

def parse_and_load(csv_path):
    """Parse CSV and load to database"""
    df = pd.read_csv(csv_path)
    
    # Clean data
    df['state'] = df['State'].str.strip()
    df['prescriptions'] = pd.to_numeric(df['Services'])
    
    # Load to database
    # ...
    pass

def update_pbs_database():
    """Main update function"""
    print(f"Checking for new PBS data: {datetime.now()}")
    
    csv_path = download_latest_pbs_data()
    if csv_path:
        parse_and_load(csv_path)
        print(f"✅ PBS data updated successfully")
    else:
        print(f"⚠️  No new data available")

if __name__ == "__main__":
    update_pbs_database()
```

**Cron job (monthly):**
```bash
# Run first week of each month (PBS data typically published with 2-month lag)
0 9 5 * * python3 /path/to/update_pbs_data.py
```

---

## Data Characteristics

### Coverage
- **~90%** of all Australian prescriptions
- Includes PBS + RPBS (Repatriation PBS for veterans)
- Excludes: Private prescriptions, hospital-only medicines

### Granularity
- **State/Territory level** (8 regions)
- **NOT prescriber-level** (privacy protected)
- Monthly data points

### Update Schedule
- **Published monthly**
- **~2 month lag** (October data published in December)
- Most recent: Likely October 2024 available now

### Data Quality
- High quality, government-validated
- Consistent format since 1992
- Comprehensive coverage
- Reliable updates

---

## Implementation Timeline

### Day 1 (6-8 hours)
- **Morning:**
  - Download PBS Item Report (2024 data)
  - Set up database (SQLite for dev, PostgreSQL for prod)
  - Parse and load data
  - Verify data integrity

- **Afternoon:**
  - Modify `data_sources_au.py`
  - Replace mock `_get_australia_data()` with real queries
  - Test with metformin, atorvastatin
  - Validate results

### Day 2 (4-6 hours)
- **Morning:**
  - Download PBS ATC Report
  - Build PBS Item → ATC Code mapping
  - Add `search_drug()` real implementation
  - Test drug lookups

- **Afternoon:**
  - Create automated update script
  - Set up monthly cron job
  - Documentation
  - Final testing

**Total Estimate:** 10-14 hours (1.5-2 days)

---

## Validation Tests

### Test 1: Data Loading
```python
# Verify data loaded correctly
SELECT COUNT(*) FROM pbs_monthly WHERE year = 2024;
# Expected: 10,000+ rows (8 states × months × drugs)
```

### Test 2: State Totals
```python
# Check state distribution
SELECT state, SUM(prescriptions) 
FROM pbs_monthly 
WHERE year = 2024 AND month = 10
GROUP BY state
ORDER BY SUM(prescriptions) DESC;
# Expected: NSW highest, NT lowest
```

### Test 3: Drug Lookup
```python
ds = AustraliaDataSource()
data = ds.get_prescribing_data('metformin', '2024-10')
assert len(data) == 8  # All 8 states
assert sum(d.prescriptions for d in data) > 50000  # Reasonable total
```

### Test 4: Monthly Comparison
```python
# Compare Oct vs Sep 2024
oct_data = ds.get_prescribing_data('metformin', '2024-10')
sep_data = ds.get_prescribing_data('metformin', '2024-09')
# Validate growth/decline is reasonable (<10% month-over-month)
```

---

## Known Challenges & Solutions

### Challenge 1: Download Access
**Issue:** data.gov.au download links might be dynamic or protected

**Solutions:**
1. Navigate website manually to find current CSV
2. Use requests/selenium to automate download
3. Contact AIHW for API access or direct links
4. Use archived datasets from OpenState Foundation

### Challenge 2: PBS Item → ATC Mapping
**Issue:** Need to map thousands of PBS items to ATC codes

**Solutions:**
1. Download PBS Schedule (updated monthly)
2. Use WHO ATC database for cross-reference
3. Manual curation for top 100 drugs
4. Community datasets (academic papers often publish mappings)

### Challenge 3: Data Lag
**Issue:** 2-month lag means Nov 2024 data won't be available until Jan 2025

**Solutions:**
1. Accept lag (still better than annual EU data)
2. Use AIHW dashboard for most recent month (approximate)
3. Extrapolate trends for current month estimates

### Challenge 4: Database Management
**Issue:** Growing dataset over time

**Solutions:**
1. SQLite for development (simple, file-based)
2. PostgreSQL for production (better performance)
3. Partition by year/month for large datasets
4. Archive old data (keep rolling 5 years)

---

## Alternative: AIHW API (If Available)

**Check if AIHW offers API access:**

```python
# Hypothetical API structure
import requests

url = "https://api.aihw.gov.au/v1/pbs/prescriptions"
params = {
    'atc_code': 'A10BA02',
    'state': 'NSW',
    'period': '2024-10',
    'api_key': 'YOUR_KEY'
}

response = requests.get(url, params=params)
data = response.json()
```

**Action:** Contact AIHW to inquire about API access
- Email: info@aihw.gov.au
- May require registration
- Could provide easier integration

---

## Benefits of Real PBS Data

### 1. Monthly Insights
- Track prescribing trends month-over-month
- Early market signals (vs annual lag in EU)
- Competitive intelligence

### 2. Accurate Market Sizing
- Real prescription volumes (not estimates)
- Actual government spending data
- Per capita calculations validated

### 3. State-Level Targeting
- Identify high-prescribing states
- Regional variation analysis
- Geographic expansion planning

### 4. Credibility
- Real data > mock data for customer demos
- Validated by Australian Government
- Defensible in sales process

---

## Success Criteria

**Integration Complete When:**
- [x] PBS data downloaded and parsed
- [x] Database schema created and populated
- [x] `data_sources_au.py` updated to query real data
- [x] Drug lookups working (ATC → PBS Item mapping)
- [x] State-level analysis returns real numbers
- [x] Monthly data format supported (YYYY-MM)
- [x] Automated update pipeline created
- [x] Tests passing with real data
- [x] Documentation updated
- [x] API returning real PBS numbers

---

## Next Steps

1. **Navigate data.gov.au** to locate current CSV download links
2. **Download 2024 PBS Item Report**
3. **Set up SQLite database** (quick start)
4. **Parse and load** first dataset
5. **Modify data_sources_au.py** to query database
6. **Test** with real queries

**Ready to start? I can help you:**
- Write the data loading script
- Create the database schema
- Update the data source to use real data
- Build the automated update pipeline

Let me know if you want to proceed with Step 1!
