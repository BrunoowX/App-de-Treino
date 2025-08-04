import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Home, Dumbbell, TrendingUp, User } from 'lucide-react';

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { id: 'home', label: 'Início', icon: Home, path: '/dashboard' },
    { id: 'workouts', label: 'Treinos', icon: Dumbbell, path: '/workouts' },
    { id: 'progress', label: 'Progresso', icon: TrendingUp, path: '/progress' },
    { id: 'profile', label: 'Perfil', icon: User, path: '/profile' }
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-black border-t border-gray-800 z-50">
      <div className="flex justify-around items-center py-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <button
              key={item.id}
              onClick={() => navigate(item.path)}
              className={`flex flex-col items-center py-2 px-4 rounded-lg transition-all duration-200 ${
                isActive 
                  ? 'text-red-500 bg-red-500/10' 
                  : 'text-gray-400 hover:text-red-400 hover:bg-red-500/5'
              }`}
            >
              <Icon size={20} className="mb-1" />
              <span className="text-xs font-medium">{item.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};

export default Navigation;