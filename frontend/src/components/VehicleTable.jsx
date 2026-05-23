import { useState, useRef, useEffect } from 'react'
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { getRouteCoordinates } from '../services/api'

// Fix leaflet default marker icons
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

function ThreeDotMenu({ onSeeRoute, onSeeCamera }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    function handleClickOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="p-2 rounded-full hover:bg-slate-100 transition text-slate-600 font-bold text-lg leading-none"
        title="Options"
      >
        ⋮
      </button>
      {open && (
        <div className="absolute right-0 z-50 mt-1 w-44 bg-white border border-gray-200 rounded-xl shadow-xl overflow-hidden">
          <button
            className="w-full px-4 py-3 text-left text-sm text-slate-700 hover:bg-blue-50 hover:text-blue-700 transition flex items-center gap-2"
            onClick={() => { setOpen(false); onSeeRoute() }}
          >
            🗺️ See Route
          </button>
          <button
            className="w-full px-4 py-3 text-left text-sm text-slate-700 hover:bg-blue-50 hover:text-blue-700 transition flex items-center gap-2"
            onClick={() => { setOpen(false); onSeeCamera() }}
          >
            📷 See Camera Feed
          </button>
        </div>
      )}
    </div>
  )
}

function RouteMapModal({ vehicle, onClose }) {
  const [coords, setCoords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getRouteCoordinates(vehicle.route)
      .then(res => {
        const points = res.data.map(p => [p.latitude, p.longitude])
        setCoords(points)
      })
      .catch(() => setError('Failed to load route coordinates'))
      .finally(() => setLoading(false))
  }, [vehicle.route])

  const center = coords.length > 0
    ? coords[Math.floor(coords.length / 2)]
    : [26.8467, 80.9462]

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl mx-4 overflow-hidden"
        onClick={e => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-slate-900 text-white">
          <div>
            <h3 className="text-lg font-bold">{vehicle.vehicle_number} — {vehicle.route}</h3>
            {coords.length > 0 && (
              <p className="text-sm text-slate-300 mt-0.5">
                {coords.length > 0 ? `${vehicle.route}` : ''}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-slate-300 hover:text-white text-2xl leading-none transition"
          >
            ×
          </button>
        </div>

        {/* Map */}
        <div className="h-96">
          {loading && (
            <div className="h-full flex items-center justify-center text-slate-500">
              Loading route...
            </div>
          )}
          {error && (
            <div className="h-full flex items-center justify-center text-red-500">
              {error}
            </div>
          )}
          {!loading && !error && coords.length > 0 && (
            <MapContainer
              center={center}
              zoom={13}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Polyline positions={coords} color="#2563eb" weight={4} />
              <Marker position={coords[0]}>
                <Popup>Start: {coords[0][0].toFixed(4)}, {coords[0][1].toFixed(4)}</Popup>
              </Marker>
              <Marker position={coords[coords.length - 1]}>
                <Popup>End: {coords[coords.length - 1][0].toFixed(4)}, {coords[coords.length - 1][1].toFixed(4)}</Popup>
              </Marker>
            </MapContainer>
          )}
        </div>

        {/* Footer info */}
        {!loading && !error && coords.length > 0 && (
          <div className="px-6 py-3 bg-slate-50 border-t border-gray-200 flex gap-6 text-sm text-slate-600">
            <span>📍 <b>Start:</b> {coords[0][0].toFixed(5)}, {coords[0][1].toFixed(5)}</span>
            <span>🏁 <b>End:</b> {coords[coords.length-1][0].toFixed(5)}, {coords[coords.length-1][1].toFixed(5)}</span>
            <span>📌 <b>Points:</b> {coords.length}</span>
          </div>
        )}
      </div>
    </div>
  )
}

function CameraFeedModal({ vehicle, onClose }) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-slate-900 text-white">
          <h3 className="text-lg font-bold">Camera Feed — {vehicle.vehicle_number}</h3>
          <button onClick={onClose} className="text-slate-300 hover:text-white text-2xl leading-none transition">×</button>
        </div>
        <div className="h-64 flex flex-col items-center justify-center gap-3 text-slate-400 bg-slate-50">
          <span className="text-5xl">📷</span>
          <p className="text-sm">Camera feed not available</p>
        </div>
      </div>
    </div>
  )
}

export default function VehicleTable({ vehicles }) {
  const [search, setSearch] = useState('')
  const [routeModal, setRouteModal] = useState(null)
  const [cameraModal, setCameraModal] = useState(null)

  const filteredVehicles = vehicles.filter((vehicle) =>
    vehicle.vehicle_number?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 overflow-hidden">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Vehicle Monitoring</h2>
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
              <th className="p-4"></th>
            </tr>
          </thead>
          <tbody>
            {filteredVehicles.map((vehicle, index) => (
              <tr key={index} className="border-b hover:bg-slate-50 transition">
                <td className="p-4 font-semibold">{vehicle.vehicle_number}</td>
                <td className="p-4">{vehicle.project_id}</td>
                <td className="p-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium
                    ${vehicle.loc_vehicle_status === 'RUNNING'
                      ? 'bg-green-100 text-green-700'
                      : vehicle.loc_vehicle_status === 'HALTED'
                      ? 'bg-red-100 text-red-700'
                      : 'bg-yellow-100 text-yellow-700'
                    }`}>
                    {vehicle.loc_vehicle_status}
                  </span>
                </td>
                <td className="p-4">{vehicle.gps}</td>
                <td className="p-4">{vehicle.route}</td>
                <td className="p-4">
                  <ThreeDotMenu
                    onSeeRoute={() => setRouteModal(vehicle)}
                    onSeeCamera={() => setCameraModal(vehicle)}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {routeModal && (
        <RouteMapModal vehicle={routeModal} onClose={() => setRouteModal(null)} />
      )}
      {cameraModal && (
        <CameraFeedModal vehicle={cameraModal} onClose={() => setCameraModal(null)} />
      )}
    </div>
  )
}
