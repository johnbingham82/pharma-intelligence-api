import { useState } from 'react'
import { MapPin, TrendingUp } from 'lucide-react'

interface RegionData {
  region: string
  prescriptions: number
  cost: number
  prescribers: number
  growth?: number
}

interface RegionalHeatMapProps {
  data: RegionData[]
  metric?: 'prescriptions' | 'cost' | 'prescribers' | 'growth'
  title?: string
  countryCode?: string
}

// Color scale generator
const getColorForValue = (value: number, max: number, min: number) => {
  const normalizedValue = (value - min) / (max - min)
  
  // Generate gradient from light blue to dark blue
  if (normalizedValue > 0.8) return 'bg-primary-700 text-white'
  if (normalizedValue > 0.6) return 'bg-primary-600 text-white'
  if (normalizedValue > 0.4) return 'bg-primary-500 text-white'
  if (normalizedValue > 0.2) return 'bg-primary-400 text-gray-900'
  return 'bg-primary-200 text-gray-900'
}

// Layout configurations for different countries
const REGION_LAYOUTS: Record<string, any> = {
  uk: {
    name: 'United Kingdom',
    regions: [
      { code: 'NEYO', name: 'NE & Yorkshire', row: 0, col: 2 },
      { code: 'NW', name: 'North West', row: 1, col: 1 },
      { code: 'MID', name: 'Midlands', row: 2, col: 2 },
      { code: 'EE', name: 'East of England', row: 2, col: 3 },
      { code: 'LDN', name: 'London', row: 3, col: 3 },
      { code: 'SE', name: 'South East', row: 3, col: 2 },
      { code: 'SW', name: 'South West', row: 3, col: 1 }
    ]
  },
  us: {
    name: 'United States',
    regions: [
      { code: 'CA', name: 'California', row: 2, col: 0 },
      { code: 'TX', name: 'Texas', row: 3, col: 2 },
      { code: 'FL', name: 'Florida', row: 4, col: 5 },
      { code: 'NY', name: 'New York', row: 1, col: 5 },
      { code: 'PA', name: 'Pennsylvania', row: 2, col: 5 },
      { code: 'IL', name: 'Illinois', row: 2, col: 3 },
      { code: 'OH', name: 'Ohio', row: 2, col: 4 },
      { code: 'GA', name: 'Georgia', row: 3, col: 5 },
      { code: 'NC', name: 'North Carolina', row: 3, col: 5 },
      { code: 'MI', name: 'Michigan', row: 1, col: 4 }
    ]
  },
  au: {
    name: 'Australia',
    regions: [
      { code: 'NSW', name: 'New South Wales', row: 2, col: 3 },
      { code: 'VIC', name: 'Victoria', row: 3, col: 3 },
      { code: 'QLD', name: 'Queensland', row: 0, col: 3 },
      { code: 'SA', name: 'South Australia', row: 3, col: 2 },
      { code: 'WA', name: 'Western Australia', row: 2, col: 0 },
      { code: 'TAS', name: 'Tasmania', row: 4, col: 3 },
      { code: 'NT', name: 'Northern Territory', row: 0, col: 2 },
      { code: 'ACT', name: 'ACT', row: 2, col: 3 }
    ]
  }
}

export default function RegionalHeatMap({ 
  data, 
  metric = 'prescriptions',
  title = 'Regional Distribution',
  countryCode = 'uk'
}: RegionalHeatMapProps) {
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)
  const [currentMetric, setCurrentMetric] = useState(metric)
  
  // Calculate min/max for color scaling
  const values = data.map(d => {
    switch (currentMetric) {
      case 'prescriptions': return d.prescriptions
      case 'cost': return d.cost
      case 'prescribers': return d.prescribers
      case 'growth': return d.growth || 0
      default: return d.prescriptions
    }
  })
  
  const maxValue = Math.max(...values)
  const minValue = Math.min(...values)
  
  const layout = REGION_LAYOUTS[countryCode.toLowerCase()] || REGION_LAYOUTS.uk
  
  // Region name mapping for better matching
  const regionNameMapping: Record<string, string[]> = {
    // UK NHS regions (7 regions)
    'NEYO': ['North East', 'Yorkshire', 'North East and Yorkshire'],
    'NW': ['North West'],
    'MID': ['Midlands'],
    'EE': ['East of England', 'East'],
    'SW': ['South West'],
    'SE': ['South East'],
    'LDN': ['London'],
    // Australia states
    'NSW': ['New South Wales', 'State: New South Wales'],
    'VIC': ['Victoria', 'State: Victoria'],
    'QLD': ['Queensland', 'State: Queensland'],
    'SA': ['South Australia', 'State: South Australia'],
    'WA': ['Western Australia', 'State: Western Australia'],
    'TAS': ['Tasmania', 'State: Tasmania'],
    'NT': ['Northern Territory', 'State: Northern Territory'],
    'ACT': ['Australian Capital Territory', 'State: Australian Capital Territory', 'ACT'],
    // US states
    'CA': ['California'],
    'TX': ['Texas'],
    'FL': ['Florida'],
    'NY': ['New York'],
    'PA': ['Pennsylvania'],
    'IL': ['Illinois'],
    'OH': ['Ohio'],
    'GA': ['Georgia'],
    'NC': ['North Carolina'],
    'MI': ['Michigan']
  }
  
  // Get region data with improved matching
  const getRegionData = (regionCode: string) => {
    const mappings = regionNameMapping[regionCode] || [regionCode]
    
    return data.find(d => {
      const regionName = d.region.toLowerCase()
      // Check direct code match
      if (d.region === regionCode) return true
      // Check if any mapping matches
      return mappings.some(mapping => 
        regionName.includes(mapping.toLowerCase()) ||
        mapping.toLowerCase().includes(regionName)
      )
    })
  }
  
  const formatValue = (value: number, type: string) => {
    if (type === 'cost') return `$${(value / 1000000).toFixed(1)}M`
    if (type === 'growth') return `${value.toFixed(1)}%`
    return value.toLocaleString()
  }
  
  // Get selected region data - handle both layout codes and direct region names
  const selectedData = selectedRegion ? (
    getRegionData(selectedRegion) || data.find(d => d.region === selectedRegion)
  ) : null
  
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
            {data.some(d => d.growth !== undefined) && (
              <button
                onClick={() => setCurrentMetric('growth')}
                className={`px-3 py-1 text-xs font-medium rounded transition-colors ${
                  currentMetric === 'growth'
                    ? 'bg-white text-primary-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Growth
              </button>
            )}
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Heat Map Grid */}
        <div className="lg:col-span-2 bg-white rounded-lg border-2 border-gray-200 p-6">
          <div className="relative" style={{ minHeight: '400px' }}>
            {layout.regions.length > 0 ? (
              <div className="grid grid-cols-6 gap-2">
                {layout.regions.map((region: any) => {
                  const regionData = getRegionData(region.code)
                  if (!regionData) return null
                
                const value = currentMetric === 'prescriptions' ? regionData.prescriptions :
                              currentMetric === 'cost' ? regionData.cost :
                              currentMetric === 'prescribers' ? regionData.prescribers :
                              regionData.growth || 0
                
                const colorClass = getColorForValue(value, maxValue, minValue)
                const isSelected = selectedRegion === region.code
                
                return (
                  <button
                    key={region.code}
                    onClick={() => setSelectedRegion(region.code)}
                    className={`
                      relative p-4 rounded-lg transition-all transform
                      ${colorClass}
                      ${isSelected ? 'ring-4 ring-accent-400 scale-105 shadow-lg z-10' : 'hover:scale-105 hover:shadow-md'}
                    `}
                    style={{
                      gridColumn: region.col + 1,
                      gridRow: region.row + 1
                    }}
                  >
                    <div className="text-xs font-semibold mb-1">{region.code}</div>
                    <div className="text-sm font-bold">
                      {formatValue(value, currentMetric)}
                    </div>
                    
                    {regionData.growth && currentMetric !== 'growth' && (
                      <div className="mt-1 flex items-center justify-center">
                        <TrendingUp className="h-3 w-3 mr-1" />
                        <span className="text-xs">{regionData.growth.toFixed(1)}%</span>
                      </div>
                    )}
                  </button>
                )
              })}
            </div>
            ) : (
              // Fallback: Simple grid for unmapped countries
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {data.map((region) => {
                  const value = currentMetric === 'prescriptions' ? region.prescriptions :
                                currentMetric === 'cost' ? region.cost :
                                currentMetric === 'prescribers' ? region.prescribers :
                                region.growth || 0
                  
                  const colorClass = getColorForValue(value, maxValue, minValue)
                  const isSelected = selectedRegion === region.region
                  
                  return (
                    <button
                      key={region.region}
                      onClick={() => setSelectedRegion(region.region)}
                      className={`
                        relative p-4 rounded-lg transition-all transform
                        ${colorClass}
                        ${isSelected ? 'ring-4 ring-accent-400 scale-105 shadow-lg z-10' : 'hover:scale-105 hover:shadow-md'}
                      `}
                    >
                      <div className="text-xs font-semibold mb-1 truncate">{region.region}</div>
                      <div className="text-sm font-bold">
                        {formatValue(value, currentMetric)}
                      </div>
                      
                      {region.growth && currentMetric !== 'growth' && (
                        <div className="mt-1 flex items-center justify-center">
                          <TrendingUp className="h-3 w-3 mr-1" />
                          <span className="text-xs">{region.growth.toFixed(1)}%</span>
                        </div>
                      )}
                    </button>
                  )
                })}
              </div>
            )}
          </div>
          
          {/* Legend */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Lower</span>
              <div className="flex space-x-1">
                <div className="w-12 h-4 bg-primary-200 rounded"></div>
                <div className="w-12 h-4 bg-primary-400 rounded"></div>
                <div className="w-12 h-4 bg-primary-500 rounded"></div>
                <div className="w-12 h-4 bg-primary-600 rounded"></div>
                <div className="w-12 h-4 bg-primary-700 rounded"></div>
              </div>
              <span className="text-gray-600">Higher</span>
            </div>
          </div>
        </div>
        
        {/* Region Details */}
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
                  
                  {selectedData.growth !== undefined && (
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">YoY Growth</span>
                      <div className="flex items-center space-x-1">
                        <TrendingUp className={`h-4 w-4 ${selectedData.growth > 0 ? 'text-green-600' : 'text-red-600'}`} />
                        <span className={`text-lg font-bold ${selectedData.growth > 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {selectedData.growth > 0 ? '+' : ''}{selectedData.growth.toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  )}
                </div>
                
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="text-xs text-gray-500">
                    Market Share: {((selectedData.prescriptions / data.reduce((sum, d) => sum + d.prescriptions, 0)) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
              
              {/* Quick Stats */}
              <div className="card bg-gradient-to-br from-primary-50 to-accent-50">
                <h5 className="text-sm font-semibold text-gray-900 mb-3">Regional Ranking</h5>
                
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">By Volume:</span>
                    <span className="font-semibold text-gray-900">
                      #{[...data].sort((a, b) => b.prescriptions - a.prescriptions)
                        .findIndex(d => d.region === selectedData.region) + 1} of {data.length}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">By Value:</span>
                    <span className="font-semibold text-gray-900">
                      #{[...data].sort((a, b) => b.cost - a.cost)
                        .findIndex(d => d.region === selectedData.region) + 1} of {data.length}
                    </span>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="card text-center py-12">
              <MapPin className="h-12 w-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-600">Click a region to view details</p>
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
                    onClick={() => setSelectedRegion(layout.regions.find((r: any) => 
                      r.name === region.region || r.code === region.region
                    )?.code || region.region)}
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
