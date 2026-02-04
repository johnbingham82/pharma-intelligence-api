# Pharma Intelligence Engine - Generalized Analysis Platform

**Version 2.0 - Drug & Country Agnostic**

---

## 🎯 Overview

The Pharma Intelligence Engine is a **generalized, modular platform** for analyzing pharmaceutical prescribing patterns across any drug and any country. Unlike the original GP Profiler (hardcoded for Leqvio/UK), this engine is:

✅ **Drug-agnostic** - Works with any pharmaceutical product  
✅ **Country-agnostic** - Pluggable data sources for any market  
✅ **Therapeutic-area agnostic** - No hardcoded clinical assumptions  
✅ **Scoring-flexible** - Multiple opportunity scoring algorithms  
✅ **Extensible** - Easy to add new countries, scorers, or features  

---

## 🏗️ Architecture

### Core Components

```
pharma_intelligence_engine.py     # Core analysis engine
├── Drug                          # Data model for products
├── Prescriber                    # Data model for prescribers
├── PrescribingData              # Data model for prescribing metrics
├── OpportunityProfile           # Data model for opportunities
├── DataSource (abstract)        # Interface for country-specific data
├── OpportunityScorer (abstract) # Interface for scoring algorithms
├── Segmenter                    # Prescriber segmentation logic
├── RecommendationEngine         # Generates actionable recommendations
└── PharmaIntelligenceEngine     # Main orchestration class
```

### Data Sources (Country-Specific)

```
data_sources_uk.py               # UK NHS OpenPrescribing
data_sources_us.py               # US Medicare (future)
data_sources_eu.py               # EU markets (future)
```

Each data source implements the `DataSource` interface:
- `search_drug(name)` - Find drug codes
- `get_prescribing_data()` - Fetch prescribing data
- `get_prescriber_details()` - Get prescriber information
- `get_latest_period()` - Get most recent data period

---

## 🚀 Quick Start

### Basic Usage

```python
from pharma_intelligence_engine import PharmaIntelligenceEngine, create_drug
from data_sources_uk import UKDataSource

# Initialize engine with UK data source
uk_data = UKDataSource()
engine = PharmaIntelligenceEngine(data_source=uk_data)

# Define your drug
my_drug = create_drug(
    name="Inclisiran",
    generic_name="inclisiran",
    therapeutic_area="Cardiovascular - Lipid Management",
    company="Novartis",
    country_codes={'UK': uk_data.find_drug_code('inclisiran')}
)

# Run analysis
report = engine.analyze_drug(
    drug=my_drug,
    country='UK',
    region=None,        # Optional: filter by region
    top_n=50           # Top N opportunities to return
)

# Report saved automatically as JSON
print(f"Analysis complete! Top opportunity: {report['top_opportunities'][0]}")
```

### Multi-Drug Analysis

```python
# Analyze multiple drugs at once
drugs = ['metformin', 'atorvastatin', 'salbutamol']

for drug_name in drugs:
    drug = create_drug(
        name=drug_name.capitalize(),
        generic_name=drug_name,
        therapeutic_area="Various",
        company="Various",
        country_codes={'UK': uk_data.find_drug_code(drug_name)}
    )
    
    report = engine.analyze_drug(drug, country='UK', top_n=20)
```

**See `demo_multi_drug_analysis.py` for a complete working example.**

---

## 📊 Output Format

### JSON Report Structure

```json
{
  "drug": {
    "name": "Inclisiran",
    "generic_name": "inclisiran",
    "therapeutic_area": "Cardiovascular - Lipid Management",
    "company": "Novartis"
  },
  "analysis_date": "2026-02-04T10:30:00",
  "country": "UK",
  "period": "2025-10-01",
  "market_summary": {
    "total_prescribers": 4520,
    "total_prescriptions": 45230,
    "total_cost": 12500000,
    "avg_prescriptions_per_prescriber": 10.01
  },
  "top_opportunities": [
    {
      "rank": 1,
      "prescriber_id": "Y12345",
      "prescriber_name": "High Street Medical Centre",
      "location": "Greater Manchester",
      "current_volume": 450,
      "opportunity_score": 1523.5,
      "recommendations": [
        "⭐ KEY ACCOUNT: Maintain strong relationship",
        "🎓 Invite to advisory board or speaker program"
      ]
    }
  ],
  "segments": {
    "by_volume": {
      "High Prescribers": 120,
      "Medium Prescribers": 580,
      "Low Prescribers": 1200,
      "Non-Prescribers": 2620
    }
  }
}
```

---

## 🧮 Scoring Algorithms

### Available Scorers

**1. SimpleVolumeScorer**
- Basic scoring based on prescription volume
- Good for quick prioritization
- No market context required

```python
from pharma_intelligence_engine import SimpleVolumeScorer
engine = PharmaIntelligenceEngine(data_source=uk_data, scorer=SimpleVolumeScorer())
```

**2. MarketShareScorer (default)**
- Advanced scoring incorporating:
  - Current volume
  - Market share (low share = high opportunity)
  - Practice size normalization
  - Drug cost weighting
- Better for competitive markets

```python
from pharma_intelligence_engine import MarketShareScorer
engine = PharmaIntelligenceEngine(data_source=uk_data, scorer=MarketShareScorer())
```

### Custom Scorer

Create your own by subclassing `OpportunityScorer`:

```python
from pharma_intelligence_engine import OpportunityScorer

class CustomScorer(OpportunityScorer):
    def calculate_score(self, data: PrescribingData, context: Dict) -> float:
        # Your custom logic here
        base_score = data.prescriptions
        
        # Example: Boost high-cost drugs
        if data.cost / data.prescriptions > 500:
            base_score *= 2.0
        
        return base_score

engine = PharmaIntelligenceEngine(data_source=uk_data, scorer=CustomScorer())
```

---

## 🎯 Segmentation

The engine automatically segments prescribers into actionable groups:

### Volume-Based Segmentation
- **High Prescribers** - Above 2x average volume
- **Medium Prescribers** - 0.5-2x average volume
- **Low Prescribers** - Below 0.5x average
- **Non-Prescribers** - Zero current volume

### Opportunity-Based Segmentation
- **Quick Wins** - High volume, low effort to grow
- **Strategic Growth** - High potential, medium effort
- **New Business** - Zero share, need conversion
- **Defend** - High share, risk of loss

---

## 🌍 Adding New Countries

To add a new country, create a data source adapter:

```python
from pharma_intelligence_engine import DataSource, PrescribingData, Prescriber

class USDataSource(DataSource):
    def __init__(self):
        # Initialize US data connections (Medicare, IQVIA, etc.)
        pass
    
    def search_drug(self, name: str) -> List[Dict]:
        # Implement drug search for US (NDC codes)
        pass
    
    def get_prescribing_data(self, drug_code: str, period: str, 
                           region: Optional[str] = None) -> List[PrescribingData]:
        # Fetch US prescribing data
        pass
    
    def get_prescriber_details(self, prescriber_ids: List[str]) -> List[Prescriber]:
        # Get US prescriber details
        pass
    
    def get_latest_period(self) -> str:
        # Return latest data period
        return "2025-Q3"
```

Then use it:

```python
us_data = USDataSource()
engine = PharmaIntelligenceEngine(data_source=us_data)

drug = create_drug(
    name="Keytruda",
    generic_name="pembrolizumab",
    therapeutic_area="Oncology",
    company="MSD",
    country_codes={'US': '12345-6789'}  # NDC code
)

report = engine.analyze_drug(drug, country='US')
```

---

## 💡 Recommendations Engine

The engine generates context-aware recommendations based on:

1. **Current volume** (new vs established prescribers)
2. **Market share** (penetration level)
3. **Competitive position** (vs alternatives)
4. **Therapeutic area** (disease-specific context)

Example recommendations:

```
🎯 NEW PRESCRIBER: Schedule introductory MSL visit
📧 Send product monograph and clinical trial data
📈 GROWTH OPPORTUNITY: Low volume, high potential
🤝 Arrange peer-to-peer meeting with high prescriber
⭐ KEY ACCOUNT: Maintain strong relationship
⚠️ LOW SHARE (8.5%): Address access barriers
```

---

## 🔧 Advanced Features

### Regional Filtering

```python
# Analyze specific region only
report = engine.analyze_drug(
    drug=my_drug,
    country='UK',
    region='15N',  # NHS Devon ICB code
    top_n=50
)
```

### Competitive Analysis (Future)

```python
# Compare against competitors
competitors = [
    create_drug("Repatha", "evolocumab", "Cardiovascular", "Amgen", {...}),
    create_drug("Praluent", "alirocumab", "Cardiovascular", "Sanofi", {...})
]

report = engine.analyze_drug(
    drug=my_drug,
    country='UK',
    competitor_drugs=competitors
)
```

---

## 📈 Performance & Scalability

### Current Performance (UK)
- **Data fetch**: 5-15 seconds (depends on API)
- **Analysis**: <1 second per 1000 prescribers
- **Memory**: ~50 MB for typical dataset

### Optimization Tips
1. **Cache practice details** - UK adapter already implements this
2. **Batch requests** - Fetch multiple drugs in parallel
3. **Regional analysis** - Filter by region to reduce data volume
4. **Asynchronous fetching** - Use `asyncio` for concurrent requests

---

## 🚀 Roadmap to Web Platform

### Phase 1: Core Engine ✅ (Current)
- [x] Generalized analysis engine
- [x] UK data source
- [x] Multiple scoring algorithms
- [x] Segmentation & recommendations

### Phase 2: API Backend (Next)
- [ ] FastAPI REST service
- [ ] Drug database / catalog
- [ ] Authentication & user management
- [ ] Rate limiting & caching

### Phase 3: Web Frontend
- [ ] 3-input wizard (Company → Drug → Country)
- [ ] Results dashboard
- [ ] Interactive maps & charts
- [ ] PDF report generation

### Phase 4: Scale
- [ ] US data source (Medicare)
- [ ] EU data sources (5+ countries)
- [ ] Real-time monitoring & alerts
- [ ] CRM integration

---

## 🛠️ Development

### Testing the Engine

```bash
# Run multi-drug demo
python demo_multi_drug_analysis.py

# Test with specific drug
python -c "
from pharma_intelligence_engine import *
from data_sources_uk import UKDataSource

uk = UKDataSource()
engine = PharmaIntelligenceEngine(data_source=uk)
drug = create_drug('Metformin', 'metformin', 'Diabetes', 'Generic', {'UK': uk.find_drug_code('metformin')})
engine.analyze_drug(drug, 'UK', top_n=10)
"
```

### Requirements

```
requests>=2.28.0
dataclasses  # Built-in Python 3.7+
```

---

## 📝 Notes

### Data Limitations
- **UK**: OpenPrescribing has ~2-3 month lag
- **Competitive data**: Currently manual input, future auto-fetch
- **Clinical context**: Therapeutic area context is basic, needs expansion

### Known Issues
- [ ] No trend analysis yet (need multi-period data)
- [ ] Market share calculation requires competitor data
- [ ] Geographic clustering not yet implemented

---

## 📞 Support

For questions or issues:
- Check `demo_multi_drug_analysis.py` for working examples
- Review `pharma_intelligence_engine.py` docstrings
- Refer to `SESSION_SUMMARY.md` for original context

---

**Built with OpenClaw** 🦾  
*Transforming pharma intelligence from £500K consulting projects to instant insights*
