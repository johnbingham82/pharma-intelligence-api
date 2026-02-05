import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { 
  Search as SearchIcon, Filter, X, Calendar, DollarSign, TrendingUp,
  Users, MapPin, Tag, ChevronDown, ChevronUp, SlidersHorizontal, Download
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import DateRangePicker from '../components/DateRangePicker'
import SavedFilters from '../components/SavedFilters'

interface SearchFilters {
  query: string
  countries: string[]
  therapeuticAreas: string[]
  dateRange: { start: string; end: string }
  minPrescriptions?: number
  maxPrescriptions?: number
  minValue?: number
  maxValue?: number
  growthRate?: 'any' | 'positive' | 'negative' | 'high'
  dataQuality: 'all' | 'real' | 'framework'
  sortBy: 'relevance' | 'prescriptions' | 'value' | 'growth'
  sortOrder: 'asc' | 'desc'
}

interface SearchResult {
  id: string
  type: 'drug' | 'prescriber' | 'region'
  name: string
  country: string
  therapeuticArea?: string
  prescriptions: number
  value: number
  growth: number
  dataQuality: 'real' | 'framework'
  lastUpdated: string
}

const COUNTRIES = [
  { code: 'UK', name: 'United Kingdom', flag: '🇬🇧', hasRealData: true },
  { code: 'US', name: 'United States', flag: '🇺🇸', hasRealData: true },
  { code: 'AU', name: 'Australia', flag: '🇦🇺', hasRealData: true },
  { code: 'JP', name: 'Japan', flag: '🇯🇵', hasRealData: true },
  { code: 'FR', name: 'France', flag: '🇫🇷', hasRealData: false },
  { code: 'DE', name: 'Germany', flag: '🇩🇪', hasRealData: false },
  { code: 'IT', name: 'Italy', flag: '🇮🇹', hasRealData: false },
  { code: 'ES', name: 'Spain', flag: '🇪🇸', hasRealData: true },
  { code: 'NL', name: 'Netherlands', flag: '🇳🇱', hasRealData: false }
]

const THERAPEUTIC_AREAS = [
  'Cardiovascular',
  'Diabetes',
  'Respiratory',
  'CNS',
  'Oncology',
  'Immunology',
  'Gastrointestinal',
  'Infectious Disease',
  'Dermatology',
  'Other'
]

const QUICK_FILTERS = [
  { name: 'High Growth Drugs', icon: TrendingUp, filter: { growthRate: 'high' as const } },
  { name: 'Real Data Only', icon: Tag, filter: { dataQuality: 'real' as const } },
  { name: 'Top Markets', icon: MapPin, filter: { countries: ['UK', 'US', 'AU', 'JP'] } },
  { name: 'High Value', icon: DollarSign, filter: { minValue: 1000000 } }
]

export default function Search() {
  const navigate = useNavigate()
  const [filters, setFilters] = useState<SearchFilters>({
    query: '',
    countries: [],
    therapeuticAreas: [],
    dateRange: { start: '', end: '' },
    dataQuality: 'all',
    sortBy: 'relevance',
    sortOrder: 'desc'
  })
  
  const [showFilters, setShowFilters] = useState(true)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<SearchResult[]>([])
  const [expandedSections, setExpandedSections] = useState({
    countries: true,
    therapeuticAreas: true,
    dateRange: false,
    values: false,
    advanced: false
  })

  // Generate sample results based on filters
  useEffect(() => {
    if (filters.query || filters.countries.length > 0 || filters.therapeuticAreas.length > 0) {
      generateSampleResults()
    }
  }, [filters])

  const generateSampleResults = () => {
    setLoading(true)
    
    setTimeout(() => {
      const sampleResults: SearchResult[] = [
        {
          id: '1',
          type: 'drug',
          name: 'Metformin',
          country: 'UK',
          therapeuticArea: 'Diabetes',
          prescriptions: 9787654,
          value: 320250000,
          growth: 12.4,
          dataQuality: 'real',
          lastUpdated: '2025-01-15'
        },
        {
          id: '2',
          type: 'drug',
          name: 'Atorvastatin',
          country: 'US',
          therapeuticArea: 'Cardiovascular',
          prescriptions: 8456321,
          value: 456789000,
          growth: 8.7,
          dataQuality: 'real',
          lastUpdated: '2025-01-10'
        },
        {
          id: '3',
          type: 'drug',
          name: 'Semaglutide',
          country: 'AU',
          therapeuticArea: 'Diabetes',
          prescriptions: 1234567,
          value: 892000000,
          growth: 87.2,
          dataQuality: 'real',
          lastUpdated: '2025-01-20'
        },
        {
          id: '4',
          type: 'drug',
          name: 'Omeprazole',
          country: 'UK',
          therapeuticArea: 'Gastrointestinal',
          prescriptions: 7654321,
          value: 234567000,
          growth: 5.3,
          dataQuality: 'real',
          lastUpdated: '2025-01-12'
        },
        {
          id: '5',
          type: 'drug',
          name: 'Inclisiran',
          country: 'US',
          therapeuticArea: 'Cardiovascular',
          prescriptions: 234567,
          value: 234000000,
          growth: 145.3,
          dataQuality: 'real',
          lastUpdated: '2025-01-18'
        }
      ]
      
      // Apply filters
      let filtered = sampleResults
      
      if (filters.query) {
        filtered = filtered.filter(r => 
          r.name.toLowerCase().includes(filters.query.toLowerCase())
        )
      }
      
      if (filters.countries.length > 0) {
        filtered = filtered.filter(r => filters.countries.includes(r.country))
      }
      
      if (filters.therapeuticAreas.length > 0) {
        filtered = filtered.filter(r => 
          r.therapeuticArea && filters.therapeuticAreas.includes(r.therapeuticArea)
        )
      }
      
      if (filters.dataQuality !== 'all') {
        filtered = filtered.filter(r => r.dataQuality === filters.dataQuality)
      }
      
      if (filters.growthRate === 'positive') {
        filtered = filtered.filter(r => r.growth > 0)
      } else if (filters.growthRate === 'negative') {
        filtered = filtered.filter(r => r.growth < 0)
      } else if (filters.growthRate === 'high') {
        filtered = filtered.filter(r => r.growth > 50)
      }
      
      if (filters.minPrescriptions) {
        filtered = filtered.filter(r => r.prescriptions >= filters.minPrescriptions!)
      }
      
      if (filters.maxPrescriptions) {
        filtered = filtered.filter(r => r.prescriptions <= filters.maxPrescriptions!)
      }
      
      if (filters.minValue) {
        filtered = filtered.filter(r => r.value >= filters.minValue!)
      }
      
      if (filters.maxValue) {
        filtered = filtered.filter(r => r.value <= filters.maxValue!)
      }
      
      // Sort
      if (filters.sortBy === 'prescriptions') {
        filtered.sort((a, b) => filters.sortOrder === 'desc' 
          ? b.prescriptions - a.prescriptions 
          : a.prescriptions - b.prescriptions
        )
      } else if (filters.sortBy === 'value') {
        filtered.sort((a, b) => filters.sortOrder === 'desc'
          ? b.value - a.value
          : a.value - b.value
        )
      } else if (filters.sortBy === 'growth') {
        filtered.sort((a, b) => filters.sortOrder === 'desc'
          ? b.growth - a.growth
          : a.growth - b.growth
        )
      }
      
      setResults(filtered)
      setLoading(false)
    }, 500)
  }

  const handleSearch = () => {
    generateSampleResults()
  }

  const applyQuickFilter = (quickFilter: any) => {
    setFilters({ ...filters, ...quickFilter.filter })
  }

  const toggleCountry = (code: string) => {
    setFilters({
      ...filters,
      countries: filters.countries.includes(code)
        ? filters.countries.filter(c => c !== code)
        : [...filters.countries, code]
    })
  }

  const toggleTherapeuticArea = (area: string) => {
    setFilters({
      ...filters,
      therapeuticAreas: filters.therapeuticAreas.includes(area)
        ? filters.therapeuticAreas.filter(a => a !== area)
        : [...filters.therapeuticAreas, area]
    })
  }

  const clearFilters = () => {
    setFilters({
      query: '',
      countries: [],
      therapeuticAreas: [],
      dateRange: { start: '', end: '' },
      dataQuality: 'all',
      sortBy: 'relevance',
      sortOrder: 'desc'
    })
    setResults([])
  }

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections({ ...expandedSections, [section]: !expandedSections[section] })
  }

  const activeFilterCount = 
    filters.countries.length +
    filters.therapeuticAreas.length +
    (filters.dataQuality !== 'all' ? 1 : 0) +
    (filters.growthRate && filters.growthRate !== 'any' ? 1 : 0) +
    (filters.minPrescriptions ? 1 : 0) +
    (filters.minValue ? 1 : 0)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Advanced Search</h1>
              <p className="text-sm text-gray-600">Search drugs, prescribers, and regions across 8 countries</p>
            </div>
            
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="btn-secondary px-4 py-2 text-sm flex items-center space-x-2"
            >
              <SlidersHorizontal className="h-4 w-4" />
              <span>{showFilters ? 'Hide' : 'Show'} Filters</span>
              {activeFilterCount > 0 && (
                <span className="ml-2 px-2 py-0.5 bg-primary-600 text-white text-xs font-bold rounded-full">
                  {activeFilterCount}
                </span>
              )}
            </button>
          </div>

          {/* Search Bar */}
          <div className="flex space-x-2">
            <div className="flex-1 relative">
              <SearchIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-lg"
                placeholder="Search for drugs, prescribers, or regions..."
                value={filters.query}
                onChange={(e) => setFilters({ ...filters, query: e.target.value })}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={loading}
              className="btn-primary px-8 disabled:opacity-50"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>

          {/* Quick Filters */}
          <div className="mt-4 flex flex-wrap gap-2">
            {QUICK_FILTERS.map((qf, idx) => (
              <button
                key={idx}
                onClick={() => applyQuickFilter(qf)}
                className="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium flex items-center space-x-2 transition-colors"
              >
                <qf.icon className="h-4 w-4" />
                <span>{qf.name}</span>
              </button>
            ))}
          </div>

          {/* Active Filters */}
          {activeFilterCount > 0 && (
            <div className="mt-4 flex flex-wrap gap-2 items-center">
              <span className="text-sm text-gray-600">Active filters:</span>
              
              {filters.countries.map(code => {
                const country = COUNTRIES.find(c => c.code === code)
                return (
                  <span key={code} className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm flex items-center space-x-1">
                    <span>{country?.flag} {country?.name}</span>
                    <button onClick={() => toggleCountry(code)} className="ml-1 hover:text-primary-900">
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                )
              })}
              
              {filters.therapeuticAreas.map(area => (
                <span key={area} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm flex items-center space-x-1">
                  <span>{area}</span>
                  <button onClick={() => toggleTherapeuticArea(area)} className="ml-1 hover:text-green-900">
                    <X className="h-3 w-3" />
                  </button>
                </span>
              ))}
              
              {filters.dataQuality !== 'all' && (
                <span className="px-3 py-1 bg-accent-100 text-accent-700 rounded-full text-sm flex items-center space-x-1">
                  <span>Real Data Only</span>
                  <button onClick={() => setFilters({ ...filters, dataQuality: 'all' })} className="ml-1 hover:text-accent-900">
                    <X className="h-3 w-3" />
                  </button>
                </span>
              )}
              
              <button
                onClick={clearFilters}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 underline"
              >
                Clear all
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          {showFilters && (
            <div className="lg:col-span-1 space-y-4">
              {/* Countries Filter */}
              <div className="card">
                <button
                  onClick={() => toggleSection('countries')}
                  className="w-full flex items-center justify-between mb-3"
                >
                  <h3 className="font-bold text-gray-900 flex items-center space-x-2">
                    <MapPin className="h-4 w-4" />
                    <span>Countries</span>
                    {filters.countries.length > 0 && (
                      <span className="px-2 py-0.5 bg-primary-100 text-primary-700 text-xs font-bold rounded-full">
                        {filters.countries.length}
                      </span>
                    )}
                  </h3>
                  {expandedSections.countries ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </button>
                
                {expandedSections.countries && (
                  <div className="space-y-2">
                    {COUNTRIES.map(country => (
                      <label key={country.code} className="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-2 rounded">
                        <input
                          type="checkbox"
                          checked={filters.countries.includes(country.code)}
                          onChange={() => toggleCountry(country.code)}
                          className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                        />
                        <span className="text-xl">{country.flag}</span>
                        <span className="text-sm text-gray-700 flex-1">{country.name}</span>
                        {country.hasRealData && (
                          <span className="px-1.5 py-0.5 bg-green-100 text-green-700 text-xs rounded">Real</span>
                        )}
                      </label>
                    ))}
                  </div>
                )}
              </div>

              {/* Therapeutic Areas Filter */}
              <div className="card">
                <button
                  onClick={() => toggleSection('therapeuticAreas')}
                  className="w-full flex items-center justify-between mb-3"
                >
                  <h3 className="font-bold text-gray-900 flex items-center space-x-2">
                    <Tag className="h-4 w-4" />
                    <span>Therapeutic Areas</span>
                    {filters.therapeuticAreas.length > 0 && (
                      <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs font-bold rounded-full">
                        {filters.therapeuticAreas.length}
                      </span>
                    )}
                  </h3>
                  {expandedSections.therapeuticAreas ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </button>
                
                {expandedSections.therapeuticAreas && (
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {THERAPEUTIC_AREAS.map(area => (
                      <label key={area} className="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-2 rounded">
                        <input
                          type="checkbox"
                          checked={filters.therapeuticAreas.includes(area)}
                          onChange={() => toggleTherapeuticArea(area)}
                          className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                        />
                        <span className="text-sm text-gray-700">{area}</span>
                      </label>
                    ))}
                  </div>
                )}
              </div>

              {/* Date Range Filter */}
              <div className="card">
                <button
                  onClick={() => toggleSection('dateRange')}
                  className="w-full flex items-center justify-between mb-3"
                >
                  <h3 className="font-bold text-gray-900 flex items-center space-x-2">
                    <Calendar className="h-4 w-4" />
                    <span>Date Range</span>
                  </h3>
                  {expandedSections.dateRange ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </button>
                
                {expandedSections.dateRange && (
                  <DateRangePicker
                    startDate={filters.dateRange.start}
                    endDate={filters.dateRange.end}
                    onStartDateChange={(date) => setFilters({ ...filters, dateRange: { ...filters.dateRange, start: date } })}
                    onEndDateChange={(date) => setFilters({ ...filters, dateRange: { ...filters.dateRange, end: date } })}
                    label=""
                  />
                )}
              </div>

              {/* Values Filter */}
              <div className="card">
                <button
                  onClick={() => toggleSection('values')}
                  className="w-full flex items-center justify-between mb-3"
                >
                  <h3 className="font-bold text-gray-900 flex items-center space-x-2">
                    <DollarSign className="h-4 w-4" />
                    <span>Values & Volume</span>
                  </h3>
                  {expandedSections.values ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </button>
                
                {expandedSections.values && (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Min Prescriptions</label>
                      <input
                        type="number"
                        className="input text-sm"
                        placeholder="e.g., 1000000"
                        value={filters.minPrescriptions || ''}
                        onChange={(e) => setFilters({ ...filters, minPrescriptions: e.target.value ? parseInt(e.target.value) : undefined })}
                      />
                    </div>
                    
                    <div>
                      <label className="block text-xs text-gray-600 mb-1">Min Market Value ($)</label>
                      <input
                        type="number"
                        className="input text-sm"
                        placeholder="e.g., 10000000"
                        value={filters.minValue || ''}
                        onChange={(e) => setFilters({ ...filters, minValue: e.target.value ? parseInt(e.target.value) : undefined })}
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Advanced Filters */}
              <div className="card">
                <button
                  onClick={() => toggleSection('advanced')}
                  className="w-full flex items-center justify-between mb-3"
                >
                  <h3 className="font-bold text-gray-900 flex items-center space-x-2">
                    <Filter className="h-4 w-4" />
                    <span>Advanced</span>
                  </h3>
                  {expandedSections.advanced ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </button>
                
                {expandedSections.advanced && (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-xs text-gray-600 mb-2">Growth Rate</label>
                      <select
                        className="input text-sm"
                        value={filters.growthRate || 'any'}
                        onChange={(e) => setFilters({ ...filters, growthRate: e.target.value as any })}
                      >
                        <option value="any">Any</option>
                        <option value="positive">Positive</option>
                        <option value="negative">Negative</option>
                        <option value="high">High (&gt;50%)</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-xs text-gray-600 mb-2">Data Quality</label>
                      <select
                        className="input text-sm"
                        value={filters.dataQuality}
                        onChange={(e) => setFilters({ ...filters, dataQuality: e.target.value as any })}
                      >
                        <option value="all">All Data</option>
                        <option value="real">Real Data Only</option>
                        <option value="framework">Framework Only</option>
                      </select>
                    </div>
                  </div>
                )}
              </div>

              {/* Saved Filters */}
              <div className="card">
                <h3 className="font-bold text-gray-900 mb-3">Saved Presets</h3>
                <SavedFilters
                  currentFilters={filters}
                  onLoadFilters={setFilters}
                />
              </div>
            </div>
          )}

          {/* Results */}
          <div className={showFilters ? 'lg:col-span-3' : 'lg:col-span-4'}>
            {/* Results Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-bold text-gray-900">
                  {results.length} Results
                </h2>
                <p className="text-sm text-gray-600">
                  {activeFilterCount > 0 && `${activeFilterCount} filter${activeFilterCount > 1 ? 's' : ''} applied`}
                </p>
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2">
                  <label className="text-sm text-gray-600">Sort by:</label>
                  <select
                    className="text-sm border border-gray-300 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-primary-500"
                    value={filters.sortBy}
                    onChange={(e) => setFilters({ ...filters, sortBy: e.target.value as any })}
                  >
                    <option value="relevance">Relevance</option>
                    <option value="prescriptions">Prescriptions</option>
                    <option value="value">Market Value</option>
                    <option value="growth">Growth Rate</option>
                  </select>
                </div>
                
                <button
                  onClick={() => setFilters({ ...filters, sortOrder: filters.sortOrder === 'asc' ? 'desc' : 'asc' })}
                  className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  title={filters.sortOrder === 'asc' ? 'Ascending' : 'Descending'}
                >
                  {filters.sortOrder === 'desc' ? '↓' : '↑'}
                </button>
                
                <button className="btn-secondary px-4 py-2 text-sm flex items-center space-x-2">
                  <Download className="h-4 w-4" />
                  <span>Export</span>
                </button>
              </div>
            </div>

            {/* Results List */}
            {loading ? (
              <div className="text-center py-16">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
                <p className="text-gray-600 mt-4">Searching...</p>
              </div>
            ) : results.length === 0 ? (
              <div className="text-center py-16">
                <SearchIcon className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No results found</h3>
                <p className="text-gray-600 mb-6">
                  {filters.query || activeFilterCount > 0 
                    ? 'Try adjusting your filters or search query'
                    : 'Enter a search query or select filters to get started'
                  }
                </p>
                {activeFilterCount > 0 && (
                  <button onClick={clearFilters} className="btn-secondary">
                    Clear All Filters
                  </button>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                {results.map((result) => (
                  <div key={result.id} className="card hover:shadow-lg transition-shadow cursor-pointer">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-lg font-bold text-gray-900">{result.name}</h3>
                          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                            {result.type}
                          </span>
                          {result.dataQuality === 'real' && (
                            <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                              Real Data
                            </span>
                          )}
                        </div>
                        
                        <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                          <span className="flex items-center space-x-1">
                            <MapPin className="h-4 w-4" />
                            <span>{COUNTRIES.find(c => c.code === result.country)?.flag} {result.country}</span>
                          </span>
                          {result.therapeuticArea && (
                            <span className="flex items-center space-x-1">
                              <Tag className="h-4 w-4" />
                              <span>{result.therapeuticArea}</span>
                            </span>
                          )}
                          <span className="flex items-center space-x-1">
                            <Calendar className="h-4 w-4" />
                            <span>Updated {new Date(result.lastUpdated).toLocaleDateString()}</span>
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-3 gap-4 pt-3 border-t border-gray-200">
                          <div>
                            <div className="text-xs text-gray-500 mb-1">Prescriptions</div>
                            <div className="text-lg font-semibold text-gray-900">
                              {(result.prescriptions / 1000000).toFixed(2)}M
                            </div>
                          </div>
                          
                          <div>
                            <div className="text-xs text-gray-500 mb-1">Market Value</div>
                            <div className="text-lg font-semibold text-gray-900">
                              ${(result.value / 1000000).toFixed(1)}M
                            </div>
                          </div>
                          
                          <div>
                            <div className="text-xs text-gray-500 mb-1">YoY Growth</div>
                            <div className={`text-lg font-semibold ${result.growth > 0 ? 'text-green-600' : 'text-red-600'}`}>
                              {result.growth > 0 ? '+' : ''}{result.growth.toFixed(1)}%
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="ml-6">
                        <ResponsiveContainer width={120} height={60}>
                          <BarChart data={[
                            { month: 'M1', value: result.prescriptions * 0.08 },
                            { month: 'M2', value: result.prescriptions * 0.09 },
                            { month: 'M3', value: result.prescriptions * 0.085 }
                          ]}>
                            <Bar dataKey="value" fill="#2563eb" radius={[4, 4, 0, 0]} />
                            <Tooltip />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
