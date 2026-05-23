import { useEffect, useState } from 'react'

import Navbar from './components/Navbar'
import DashboardCards from './components/DashboardCards'
import VehicleTable from './components/VehicleTable'

import {
  getDashboard,
  getVehicles
} from './services/api'

export default function App() {
  const [dashboard, setDashboard] = useState(null)
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const dashboardRes = await getDashboard(1)
      const vehiclesRes = await getVehicles()

      setDashboard(dashboardRes.data)
      setVehicles(vehiclesRes.data)
    } catch (error) {
      console.log(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-slate-100">
        <div className="text-3xl font-bold animate-pulse">
          Loading Dashboard...
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <Navbar />

      <div className="max-w-7xl mx-auto p-6">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-800 mb-2">
            Fleet Analytics Dashboard
          </h1>

          <p className="text-gray-600">
            Monitor fuel transportation, fleet activity, and analytics.
          </p>
        </div>

        <DashboardCards dashboard={dashboard} />

        <VehicleTable vehicles={vehicles} />
      </div>
    </div>
  )
}