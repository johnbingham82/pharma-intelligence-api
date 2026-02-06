import { useEffect, useState, useMemo } from 'react'
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import 'leaflet.markercluster'
import 'leaflet.heat'
import { MapPin, Layers, Activity } from 'lucide-react'
import { API_BASE_URL } from '../config'

interface RegionData {
  region?: string
  local_authority?: string
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
  drug?: string
  granularity?: 'region' | 'local-authority'
  onGranularityChange?: (granularity: 'region' | 'local-authority') => void
}

interface PracticeData {
  id: string
  name: string
  prescriptions: number
  cost: number
  lat?: number
  lng?: number
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

// Heat map layer component
function HeatMapLayer({ practices, metric }: { practices: PracticeData[]; metric: string }) {
  const map = useMap()
  
  useEffect(() => {
    if (practices.length === 0) return
    
    // Filter practices with coordinates (for demo, use mock coordinates)
    const heatData = practices
      .filter(p => p.lat && p.lng)
      .map(p => {
        const value = metric === 'prescriptions' ? p.prescriptions : p.cost
        return [p.lat!, p.lng!, value / 100] // Normalize intensity
      })
    
    if (heatData.length === 0) return
    
    // @ts-ignore - leaflet.heat types
    const heatLayer = L.heatLayer(heatData, {
      radius: 25,
      blur: 35,
      maxZoom: 13,
      max: 1.0,
      gradient: {
        0.0: '#3b82f6',
        0.5: '#8b5cf6',
        0.75: '#ec4899',
        1.0: '#ef4444'
      }
    }).addTo(map)
    
    return () => {
      map.removeLayer(heatLayer)
    }
  }, [practices, metric, map])
  
  return null
}

// Marker cluster layer component
function MarkerClusterLayer({ practices, onPracticeClick }: { 
  practices: PracticeData[]; 
  onPracticeClick: (practice: PracticeData) => void 
}) {
  const map = useMap()
  
  useEffect(() => {
    if (practices.length === 0) return
    
    // @ts-ignore - markercluster types
    const markers = L.markerClusterGroup({
      chunkedLoading: true,
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: false,
      zoomToBoundsOnClick: true,
      maxClusterRadius: 80
    })
    
    practices
      .filter(p => p.lat && p.lng)
      .forEach(practice => {
        const marker = L.marker([practice.lat!, practice.lng!], {
          icon: L.divIcon({
            className: 'custom-practice-marker',
            html: `<div class="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-xs font-bold shadow-lg">${practice.prescriptions > 1000 ? '1K+' : practice.prescriptions}</div>`,
            iconSize: [32, 32]
          })
        })
        
        marker.bindPopup(`
          <div class="p-2">
            <strong class="text-sm">${practice.name}</strong><br/>
            <span class="text-xs text-gray-600">Prescriptions: ${practice.prescriptions.toLocaleString()}</span><br/>
            <span class="text-xs text-gray-600">Cost: $${(practice.cost / 1000).toFixed(1)}K</span>
          </div>
        `)
        
        marker.on('click', () => onPracticeClick(practice))
        
        markers.addLayer(marker)
      })
    
    map.addLayer(markers)
    
    return () => {
      map.removeLayer(markers)
    }
  }, [practices, map, onPracticeClick])
  
  return null
}

export default function GeographicHeatMap({ 
  data, 
  metric = 'prescriptions',
  title = 'Geographic Distribution',
  countryCode = 'uk',
  drug = 'atorvastatin',
  granularity = 'region',
  onGranularityChange
}: GeographicHeatMapProps) {
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)
  const [currentMetric, setCurrentMetric] = useState(metric)
  const [currentGranularity, setCurrentGranularity] = useState(granularity)
  const [geoJsonData, setGeoJsonData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [bounds, setBounds] = useState<L.LatLngBounds | null>(null)
  const [practiceData, setPracticeData] = useState<PracticeData[]>([])
  const [loadingPractices, setLoadingPractices] = useState(false)
  const [showHeatMap, setShowHeatMap] = useState(false)
  const [showMarkers, setShowMarkers] = useState(false)
  
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
  
  // Load practice-level data for granular visualization
  useEffect(() => {
    if (!showHeatMap && !showMarkers) return
    
    const loadPractices = async () => {
      setLoadingPractices(true)
      try {
        const response = await fetch(
          `${API_BASE_URL}/country/${countryCode.toUpperCase()}/practices?drug=${drug}&limit=500`
        )
        
        if (!response.ok) {
          console.error('Failed to load practice data')
          return
        }
        
        const result = await response.json()
        
        // Mock geocoding for demo (in production, get real lat/lng from API)
        const practicesWithCoords = result.practices.map((p: any, idx: number) => ({
          ...p,
          // Mock coordinates - spread around UK for visualization
          lat: 51.5 + (Math.random() - 0.5) * 8,
          lng: -1.5 + (Math.random() - 0.5) * 8
        }))
        
        setPracticeData(practicesWithCoords)
        console.log(`Loaded ${practicesWithCoords.length} practices`)
      } catch (error) {
        console.error('Error loading practices:', error)
      } finally {
        setLoadingPractices(false)
      }
    }
    
    loadPractices()
  }, [showHeatMap, showMarkers, countryCode, drug])
  
  // Load GeoJSON data for the country
  useEffect(() => {
    const loadGeoJSON = async () => {
      setLoading(true)
      try {
        let geojson: any = null
        
        // Try to fetch GeoJSON from public sources
        const country = countryCode.toUpperCase()
        
        if (country === 'UK') {
          if (currentGranularity === 'local-authority') {
            // UK Local Authorities (~150 areas)
            try {
              const response = await fetch('/geojson/uk-local-authorities.json')
              if (response.ok) {
                geojson = await response.json()
                console.log('✓ Loaded UK Local Authorities GeoJSON')
              }
            } catch (e) {
              console.error('Failed to load UK LA GeoJSON', e)
            }
          } else {
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
  }, [countryCode, currentGranularity])
  
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
    // Extract feature name from various possible properties
    const featureName = (feature.properties?.name || feature.properties?.NAME || 
                        feature.properties?.admin || feature.properties?.ADMIN ||
                        feature.properties?.region || feature.properties?.EER13NM ||
                        feature.properties?.LAD13NM || feature.properties?.LAD21NM ||
                        feature.properties?.lad21nm || feature.properties?.lad13nm ||
                        '').toLowerCase().trim()
    
    if (!featureName) return null
    
    // Match based on granularity
    if (currentGranularity === 'local-authority') {
      // Direct match for Local Authorities
      const directMatch = data.find(d => {
        const laName = (d.local_authority || '').toLowerCase().trim()
        return laName === featureName || 
               featureName.includes(laName) || 
               laName.includes(featureName)
      })
      if (directMatch) return directMatch
    } else {
      // Try direct mapping first for regions
      const mappings = regionMappings[featureName] || []
      
      for (const mapping of mappings) {
        const match = data.find(d => {
          const regionName = (d.region || '').toLowerCase()
          return regionName.includes(mapping) || mapping.includes(regionName)
        })
        if (match) return match
      }
      
      // Fallback: fuzzy matching for regions
      return data.find(d => {
        const regionName = (d.region || '').toLowerCase()
        const cleanRegion = regionName.replace(/nhs england\s*/i, '').trim()
        const cleanFeature = featureName.replace(/nhs england\s*/i, '').trim()
        
        // Check if one contains the other
        if (cleanRegion.includes(cleanFeature) || cleanFeature.includes(cleanRegion)) {
          return true
        }
        
        // Check word-by-word overlap
        const regionWords = cleanRegion.split(/\s+/)
        const featureWords = cleanFeature.split(/\s+/)
        
        const overlap = regionWords.filter(word => 
          word.length > 3 && featureWords.includes(word)
        ).length
        
        return overlap >= 2 || (overlap >= 1 && regionWords.length === 1)
      }) || null
    }
    
    return null
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
          // Use local_authority for LA granularity, region for region granularity
          const selectedName = regionData.local_authority || regionData.region
          setSelectedRegion(selectedName)
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
      
      // Use local_authority for LA granularity, region for region granularity
      const displayName = regionData.local_authority || regionData.region
      
      layer.bindTooltip(
        `<strong>${displayName}</strong><br/>${formattedValue}`,
        { sticky: true }
      )
    }
  }
  
  const selectedData = selectedRegion 
    ? data.find(d => d.region === selectedRegion || d.local_authority === selectedRegion) 
    : null
  
  const formatValue = (value: number, type: string) => {
    if (type === 'cost') return `$${(value / 1000000).toFixed(1)}M`
    if (type === 'growth') return `${value.toFixed(1)}%`
    return value.toLocaleString()
  }
  
  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <h3 className="text-lg font-bold text-gray-900">{title}</h3>
        
        <div className="flex items-center space-x-4">
          {/* Granularity selector (UK only) */}
          {countryCode.toUpperCase() === 'UK' && (
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Detail:</span>
              <div className="flex bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => {
                    setCurrentGranularity('region')
                    if (onGranularityChange) onGranularityChange('region')
                  }}
                  className={`px-3 py-1 text-xs font-medium rounded transition-colors ${
                    currentGranularity === 'region'
                      ? 'bg-white text-primary-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Regions (7)
                </button>
                <button
                  onClick={() => {
                    setCurrentGranularity('local-authority')
                    if (onGranularityChange) onGranularityChange('local-authority')
                  }}
                  className={`px-3 py-1 text-xs font-medium rounded transition-colors ${
                    currentGranularity === 'local-authority'
                      ? 'bg-white text-primary-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Local Auth. (150+)
                </button>
              </div>
            </div>
          )}
          
          {/* Metric selector */}
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
          
          {/* Overlay toggles */}
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600">Overlays:</span>
            <button
              onClick={() => setShowHeatMap(!showHeatMap)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                showHeatMap
                  ? 'bg-purple-100 text-purple-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <Activity className="h-3.5 w-3.5" />
              Heat Map
            </button>
            <button
              onClick={() => setShowMarkers(!showMarkers)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                showMarkers
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <Layers className="h-3.5 w-3.5" />
              Practices
              {loadingPractices && <span className="animate-spin">⏳</span>}
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
                
                {/* Heat map overlay */}
                {showHeatMap && practiceData.length > 0 && (
                  <HeatMapLayer practices={practiceData} metric={currentMetric} />
                )}
                
                {/* Marker cluster overlay */}
                {showMarkers && practiceData.length > 0 && (
                  <MarkerClusterLayer 
                    practices={practiceData} 
                    onPracticeClick={(practice) => {
                      console.log('Practice clicked:', practice)
                      // Could show practice detail modal here
                    }} 
                  />
                )}
                
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
          
          {/* Granular data info */}
          {(showHeatMap || showMarkers) && practiceData.length > 0 && (
            <div className="mt-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-200 p-4">
              <div className="flex items-start space-x-3">
                <Layers className="h-5 w-5 text-purple-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-gray-900 mb-1">
                    Granular Practice Data
                  </h4>
                  <p className="text-xs text-gray-600 mb-2">
                    Showing {practiceData.length.toLocaleString()} GP practices for {drug}
                  </p>
                  {showHeatMap && (
                    <p className="text-xs text-purple-700">
                      🔥 Heat map shows prescribing density across practices
                    </p>
                  )}
                  {showMarkers && (
                    <p className="text-xs text-blue-700">
                      📍 Click markers to see individual practice details
                    </p>
                  )}
                </div>
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
                  <h4 className="font-bold text-gray-900">
                    {selectedData.local_authority || selectedData.region}
                  </h4>
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
