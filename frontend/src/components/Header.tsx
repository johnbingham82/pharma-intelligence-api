import { Activity, Database, Globe, DollarSign, Target, Search } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'

export default function Header() {
  const location = useLocation()
  
  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true
    if (path !== '/' && location.pathname.startsWith(path)) return true
    return false
  }
  
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                Pharma Intelligence
                <span className="px-2 py-0.5 bg-accent-100 text-accent-700 text-xs font-medium rounded-full flex items-center gap-1">
                  <Database className="h-3 w-3" />
                  8 Countries
                </span>
              </h1>
              <p className="text-xs text-gray-500">Real Data from UK • US • Australia</p>
            </div>
          </Link>
          
          <nav className="hidden md:flex items-center space-x-6">
            <Link 
              to="/dashboard" 
              className={`text-sm font-medium transition-colors flex items-center gap-1.5 ${
                isActive('/dashboard')
                  ? 'text-primary-600' 
                  : 'text-gray-700 hover:text-primary-600'
              }`}
            >
              <Activity className="h-4 w-4" />
              Dashboard
            </Link>
            
            <Link 
              to="/" 
              className={`text-sm font-medium transition-colors flex items-center gap-1.5 ${
                isActive('/') && location.pathname === '/' 
                  ? 'text-primary-600' 
                  : 'text-gray-700 hover:text-primary-600'
              }`}
            >
              <Target className="h-4 w-4" />
              Analysis
            </Link>
            
            <Link 
              to="/search" 
              className={`text-sm font-medium transition-colors flex items-center gap-1.5 ${
                isActive('/search') 
                  ? 'text-primary-600' 
                  : 'text-gray-700 hover:text-primary-600'
              }`}
            >
              <Search className="h-4 w-4" />
              Search
            </Link>
            
            <Link 
              to="/compare" 
              className={`text-sm font-medium transition-colors flex items-center gap-1.5 ${
                isActive('/compare') 
                  ? 'text-primary-600' 
                  : 'text-gray-700 hover:text-primary-600'
              }`}
            >
              <DollarSign className="h-4 w-4" />
              Pricing
            </Link>
            
            <div className="relative group">
              <button className="text-sm font-medium text-gray-700 hover:text-primary-600 transition-colors flex items-center gap-1.5">
                <Globe className="h-4 w-4" />
                Countries
              </button>
              
              {/* Dropdown on hover */}
              <div className="absolute hidden group-hover:block top-full left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2">
                <Link to="/country/uk" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  🇬🇧 United Kingdom
                </Link>
                <Link to="/country/us" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  🇺🇸 United States
                </Link>
                <Link to="/country/au" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  🇦🇺 Australia
                </Link>
                <div className="border-t border-gray-200 my-1"></div>
                <Link to="/country/fr" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  🇫🇷 France
                </Link>
                <Link to="/country/de" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  🇩🇪 Germany
                </Link>
                <Link to="/country/it" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  🇮🇹 Italy
                </Link>
                <Link to="/country/es" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  🇪🇸 Spain
                </Link>
                <Link to="/country/nl" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                  🇳🇱 Netherlands
                </Link>
              </div>
            </div>
            
            <button className="btn-primary text-sm px-4 py-2">
              Book Demo
            </button>
          </nav>
        </div>
      </div>
    </header>
  )
}
