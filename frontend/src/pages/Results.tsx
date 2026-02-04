import { useLocation, Link } from 'react-router-dom'
import { ArrowLeft, Download, Users, TrendingUp, DollarSign, Target, MapPin, Award } from 'lucide-react'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

export default function Results() {
  const location = useLocation()
  const { data, formData } = location.state || {}

  if (!data) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">No Data Available</h2>
          <Link to="/" className="btn-primary">
            Run New Analysis
          </Link>
        </div>
      </div>
    )
  }

  const { drug, market_summary, top_opportunities, segments } = data

  // Prepare chart data
  const segmentData = Object.entries(segments.by_volume).map(([name, value]) => ({
    name,
    value: value as number
  }))

  const topOpportunitiesChart = top_opportunities.slice(0, 10).map((opp: any, idx: number) => ({
    name: `#${idx + 1}`,
    volume: opp.current_volume,
    score: Math.round(opp.opportunity_score)
  }))

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/" className="btn-secondary py-2 px-4 text-sm">
                <ArrowLeft className="h-4 w-4 mr-2 inline" />
                New Analysis
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  {drug.name} Analysis
                </h1>
                <p className="text-sm text-gray-600">
                  {formData.company} • {drug.therapeutic_area} • {data.country}
                </p>
              </div>
            </div>
            <button className="btn-primary py-2 px-4 text-sm">
              <Download className="h-4 w-4 mr-2 inline" />
              Export Report
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Prescribers</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {market_summary.total_prescribers.toLocaleString()}
                </p>
              </div>
              <div className="bg-primary-100 p-3 rounded-lg">
                <Users className="h-6 w-6 text-primary-600" />
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Active prescribers in market</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Prescriptions</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {market_summary.total_prescriptions.toLocaleString()}
                </p>
              </div>
              <div className="bg-accent-100 p-3 rounded-lg">
                <TrendingUp className="h-6 w-6 text-accent-600" />
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Period: {data.period}</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Market Value</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  ${market_summary.total_cost.toLocaleString()}
                </p>
              </div>
              <div className="bg-yellow-100 p-3 rounded-lg">
                <DollarSign className="h-6 w-6 text-yellow-600" />
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Total drug spend</p>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Per Prescriber</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {Math.round(market_summary.avg_prescriptions_per_prescriber)}
                </p>
              </div>
              <div className="bg-purple-100 p-3 rounded-lg">
                <Target className="h-6 w-6 text-purple-600" />
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-2">Prescriptions per prescriber</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Segmentation Chart */}
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Prescriber Segmentation</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={segmentData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {segmentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {Object.entries(segments.by_volume).map(([name, value], idx) => (
                <div key={name} className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[idx % COLORS.length] }}></div>
                    <span className="text-gray-700">{name}</span>
                  </div>
                  <span className="font-semibold text-gray-900">{value} prescribers</span>
                </div>
              ))}
            </div>
          </div>

          {/* Top Opportunities Chart */}
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Top 10 Opportunity Scores</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topOpportunitiesChart}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="volume" fill="#2563eb" name="Current Volume" />
                <Bar dataKey="score" fill="#10b981" name="Opportunity Score" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Opportunities Table */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-bold text-gray-900">Top {top_opportunities.length} Opportunities</h2>
            <span className="px-3 py-1 bg-primary-100 text-primary-700 text-sm font-medium rounded-full">
              Focus Targets
            </span>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Prescriber
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Current Volume
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Opportunity Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Recommendations
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {top_opportunities.map((opp: any, idx: number) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {idx < 3 ? (
                          <Award className="h-5 w-5 text-yellow-500 mr-2" />
                        ) : (
                          <span className="text-sm font-medium text-gray-500 mr-2">#{idx + 1}</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{opp.prescriber_name}</div>
                        <div className="text-sm text-gray-500">ID: {opp.prescriber_id}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center text-sm text-gray-900">
                        <MapPin className="h-4 w-4 mr-1 text-gray-400" />
                        {opp.location || 'N/A'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-semibold text-gray-900">
                        {opp.current_volume.toLocaleString()}
                      </div>
                      <div className="text-xs text-gray-500">prescriptions</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-semibold text-primary-600">
                        {Math.round(opp.opportunity_score)}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        {opp.recommendations.slice(0, 2).map((rec: string, recIdx: number) => (
                          <div key={recIdx} className="text-xs text-gray-600">
                            {rec}
                          </div>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Insights */}
        <div className="card mt-8">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Key Insights</h2>
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                1
              </div>
              <p className="text-gray-700">
                Top 20% of prescribers account for {((segments.by_volume['High Prescribers'] / market_summary.total_prescribers) * 100).toFixed(1)}% of total volume
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                2
              </div>
              <p className="text-gray-700">
                Focus sales resources on top {top_opportunities.length} targets for maximum ROI
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                3
              </div>
              <p className="text-gray-700">
                Estimated addressable market: {top_opportunities.slice(0, 20).reduce((sum: number, opp: any) => sum + opp.current_volume, 0).toLocaleString()} prescriptions
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
