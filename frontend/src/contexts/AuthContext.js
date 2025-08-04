import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Verificar token salvo no localStorage
    const token = localStorage.getItem('fitness_token');
    const savedUser = localStorage.getItem('fitness_user');
    
    if (token && savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        setUser(userData);
        // Configurar token padrão para axios
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      } catch (error) {
        console.error('Erro ao carregar dados do usuário:', error);
        localStorage.removeItem('fitness_token');
        localStorage.removeItem('fitness_user');
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email, password) => {
    setIsLoading(true);
    
    try {
      const response = await axios.post(`${API}/auth/login`, {
        email,
        password
      });

      const { user: userData, token } = response.data;
      
      setUser(userData);
      localStorage.setItem('fitness_token', token);
      localStorage.setItem('fitness_user', JSON.stringify(userData));
      
      // Configurar token padrão para futuras requisições
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      return { success: true };
    } catch (error) {
      console.error('Erro no login:', error);
      const message = error.response?.data?.detail || 'Erro ao fazer login';
      return { success: false, error: message };
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (name, email, password) => {
    setIsLoading(true);
    
    try {
      const response = await axios.post(`${API}/auth/register`, {
        name,
        email,
        password
      });

      const { user: userData, token } = response.data;
      
      setUser(userData);
      localStorage.setItem('fitness_token', token);
      localStorage.setItem('fitness_user', JSON.stringify(userData));
      
      // Configurar token padrão para futuras requisições
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      return { success: true };
    } catch (error) {
      console.error('Erro no registro:', error);
      const message = error.response?.data?.detail || 'Erro ao criar conta';
      return { success: false, error: message };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('fitness_token');
    localStorage.removeItem('fitness_user');
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    user,
    login,
    register,
    logout,
    isLoading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};