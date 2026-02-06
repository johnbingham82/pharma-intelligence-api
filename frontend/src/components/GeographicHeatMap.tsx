import { useEffect, useState, useMemo } from 'react'
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { MapPin } from 'lucide-react'

interface RegionData {
  region: string
  prescriptions: number
  cost: number
  prescribers: number
  growth?: number
}

interface GeographicHeatMapProps {
  data: RegionData[]
  metric?: 'prescriptions' | 'cost' | 'prescribers' | 'growth'
  title?: string
  countryCode?: string
}

// Map center coordinates for different countries
const MAP_CENTERS: Record<string, { center: [number, number]; zoom: number }> = {
  uk: { center: [54.5, -3.5], zoom: 6 },
  us: { center: [37.8, -96], zoom: 4 },
  au: { center: [-25, 133], zoom: 4 },
  fr: { center: [46.6, 2.3], zoom: 6 },
  de: { center: [51.2, 10.4], zoom: 6 },
  it: { center: [42.8, 12.6], zoom: 6 },
  es: { center: [40.5, -3.7], zoom: 6 },
  nl: { center: [52.1, 5.3], zoom: 7 }
}

// Color scale generator
const getColorForValue = (value: number, max: number, min: number): string => {
  const normalizedValue = (value - min) / (max - min)
  
  // Generate gradient from light to dark blue
  if (normalizedValue > 0.8) return '#1e3a8a' // primary-900
  if (normalizedValue > 0.6) return '#1e40af' // primary-800
  if (normalizedValue > 0.4) return '#2563eb' // primary-700
  if (normalizedValue > 0.2) return '#3b82f6' // primary-600
  return '#93c5fd' // primary-300
}

// Fitbounds component to auto-zoom to GeoJSON layer
function FitBounds({ bounds }: { bounds: L.LatLngBounds | null }) {
  const map = useMap()
  
  useEffect(() => {
    if (bounds) {
      map.fitBounds(bounds, { padding: [50, 50] })
    }
  }, [bounds, map])
  
  return null
}

export default function GeographicHeatMap({ 
  data, 
  metric = 'prescriptions',
  title = 'Geographic Distribution',
  countryCode = 'uk'
}: GeographicHeatMapProps) {
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)
  const [currentMetric, setCurrentMetric] = useState(metric)
  const [geoJsonData, setGeoJsonData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [bounds, setBounds] = useState<L.LatLngBounds | null>(null)
  
  const mapConfig = MAP_CENTERS[countryCode.toLowerCase()] || MAP_CENTERS.uk
  
  // Calculate min/max for color scaling
  const { maxValue, minValue } = useMemo(() => {
    const values = data.map(d => {
      switch (currentMetric) {
        case 'prescriptions': return d.prescriptions
        case 'cost': return d.cost
        case 'prescribers': return d.prescribers
        case 'growth': return d.growth || 0
        default: return d.prescriptions
      }
    })
    return {
      maxValue: Math.max(...values),
      minValue: Math.min(...values)
    }
  }, [data, currentMetric])
  
  // Load GeoJSON data for the country
  useEffect(() => {
    const loadGeoJSON = async () => {
      setLoading(true)
      try {
        let geojson: any = null
        
        // Try to fetch GeoJSON from public sources
        const country = countryCode.toUpperCase()
        
        if (country === 'UK') {
          // UK NHS regions - use local simplified GeoJSON with exact name matches
          try {
            const response = await fetch('/geojson/uk-nhs-regions-simple.json')
            if (response.ok) {
              geojson = await response.json()
              console.log('✓ Loaded local UK NHS regions GeoJSON')
            }
          } catch (e) {
            console.warn('Failed to load local UK GeoJSON, trying external source', e)
            
            // Fallback: external source
            try {
              const response = await fetch('https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/electoral/eng/eer.json')
              if (response.ok) {
                geojson = await response.json()
              }
            } catch (e2) {
              console.error('All UK GeoJSON sources failed', e2)
            }
          }
        } else if (country === 'AU') {
          // Australia states
          const response = await fetch('https://raw.githubusercontent.com/tonywr71/GeoJson-Data/master/australian-states.json')
          if (response.ok) {
            geojson = await response.json()
          }
        } else if (country === 'US') {
          // US states
          const response = await fetch('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')
          if (response.ok) {
            geojson = await response.json()
          }
        }
        
        if (geojson && geojson.features) {
          setGeoJsonData(geojson)
          
          // Debug: Log feature names and matching
          console.log('GeoJSON features loaded:', geojson.features.length)
          console.log('Sample feature properties:', geojson.features[0]?.properties)
          console.log('API region names:', data.map(d => d.region))
          
          // Test matching for all features
          const matchResults = geojson.features.map((f: any) => {
            const fname = f.properties?.name || f.properties?.NAME || f.properties?.EER13NM || 'unknown'
            return {
              geojsonName: fname,
              apiMatch: data.find(d => {
                const regionName = d.region.toLowerCase()
                const cleanRegion = regionName.replace(/nhs england\s*/i, '').trim()
                const cleanFeature = fname.toLowerCase().trim()
                return cleanRegion.includes(cleanFeature) || cleanFeature.includes(cleanRegion)
              })?.region || 'NO MATCH'
            }
          })
          console.log('Matching results:', matchResults)
          
          // Calculate bounds
          const layer = L.geoJSON(geojson)
          setBounds(layer.getBounds())
        }
      } catch (error) {
        console.error('Error loading GeoJSON:', error)
      } finally {
        setLoading(false)
      }
    }
    
    loadGeoJSON()
  }, [countryCode])
  
  // Region name mapping for better matching between GeoJSON and API names
  const regionMappings: Record<string, string[]> = {
    // UK NHS regions - map GeoJSON names to possible API names
    'north east': ['north east', 'yorkshire', 'north east and yorkshire'],
    'yorkshire and the humber': ['yorkshire', 'north east and yorkshire', 'north east'],
    'north west': ['north west'],
    'east midlands': ['midlands', 'east midlands'],
    'west midlands': ['midlands', 'west midlands'],
    'east of england': ['east of england', 'east'],
    'london': ['london'],
    'south east': ['south east'],
    'south west': ['south west'],
    // Australia states
    'new south wales': ['new south wales', 'nsw', 'state: new south wales'],
    'victoria': ['victoria', 'vic', 'state: victoria'],
    'queensland': ['queensland', 'qld', 'state: queensland'],
    'south australia': ['south australia', 'sa', 'state: south australia'],
    'western australia': ['western australia', 'wa', 'state: western australia'],
    'tasmania': ['tasmania', 'tas', 'state: tasmania'],
    'northern territory': ['northern territory', 'nt', 'state: northern territory'],
    'australian capital territory': ['australian capital territory', 'act', 'state: australian capital territory'],
    // US states
    'california': ['california'],
    'texas': ['texas'],
    'florida': ['florida'],
    'new york': ['new york'],
    'pennsylvania': ['pennsylvania'],
    'illinois': ['illinois'],
    'ohio': ['ohio'],
    'georgia': ['georgia'],
    'north carolina': ['north carolina'],
    'michigan': ['michigan']
  }
  
  // Match region data to GeoJSON feature
  const getRegionDataForFeature = (feature: any): RegionData | null => {
    const featureName = (feature.properties?.name || feature.properties?.NAME || 
                        feature.properties?.admin || feature.properties?.ADMIN ||
                        feature.properties?.region || feature.properties?.EER13NM ||
                        '').toLowerCase().trim()
    
    if (!featureName) return null
    
    // Try direct mapping first
    const mappings = regionMappings[featureName] || []
    
    for (const mapping of mappings) {
      const match = data.find(d => {
        const regionName = d.region.toLowerCase()
        return regionName.includes(mapping) || mapping.includes(regionName)
      })
      if (match) return match
    }
    
    // Fallback: fuzzy matching
    return data.find(d => {
      const regionName = d.region.toLowerCase()
      const cleanRegion = regionName.replace(/nhs england\s*/i, '').trim()
      const cleanFeature = featureName.replace(/nhs england\s*/i, '').trim()
      
      // Check if one contains the other
      if (cleanRegion.includes(cleanFeature) || cleanFeature.includes(cleanRegion)) {
        return true
      }
      
      // Check word-by-word overlap (e.g., "North East" matches "North East and Yorkshire")
      const regionWords = cleanRegion.split(/\s+/)
      const featureWords = cleanFeature.split(/\s+/)
      
      const overlap = regionWords.filter(word => 
        word.length > 3 && featureWords.includes(word)
      ).length
      
      return overlap >= 2 || (overlap >= 1 && regionWords.length === 1)
    }) || null
  }
  
  // Style function for GeoJSON features
  const style = (feature: any) => {
    const regionData = getRegionDataForFeature(feature)
    
    if (!regionData) {
      return {
        fillColor: '#e5e7eb',
        fillOpacity: 0.3,
        color: '#9ca3af',
        weight: 1
      }
    }
    
    const value = currentMetric === 'prescriptions' ? regionData.prescriptions :
                  currentMetric === 'cost' ? regionData.cost :
                  currentMetric === 'prescribers' ? regionData.prescribers :
                  regionData.growth || 0
    
    return {
      fillColor: getColorForValue(value, maxValue, minValue),
      fillOpacity: 0.7,
      color: '#ffffff',
      weight: 2,
      dashArray: ''
    }
  }
  
  // Interaction handlers
  const onEachFeature = (feature: any, layer: L.Layer) => {
    const regionData = getRegionDataForFeature(feature)
    
    if (regionData) {
      layer.on({
        mouseover: (e: L.LeafletMouseEvent) => {
          const layer = e.target
          layer.setStyle({
            weight: 3,
            fillOpacity: 0.9
          })
        },
        mouseout: (e: L.LeafletMouseEvent) => {
          const layer = e.target
          layer.setStyle({
            weight: 2,
            fillOpacity: 0.7
          })
        },
        click: () => {
          setSelectedRegion(regionData.region)
        }
      })
      
      // Tooltip
      const value = currentMetric === 'prescriptions' ? regionData.prescriptions :
                    currentMetric === 'cost' ? regionData.cost :
                    currentMetric === 'prescribers' ? regionData.prescribers :
                    regionData.growth || 0
      
      const formattedValue = currentMetric === 'cost' ? 
        `$${(value / 1000000).toFixed(1)}M` :
        currentMetric === 'growth' ?
        `${value.toFixed(1)}%` :
        value.toLocaleString()
      
      layer.bindTooltip(
        `<strong>${regionData.region}</strong><br/>${formattedValue}`,
        { sticky: true }
      )
    }
  }
  
  const selectedData = selectedRegion ? data.find(d => d.region === selectedRegion) : null
  
  const formatValue = (value: number, type: string) => {
    if (type === 'cost') return `$${(value / 1000000).toFixed(1)}M`
    if (type === 'growth') return `${value.toFixed(1)}%`
    return value.toLocaleString()
  }
  
  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-gray-900">{title}</h3>
        
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600">View by:</span>
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setCurrentMetric('prescriptions')}
              className={`px-3 py-1 text-xs font-medium rounded transition-colors ${
                currentMetric === 'prescriptions'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Volume
            </button>
            <button
              onClick={() => setCurrentMetric('cost')}
              className={`px-3 py-1 text-xs font-medium rounded transition-colors ${
                currentMetric === 'cost'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Cost
            </button>
            <button
              onClick={() => setCurrentMetric('prescribers')}
              className={`px-3 py-1 text-xs font-medium rounded transition-colors ${
                currentMetric === 'prescribers'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Prescribers
            </button>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg border-2 border-gray-200 overflow-hidden" style={{ height: '600px' }}>
            {loading ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Loading map...</p>
                </div>
              </div>
            ) : geoJsonData ? (
              <MapContainer
                center={mapConfig.center}
                zoom={mapConfig.zoom}
                style={{ height: '100%', width: '100%' }}
                scrollWheelZoom={true}
              >
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                
                <GeoJSON
                  data={geoJsonData}
                  style={style}
                  onEachFeature={onEachFeature}
                />
                
                <FitBounds bounds={bounds} />
              </MapContainer>
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <MapPin className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-600">Map data not available for this country</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Geographic boundaries are being prepared
                  </p>
                </div>
              </div>
            )}
          </div>
          
          {/* Legend */}
          {geoJsonData && (
            <div className="mt-4 bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Lower</span>
                <div className="flex space-x-1">
                  <div className="w-12 h-4 rounded" style={{ backgroundColor: '#93c5fd' }}></div>
                  <div className="w-12 h-4 rounded" style={{ backgroundColor: '#3b82f6' }}></div>
                  <div className="w-12 h-4 rounded" style={{ backgroundColor: '#2563eb' }}></div>
                  <div className="w-12 h-4 rounded" style={{ backgroundColor: '#1e40af' }}></div>
                  <div className="w-12 h-4 rounded" style={{ backgroundColor: '#1e3a8a' }}></div>
                </div>
                <span className="text-gray-600">Higher</span>
              </div>
            </div>
          )}
        </div>
        
        {/* Region Details Panel */}
        <div className="space-y-4">
          {selectedData ? (
            <>
              <div className="card">
                <div className="flex items-center space-x-2 mb-4">
                  <MapPin className="h-5 w-5 text-primary-600" />
                  <h4 className="font-bold text-gray-900">{selectedData.region}</h4>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center pb-3 border-b border-gray-200">
                    <span className="text-sm text-gray-600">Prescriptions</span>
                    <span className="text-lg font-bold text-gray-900">
                      {selectedData.prescriptions.toLocaleString()}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center pb-3 border-b border-gray-200">
                    <span className="text-sm text-gray-600">Market Value</span>
                    <span className="text-lg font-bold text-gray-900">
                      ${(selectedData.cost / 1000000).toFixed(2)}M
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center pb-3 border-b border-gray-200">
                    <span className="text-sm text-gray-600">Prescribers</span>
                    <span className="text-lg font-bold text-gray-900">
                      {selectedData.prescribers.toLocaleString()}
                    </span>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="text-xs text-gray-500">
                    Market Share: {((selectedData.prescriptions / data.reduce((sum, d) => sum + d.prescriptions, 0)) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="card text-center py-12">
              <MapPin className="h-12 w-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-600">Click a region on the map</p>
            </div>
          )}
          
          {/* Top 3 Regions */}
          <div className="card">
            <h5 className="text-sm font-semibold text-gray-900 mb-3">Top 3 Regions</h5>
            <div className="space-y-2">
              {[...data]
                .sort((a, b) => {
                  const aVal = currentMetric === 'prescriptions' ? a.prescriptions :
                               currentMetric === 'cost' ? a.cost :
                               currentMetric === 'prescribers' ? a.prescribers :
                               a.growth || 0
                  const bVal = currentMetric === 'prescriptions' ? b.prescriptions :
                               currentMetric === 'cost' ? b.cost :
                               currentMetric === 'prescribers' ? b.prescribers :
                               b.growth || 0
                  return bVal - aVal
                })
                .slice(0, 3)
                .map((region, idx) => (
                  <button
                    key={region.region}
                    onClick={() => setSelectedRegion(region.region)}
                    className="w-full flex items-center justify-between p-2 rounded hover:bg-gray-50 transition-colors text-left"
                  >
                    <div className="flex items-center space-x-2">
                      <span className="text-lg font-bold text-primary-600">#{idx + 1}</span>
                      <span className="text-sm font-medium text-gray-900">{region.region}</span>
                    </div>
                    <span className="text-sm font-semibold text-gray-900">
                      {formatValue(
                        currentMetric === 'prescriptions' ? region.prescriptions :
                        currentMetric === 'cost' ? region.cost :
                        currentMetric === 'prescribers' ? region.prescribers :
                        region.growth || 0,
                        currentMetric
                      )}
                    </span>
                  </button>
                ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
