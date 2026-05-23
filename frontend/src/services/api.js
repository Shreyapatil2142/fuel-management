import axios from 'axios'

const API = axios.create({
  baseURL: 'http://127.0.0.1:5000/api'
})

export const getDashboard = (projectId) =>
  API.get(`/dashboard?project_id=${projectId}`)

export const getVehicles = () =>
  API.get('/vehicles')

export const getProjectVehicles = (projectId) =>
  API.get(`/project_vehicles?project_id=${projectId}`)

export const getVehicleDetails = (vehicleNumber) =>
  API.get(`/vehicle_details?vehicle_number=${vehicleNumber}`)

export const getTrips = (projectId) =>
  API.get(`/trips?project_id=${projectId}`)

export const getRouteCoordinates = (route) =>
  API.get(`/route_coordinates?route=${route}`)

export default API