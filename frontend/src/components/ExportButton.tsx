import { useState } from 'react'
import { Download, FileText, FileSpreadsheet, Image } from 'lucide-react'

interface ExportButtonProps {
  data: any
  filename?: string
  formats?: ('csv' | 'json' | 'png')[]
  onExport?: (format: string) => void
}

export default function ExportButton({ 
  data, 
  filename = 'export',
  formats = ['csv', 'json'],
  onExport
}: ExportButtonProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [exporting, setExporting] = useState(false)

  const handleExport = async (format: string) => {
    setExporting(true)
    
    try {
      if (onExport) {
        onExport(format)
      } else {
        // Default export logic
        switch (format) {
          case 'csv':
            exportToCSV(data, filename)
            break
          case 'json':
            exportToJSON(data, filename)
            break
          case 'png':
            // Would require html2canvas or similar
            alert('PNG export requires additional setup')
            break
        }
      }
    } catch (error) {
      console.error('Export failed:', error)
      alert('Export failed. Please try again.')
    } finally {
      setExporting(false)
      setIsOpen(false)
    }
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={exporting}
        className="btn-primary px-4 py-2 text-sm flex items-center space-x-2 disabled:opacity-50"
      >
        <Download className="h-4 w-4" />
        <span>{exporting ? 'Exporting...' : 'Export'}</span>
      </button>

      {isOpen && (
        <>
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setIsOpen(false)}
          />
          
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 py-2 z-20">
            {formats.includes('csv') && (
              <button
                onClick={() => handleExport('csv')}
                className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-3"
              >
                <FileSpreadsheet className="h-4 w-4 text-green-600" />
                <div>
                  <div className="font-medium">Export as CSV</div>
                  <div className="text-xs text-gray-500">Spreadsheet format</div>
                </div>
              </button>
            )}
            
            {formats.includes('json') && (
              <button
                onClick={() => handleExport('json')}
                className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-3"
              >
                <FileText className="h-4 w-4 text-blue-600" />
                <div>
                  <div className="font-medium">Export as JSON</div>
                  <div className="text-xs text-gray-500">API format</div>
                </div>
              </button>
            )}
            
            {formats.includes('png') && (
              <button
                onClick={() => handleExport('png')}
                className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-3"
              >
                <Image className="h-4 w-4 text-purple-600" />
                <div>
                  <div className="font-medium">Export as PNG</div>
                  <div className="text-xs text-gray-500">Image format</div>
                </div>
              </button>
            )}
          </div>
        </>
      )}
    </div>
  )
}

// Helper function to export to CSV
function exportToCSV(data: any, filename: string) {
  // Convert data to CSV format
  let csv = ''
  
  if (Array.isArray(data)) {
    // Get headers from first object
    const headers = Object.keys(data[0] || {})
    csv = headers.join(',') + '\n'
    
    // Add rows
    data.forEach(row => {
      const values = headers.map(header => {
        const value = row[header]
        // Escape commas and quotes
        if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
          return `"${value.replace(/"/g, '""')}"`
        }
        return value
      })
      csv += values.join(',') + '\n'
    })
  } else {
    // Single object - convert to key-value pairs
    csv = 'Key,Value\n'
    Object.entries(data).forEach(([key, value]) => {
      csv += `${key},${value}\n`
    })
  }
  
  // Create download link
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}.csv`)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Helper function to export to JSON
function exportToJSON(data: any, filename: string) {
  const json = JSON.stringify(data, null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}.json`)
  link.style.visibility = 'hidden'
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Simple Export Button (no dropdown)
export function SimpleExportButton({ 
  onClick, 
  label = 'Export',
  variant = 'primary'
}: { 
  onClick: () => void
  label?: string
  variant?: 'primary' | 'secondary'
}) {
  return (
    <button
      onClick={onClick}
      className={`${variant === 'primary' ? 'btn-primary' : 'btn-secondary'} px-4 py-2 text-sm flex items-center space-x-2`}
    >
      <Download className="h-4 w-4" />
      <span>{label}</span>
    </button>
  )
}
