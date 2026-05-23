import { Truck } from 'lucide-react'

export default function Navbar() {
  return (
    <div className="bg-slate-900 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-blue-500 p-2 rounded-xl">
            <Truck size={24} />
          </div>

          <div>
            <h1 className="text-2xl font-bold">Fuel Management</h1>
            <p className="text-sm text-slate-300">
              Fleet Monitoring Dashboard
            </p>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-4">
          <button className="bg-blue-500 hover:bg-blue-600 transition px-4 py-2 rounded-lg">
            Dashboard
          </button>

          <button className="bg-slate-700 hover:bg-slate-600 transition px-4 py-2 rounded-lg">
            Vehicles
          </button>
        </div>
      </div>
    </div>
  )
}