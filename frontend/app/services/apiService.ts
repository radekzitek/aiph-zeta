// services/apiService.js

import axios from 'axios';

// Create a new Axios instance with a custom configuration
const apiService = axios.create({
  // The `baseURL` will be prefixed to all requests
  // Your Nginx proxy will intercept `/api/` and forward it.
  baseURL: '/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Optional: Add Request Interceptor ---
// You can intercept requests to add things like authorization tokens dynamically
apiService.interceptors.request.use(config => {
  // For example, get a token from localStorage or a cookie
  // const token = localStorage.getItem('token');
  // if (token) {
  //   config.headers.Authorization = `Bearer ${token}`;
  // }
  return config;
}, error => {
  return Promise.reject(error);
});


// --- Optional: Add Response Interceptor ---
// You can intercept responses to handle global errors
apiService.interceptors.response.use(response => {
  return response;
}, error => {
  if (error.response && error.response.status === 401) {
    console.error("Unauthorized! You could redirect to login here.");
  }
  return Promise.reject(error);
});


// Export the configured instance to be used by the plugin
export default apiService;