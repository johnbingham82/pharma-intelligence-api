# Pharma Data Sources - Global Research

**Objective:** Identify public prescribing data sources for US and EU markets

---

## 🇺🇸 UNITED STATES

### Primary Sources

#### 1. **CMS Medicare Part D Prescriber Data** ⭐ RECOMMENDED
**Provider:** Centers for Medicare & Medicaid Services (CMS)  
**Coverage:** Medicare Part D prescriptions (seniors, 65+)  
**Data:** Prescriber-level prescribing by drug  
**Access:** **Public, Free API**  
**URL:** https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers

**Endpoints:**
- Provider Summary: https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-provider
- Geography: https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-geography-and-drug

**Data Fields:**
- NPI (National Provider Identifier)
- Prescriber name, specialty, location
- Drug name (brand/generic)
- Total prescriptions
- Total cost
- Beneficiary count

**Pros:**
✅ Free, public data  
✅ REST API available  
✅ Comprehensive (covers ~40M Medicare beneficiaries)  
✅ Updated annually  
✅ Prescriber-level detail  

**Cons:**
❌ Medicare only (not commercial insurance)  
❌ Annual updates (not real-time)  
❌ Requires NDC → Drug name mapping  

**Implementation:** Direct REST API, similar to UK OpenPrescribing

---

#### 2. **FDA National Drug Code (NDC) Directory**
**Provider:** US Food & Drug Administration  
**Coverage:** All approved drugs in US  
**Access:** **Public, Free API**  
**URL:** https://open.fda.gov/apis/drug/ndc/

**Use Case:** Drug name → NDC code resolution  
**Needed for:** Medicare data queries

---

#### 3. **OpenPayments (CMS)**
**Provider:** Centers for Medicare & Medicaid Services  
**Coverage:** Pharma payments to prescribers  
**Access:** **Public, Free API**  
**URL:** https://openpaymentsdata.cms.gov/

**Use Case:** Identify pharma-engaged prescribers (already receiving support)  
**Useful for:** Competitive intelligence

---

#### 4. **IQVIA (Commercial)** 💰
**Provider:** IQVIA (formerly IMS Health)  
**Coverage:** Total prescribing (Medicare + commercial)  
**Access:** **Commercial license required** ($$$)  
**URL:** https://www.iqvia.com/

**Pros:** Most comprehensive US data  
**Cons:** Expensive, requires contract

---

### Recommendation for US

**Phase 1:** Use **CMS Medicare Part D** (free, public)
- Covers 40M+ beneficiaries
- Good representation for many drug classes
- Free REST API

**Phase 2:** Add **IQVIA** (if customer demands total market view)
- Requires paid license
- Premium feature for enterprise customers

---

## 🇪🇺 EUROPEAN UNION

### Germany 🇩🇪

#### **GKV-Spitzenverband (National Association of Statutory Health Insurance Funds)**
**Coverage:** ~90% of German population (73M people)  
**Access:** **Public reports** (PDF/Excel), no real-time API  
**URL:** https://www.gkv-spitzenverband.de/

**Data Available:**
- Top prescribed drugs by volume
- Prescribing trends
- Regional breakdowns

**Limitation:** No prescriber-level data (privacy laws)

#### **IMS Health Germany** 💰
**Access:** Commercial license required  
**Coverage:** Pharmacy-level dispensing data

---

### France 🇫🇷

#### **Assurance Maladie (Public Health Insurance)**
**Coverage:** Entire French population  
**Access:** **Public portal** "Open Data Assurance Maladie"  
**URL:** https://data.ameli.fr/

**Data Available:**
- Drug prescribing by region
- Prescribing trends
- Cost data

**Limitation:** 
- No real-time API (downloadable datasets)
- Limited prescriber-level detail (privacy)

#### **ANSM (National Agency for Medicines Safety)**
**URL:** https://www.ansm.sante.fr/  
**Access:** Public reports only

---

### Spain 🇪🇸

#### **Ministry of Health (Ministerio de Sanidad)**
**URL:** https://www.sanidad.gob.es/  
**Access:** Public statistics, no API

**Data Available:**
- National prescribing statistics
- Regional breakdowns
- Therapeutic area summaries

**Limitation:** Aggregated only, no prescriber level

---

### Netherlands 🇳🇱

#### **GIP Databank (Foundation Pharmaceutical Statistics)**
**URL:** https://www.gipdatabank.nl/  
**Access:** **Public data** with registration  

**Data Available:**
- Prescribing volumes by drug
- Regional analysis
- Trend data

**Limitation:** No prescriber-level data

---

### Italy 🇮🇹

#### **AIFA (Italian Medicines Agency)**
**URL:** https://www.aifa.gov.it/  
**Access:** Public reports, no API

**Data Available:**
- National drug consumption
- Regional spending
- Therapeutic area analysis

---

## 🌍 Global Commercial Sources

### IQVIA (Formerly IMS Health) 💰
**Coverage:** 90+ countries  
**Access:** Commercial license ($$$)  
**Best-in-class** for global pharma intelligence

### Pharmaspectra 💰
**Coverage:** Major EU markets  
**Access:** Commercial

### Symphony Health 💰
**Coverage:** US claims data  
**Access:** Commercial

---

## 🎯 Implementation Strategy

### Phase 1: US Medicare (Week 1)
✅ **Free, public data**  
✅ REST API available  
✅ Good coverage (40M beneficiaries)  
✅ Similar structure to UK

**Effort:** 1-2 days  
**ROI:** Immediate US market access

---

### Phase 2: EU Aggregated Data (Week 2-3)
✅ **Free, public data**  
⚠️ No prescriber-level detail  
⚠️ No real-time API (batch downloads)

**Countries to prioritize:**
1. **France** - Best public data (Open Data Assurance Maladie)
2. **Netherlands** - Good structure (GIP Databank)
3. **Germany** - Large market, limited public data

**Effort:** 3-5 days per country  
**ROI:** EU market coverage (450M population)

**Limitation:** Analysis will be regional/aggregate (not prescriber-level) due to EU privacy laws

---

### Phase 3: Commercial Data (Future)
For customers who need:
- Prescriber-level EU data
- Total US market (not just Medicare)
- Real-time updates

**Partner with:**
- IQVIA (best global coverage)
- Symphony Health (US claims)
- Local vendors per country

**Business model:** Pass license costs to enterprise customers

---

## 🔒 Privacy & Compliance

### US (HIPAA)
✅ Medicare Part D data is de-identified and public  
✅ No PHI (Protected Health Information)  
✅ Safe to use commercially

### EU (GDPR)
⚠️ Strict privacy laws limit prescriber-level data  
✅ Aggregated/anonymized data is public  
⚠️ Must comply with GDPR for any EU operations

**Recommendation:** 
- US: Prescriber-level analysis (like UK)
- EU: Regional/aggregate analysis (different UX)

---

## 💡 Key Insights

### What Works (Prescriber-Level)
1. **UK** - NHS OpenPrescribing ✅
2. **US** - CMS Medicare Part D ✅

### What Doesn't (Privacy Restrictions)
1. **EU** - Most countries don't publish prescriber-level data
2. **Alternative:** Offer regional/aggregate analysis for EU

### Commercial Gap
- EU prescriber-level data = competitive advantage
- Requires IQVIA or similar license
- Premium feature for enterprise customers

---

## 🚀 Recommended Build Order

**Week 1:** US Medicare Part D
- Biggest immediate value
- Free, public API
- 40M+ beneficiaries
- Similar to UK structure

**Week 2:** France (EU pilot)
- Best public EU data
- Test aggregated analysis UX
- Large market (67M population)

**Week 3:** Germany + Netherlands
- Round out EU coverage
- Aggregate analysis

**Future:** IQVIA integration (for prescriber-level EU + total US market)

---

## 📊 Market Coverage After Phase 1-3

| Region | Population | Coverage Type | Data Source |
|--------|-----------|---------------|-------------|
| **UK** | 67M | Prescriber-level | NHS OpenPrescribing ✅ |
| **US** | 330M | Prescriber-level (Medicare) | CMS Part D ✅ |
| **France** | 67M | Regional/aggregate | Open Data Assurance Maladie |
| **Germany** | 83M | Regional/aggregate | GKV Reports |
| **Netherlands** | 17M | Regional/aggregate | GIP Databank |
| **Total** | **564M** | Mixed | **Free sources** |

**With IQVIA (paid):** Add prescriber-level for EU + full US commercial = **850M+ total**

---

## 📁 Next Steps

1. ✅ **Research complete** (this document)
2. **Build US adapter** (CMS Medicare Part D)
3. **Build EU adapter** (France pilot)
4. **Document limitations** (prescriber vs aggregate)
5. **Test with real data**
6. **Add to API** (new country codes)

Ready to start with US Medicare adapter! 🚀
