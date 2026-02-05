import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  TrendingUp, TrendingDown, Users, DollarSign, Globe, Activity,
  ArrowUpRight, ArrowDownRight, Calendar, Target, Award
} from 'lucide-react'
import {
  AreaChart, Area, BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import ExportButton from '../components/ExportButton'

const COLORS = {
  primary: ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'],
  accent: ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5'],
  warm: ['#f59e0b', '#fbbf24', '#fcd34d', '#fde68a', '#fef3c7'],
  cool: ['#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe']
}

// Animated counter component
function AnimatedCounter({ value, duration = 2000, prefix = '', suffix = '' }: { 
  value: number
  duration?: number
  prefix?: string
  suffix?: string
}) {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    let start = 0
    const end = value
    const increment = end / (duration / 16)
    
    const timer = setInterval(() => {
      start += increment
      if (start >= end) {
        setCount(end)
        clearInterval(timer)
      } else {
        setCount(Math.floor(start))
      }
    }, 16)
    
    return () => clearInterval(timer)
  }, [value, duration])
  
  return <span>{prefix}{count.toLocaleString()}{suffix}</span>
}

export default function Dashboard() {
  // Sample data - in production, fetch from API
  const [timeRange, setTimeRange] = useState('12m')
  
  // Global market data
  const globalStats = {
    totalPrescriptions: 45678900,
    totalValue: 8920000000,
    totalPrescribers: 234567,
    countries: 9,
    growth: 12.4,
    topDrug: 'Metformin'
  }
  
  // Monthly trend data
  const monthlyTrends = [
    { month: 'Jan', prescriptions: 3456, value: 678, growth: 5.2 },
    { month: 'Feb', prescriptions: 3589, value: 702, growth: 3.8 },
    { month: 'Mar', prescriptions: 3812, value: 745, growth: 6.2 },
    { month: 'Apr', prescriptions: 3678, value: 720, growth: -3.5 },
    { month: 'May', prescriptions: 3923, value: 768, growth: 6.7 },
    { month: 'Jun', prescriptions: 4012, value: 785, growth: 2.3 },
    { month: 'Jul', prescriptions: 4156, value: 813, growth: 3.6 },
    { month: 'Aug', prescriptions: 4234, value: 828, growth: 1.9 },
    { month: 'Sep', prescriptions: 4089, value: 799, growth: -3.4 },
    { month: 'Oct', prescriptions: 4312, value: 843, growth: 5.5 },
    { month: 'Nov', prescriptions: 4445, value: 869, growth: 3.1 },
    { month: 'Dec', prescriptions: 4598, value: 898, growth: 3.4 }
  ]
  
  // Market share by country
  const marketShareData = [
    { country: 'US', value: 32, color: COLORS.primary[0] },
    { country: 'Japan', value: 20, color: COLORS.accent[1] },
    { country: 'UK', value: 15, color: COLORS.primary[1] },
    { country: 'Germany', value: 12, color: COLORS.primary[2] },
    { country: 'France', value: 10, color: COLORS.primary[3] },
    { country: 'Australia', value: 6, color: COLORS.accent[0] },
    { country: 'Others', value: 5, color: COLORS.cool[2] }
  ]
  
  // Therapeutic area distribution
  const therapeuticAreas = [
    { area: 'Cardiovascular', prescriptions: 12500, value: 2890, growth: 8.3 },
    { area: 'Diabetes', prescriptions: 9800, value: 2340, growth: 12.1 },
    { area: 'Respiratory', prescriptions: 8200, value: 1890, growth: 5.6 },
    { area: 'CNS', prescriptions: 7600, value: 3420, growth: 15.2 },
    { area: 'Oncology', prescriptions: 3200, value: 4560, growth: 22.8 },
    { area: 'Other', prescriptions: 4400, value: 1820, growth: 4.2 }
  ]
  
  // Country comparison radar data
  const countryMetrics = [
    { metric: 'Volume', UK: 85, US: 95, AU: 75, DE: 80, FR: 70 },
    { metric: 'Growth', UK: 70, US: 60, AU: 90, DE: 65, FR: 55 },
    { metric: 'Value', UK: 75, US: 100, AU: 65, DE: 85, FR: 80 },
    { metric: 'Access', UK: 95, US: 70, AU: 90, DE: 85, FR: 88 },
    { metric: 'Competition', UK: 80, US: 90, AU: 70, DE: 75, FR: 72 }
  ]
  
  // Top growing drugs
  const topGrowers = [
    { drug: 'Inclisiran', growth: 145.3, value: 234, category: 'Cardiovascular' },
    { drug: 'Bimekizumab', growth: 98.7, value: 156, category: 'Immunology' },
    { drug: 'Semaglutide', growth: 87.2, value: 892, category: 'Diabetes' },
    { drug: 'Tirzepatide', growth: 76.4, value: 445, category: 'Diabetes' },
    { drug: 'Mavacamten', growth: 65.1, value: 178, category: 'Cardiovascular' }
  ]
  
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold mb-2">Global Pharma Dashboard</h1>
              <p className="text-primary-100">Real-time insights across 9 countries</p>
            </div>
            
            <div className="flex items-center space-x-3">
              <select 
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="bg-white/10 border border-white/20 text-white rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-white/30"
              >
                <option value="1m">Last Month</option>
                <option value="3m">Last 3 Months</option>
                <option value="6m">Last 6 Months</option>
                <option value="12m">Last 12 Months</option>
                <option value="ytd">Year to Date</option>
              </select>
              
              <ExportButton 
                data={{
                  stats: globalStats,
                  monthlyTrends,
                  marketShare: marketShareData,
                  therapeuticAreas,
                  topGrowers
                }}
                filename={`pharma-dashboard-${new Date().toISOString().split('T')[0]}`}
                formats={['csv', 'json']}
              />
            </div>
          </div>
          
          {/* Key Stats Row */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <span className="text-primary-100 text-sm">Total Prescriptions</span>
                <Activity className="h-5 w-5 text-primary-200" />
              </div>
              <div className="text-2xl font-bold mb-1">
                <AnimatedCounter value={45678900} />
              </div>
              <div className="flex items-center text-sm text-green-300">
                <ArrowUpRight className="h-4 w-4 mr-1" />
                <span>{globalStats.growth}% vs last year</span>
              </div>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <span className="text-primary-100 text-sm">Market Value</span>
                <DollarSign className="h-5 w-5 text-primary-200" />
              </div>
              <div className="text-2xl font-bold mb-1">
                $<AnimatedCounter value={8920} />M
              </div>
              <div className="flex items-center text-sm text-green-300">
                <ArrowUpRight className="h-4 w-4 mr-1" />
                <span>18.3% growth</span>
              </div>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <span className="text-primary-100 text-sm">Active Prescribers</span>
                <Users className="h-5 w-5 text-primary-200" />
              </div>
              <div className="text-2xl font-bold mb-1">
                <AnimatedCounter value={234567} />
              </div>
              <div className="flex items-center text-sm text-primary-200">
                <Globe className="h-4 w-4 mr-1" />
                <span>{globalStats.countries} countries</span>
              </div>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <span className="text-primary-100 text-sm">Top Drug</span>
                <Award className="h-5 w-5 text-primary-200" />
              </div>
              <div className="text-2xl font-bold mb-1">{globalStats.topDrug}</div>
              <div className="text-sm text-primary-200">9.8M prescriptions</div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Main Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Trend Chart */}
          <div className="lg:col-span-2 card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">Prescription Trends</h2>
              <div className="flex items-center space-x-2">
                <button className="px-3 py-1 text-xs bg-primary-100 text-primary-700 rounded-full font-medium">
                  Volume
                </button>
                <button className="px-3 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                  Value
                </button>
              </div>
            </div>
            
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={monthlyTrends}>
                <defs>
                  <linearGradient id="colorPrescriptions" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563eb" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="month" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'white', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                  formatter={(value: number, name: string) => {
                    if (name === 'value') return [`$${value}M`, 'Value']
                    return [`${value}K`, 'Prescriptions']
                  }}
                />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="prescriptions" 
                  stroke="#2563eb" 
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorPrescriptions)"
                  name="Prescriptions (K)"
                />
                <Area 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorValue)"
                  name="Value ($M)"
                />
              </AreaChart>
            </ResponsiveContainer>
            
            {/* Mini stats below chart */}
            <div className="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-gray-200">
              <div>
                <div className="text-xs text-gray-500 mb-1">Avg Monthly</div>
                <div className="text-lg font-semibold text-gray-900">4,025K</div>
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Peak Month</div>
                <div className="text-lg font-semibold text-gray-900">Dec (4,598K)</div>
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">YoY Growth</div>
                <div className="text-lg font-semibold text-green-600">+12.4%</div>
              </div>
            </div>
          </div>
          
          {/* Market Share Donut */}
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 mb-6">Market Share by Country</h2>
            
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={marketShareData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  fill="#8884d8"
                  paddingAngle={2}
                  dataKey="value"
                >
                  {marketShareData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number) => [`${value}%`, 'Share']} />
              </PieChart>
            </ResponsiveContainer>
            
            {/* Legend */}
            <div className="space-y-2 mt-4">
              {marketShareData.map((item, idx) => (
                <div key={idx} className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                    <span className="text-gray-700">{item.country}</span>
                  </div>
                  <span className="font-semibold text-gray-900">{item.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Therapeutic Areas & Country Radar */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Therapeutic Areas */}
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 mb-6">Performance by Therapeutic Area</h2>
            
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={therapeuticAreas} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="area" type="category" width={100} />
                <Tooltip 
                  formatter={(value: number, name: string) => {
                    if (name === 'value') return [`$${value}M`, 'Value']
                    if (name === 'growth') return [`${value}%`, 'Growth']
                    return [value, name]
                  }}
                />
                <Legend />
                <Bar dataKey="prescriptions" fill="#2563eb" name="Prescriptions (K)" radius={[0, 4, 4, 0]} />
                <Bar dataKey="value" fill="#10b981" name="Value ($M)" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          {/* Country Comparison Radar */}
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 mb-6">Country Comparison (Top 5)</h2>
            
            <ResponsiveContainer width="100%" height={350}>
              <RadarChart data={countryMetrics}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="metric" stroke="#6b7280" />
                <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#6b7280" />
                <Radar name="UK" dataKey="UK" stroke="#2563eb" fill="#2563eb" fillOpacity={0.3} />
                <Radar name="US" dataKey="US" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                <Radar name="AU" dataKey="AU" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} />
                <Radar name="DE" dataKey="DE" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} />
                <Radar name="FR" dataKey="FR" stroke="#ec4899" fill="#ec4899" fillOpacity={0.3} />
                <Legend />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
            
            <div className="mt-4 text-xs text-gray-500">
              Metrics scaled 0-100: Volume (prescription volume), Growth (YoY %), Value (market $), 
              Access (healthcare coverage), Competition (market concentration)
            </div>
          </div>
        </div>
        
        {/* Top Growing Drugs */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold text-gray-900">Top Growing Drugs (YoY)</h2>
            <Link to="/compare" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
              Compare All Drugs →
            </Link>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {topGrowers.map((drug, idx) => (
              <div 
                key={drug.drug}
                className="relative group bg-gradient-to-br from-primary-50 to-accent-50 rounded-lg p-4 border-2 border-transparent hover:border-primary-300 transition-all cursor-pointer"
              >
                <div className="absolute top-2 right-2">
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full">
                    #{idx + 1}
                  </span>
                </div>
                
                <div className="mb-3">
                  <h3 className="font-bold text-gray-900 text-sm mb-1">{drug.drug}</h3>
                  <p className="text-xs text-gray-600">{drug.category}</p>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-600">Growth</span>
                    <div className="flex items-center text-green-600">
                      <TrendingUp className="h-3 w-3 mr-1" />
                      <span className="text-sm font-bold">{drug.growth}%</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-600">Value</span>
                    <span className="text-sm font-semibold text-gray-900">${drug.value}M</span>
                  </div>
                </div>
                
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <button className="text-xs text-primary-600 hover:text-primary-700 font-medium w-full text-center">
                    View Details →
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
          <Link to="/" className="card group hover:shadow-lg transition-shadow">
            <div className="flex items-center space-x-4">
              <div className="bg-primary-100 p-3 rounded-lg group-hover:bg-primary-200 transition-colors">
                <Target className="h-6 w-6 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Run Analysis</h3>
                <p className="text-sm text-gray-600">Target prescribers in any market</p>
              </div>
            </div>
          </Link>
          
          <Link to="/search" className="card group hover:shadow-lg transition-shadow">
            <div className="flex items-center space-x-4">
              <div className="bg-blue-100 p-3 rounded-lg group-hover:bg-blue-200 transition-colors">
                <Users className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Advanced Search</h3>
                <p className="text-sm text-gray-600">Filter drugs & regions</p>
              </div>
            </div>
          </Link>
          
          <Link to="/compare" className="card group hover:shadow-lg transition-shadow">
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 p-3 rounded-lg group-hover:bg-green-200 transition-colors">
                <DollarSign className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Compare Prices</h3>
                <p className="text-sm text-gray-600">Cross-country drug pricing</p>
              </div>
            </div>
          </Link>
          
          <div className="card group hover:shadow-lg transition-shadow cursor-pointer">
            <div className="flex items-center space-x-4">
              <div className="bg-purple-100 p-3 rounded-lg group-hover:bg-purple-200 transition-colors">
                <Calendar className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">Schedule Report</h3>
                <p className="text-sm text-gray-600">Automated insights delivery</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
