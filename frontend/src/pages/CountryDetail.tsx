import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, TrendingUp, DollarSign, Users, MapPin, Calendar, AlertCircle, BarChart3, Map } from 'lucide-react'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import RegionalHeatMap from '../components/RegionalHeatMap'
import { API_BASE_URL } from '../config'

interface RegionalData {
  region: string
  prescriptions: number
  cost: number
  prescribers: number
}

interface MonthlyData {
  month: string
  prescriptions: number
  cost: number
}

interface CountryData {
  name: string
  code: string
  population: string
  market_value: string
  has_real_data: boolean
  data_source?: string
  update_frequency?: string
  currency: string
  regions: RegionalData[]
  monthly_data?: MonthlyData[]
  top_drugs: { name: string; prescriptions: number; cost: number }[]
}

const COUNTRY_INFO: Record<string, { name: string; flag: string; currency: string }> = {
  uk: { name: 'United Kingdom', flag: '🇬🇧', currency: '£' },
  us: { name: 'United States', flag: '🇺🇸', currency: '$' },
  au: { name: 'Australia', flag: '🇦🇺', currency: 'A$' },
  fr: { name: 'France', flag: '🇫🇷', currency: '€' },
  de: { name: 'Germany', flag: '🇩🇪', currency: '€' },
  it: { name: 'Italy', flag: '🇮🇹', currency: '€' },
  es: { name: 'Spain', flag: '🇪🇸', currency: '€' },
  nl: { name: 'Netherlands', flag: '🇳🇱', currency: '€' }
}

export default function CountryDetail() {
  const { countryCode } = useParams<{ countryCode: string }>()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<CountryData | null>(null)
  const [viewMode, setViewMode] = useState<'chart' | 'heatmap'>('chart')

  useEffect(() => {
    fetchCountryData()
  }, [countryCode])

  const fetchCountryData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`${API_BASE_URL}/country/${countryCode}`)
      
      if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.statusText}`)
      }
      
      const result = await response.json()
      setData(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load country data')
      console.error('Error fetching country data:', err)
    } finally {
      setLoading(false)
    }
  }

  const countryInfo = countryCode ? COUNTRY_INFO[countryCode.toLowerCase()] : null

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    )
  }

  if (error || !data || !countryInfo) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <AlertCircle className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Unable to Load Data</h2>
          <p className="text-gray-600 mb-6">{error || 'Country not found'}</p>
          <Link to="/" className="btn-primary">
            <ArrowLeft className="h-4 w-4 mr-2 inline" />
            Back to Home
          </Link>
        </div>
      </div>
    )
  }

  const totalPrescriptions = data.regions.reduce((sum, r) => sum + r.prescriptions, 0)
  const totalCost = data.regions.reduce((sum, r) => sum + r.cost, 0)
  const totalPrescribers = data.regions.reduce((sum, r) => sum + r.prescribers, 0)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/" className="btn-secondary py-2 px-4 text-sm">
                <ArrowLeft className="h-4 w-4 mr-2 inline" />
                All Countries
              </Link>
              <div>
                <div className="flex items-center space-x-3">
                  <span className="text-4xl">{countryInfo.flag}</span>
                  <div>
                    <h1 className="text-2xl font-bold text-gray-900">{countryInfo.name}</h1>
                    <div className="flex items-center space-x-3 mt-1">
                      <span className="text-sm text-gray-600">Population: {data.population}</span>
                      {data.has_real_data && (
                        <span className="px-2 py-0.5 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                          Real Data
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            {data.data_source && (
              <div className="text-right">
                <div className="text-sm font-medium text-gray-900">Data Source</div>
                <div className="text-sm text-gray-600">{data.data_source}</div>
                {data.update_frequency && (
                  <div className="text-xs text-gray-500 mt-1">Updates: {data.update_frequency}</div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Prescriptions</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {totalPrescriptions.toLocaleString()}
                </p>
              </div>
              <div className="bg-primary-100 p-3 rounded-lg">
                <TrendingUp className="h-6 w-6 text-primary-600" />
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Across all regions</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Market Value</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {countryInfo.currency}{(totalCost / 1_000_000).toFixed(1)}M
                </p>
              </div>
              <div className="bg-green-100 p-3 rounded-lg">
                <DollarSign className="h-6 w-6 text-green-600" />
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Total drug spend</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Prescribers</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {totalPrescribers.toLocaleString()}
                </p>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <Users className="h-6 w-6 text-blue-600" />
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Active prescribers</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Regions</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {data.regions.length}
                </p>
              </div>
              <div className="bg-purple-100 p-3 rounded-lg">
                <MapPin className="h-6 w-6 text-purple-600" />
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Coverage areas</p>
          </div>
        </div>

        {/* Regional Breakdown */}
        <div className="card mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold text-gray-900">Regional Distribution</h2>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setViewMode('chart')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  viewMode === 'chart'
                    ? 'bg-primary-100 text-primary-700'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <BarChart3 className="h-4 w-4" />
                Chart
              </button>
              <button
                onClick={() => setViewMode('heatmap')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  viewMode === 'heatmap'
                    ? 'bg-primary-100 text-primary-700'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                <Map className="h-4 w-4" />
                Heat Map
              </button>
            </div>
          </div>
          
          {viewMode === 'chart' ? (
            <div className="space-y-4">
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={data.regions}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="region" angle={-45} textAnchor="end" height={100} />
                  <YAxis yAxisId="left" orientation="left" stroke="#2563eb" />
                  <YAxis yAxisId="right" orientation="right" stroke="#10b981" />
                  <Tooltip 
                    formatter={(value: number, name: string) => {
                      if (name === 'cost') return [`${countryInfo.currency}${value.toLocaleString()}`, 'Cost']
                      return [value.toLocaleString(), name === 'prescriptions' ? 'Prescriptions' : 'Prescribers']
                    }}
                  />
                  <Legend />
                  <Bar yAxisId="left" dataKey="prescriptions" fill="#2563eb" name="Prescriptions" />
                  <Bar yAxisId="right" dataKey="cost" fill="#10b981" name={`Cost (${countryInfo.currency})`} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <RegionalHeatMap 
              data={data.regions}
              countryCode={countryCode || 'uk'}
              title=""
            />
          )}

          {/* Regional Table */}
          <div className="mt-6 overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Region
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Prescriptions
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Market Share
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cost ({countryInfo.currency})
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Prescribers
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data.regions
                  .sort((a, b) => b.prescriptions - a.prescriptions)
                  .map((region, idx) => (
                    <tr key={region.region} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <MapPin className="h-4 w-4 text-gray-400 mr-2" />
                          <span className="text-sm font-medium text-gray-900">{region.region}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                        {region.prescriptions.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-600">
                        {((region.prescriptions / totalPrescriptions) * 100).toFixed(1)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                        {region.cost.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                        {region.prescribers.toLocaleString()}
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Time Series (if available) */}
        {data.monthly_data && data.monthly_data.length > 0 && (
          <div className="card mb-8">
            <h2 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Prescription Trends Over Time
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.monthly_data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip 
                  formatter={(value: number, name: string) => {
                    if (name === 'cost') return [`${countryInfo.currency}${(value / 1_000_000).toFixed(2)}M`, 'Cost']
                    return [(value / 1000).toFixed(1) + 'K', 'Prescriptions']
                  }}
                />
                <Legend />
                <Line 
                  yAxisId="left"
                  type="monotone" 
                  dataKey="prescriptions" 
                  stroke="#2563eb" 
                  strokeWidth={2}
                  name="Prescriptions"
                  dot={{ r: 4 }}
                />
                <Line 
                  yAxisId="right"
                  type="monotone" 
                  dataKey="cost" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  name={`Cost (${countryInfo.currency})`}
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Top Drugs */}
        {data.top_drugs && data.top_drugs.length > 0 && (
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 mb-6">Top Prescribed Drugs</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rank
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Drug Name
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Prescriptions
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Cost ({countryInfo.currency})
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {data.top_drugs.map((drug, idx) => (
                    <tr key={drug.name} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{idx + 1}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {drug.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                        {drug.prescriptions.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">
                        {drug.cost.toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
