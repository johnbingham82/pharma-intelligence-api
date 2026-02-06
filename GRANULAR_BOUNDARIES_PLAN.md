# Granular Geographic Boundaries + Point Geocoding

## Phase 1A: UK Local Authority Boundaries (~150 areas)

### Current Status:
- ✅ Have 7 NHS Regions working
- ✅ Have ~6,349 GP practices from OpenPrescribing
- ✅ Have Local Authority GeoJSON (326 LAs)

### Implementation:
1. **Map CCGs → Local Authorities**
   - OpenPrescribing has 106 CCGs
   - Each CCG maps to one or more Local Authorities
   - Aggregate practice-level data to LA level

2. **Update Data Source**
   - Modify `data_sources_uk.py` to support LA-level queries
   - Add CCG→LA mapping function
   - Aggregate prescriptions by LA

3. **Update Frontend**
   - Add granularity selector: "Regions" vs "Local Authorities"
   - Load appropriate GeoJSON based on selection
   - Render choropleth at selected granularity

## Phase 1B: UK Practice Point Markers

### Geocoding Strategy:
1. **Get Practice Postcodes:**
   - NHS ODS API: https://directory.spineservices.nhs.uk/ORD/2-0-0/organisations/{code}
   - Returns full address including postcode

2. **Geocode Postcodes:**
   - postcodes.io (free, no API key): https://api.postcodes.io/postcodes/{postcode}
   - Returns lat/lng

3. **Cache Locations:**
   - Store in `api/cache/uk_practice_locations.json`
   - Format: `{practice_code: {lat, lng, name, postcode}}`

4. **Display on Map:**
   - Use Leaflet marker clusters for 6000+ practices
   - Color by prescription volume
   - Click for practice details

## Phase 2A: Australia LGA Boundaries (~500 areas)

### Current Status:
- ✅ Have 8 States working
- ✅ Have PBS state-level data

### Implementation:
1. **Get LGA GeoJSON**
   - Source: Australian Bureau of Statistics
   - Or: https://github.com/rowanhogan/australian-geojson

2. **Distribute State Data → LGAs**
   - Use population weights by LGA
   - Apply regional health factors

3. **Update Frontend**
   - Add granularity selector for AU
   - Render LGA-level choropleths

## Phase 2B: Australia Pharmacy Point Markers

### Challenge:
- PBS data is state-level only, no pharmacy-level data publicly available

### Options:
1. **Generate Representative Points:**
   - Distribute state totals to ~10-20 major cities per state
   - Use population centers as proxy locations

2. **Use Hospital Locations:**
   - Australian hospital directory
   - Overlay as representative prescriber locations

## Technical Architecture

### Backend Changes:

```python
# api/data_sources_uk.py - Add LA support
def get_prescribing_data_by_local_authority(self, drug_code, period):
    """Get prescribing data aggregated by Local Authority"""
    # 1. Query practice-level data
    # 2. Get practice postcodes from NHS ODS
    # 3. Map postcodes → LAs
    # 4. Aggregate by LA
    pass

def get_practice_locations(self, practice_codes):
    """Get lat/lng for practices via NHS ODS + postcodes.io"""
    pass
```

### Frontend Changes:

```tsx
// frontend/src/components/GeographicHeatMap.tsx
interface GeographicHeatMapProps {
  granularity: 'region' | 'local-authority' | 'practice-points';
  showPoints?: boolean;  // Overlay practice markers on choropleth
}
```

### Cache Files:

```
api/cache/
  uk_practice_locations.json       # {code: {lat, lng, name, postcode}}
  uk_la_aggregates.json            # {la_code: {prescriptions, cost, ...}}
  au_lga_boundaries.json           # GeoJSON for Australian LGAs
  au_city_locations.json           # Representative pharmacy locations
```

## Deployment Steps

### Step 1: UK Local Authorities (2-3 hours)
1. Download LA GeoJSON to `frontend/public/geojson/uk-local-authorities.json`
2. Update `data_sources_uk.py` with LA mapping
3. Update aggregation script for LA-level
4. Update GeographicHeatMap component
5. Test locally
6. Deploy

### Step 2: UK Practice Points (3-4 hours)
1. Create practice location caching script
2. Integrate NHS ODS API + postcodes.io
3. Add MarkerCluster to GeographicHeatMap
4. Cache ~6,000 practice locations
5. Test with marker overlay
6. Deploy

### Step 3: Australia LGAs (2-3 hours)
1. Download LGA GeoJSON
2. Create population distribution model
3. Update AU data source
4. Update frontend for AU granularity
5. Deploy

### Step 4: Australia Representative Points (1-2 hours)
1. Identify major cities per state
2. Create representative locations
3. Add to map as markers
4. Deploy

## Timeline

- **Phase 1A (UK LAs):** 2-3 hours
- **Phase 1B (UK Points):** 3-4 hours
- **Phase 2A (AU LGAs):** 2-3 hours  
- **Phase 2B (AU Points):** 1-2 hours

**Total:** ~8-12 hours of development

## Priority

Start with **Phase 1A (UK Local Authorities)** - highest impact, leverages existing data, manageable complexity.
