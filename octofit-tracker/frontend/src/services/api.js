import axios from 'axios';

// Determinar la URL base de la API
const getBaseURL = () => {
  const codespaceName = process.env.REACT_APP_CODESPACE_NAME || '';
  if (codespaceName) {
    return `https://${codespaceName}-8000.app.github.dev/api`;
  }
  return process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
};

const API_BASE_URL = getBaseURL();

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token de autenticación
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejo de errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Servicios de Autenticación
export const authService = {
  login: (username, password) =>
    apiClient.post('auth/login/', { username, password }),
  
  register: (userData) =>
    apiClient.post('auth/registration/', userData),
  
  getCurrentUser: () =>
    apiClient.get('users/me/'),
  
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  },
};

// Servicios de Usuarios
export const userService = {
  getUsers: (params) =>
    apiClient.get('users/', { params }),
  
  getUser: (id) =>
    apiClient.get(`users/${id}/`),
  
  updateProfile: (id, data) =>
    apiClient.patch(`users/${id}/update_profile/`, data),
  
  changePassword: (data) =>
    apiClient.post('users/change_password/', data),
  
  getLeaderboard: () =>
    apiClient.get('users/leaderboard/'),
};

// Servicios de Actividades
export const activityService = {
  getActivities: (params) =>
    apiClient.get('activities/', { params }),
  
  getActivity: (id) =>
    apiClient.get(`activities/${id}/`),
  
  createActivity: (data) =>
    apiClient.post('activities/', data),
  
  updateActivity: (id, data) =>
    apiClient.patch(`activities/${id}/`, data),
  
  deleteActivity: (id) =>
    apiClient.delete(`activities/${id}/`),
  
  getStatistics: () =>
    apiClient.get('activities/statistics/'),
  
  getTodayActivities: () =>
    apiClient.get('activities/today/'),
  
  getWeekActivities: () =>
    apiClient.get('activities/week/'),
  
  getMonthActivities: () =>
    apiClient.get('activities/month/'),
};

// Servicios de Equipos
export const teamService = {
  getTeams: (params) =>
    apiClient.get('teams/', { params }),
  
  getTeam: (id) =>
    apiClient.get(`teams/${id}/`),
  
  createTeam: (data) =>
    apiClient.post('teams/', data),
  
  updateTeam: (id, data) =>
    apiClient.patch(`teams/${id}/`, data),
  
  deleteTeam: (id) =>
    apiClient.delete(`teams/${id}/`),
  
  addMember: (teamId, userId) =>
    apiClient.post(`teams/${teamId}/add_member/`, { user_id: userId }),
  
  removeMember: (teamId, userId) =>
    apiClient.post(`teams/${teamId}/remove_member/`, { user_id: userId }),
  
  getMembers: (teamId) =>
    apiClient.get(`teams/${teamId}/members/`),
};

// Servicios de Leaderboard
export const leaderboardService = {
  getLeaderboard: (params) =>
    apiClient.get('leaderboard/', { params }),
  
  getCurrentWeek: () =>
    apiClient.get('leaderboard/current_week/'),
  
  getTopTen: () =>
    apiClient.get('leaderboard/top_ten/'),
  
  getUserHistory: (userId) =>
    apiClient.get('leaderboard/user_history/', { params: { user_id: userId } }),
};

// Servicios de Recomendaciones
export const recommendationService = {
  getRecommendations: (params) =>
    apiClient.get('recommendations/', { params }),
  
  getRecommendation: (id) =>
    apiClient.get(`recommendations/${id}/`),
  
  viewRecommendation: (id) =>
    apiClient.post(`recommendations/${id}/view/`),
  
  acceptRecommendation: (id) =>
    apiClient.post(`recommendations/${id}/accept/`),
  
  rejectRecommendation: (id) =>
    apiClient.post(`recommendations/${id}/reject/`),
  
  completeRecommendation: (id) =>
    apiClient.post(`recommendations/${id}/complete/`),
  
  getPending: () =>
    apiClient.get('recommendations/pending/'),
  
  getActive: () =>
    apiClient.get('recommendations/active/'),
  
  getCompleted: () =>
    apiClient.get('recommendations/completed/'),
  
  getStats: () =>
    apiClient.get('recommendations/stats/'),
};

export default apiClient;
