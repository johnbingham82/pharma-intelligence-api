/**
 * Application Configuration
 * 
 * For Vite, use VITE_ prefix for environment variables.
 * Access them via import.meta.env.VITE_*
 */

// API Base URL - Update this to switch between local and production
export const API_BASE_URL = 
  import.meta.env.VITE_API_URL || 
  'https://pharma-intelligence-api-ee752ce1773a.herokuapp.com';

// Alternative: Use environment-based configuration
// export const API_BASE_URL = import.meta.env.MODE === 'production'
//   ? 'https://pharma-intelligence-api-ee752ce1773a.herokuapp.com'
//   : 'http://localhost:8000';
