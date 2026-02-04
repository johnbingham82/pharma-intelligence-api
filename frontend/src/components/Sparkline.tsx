import { LineChart, Line, ResponsiveContainer } from 'recharts'

interface SparklineProps {
  data: number[]
  width?: number
  height?: number
  color?: string
  trend?: 'up' | 'down' | 'neutral'
  className?: string
}

export default function Sparkline({ 
  data, 
  width = 100, 
  height = 40, 
  color,
  trend,
  className = ''
}: SparklineProps) {
  // Determine color based on trend if not explicitly provided
  const lineColor = color || (
    trend === 'up' ? '#10b981' :
    trend === 'down' ? '#ef4444' :
    '#2563eb'
  )
  
  // Transform data into chart format
  const chartData = data.map((value, index) => ({ value, index }))
  
  return (
    <div className={`inline-block ${className}`} style={{ width, height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <Line 
            type="monotone" 
            dataKey="value" 
            stroke={lineColor} 
            strokeWidth={2}
            dot={false}
            isAnimationActive={true}
            animationDuration={1000}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

// Mini trend indicator with sparkline
interface TrendIndicatorProps {
  value: number
  previousValue: number
  data: number[]
  label?: string
  unit?: string
  showSparkline?: boolean
}

export function TrendIndicator({ 
  value, 
  previousValue, 
  data,
  label,
  unit = '',
  showSparkline = true
}: TrendIndicatorProps) {
  const change = value - previousValue
  const changePercent = ((change / previousValue) * 100).toFixed(1)
  const trend = change > 0 ? 'up' : change < 0 ? 'down' : 'neutral'
  
  return (
    <div className="flex items-center space-x-3">
      <div className="flex-1">
        {label && <div className="text-xs text-gray-500 mb-1">{label}</div>}
        <div className="flex items-baseline space-x-2">
          <span className="text-2xl font-bold text-gray-900">
            {value.toLocaleString()}{unit}
          </span>
          <span className={`text-sm font-medium ${
            trend === 'up' ? 'text-green-600' :
            trend === 'down' ? 'text-red-600' :
            'text-gray-600'
          }`}>
            {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'} {changePercent}%
          </span>
        </div>
      </div>
      
      {showSparkline && data.length > 0 && (
        <Sparkline 
          data={data} 
          width={80} 
          height={40}
          trend={trend}
        />
      )}
    </div>
  )
}

// Mini chart card with sparkline
interface SparklineCardProps {
  title: string
  value: string | number
  change?: number
  data: number[]
  icon?: React.ReactNode
  trend?: 'up' | 'down' | 'neutral'
}

export function SparklineCard({ 
  title, 
  value, 
  change,
  data,
  icon,
  trend
}: SparklineCardProps) {
  const trendColor = trend === 'up' ? 'text-green-600' :
                     trend === 'down' ? 'text-red-600' :
                     'text-gray-600'
  
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-1">
            {icon && <div className="text-gray-400">{icon}</div>}
            <span className="text-sm text-gray-600">{title}</span>
          </div>
          <div className="text-2xl font-bold text-gray-900">{value}</div>
          {change !== undefined && (
            <div className={`text-sm font-medium ${trendColor} mt-1`}>
              {change > 0 ? '+' : ''}{change}%
            </div>
          )}
        </div>
        
        <Sparkline 
          data={data} 
          width={80} 
          height={50}
          trend={trend}
        />
      </div>
    </div>
  )
}
