import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { Toaster } from "./components/ui/toaster";
import AuthPage from "./pages/AuthPage";
import Dashboard from "./components/Dashboard/Dashboard";
import WorkoutSession from "./components/Workout/WorkoutSession";
import ProgressPage from "./pages/ProgressPage";
import Navigation from "./components/Layout/Navigation";

// Componente para proteger rotas
const ProtectedRoute = ({ children }) => {
  const { user, isLoading } = useAuth();
  
  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-500 mx-auto mb-4"></div>
          <p>Carregando...</p>
        </div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/auth" replace />;
};

// Layout principal com navegação
const AppLayout = ({ children }) => {
  return (
    <>
      {children}
      <Navigation />
    </>
  );
};

// Componente principal das rotas
const AppRoutes = () => {
  const { user } = useAuth();

  return (
    <Routes>
      <Route 
        path="/auth" 
        element={user ? <Navigate to="/dashboard" replace /> : <AuthPage />} 
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <AppLayout>
              <Dashboard />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/workout-session"
        element={
          <ProtectedRoute>
            <WorkoutSession />
          </ProtectedRoute>
        }
      />
      <Route
        path="/progress"
        element={
          <ProtectedRoute>
            <AppLayout>
              <ProgressPage />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/workouts"
        element={
          <ProtectedRoute>
            <AppLayout>
              <div className="min-h-screen bg-black text-white pb-20 flex items-center justify-center">
                <p className="text-gray-400">Página de Treinos em desenvolvimento</p>
              </div>
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <AppLayout>
              <div className="min-h-screen bg-black text-white pb-20 flex items-center justify-center">
                <p className="text-gray-400">Página de Perfil em desenvolvimento</p>
              </div>
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <BrowserRouter>
          <AppRoutes />
          <Toaster />
        </BrowserRouter>
      </AuthProvider>
    </div>
  );
}

export default App;