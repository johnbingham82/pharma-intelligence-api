import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Building2, Pill, Globe, ArrowRight, Check, Zap, Database, Search } from 'lucide-react'
import axios from 'axios'
import { API_BASE_URL } from '../config'

const COUNTRIES = [
  { 
    code: 'UK', 
    name: 'United Kingdom', 
    flag: '🇬🇧', 
    status: 'live', 
    dataQuality: 'real',
    coverage: '67M', 
    type: 'Prescriber-level',
    updateFreq: 'Daily',
    source: 'NHS OpenPrescribing'
  },
  { 
    code: 'US', 
    name: 'United States', 
    flag: '🇺🇸', 
    status: 'live', 
    dataQuality: 'real',
    coverage: '40M Medicare', 
    type: 'Prescriber-level',
    updateFreq: 'Quarterly',
    source: 'CMS Medicare Part D'
  },
  { 
    code: 'AU', 
    name: 'Australia', 
    flag: '🇦🇺', 
    status: 'live', 
    dataQuality: 'real',
    coverage: '26M', 
    type: 'State/Territory',
    updateFreq: 'Monthly',
    source: 'PBS (Real Data)'
  },
  { 
    code: 'JP', 
    name: 'Japan', 
    flag: '🇯🇵', 
    status: 'live', 
    dataQuality: 'real',
    coverage: '125M', 
    type: 'Prefecture-level',
    updateFreq: 'Annual',
    source: 'NDB Open Data (MHLW)'
  },
  { 
    code: 'FR', 
    name: 'France', 
    flag: '🇫🇷', 
    status: 'framework', 
    dataQuality: 'framework',
    coverage: '67M', 
    type: 'Regional',
    updateFreq: 'Annual',
    source: 'Framework Ready'
  },
  { 
    code: 'DE', 
    name: 'Germany', 
    flag: '🇩🇪', 
    status: 'framework', 
    dataQuality: 'framework',
    coverage: '83M', 
    type: 'Regional',
    updateFreq: 'Annual',
    source: 'Framework Ready'
  },
  { 
    code: 'IT', 
    name: 'Italy', 
    flag: '🇮🇹', 
    status: 'framework', 
    dataQuality: 'framework',
    coverage: '60M', 
    type: 'Regional',
    updateFreq: 'Annual',
    source: 'AIFA Ready'
  },
  { 
    code: 'ES', 
    name: 'Spain', 
    flag: '🇪🇸', 
    status: 'live', 
    dataQuality: 'framework',
    coverage: '47M', 
    type: 'Regional',
    updateFreq: 'Annual',
    source: 'Framework (Mock Data)'
  },
  { 
    code: 'NL', 
    name: 'Netherlands', 
    flag: '🇳🇱', 
    status: 'framework', 
    dataQuality: 'framework',
    coverage: '17.5M', 
    type: 'Regional',
    updateFreq: 'Annual',
    source: 'GIP Ready'
  },
]

export default function Home() {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  
  const [formData, setFormData] = useState({
    company: '',
    drugName: '',
    country: ''
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        company: formData.company,
        drug_name: formData.drugName,
        country: formData.country,
        top_n: 50,
        scorer: 'market_share'
      })
      
      // Navigate to results with data
      navigate('/results', { state: { data: response.data, formData } })
    } catch (error) {
      console.error('Analysis failed:', error)
      alert(`Analysis failed. Please check the API connection.`)
    } finally {
      setLoading(false)
    }
  }

  const canProceed = (currentStep: number) => {
    switch (currentStep) {
      case 1: return formData.company.length > 0
      case 2: return formData.drugName.length > 0
      case 3: return formData.country.length > 0
      default: return false
    }
  }

  // Stats
  const totalCoverage = COUNTRIES.reduce((sum, c) => {
    const pop = parseFloat(c.coverage.replace(/[^0-9.]/g, ''))
    return sum + pop
  }, 0)
  const realDataCountries = COUNTRIES.filter(c => c.dataQuality === 'real').length
  const totalCountries = COUNTRIES.length

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-primary-50 via-white to-accent-50">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Global Pharma Intelligence. <span className="text-primary-600">Instant Insights.</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-6">
            Real prescribing data from {realDataCountries} countries. Analyze any drug across {totalCountries} markets 
            covering {Math.round(totalCoverage)}M+ population. 🏆 6 of Top 10 global pharma markets!
          </p>
          
          {/* Stats Bar */}
          <div className="flex justify-center items-center gap-8 mt-8">
            <div className="flex items-center gap-2">
              <Database className="h-5 w-5 text-primary-600" />
              <span className="text-sm font-semibold text-gray-700">
                {totalCountries} Countries
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-accent-600" />
              <span className="text-sm font-semibold text-gray-700">
                {realDataCountries} with Real Data
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Globe className="h-5 w-5 text-primary-600" />
              <span className="text-sm font-semibold text-gray-700">
                {Math.round(totalCoverage)}M+ Population
              </span>
            </div>
          </div>
        </div>

        {/* Dashboard CTA */}
        <Link 
          to="/dashboard"
          className="block max-w-4xl mx-auto mb-12 bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl p-8 text-white hover:shadow-2xl transition-all transform hover:-translate-y-1"
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2">📊 View Global Dashboard</h2>
              <p className="text-primary-100 mb-4">
                Explore comprehensive analytics across all 9 countries with interactive charts, 
                heat maps, and real-time insights.
              </p>
              <div className="flex items-center space-x-6 text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Live Data</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                  <span>12+ Charts</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                  <span>Interactive</span>
                </div>
              </div>
            </div>
            <div className="ml-8">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 text-center border border-white/20">
                <div className="text-4xl font-bold mb-1">{totalCountries}</div>
                <div className="text-sm text-primary-100">Countries</div>
              </div>
            </div>
          </div>
        </Link>

        {/* Browse Countries Section */}
        <div className="mb-12">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Browse Country Data</h2>
            <p className="text-gray-600">Explore detailed regional breakdowns and prescription trends</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {COUNTRIES.map((country) => (
              <button
                key={country.code}
                onClick={() => navigate(`/country/${country.code.toLowerCase()}`)}
                className={`group relative p-5 bg-white border-2 rounded-xl text-left transition-all hover:border-primary-400 hover:shadow-lg transform hover:-translate-y-1 ${
                  country.dataQuality === 'real' 
                    ? 'border-green-200 hover:border-green-400' 
                    : 'border-gray-200'
                } ${country.status !== 'live' ? 'opacity-60' : ''}`}
                disabled={country.status !== 'live'}
              >
                <div className="flex flex-col h-full">
                  <div className="flex items-start justify-between mb-3">
                    <span className="text-4xl">{country.flag}</span>
                    {country.dataQuality === 'real' && (
                      <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full flex items-center gap-1">
                        <Database className="h-3 w-3" />
                        REAL
                      </span>
                    )}
                  </div>
                  
                  <h3 className="font-bold text-gray-900 text-lg mb-1">{country.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">{country.coverage}</p>
                  
                  <div className="mt-auto">
                    <p className="text-xs text-gray-500 mb-1">{country.type}</p>
                    <p className="text-xs text-primary-600 font-medium group-hover:text-primary-700">
                      View Details →
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div className="max-w-3xl mx-auto mb-12">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-gradient-to-br from-primary-50 via-white to-accent-50 text-gray-500 font-medium">
                Or run a custom analysis
              </span>
            </div>
          </div>
        </div>

        {/* Progress Steps */}
        <div className="max-w-3xl mx-auto mb-8">
          <div className="flex items-center justify-between">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex items-center flex-1">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all ${
                  step >= s 
                    ? 'bg-primary-600 border-primary-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-400'
                }`}>
                  {step > s ? <Check className="h-5 w-5" /> : s}
                </div>
                {s < 3 && (
                  <div className={`flex-1 h-1 mx-2 transition-all ${
                    step > s ? 'bg-primary-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-between mt-2">
            <span className="text-sm font-medium text-gray-700">Company</span>
            <span className="text-sm font-medium text-gray-700">Drug</span>
            <span className="text-sm font-medium text-gray-700">Market</span>
          </div>
        </div>

        {/* Main Card */}
        <div className="max-w-3xl mx-auto">
          <div className="card">
            <form onSubmit={handleSubmit}>
              {/* Step 1: Company */}
              {step === 1 && (
                <div className="space-y-6">
                  <div className="flex items-center space-x-3 mb-6">
                    <div className="bg-primary-100 p-3 rounded-lg">
                      <Building2 className="h-6 w-6 text-primary-600" />
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900">Your Company</h2>
                      <p className="text-gray-600">Enter your pharmaceutical company name</p>
                    </div>
                  </div>

                  <div>
                    <label className="label">Company Name</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g., Novartis, Pfizer, AstraZeneca"
                      value={formData.company}
                      onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                      autoFocus
                    />
                    <p className="mt-2 text-sm text-gray-500">
                      This helps us tailor the analysis to your organization
                    </p>
                  </div>

                  <div className="flex justify-end">
                    <button
                      type="button"
                      onClick={() => setStep(2)}
                      disabled={!canProceed(1)}
                      className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                    >
                      <span>Next: Select Drug</span>
                      <ArrowRight className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              )}

              {/* Step 2: Drug */}
              {step === 2 && (
                <div className="space-y-6">
                  <div className="flex items-center space-x-3 mb-6">
                    <div className="bg-primary-100 p-3 rounded-lg">
                      <Pill className="h-6 w-6 text-primary-600" />
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900">Your Drug</h2>
                      <p className="text-gray-600">Enter the drug name you want to analyze</p>
                    </div>
                  </div>

                  <div>
                    <label className="label">Drug Name</label>
                    <input
                      type="text"
                      className="input"
                      placeholder="e.g., Metformin, Atorvastatin, Inclisiran"
                      value={formData.drugName}
                      onChange={(e) => setFormData({ ...formData, drugName: e.target.value })}
                      autoFocus
                    />
                    <p className="mt-2 text-sm text-gray-500">
                      Enter brand name or generic name
                    </p>
                  </div>

                  <div className="flex justify-between">
                    <button
                      type="button"
                      onClick={() => setStep(1)}
                      className="btn-secondary"
                    >
                      Back
                    </button>
                    <button
                      type="button"
                      onClick={() => setStep(3)}
                      disabled={!canProceed(2)}
                      className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                    >
                      <span>Next: Select Market</span>
                      <ArrowRight className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              )}

              {/* Step 3: Country */}
              {step === 3 && (
                <div className="space-y-6">
                  <div className="flex items-center space-x-3 mb-6">
                    <div className="bg-primary-100 p-3 rounded-lg">
                      <Globe className="h-6 w-6 text-primary-600" />
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900">Select Market</h2>
                      <p className="text-gray-600">Choose the country to analyze</p>
                    </div>
                  </div>

                  <div className="grid gap-3">
                    {COUNTRIES.map((country) => (
                      <button
                        key={country.code}
                        type="button"
                        onClick={() => setFormData({ ...formData, country: country.code })}
                        className={`p-4 border-2 rounded-lg text-left transition-all hover:border-primary-300 ${
                          formData.country === country.code
                            ? 'border-primary-600 bg-primary-50'
                            : 'border-gray-200 bg-white'
                        } ${country.status !== 'live' ? 'opacity-60' : ''}`}
                        disabled={country.status !== 'live'}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-3">
                            <span className="text-3xl">{country.flag}</span>
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <h3 className="font-semibold text-gray-900">{country.name}</h3>
                                {country.dataQuality === 'real' && (
                                  <span className="px-2 py-0.5 bg-accent-100 text-accent-700 text-xs font-medium rounded-full flex items-center gap-1">
                                    <Database className="h-3 w-3" />
                                    REAL DATA
                                  </span>
                                )}
                                {country.status === 'framework' && (
                                  <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs font-medium rounded-full">
                                    Framework
                                  </span>
                                )}
                              </div>
                              <div className="space-y-1">
                                <p className="text-sm text-gray-600">
                                  {country.type} • {country.coverage} coverage
                                </p>
                                <p className="text-xs text-gray-500">
                                  {country.source} • {country.updateFreq} updates
                                </p>
                              </div>
                            </div>
                          </div>
                          {formData.country === country.code && (
                            <Check className="h-6 w-6 text-primary-600 flex-shrink-0 ml-2" />
                          )}
                        </div>
                      </button>
                    ))}
                  </div>

                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <p className="text-sm text-blue-800">
                      <strong>💡 Tip:</strong> Countries with "Real Data" use actual government prescribing statistics. 
                      Framework countries use population-based models and will be upgraded with real data soon.
                    </p>
                  </div>

                  <div className="flex justify-between">
                    <button
                      type="button"
                      onClick={() => setStep(2)}
                      className="btn-secondary"
                    >
                      Back
                    </button>
                    <button
                      type="submit"
                      disabled={!canProceed(3) || loading}
                      className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                    >
                      {loading ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                          <span>Analyzing...</span>
                        </>
                      ) : (
                        <>
                          <span>Run Analysis</span>
                          <ArrowRight className="h-5 w-5" />
                        </>
                      )}
                    </button>
                  </div>
                </div>
              )}
            </form>
          </div>

          {/* Platform Stats */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="text-2xl font-bold text-primary-600">{totalCountries}</div>
              <div className="text-sm text-gray-600">Countries</div>
              <div className="text-xs text-gray-500 mt-1">{Math.round(totalCoverage)}M population</div>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="text-2xl font-bold text-accent-600">{realDataCountries}</div>
              <div className="text-sm text-gray-600">Real Data Sources</div>
              <div className="text-xs text-gray-500 mt-1">Government-validated</div>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="text-2xl font-bold text-primary-600">Monthly</div>
              <div className="text-sm text-gray-600">Update Frequency</div>
              <div className="text-xs text-gray-500 mt-1">Best in class (PBS)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
