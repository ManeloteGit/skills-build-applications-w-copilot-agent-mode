import React, { createContext, useState, useCallback, useEffect } from 'react';
import { authService } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Verificar autenticación al cargar
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('authToken');
      const savedUser = localStorage.getItem('user');
      
      if (token && savedUser) {
        try {
          const response = await authService.getCurrentUser();
          setUser(response.data);
          setLoading(false);
        } catch (err) {
          localStorage.removeItem('authToken');
          localStorage.removeItem('user');
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(async (username, password) => {
    try {
      setError(null);
      const response = await authService.login(username, password);
      const { token, user: userData } = response.data;
      
      localStorage.setItem('authToken', token);
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
      return userData;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Error de autenticación';
      setError(errorMsg);
      throw err;
    }
  }, []);

  const register = useCallback(async (userData) => {
    try {
      setError(null);
      const response = await authService.register(userData);
      const { token, user: newUser } = response.data;
      
      localStorage.setItem('authToken', token);
      localStorage.setItem('user', JSON.stringify(newUser));
      setUser(newUser);
      return newUser;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Error al registrarse';
      setError(errorMsg);
      throw err;
    }
  }, []);

  const logout = useCallback(() => {
    authService.logout();
    setUser(null);
    setError(null);
  }, []);

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
