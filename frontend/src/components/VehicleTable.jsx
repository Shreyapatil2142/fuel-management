import { useState } from 'react'

export default function VehicleTable({ vehicles }) {
  const [search, setSearch] = useState('')

  const filteredVehicles = vehicles.filter((vehicle) =>
    vehicle.vehicle_number
      ?.toLowerCase()
      .includes(search.toLowerCase())
  )

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 overflow-hidden">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
        <h2 className="text-2xl font-bold text-slate-800">
          Vehicle Monitoring
        </h2>

        <input
          type="text"
          placeholder="Search Vehicle Number"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border border-gray-300 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-900 text-white">
              <th className="p-4">Vehicle</th>
              <th className="p-4">Project</th>
              <th className="p-4">Status</th>
              <th className="p-4">GPS</th>
              <th className="p-4">Route</th>
            </tr>
          </thead>

          <tbody>
            {filteredVehicles.map((vehicle, index) => (
              <tr
                key={index}
                className="border-b hover:bg-slate-50 transition"
              >
                <td className="p-4 font-semibold">
                  {vehicle.vehicle_number}
                </td>

                <td className="p-4">{vehicle.project_id}</td>

                <td className="p-4">
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium
                    ${vehicle.loc_vehicle_status === 'RUNNING'
                        ? 'bg-green-100 text-green-700'
                        : vehicle.loc_vehicle_status === 'HALTED'
                        ? 'bg-red-100 text-red-700'
                        : 'bg-yellow-100 text-yellow-700'
                    }`}
                  >
                    {vehicle.loc_vehicle_status}
                  </span>
                </td>

                <td className="p-4">{vehicle.gps}</td>

                <td className="p-4">{vehicle.route}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}