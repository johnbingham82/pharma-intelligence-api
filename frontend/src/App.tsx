import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Results from './pages/Results'
import CountryDetail from './pages/CountryDetail'
import PriceComparison from './pages/PriceComparison'
import Dashboard from './pages/Dashboard'
import Search from './pages/Search'
import Header from './components/Header'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/search" element={<Search />} />
            <Route path="/results" element={<Results />} />
            <Route path="/country/:countryCode" element={<CountryDetail />} />
            <Route path="/compare" element={<PriceComparison />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
