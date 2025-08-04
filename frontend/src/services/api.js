import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Configure axios defaults
axios.defaults.baseURL = API;

// Add request interceptor to include token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('fitness_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('fitness_token');
      localStorage.removeItem('fitness_user');
      window.location.href = '/auth';
    }
    return Promise.reject(error);
  }
);

export const api = {
  // Auth endpoints
  auth: {
    login: (email, password) => axios.post('/auth/login', { email, password }),
    register: (name, email, password) => axios.post('/auth/register', { name, email, password }),
  },

  // User endpoints  
  user: {
    getProfile: () => axios.get('/user/profile'),
  },

  // Workout endpoints
  workouts: {
    getAll: () => axios.get('/workouts'),
    getToday: () => axios.get('/workouts/today'),
    completeSet: (workoutId, exerciseId, setData) => 
      axios.post(`/workouts/${workoutId}/exercises/${exerciseId}/complete-set`, setData),
  },

  // Progress endpoints
  progress: {
    getWeekly: () => axios.get('/progress/weekly'),
    getStats: () => axios.get('/progress/stats'),
  },
};

export default api;