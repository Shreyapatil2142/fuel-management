import {
  Truck,
  Route,
  Fuel,
  AlertTriangle,
  PauseCircle,
  PlayCircle
} from 'lucide-react'

export default function DashboardCards({ dashboard }) {
  if (!dashboard) return null

  const cards = [
    {
      title: 'Total Vehicles',
      value: dashboard.total_vehicles,
      icon: <Truck size={30} />,
      color: 'bg-blue-500'
    },
    {
      title: 'Trips',
      value: dashboard.trips,
      icon: <Route size={30} />,
      color: 'bg-purple-500'
    },
    {
      title: 'Running',
      value: dashboard.running,
      icon: <PlayCircle size={30} />,
      color: 'bg-green-500'
    },
    {
      title: 'Halted',
      value: dashboard.halted,
      icon: <PauseCircle size={30} />,
      color: 'bg-red-500'
    },
    {
      title: 'Fuel Difference',
      value: dashboard.gallons_difference,
      icon: <Fuel size={30} />,
      color: 'bg-orange-500'
    },
    {
      title: 'Alerts',
      value: dashboard.alerts,
      icon: <AlertTriangle size={30} />,
      color: 'bg-pink-500'
    }
  ]

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6 mb-8">
      {cards.map((card, index) => (
        <div
          key={index}
          className="bg-white rounded-2xl shadow-md hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <div className={`${card.color} text-white p-3 rounded-xl`}>
              {card.icon}
            </div>
          </div>

          <h3 className="text-gray-500 text-sm font-medium">
            {card.title}
          </h3>

          <p className="text-3xl font-bold mt-2 text-slate-800">
            {card.value}
          </p>
        </div>
      ))}
    </div>
  )
}