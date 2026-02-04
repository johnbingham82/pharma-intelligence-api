import { useState } from 'react'
import { Calendar, X } from 'lucide-react'

interface DateRangePickerProps {
  startDate: string
  endDate: string
  onStartDateChange: (date: string) => void
  onEndDateChange: (date: string) => void
  label?: string
  quickRanges?: boolean
}

const QUICK_RANGES = [
  { label: 'Last 7 days', days: 7 },
  { label: 'Last 30 days', days: 30 },
  { label: 'Last 3 months', days: 90 },
  { label: 'Last 6 months', days: 180 },
  { label: 'Last year', days: 365 },
  { label: 'Year to date', ytd: true }
]

export default function DateRangePicker({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  label = 'Date Range',
  quickRanges = true
}: DateRangePickerProps) {
  const [showQuickRanges, setShowQuickRanges] = useState(false)

  const applyQuickRange = (range: typeof QUICK_RANGES[0]) => {
    const today = new Date()
    const end = today.toISOString().split('T')[0]
    
    let start: string
    if (range.ytd) {
      // Year to date
      start = `${today.getFullYear()}-01-01`
    } else {
      // Days back
      const startDate = new Date(today)
      startDate.setDate(startDate.getDate() - range.days!)
      start = startDate.toISOString().split('T')[0]
    }
    
    onStartDateChange(start)
    onEndDateChange(end)
    setShowQuickRanges(false)
  }

  const clearDates = () => {
    onStartDateChange('')
    onEndDateChange('')
  }

  const hasDateRange = startDate || endDate

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <label className="block text-sm font-medium text-gray-700 flex items-center space-x-2">
          <Calendar className="h-4 w-4" />
          <span>{label}</span>
        </label>
        {hasDateRange && (
          <button
            onClick={clearDates}
            className="text-xs text-gray-500 hover:text-gray-700 flex items-center space-x-1"
          >
            <X className="h-3 w-3" />
            <span>Clear</span>
          </button>
        )}
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs text-gray-500 mb-1">Start Date</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => onStartDateChange(e.target.value)}
            className="input text-sm"
          />
        </div>
        
        <div>
          <label className="block text-xs text-gray-500 mb-1">End Date</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => onEndDateChange(e.target.value)}
            min={startDate}
            className="input text-sm"
          />
        </div>
      </div>

      {quickRanges && (
        <div className="relative">
          <button
            onClick={() => setShowQuickRanges(!showQuickRanges)}
            className="text-xs text-primary-600 hover:text-primary-700 font-medium"
          >
            Quick ranges ▼
          </button>

          {showQuickRanges && (
            <>
              <div 
                className="fixed inset-0 z-10" 
                onClick={() => setShowQuickRanges(false)}
              />
              
              <div className="absolute left-0 top-full mt-1 w-48 bg-white rounded-lg shadow-xl border border-gray-200 py-2 z-20">
                {QUICK_RANGES.map((range, idx) => (
                  <button
                    key={idx}
                    onClick={() => applyQuickRange(range)}
                    className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
                  >
                    {range.label}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {hasDateRange && (
        <div className="text-xs text-gray-500">
          {startDate && endDate ? (
            <>
              Showing data from{' '}
              <span className="font-medium">{new Date(startDate).toLocaleDateString()}</span>
              {' to '}
              <span className="font-medium">{new Date(endDate).toLocaleDateString()}</span>
            </>
          ) : startDate ? (
            <>
              Showing data from{' '}
              <span className="font-medium">{new Date(startDate).toLocaleDateString()}</span>
              {' onwards'}
            </>
          ) : (
            <>
              Showing data up to{' '}
              <span className="font-medium">{new Date(endDate).toLocaleDateString()}</span>
            </>
          )}
        </div>
      )}
    </div>
  )
}

// Compact version for inline use
export function CompactDateRangePicker({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange
}: Omit<DateRangePickerProps, 'label' | 'quickRanges'>) {
  return (
    <div className="flex items-center space-x-2">
      <input
        type="date"
        value={startDate}
        onChange={(e) => onStartDateChange(e.target.value)}
        className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500"
      />
      <span className="text-gray-500 text-sm">to</span>
      <input
        type="date"
        value={endDate}
        onChange={(e) => onEndDateChange(e.target.value)}
        min={startDate}
        className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500"
      />
    </div>
  )
}
