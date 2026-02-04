import { useState, useEffect } from 'react'
import { Save, Star, Trash2, X } from 'lucide-react'

interface FilterPreset {
  id: string
  name: string
  filters: any
  createdAt: string
  starred: boolean
}

interface SavedFiltersProps {
  currentFilters: any
  onLoadFilters: (filters: any) => void
}

export default function SavedFilters({ currentFilters, onLoadFilters }: SavedFiltersProps) {
  const [presets, setPresets] = useState<FilterPreset[]>([])
  const [showSaveDialog, setShowSaveDialog] = useState(false)
  const [showLoadDialog, setShowLoadDialog] = useState(false)
  const [presetName, setPresetName] = useState('')

  // Load presets from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('filterPresets')
    if (saved) {
      setPresets(JSON.parse(saved))
    }
  }, [])

  // Save presets to localStorage
  const savePresetsToStorage = (newPresets: FilterPreset[]) => {
    localStorage.setItem('filterPresets', JSON.stringify(newPresets))
    setPresets(newPresets)
  }

  const saveCurrentFilters = () => {
    if (!presetName.trim()) return

    const newPreset: FilterPreset = {
      id: Date.now().toString(),
      name: presetName.trim(),
      filters: currentFilters,
      createdAt: new Date().toISOString(),
      starred: false
    }

    savePresetsToStorage([...presets, newPreset])
    setPresetName('')
    setShowSaveDialog(false)
  }

  const loadPreset = (preset: FilterPreset) => {
    onLoadFilters(preset.filters)
    setShowLoadDialog(false)
  }

  const deletePreset = (id: string) => {
    savePresetsToStorage(presets.filter(p => p.id !== id))
  }

  const toggleStar = (id: string) => {
    savePresetsToStorage(
      presets.map(p => p.id === id ? { ...p, starred: !p.starred } : p)
    )
  }

  const starredPresets = presets.filter(p => p.starred)
  const otherPresets = presets.filter(p => !p.starred)

  return (
    <div className="space-y-2">
      {/* Quick Load Buttons for Starred */}
      {starredPresets.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {starredPresets.map(preset => (
            <button
              key={preset.id}
              onClick={() => loadPreset(preset)}
              className="px-3 py-1.5 bg-yellow-50 hover:bg-yellow-100 border border-yellow-200 text-yellow-800 rounded-lg text-sm font-medium flex items-center space-x-2 transition-colors"
            >
              <Star className="h-3 w-3 fill-current" />
              <span>{preset.name}</span>
            </button>
          ))}
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center space-x-2">
        <button
          onClick={() => setShowSaveDialog(true)}
          className="flex-1 btn-secondary py-2 text-sm flex items-center justify-center space-x-2"
        >
          <Save className="h-4 w-4" />
          <span>Save Filters</span>
        </button>

        <button
          onClick={() => setShowLoadDialog(true)}
          disabled={presets.length === 0}
          className="flex-1 btn-secondary py-2 text-sm flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          <Star className="h-4 w-4" />
          <span>Load ({presets.length})</span>
        </button>
      </div>

      {/* Save Dialog */}
      {showSaveDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-900">Save Filter Preset</h3>
              <button
                onClick={() => setShowSaveDialog(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Preset Name
              </label>
              <input
                type="text"
                value={presetName}
                onChange={(e) => setPresetName(e.target.value)}
                placeholder="e.g., High Growth Diabetes Drugs"
                className="input w-full"
                autoFocus
                onKeyPress={(e) => e.key === 'Enter' && saveCurrentFilters()}
              />
            </div>

            <div className="bg-gray-50 rounded-lg p-3 mb-4">
              <p className="text-xs text-gray-600 mb-2">This preset will save:</p>
              <ul className="text-xs text-gray-700 space-y-1">
                {currentFilters.countries?.length > 0 && (
                  <li>• {currentFilters.countries.length} selected countries</li>
                )}
                {currentFilters.therapeuticAreas?.length > 0 && (
                  <li>• {currentFilters.therapeuticAreas.length} therapeutic areas</li>
                )}
                {currentFilters.minPrescriptions && (
                  <li>• Min prescriptions: {currentFilters.minPrescriptions.toLocaleString()}</li>
                )}
                {currentFilters.dataQuality !== 'all' && (
                  <li>• Data quality: {currentFilters.dataQuality}</li>
                )}
              </ul>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={() => setShowSaveDialog(false)}
                className="flex-1 btn-secondary"
              >
                Cancel
              </button>
              <button
                onClick={saveCurrentFilters}
                disabled={!presetName.trim()}
                className="flex-1 btn-primary disabled:opacity-50"
              >
                Save Preset
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Load Dialog */}
      {showLoadDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-bold text-gray-900">Saved Filter Presets</h3>
              <button
                onClick={() => setShowLoadDialog(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {presets.length === 0 ? (
              <div className="text-center py-8">
                <Save className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-600">No saved presets yet</p>
                <p className="text-sm text-gray-500 mt-1">
                  Apply some filters and click "Save Filters" to create a preset
                </p>
              </div>
            ) : (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {/* Starred First */}
                {starredPresets.length > 0 && (
                  <>
                    <h4 className="text-sm font-semibold text-gray-700 flex items-center space-x-2">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span>Starred</span>
                    </h4>
                    {starredPresets.map(preset => (
                      <PresetCard
                        key={preset.id}
                        preset={preset}
                        onLoad={() => loadPreset(preset)}
                        onDelete={() => deletePreset(preset.id)}
                        onToggleStar={() => toggleStar(preset.id)}
                      />
                    ))}
                  </>
                )}

                {/* Other Presets */}
                {otherPresets.length > 0 && (
                  <>
                    {starredPresets.length > 0 && (
                      <h4 className="text-sm font-semibold text-gray-700 mt-6">Other Presets</h4>
                    )}
                    {otherPresets.map(preset => (
                      <PresetCard
                        key={preset.id}
                        preset={preset}
                        onLoad={() => loadPreset(preset)}
                        onDelete={() => deletePreset(preset.id)}
                        onToggleStar={() => toggleStar(preset.id)}
                      />
                    ))}
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

function PresetCard({ 
  preset, 
  onLoad, 
  onDelete, 
  onToggleStar 
}: { 
  preset: FilterPreset
  onLoad: () => void
  onDelete: () => void
  onToggleStar: () => void
}) {
  const filterCount = 
    (preset.filters.countries?.length || 0) +
    (preset.filters.therapeuticAreas?.length || 0) +
    (preset.filters.minPrescriptions ? 1 : 0) +
    (preset.filters.dataQuality !== 'all' ? 1 : 0)

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors">
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900 flex items-center space-x-2">
            <span>{preset.name}</span>
            {preset.starred && (
              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
            )}
          </h4>
          <p className="text-xs text-gray-500 mt-1">
            Created {new Date(preset.createdAt).toLocaleDateString()} • {filterCount} filters
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={onToggleStar}
            className="p-1 hover:bg-gray-100 rounded transition-colors"
            title={preset.starred ? 'Remove from starred' : 'Add to starred'}
          >
            <Star className={`h-4 w-4 ${preset.starred ? 'fill-yellow-400 text-yellow-400' : 'text-gray-400'}`} />
          </button>
          
          <button
            onClick={onDelete}
            className="p-1 hover:bg-red-50 text-red-600 rounded transition-colors"
            title="Delete preset"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="flex flex-wrap gap-1 mb-3">
        {preset.filters.countries?.length > 0 && (
          <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">
            {preset.filters.countries.length} countries
          </span>
        )}
        {preset.filters.therapeuticAreas?.length > 0 && (
          <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
            {preset.filters.therapeuticAreas.length} areas
          </span>
        )}
        {preset.filters.dataQuality === 'real' && (
          <span className="px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded-full">
            Real data
          </span>
        )}
      </div>

      <button
        onClick={onLoad}
        className="w-full btn-primary py-2 text-sm"
      >
        Load Preset
      </button>
    </div>
  )
}
