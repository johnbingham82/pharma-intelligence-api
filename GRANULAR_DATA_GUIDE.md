# Granular Data Guide

## Overview

The platform now supports **practice-level granular data** for detailed geographic analysis and visualization.

## Granularity Levels

### Current Implementation

| Country | Regional Level | Granular Level | Count |
|---------|---------------|----------------|-------|
| 🇬🇧 UK | 7 NHS Regions | ~10,000 GP Practices | Practice-level |
| 🇦🇺 AU | 8 States | TBD (can add LGA) | State-level |
| 🇺🇸 US | 10 States | TBD (can add counties) | State-level |

### UK Practice-Level Data

**What you get:**
- Individual GP practice prescribing data
- Practice name, code, and location
- Prescription volume per practice
- Cost data per practice
- Practice size (patient list size)

**Data source:** NHS OpenPrescribing API (live, updated monthly)

---

## API Endpoints

### 1. Get Practice-Level Data

```http
GET /country/{country_code}/practices?drug={drug_name}&region={region}&limit={limit}
```

**Parameters:**
- `country_code`: Country code (UK, US, AU)
- `drug`: Drug name to query (required)
- `region`: Filter by region (optional)
- `limit`: Max practices to return (default: 1000)

**Example:**
```bash
curl "https://pharma-intelligence-api.herokuapp.com/country/UK/practices?drug=atorvastatin&limit=100"
```

**Response:**
```json
{
  "country": "UK",
  "drug": "atorvastatin",
  "drug_code": "0212000B0",
  "period": "2025-10",
  "practices": [
    {
      "id": "Y00001",
      "name": "Example Medical Centre",
      "type": "GP Practice",
      "prescriptions": 1250,
      "cost": 12500.50,
      "quantity": 95000,
      "list_size": 8500,
      "location": "London"
    },
    // ... more practices
  ],
  "count": 100,
  "total_prescriptions": 125000,
  "total_cost": 1250000
}
```

### 2. Get Practice Detail

```http
GET /country/{country_code}/practices/{practice_id}?drug={drug_name}
```

**Parameters:**
- `country_code`: Country code
- `practice_id`: Practice/prescriber ID
- `drug`: Drug name for prescribing data (optional)

**Example:**
```bash
curl "https://pharma-intelligence-api.herokuapp.com/country/UK/practices/Y00001?drug=atorvastatin"
```

**Response:**
```json
{
  "id": "Y00001",
  "name": "Example Medical Centre",
  "type": "GP Practice",
  "location": "London",
  "list_size": 8500,
  "specialty": "General Practice",
  "prescribing": {
    "drug": "atorvastatin",
    "drug_code": "0212000B0",
    "period": "2025-10",
    "prescriptions": 1250,
    "cost": 12500.50,
    "quantity": 95000
  }
}
```

---

## Visualization Use Cases

### 1. Practice Markers on Map

Show individual practices as clickable markers:
```javascript
// Fetch practice data
const response = await fetch('/country/UK/practices?drug=atorvastatin&limit=1000')
const data = await response.json()

// Add marker for each practice
data.practices.forEach(practice => {
  L.marker([practice.lat, practice.lng])
    .bindPopup(`
      <strong>${practice.name}</strong><br/>
      Prescriptions: ${practice.prescriptions.toLocaleString()}<br/>
      Cost: £${practice.cost.toLocaleString()}
    `)
    .addTo(map)
})
```

### 2. Practice Clustering

Use Leaflet MarkerCluster for thousands of practices:
```javascript
import MarkerClusterGroup from 'leaflet.markercluster'

const markers = new MarkerClusterGroup()
practices.forEach(p => {
  markers.addLayer(L.marker([p.lat, p.lng]))
})
map.addLayer(markers)
```

### 3. Heat Map Overlay

Show prescribing intensity as a heat map:
```javascript
import HeatmapLayer from 'leaflet-heatmap'

const heatData = practices.map(p => ({
  lat: p.lat,
  lng: p.lng,
  value: p.prescriptions
}))

const heatLayer = new HeatmapLayer({ data: heatData })
map.addLayer(heatLayer)
```

### 4. Postcode Sectors

Group practices by postcode sector:
```javascript
// Group by first part of postcode
const sectors = practices.reduce((acc, p) => {
  const sector = p.id.slice(0, 4) // e.g., "SW1A"
  if (!acc[sector]) acc[sector] = []
  acc[sector].push(p)
  return acc
}, {})

// Color by sector density
Object.entries(sectors).forEach(([sector, practices]) => {
  const total = practices.reduce((sum, p) => sum + p.prescriptions, 0)
  // Draw polygon for sector colored by total
})
```

---

## Frontend Integration

### Step 1: Add "Granular View" Toggle

Update `CountryDetail.tsx`:
```typescript
const [showGranular, setShowGranular] = useState(false)
const [practiceData, setPracticeData] = useState<Practice[]>([])

// Fetch practices when toggled
useEffect(() => {
  if (showGranular) {
    fetch(`${API_BASE_URL}/country/${countryCode}/practices?drug=atorvastatin`)
      .then(r => r.json())
      .then(data => setPracticeData(data.practices))
  }
}, [showGranular, countryCode])
```

### Step 2: Render Practice Markers

```typescript
{showGranular && practiceData.map(practice => (
  <Marker
    key={practice.id}
    position={[practice.lat, practice.lng]}
    icon={createPracticeIcon(practice.prescriptions)}
  >
    <Popup>
      <strong>{practice.name}</strong><br/>
      {practice.prescriptions.toLocaleString()} prescriptions
    </Popup>
  </Marker>
))}
```

### Step 3: Progressive Detail

Show more detail as user zooms in:
```typescript
const zoomLevel = useMapEvent('zoomend', (e) => {
  const zoom = e.target.getZoom()
  
  if (zoom < 8) {
    // Show regions only
    setDetailLevel('region')
  } else if (zoom < 12) {
    // Show clustered practices
    setDetailLevel('cluster')
  } else {
    // Show individual practices
    setDetailLevel('practice')
  }
})
```

---

## Data Granularity Options

### UK - Multiple Levels Available

1. **NHS Regions** (7) - Current default
   - NHS England North East and Yorkshire
   - NHS England North West
   - etc.

2. **CCGs** (~100) - Can be added
   - Clinical Commissioning Groups
   - More granular than regions

3. **GP Practices** (~10,000) - **NOW AVAILABLE**
   - Individual practices with postcodes
   - Most granular level

4. **Postcode Sectors** (~10,000) - Can be added
   - Group practices by postcode area
   - e.g., "SW1A", "M1 4"

### Australia - Can Add

1. **States** (8) - Current
2. **Statistical Areas** (SA2, SA3, SA4) - Can add
3. **LGAs** (~500) - Local Government Areas
4. **Postcodes** (~2,500)

### US - Can Add

1. **States** (50) - Current
2. **Counties** (~3,000) - Can add
3. **ZIP Codes** (~40,000) - Can add
4. **Prescriber addresses** - Very granular

---

## Performance Considerations

### Large Datasets

**Problem:** 10,000 practices = slow rendering

**Solutions:**

1. **Limit initial load**
   ```javascript
   fetch('/practices?limit=100') // Top 100 only
   ```

2. **Lazy load on zoom**
   ```javascript
   map.on('moveend', () => {
     const bounds = map.getBounds()
     fetch(`/practices?bounds=${bounds}`)
   })
   ```

3. **Use clustering**
   - Leaflet MarkerCluster plugin
   - Shows counts at high zoom
   - Expands to markers when zoomed in

4. **Server-side filtering**
   ```javascript
   fetch('/practices?region=London&limit=500')
   ```

---

## Next Steps

### Immediate (Available Now)

1. ✅ API endpoint: `/country/UK/practices`
2. ✅ Practice-level data for any drug
3. ✅ Filter by region
4. ✅ Limit results for performance

### Quick Wins (Can Add)

1. **Geocoding:** Add lat/lng to practice data
   - Use NHS postcode database
   - Add to API response

2. **Clustering:** Add MarkerCluster to frontend
   - `npm install leaflet.markercluster`
   - Show practice clusters on map

3. **Drill-down:** Click region → show practices
   - Filter practices by region
   - Zoom to region bounds

### Advanced (Future)

1. **Postcode boundaries:** Get GeoJSON for UK postcodes
2. **CCG/ICS level:** Add intermediate granularity
3. **Historical data:** Show practice trends over time
4. **Custom regions:** Draw polygon, get practices inside

---

## Example: Full Granular Flow

```typescript
// 1. User loads country page → sees 7 regions
<GeographicHeatMap data={regions} countryCode="UK" />

// 2. User toggles "Show Practices" → fetch granular data
const practices = await fetch('/country/UK/practices?drug=atorvastatin&limit=1000')

// 3. Add clustered markers to map
<MarkerClusterGroup>
  {practices.map(p => (
    <Marker key={p.id} position={[p.lat, p.lng]}>
      <Popup>{p.name}: {p.prescriptions} Rx</Popup>
    </Marker>
  ))}
</MarkerClusterGroup>

// 4. User clicks practice → show detail modal
<PracticeDetailModal 
  practice={selectedPractice}
  prescribingData={practice.prescribing}
/>
```

---

## Summary

✅ **NOW AVAILABLE:**
- Practice-level API endpoint
- 10,000+ UK GP practices
- Filter by drug and region
- Individual prescribing data

🎯 **NEXT:**
- Add geocoding (lat/lng)
- Frontend marker visualization
- Practice clustering
- Drill-down interaction

📊 **RESULT:**
- Users can zoom from country → region → practice
- See individual prescriber prescribing patterns
- Target specific high-value practices
- Most granular pharma intelligence platform

---

**Ready to visualize practice-level data on the map!** 🗺️
